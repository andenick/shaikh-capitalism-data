"""
Phase 3 Research Stubber — RSCD

For each candidate series in series_registry.json, generate a research stub
in research/{SID}_research.json pre-filled with what we already know from
the candidates (figures, predecessor IDs, year range). A human (or anu-research
skill) then fills the book_quotes, primary_source, methodology_notes.

One-shot scaffolding (prefix _). Run once after Phase 2 to bootstrap Phase 3.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths


def main():
    registry = json.loads(paths.REGISTRY.read_text(encoding="utf-8"))
    template = json.loads((paths.DOCS_SERIES / "_RESEARCH_TEMPLATE.json").read_text(encoding="utf-8"))

    paths.RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    n_new = n_skip = 0

    for sid, det in registry["series"].items():
        out = paths.RESEARCH_DIR / f"{sid}_research.json"
        if out.exists():
            n_skip += 1
            continue

        stub = dict(template)
        for k in ("_template_version", "_template_notes"):
            stub.pop(k, None)
        stub["series_id"] = sid
        stub["name"] = det["name"]
        stub["chapter"] = det["chapter"]
        stub["figures"] = det.get("figures", [])
        stub["content_type"] = det.get("content_type")
        stub["predecessor_ids"] = det.get("predecessor_ids", {})
        stub["construction"] = det.get("construction", "direct")
        stub["year_range_book"] = det.get("year_range", [None, None])
        stub["year_range_extension"] = [None, None]
        stub["book_quotes"] = []
        stub["primary_source"] = None
        stub["extension_candidates"] = []
        stub["methodology_notes"] = []
        stub["open_questions"] = [
            "POPULATE: read the relevant chapter and quote the series definition.",
            "POPULATE: confirm primary_source agency/table/url.",
            "POPULATE: identify extension subseries (FRED/BEA/BLS keys).",
        ]
        stub["review_history"] = [{"reviewer": "phase3_stubber", "date": "2026-05-18", "status": "draft", "notes": "auto-generated stub"}]

        out.write_text(json.dumps(stub, indent=2, ensure_ascii=False), encoding="utf-8")
        n_new += 1

    print(f"Phase 3 stubs: {n_new} new, {n_skip} skipped (already exist)")


if __name__ == "__main__":
    main()
