"""
Phase 4 Adequacy Validator — RSCD

Validates per-chapter adequacy reports. Confirms each report meets the schema,
the 80/100 score threshold, and per-series fields are filled.

Run after each wave:
    python Technical/code/utils/_phase4_adequacy_validator.py
    python Technical/code/utils/_phase4_adequacy_validator.py --chapter 2
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths

GATE_THRESHOLD = 80


def validate_one(report_path: Path) -> tuple[bool, list[str], int]:
    issues: list[str] = []
    try:
        rep = json.loads(report_path.read_text(encoding="utf-8"))
    except Exception as e:
        return (False, [f"JSON parse error: {e}"], 0)

    if rep.get("schema_version") != "rscd-adequacy-v1.0":
        issues.append(f"schema_version mismatch: {rep.get('schema_version')!r}")

    if not isinstance(rep.get("chapter"), (int, str)):
        issues.append("chapter: missing or wrong type")
    if not rep.get("reviewer"):
        issues.append("reviewer: empty")
    if not rep.get("review_date"):
        issues.append("review_date: empty")

    scores = rep.get("scores") or {}
    expected_dims = ["D1_source_reachability", "D2_year_coverage", "D3_license_compatibility",
                     "D4_units_consistency", "D5_extension_feasibility", "D6_no_proxy_compliance"]
    expected_max = [25, 20, 15, 15, 15, 10]
    for dim, mx in zip(expected_dims, expected_max):
        d = scores.get(dim) or {}
        if d.get("max") != mx:
            issues.append(f"scores.{dim}.max != {mx}")
        v = d.get("value")
        if not isinstance(v, (int, float)) or v < 0 or v > mx:
            issues.append(f"scores.{dim}.value invalid: {v}")
        if not (d.get("details") or "").strip():
            issues.append(f"scores.{dim}.details empty")

    total = rep.get("total_score", 0)
    computed = sum((scores.get(d) or {}).get("value", 0) for d in expected_dims)
    if abs(total - computed) > 1:
        issues.append(f"total_score {total} != sum of dimensions {computed}")

    per_series = rep.get("per_series") or []
    if not per_series:
        issues.append("per_series: empty")
    for i, s in enumerate(per_series):
        sid = s.get("sid", "")
        if not sid.startswith(("S", "AS", "ES")):
            issues.append(f"per_series[{i}].sid invalid: {sid!r}")
        if not s.get("url_status"):
            issues.append(f"per_series[{i}={sid}].url_status empty")
        if s.get("year_coverage_pct") is None and s.get("extension_status") not in {"not_applicable_cross_sectional", "not_applicable_theoretical"}:
            issues.append(f"per_series[{i}={sid}].year_coverage_pct empty for non-theoretical series")
        if not s.get("units"):
            issues.append(f"per_series[{i}={sid}].units empty")
        if not s.get("extension_status"):
            issues.append(f"per_series[{i}={sid}].extension_status empty")
        if not s.get("adequacy_status"):
            issues.append(f"per_series[{i}={sid}].adequacy_status empty")

    gate = bool(rep.get("gate_passed"))
    if gate and total < GATE_THRESHOLD:
        issues.append(f"gate_passed=true but total_score {total} < {GATE_THRESHOLD}")
    if not gate and total >= GATE_THRESHOLD:
        issues.append(f"total_score {total} >= {GATE_THRESHOLD} but gate_passed=false")

    return (len(issues) == 0, issues, total)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", help="Validate a single chapter only (e.g. 2 or ES)")
    args = ap.parse_args()

    chapter_dir = paths.DOCS_CHAPTERS
    if args.chapter:
        pattern = f"CH{args.chapter}_ADEQUACY_REPORT.json"
        files = [chapter_dir / pattern] if (chapter_dir / pattern).exists() else []
    else:
        files = sorted(chapter_dir.glob("CH*_ADEQUACY_REPORT.json"))

    summary = {
        "schema_version": "rscd-phase4-validation-v1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_chapters": len(files),
        "pass": 0,
        "fail": 0,
        "by_chapter": {},
        "all_passed": False,
    }

    for fp in files:
        chap = fp.name.replace("_ADEQUACY_REPORT.json", "").replace("CH", "")
        ok, issues, score = validate_one(fp)
        summary["by_chapter"][chap] = {
            "score": score,
            "gate_passed": ok and score >= GATE_THRESHOLD,
            "schema_pass": ok,
            "issues": issues,
        }
        if ok and score >= GATE_THRESHOLD:
            summary["pass"] += 1
        else:
            summary["fail"] += 1

    summary["all_passed"] = (summary["fail"] == 0 and summary["pass"] == summary["total_chapters"])

    out = paths.BUILD_DIR / "PHASE4_VALIDATION_REPORT.json"
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Adequacy: {summary['pass']}/{summary['total_chapters']} chapters PASS (gate >= {GATE_THRESHOLD})")
    print(f"Report: {out}")

    if summary["fail"]:
        print("\nFailures:")
        for chap, v in sorted(summary["by_chapter"].items()):
            if not v["gate_passed"]:
                print(f"  Ch{chap}: score={v['score']}, schema_pass={v['schema_pass']}, {len(v['issues'])} issue(s)")
                for issue in v["issues"][:3]:
                    print(f"    - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
