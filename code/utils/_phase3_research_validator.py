"""
Phase 3 Research Validator — RSCD

Validates every research/{SID}_research.json against the Phase 3 acceptance
criteria. Writes Build/PHASE3_VALIDATION_REPORT.json and exits 0 if all PASS.

Run after each Phase 3 wave:
    python Technical/code/utils/_phase3_research_validator.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths


def validate_one(sid: str, doc: dict) -> tuple[bool, list[str]]:
    issues: list[str] = []

    quotes = doc.get("book_quotes") or []
    if len(quotes) < 2:
        issues.append(f"book_quotes: need >=2, have {len(quotes)}")
    roles = {q.get("role") for q in quotes if isinstance(q, dict)}
    if "definition" not in roles:
        issues.append("book_quotes: missing role='definition'")
    if "source" not in roles:
        issues.append("book_quotes: missing role='source'")
    for i, q in enumerate(quotes):
        if not isinstance(q, dict):
            issues.append(f"book_quotes[{i}]: not a dict")
            continue
        if not (q.get("quote") or "").strip():
            issues.append(f"book_quotes[{i}]: empty quote")
        if not q.get("page"):
            issues.append(f"book_quotes[{i}]: missing page")
        if not q.get("verbatim_check"):
            issues.append(f"book_quotes[{i}]: verbatim_check not true")

    ps = doc.get("primary_source")
    if not ps:
        issues.append("primary_source: null/missing")
    else:
        for k in ("agency", "publication", "table_or_series_id", "url", "units", "frequency"):
            if not ps.get(k):
                issues.append(f"primary_source.{k}: missing")

    cons = doc.get("construction")
    if cons not in {"direct", "formula", "composite"}:
        issues.append(f"construction: invalid value {cons!r}")

    if cons == "formula" and not doc.get("formula"):
        issues.append("construction=formula but formula field missing")
    if cons in {"formula", "composite"} and not doc.get("components"):
        issues.append("construction in {formula, composite} but components empty")

    yrb = doc.get("year_range_book") or []
    if not (isinstance(yrb, list) and len(yrb) == 2 and all(isinstance(y, (int, type(None))) for y in yrb)):
        issues.append("year_range_book: malformed")

    ctype = doc.get("content_type")
    ext = doc.get("extension_candidates") or []
    if ctype == "time_series" and not ext:
        issues.append("extension_candidates: empty for time_series")

    if not (doc.get("methodology_notes") or []):
        issues.append("methodology_notes: empty (recommend >=1)")

    rh = doc.get("review_history") or []
    if not rh:
        issues.append("review_history: empty")

    return (len(issues) == 0, issues)


def main():
    report = {
        "schema_version": "rscd-phase3-validation-v1.0",
        "generated_at": "",
        "total": 0,
        "pass": 0,
        "fail": 0,
        "by_series": {},
    }
    from datetime import datetime, timezone
    report["generated_at"] = datetime.now(timezone.utc).isoformat()

    files = sorted(paths.RESEARCH_DIR.glob("*_research.json"))
    for fp in files:
        sid = fp.stem.replace("_research", "")
        try:
            doc = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            report["by_series"][sid] = {"status": "FAIL", "issues": [f"JSON parse error: {e}"]}
            report["fail"] += 1
            report["total"] += 1
            continue

        ok, issues = validate_one(sid, doc)
        report["by_series"][sid] = {"status": "PASS" if ok else "FAIL", "issues": issues}
        report["pass" if ok else "fail"] += 1
        report["total"] += 1

    out = paths.BUILD_DIR / "PHASE3_VALIDATION_REPORT.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Validated {report['total']} dossiers: {report['pass']} PASS, {report['fail']} FAIL")
    print(f"Report: {out}")
    if report["fail"]:
        print("\nFailures:")
        for sid, v in sorted(report["by_series"].items()):
            if v["status"] == "FAIL":
                print(f"  {sid}: {len(v['issues'])} issue(s)")
                for issue in v["issues"][:3]:
                    print(f"    - {issue}")
                if len(v["issues"]) > 3:
                    print(f"    ... and {len(v['issues'])-3} more")
        sys.exit(1)


if __name__ == "__main__":
    main()
