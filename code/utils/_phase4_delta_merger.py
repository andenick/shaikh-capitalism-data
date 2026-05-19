"""
Phase 4 Delta Merger — RSCD

Merges all 16 per-chapter CH{N}_REGISTRY_DELTA.json files into the live
series_registry.json. Each delta adds/updates the per-series `adequacy` block
+ any primary_source URL substitutions / unit corrections that the adequacy
reviewer proposed.

One-shot, idempotent. Run after all Phase 4 waves complete.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths


def main():
    reg = json.loads(paths.REGISTRY.read_text(encoding="utf-8"))
    delta_files = sorted(paths.DOCS_CHAPTERS.glob("CH*_REGISTRY_DELTA.json"))

    merged = 0
    skipped = 0
    series_touched = set()

    for df in delta_files:
        try:
            delta = json.loads(df.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  SKIP {df.name}: parse error {e}")
            skipped += 1
            continue

        # Delta schemas vary by subagent. Common shapes observed:
        #   {"operations": [{"sid": ..., "op": "set_adequacy", "adequacy": {...}}, ...]}
        #   {"deltas": {"S###": {"adequacy": {...}}, ...}}
        #   {"per_series": [{"sid": ..., "adequacy": {...}}, ...]}
        #   {"series": {"S###": {...}}}
        per_series_list = []
        if isinstance(delta, dict) and "series_patches" in delta:
            for p in delta["series_patches"]:
                if isinstance(p, dict) and (p.get("sid") or p.get("series_id")):
                    per_series_list.append(p)
        elif isinstance(delta, dict) and "operations" in delta:
            for op in delta["operations"]:
                if isinstance(op, dict) and op.get("sid"):
                    per_series_list.append(op)
        elif isinstance(delta, dict) and "deltas" in delta and isinstance(delta["deltas"], dict):
            for sid, body in delta["deltas"].items():
                if isinstance(body, dict):
                    per_series_list.append({"sid": sid, **body})
        elif isinstance(delta, dict) and "per_series" in delta:
            per_series_list = delta["per_series"]
        elif isinstance(delta, dict) and "series" in delta:
            per_series_list = [{"sid": k, **v} for k, v in delta["series"].items()]
        elif isinstance(delta, dict):
            META = {"chapter", "schema_version", "generated_at", "_notes", "_schema", "_purpose",
                    "generated_by", "applies_to_registry", "chapter_recommendations_for_main_thread",
                    "reviewer", "review_date", "url_substitutions", "data_substitutions"}
            per_series_list = [{"sid": k, **v} for k, v in delta.items() if k not in META and isinstance(v, dict)]

        if not per_series_list:
            print(f"  SKIP {df.name}: no per-series content found")
            skipped += 1
            continue

        for entry in per_series_list:
            sid = entry.get("sid") or entry.get("series_id")
            if not sid or sid not in reg["series"]:
                continue
            ser = reg["series"][sid]

            # Adequacy block may be nested under entry["adequacy"] (most common)
            # or flat fields (less common).
            adequacy_block = {}
            if isinstance(entry.get("adequacy"), dict):
                adequacy_block.update(entry["adequacy"])
            for k in ("adequacy_status", "url_status", "year_coverage_pct", "license",
                      "extension_status", "proposed_substitute", "proxy_flags",
                      "remediation", "content_type_correction", "status",
                      "score_contribution", "reviewed_at", "issues_resolved",
                      "issues_outstanding"):
                if k in entry:
                    adequacy_block[k] = entry[k]
            if adequacy_block:
                ser.setdefault("adequacy", {}).update(adequacy_block)
                ser["adequacy"]["reviewed_by"] = entry.get("reviewer") or f"phase4_delta_{df.stem}"

            # Patch primary_source URL/units if delta proposes
            for patch_key in ("primary_source_patch", "primary_source"):
                if isinstance(entry.get(patch_key), dict):
                    ser.setdefault("primary_source", {}).update(entry[patch_key])
                    break

            series_touched.add(sid)
        merged += 1

    paths.REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Merged {merged} delta files, {skipped} skipped")
    print(f"Series with adequacy blocks: {len(series_touched)}")


if __name__ == "__main__":
    main()
