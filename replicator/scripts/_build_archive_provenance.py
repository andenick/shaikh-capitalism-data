"""Build per-series provenance manifest for the Archive package.

For every series, produce a JSON record:
  - SID, name, chapter, figures
  - book_quote (verbatim from research/{SID}_research.json)
  - book_source_citation (Shaikh's stated source)
  - replication_source (modern API used)
  - dpr_path, epr_path
  - chopped_csv_path (if present)
  - chopped_n_rows, chopped_year_range
  - extenbook_path
  - validation_status, mae, max_abs_err

Output: ARCHIVE/PROVENANCE_MANIFEST.json  (master)
        ARCHIVE/provenance/{SID}.json     (per-series)
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path


# Parameterized 2026-05-19 per Decision 0006: derive paths from script location
# (scripts/ -> replicator/ -> Technical/ -> RSCD/). Env overrides:
#   RSCD_TECHNICAL  -> the Technical/ directory
#   RSCD_ARCHIVE    -> the per-version Archive/ output directory
_SCRIPT_DIR = Path(__file__).resolve().parent
_TECHNICAL_DEFAULT = _SCRIPT_DIR.parents[1]   # replicator/scripts -> Technical
_RSCD_ROOT_DEFAULT = _TECHNICAL_DEFAULT.parent  # Technical -> RSCD
TECHNICAL = Path(os.environ.get("RSCD_TECHNICAL", str(_TECHNICAL_DEFAULT)))
ARC = Path(os.environ.get(
    "RSCD_ARCHIVE",
    str(_RSCD_ROOT_DEFAULT / "Outputs" / "Archive" / "RSCD_v1.0"),
))


def _load_research(sid: str) -> dict:
    p = TECHNICAL / "research" / f"{sid}_research.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return {"_error": str(e)}


def _extract_quote(research: dict) -> tuple[str, str, list]:
    """Return (verbatim_quote, book_source_citation, all_quotes).

    Schema (anu-research-v*): research['book_quotes'] is a list of
    {chapter, page, quote, role, verbatim_check} dicts.
    research['primary_source'] is a dict with {agency, publication,
    table_or_series_id, url, frequency, units, license}.
    """
    quote = ""
    src = ""
    all_quotes = []

    bq = research.get("book_quotes")
    if isinstance(bq, list):
        for item in bq:
            if isinstance(item, dict):
                q = (item.get("quote") or "").strip()
                if q:
                    all_quotes.append({
                        "page": item.get("page"),
                        "chapter": item.get("chapter"),
                        "role": item.get("role"),
                        "verbatim_check": item.get("verbatim_check"),
                        "quote": q,
                    })
                    # First definitional quote (or first if none marked)
                    if not quote and item.get("role") == "definition":
                        quote = q
        if not quote and all_quotes:
            quote = all_quotes[0]["quote"]

    ps = research.get("primary_source")
    if isinstance(ps, dict):
        parts = []
        for k in ("agency", "publication", "table_or_series_id", "url"):
            v = ps.get(k)
            if isinstance(v, str) and v.strip():
                parts.append(v.strip())
        src = " | ".join(parts)
    elif isinstance(ps, str):
        src = ps.strip()

    return quote, src, all_quotes


def _chopped_stats(sid: str) -> dict:
    p = TECHNICAL / "chopped" / f"{sid}.csv"
    if not p.exists():
        return {"present": False}
    n = 0
    yrs = []
    yr_col = None
    with p.open(encoding="utf-8") as fh:
        r = csv.reader(fh)
        header = next(r, None) or []
        for cand in ("year", "Year", "YEAR", "period", "date", "time"):
            if cand in header:
                yr_col = header.index(cand)
                break
        for row in r:
            n += 1
            if yr_col is not None and yr_col < len(row):
                try:
                    yrs.append(int(str(row[yr_col])[:4]))
                except (ValueError, IndexError):
                    pass
    return {
        "present": True,
        "path": f"chopped/{sid}.csv",
        "n_rows": n,
        "year_range": [min(yrs), max(yrs)] if yrs else None,
        "columns": header,
    }


def main() -> None:
    reg = json.loads((TECHNICAL / "series_registry.json").read_text(encoding="utf-8"))
    vrpt = json.loads((TECHNICAL / "VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    series = reg.get("series", {})
    vseries = vrpt.get("series", {})

    prov_dir = ARC / "provenance"
    prov_dir.mkdir(parents=True, exist_ok=True)

    master = {
        "schema_version": "rscd-provenance-v1.0",
        "generated_at": "2026-05-19",
        "n_series": len(series),
        "series": {},
    }

    for sid in sorted(series.keys()):
        meta = series[sid]
        research = _load_research(sid)
        quote, src, all_quotes = _extract_quote(research)
        v = vseries.get(sid, {})
        chopped = _chopped_stats(sid)

        rec = {
            "sid": sid,
            "name": meta.get("name"),
            "chapter": meta.get("chapter"),
            "figures": meta.get("figures"),
            "year_range_book": meta.get("year_range_book"),
            "year_range_extension": meta.get("year_range_extension"),
            "content_type": meta.get("content_type"),
            "construction": meta.get("construction"),
            "units": meta.get("units"),
            "primary_source": meta.get("primary_source"),
            "proxy": meta.get("proxy"),
            "book_verbatim_quote": quote or "(no quote captured; see research dossier)",
            "book_verbatim_quotes_all": all_quotes,
            "book_source_citation": src or "(no explicit source citation; see research dossier)",
            "research_dossier_path": f"research/{sid}_research.json",
            "dpr_path": meta.get("dpr"),
            "epr_path": meta.get("epr"),
            "chopped_csv": chopped,
            "extenbook_path": f"extenbooks/{sid}_extenbook.xlsx"
                              if (TECHNICAL / "extenbooks" / f"{sid}_extenbook.xlsx").exists()
                              else None,
            "validation": {
                "status": v.get("status"),
                "mae": v.get("mae"),
                "max_abs_err": v.get("max_abs_err"),
                "n_compared": v.get("n_compared"),
                "compare_range": v.get("compare_range"),
                "divergence_count": v.get("divergence_count", 0),
            },
            "loader_path": f"code/L01_loaders/L01_{sid}_load.py",
            "processor_path": f"code/P02_processors/P02_{sid}_construct.py",
            "validator_path": f"code/V03_validators/V03_{sid}_validate.py",
        }
        # Per-series file
        (prov_dir / f"{sid}.json").write_text(
            json.dumps(rec, indent=2, default=str), encoding="utf-8")
        master["series"][sid] = {
            "name": rec["name"],
            "chapter": rec["chapter"],
            "validation_status": rec["validation"]["status"],
            "has_chopped": chopped.get("present", False),
            "n_rows": chopped.get("n_rows"),
            "provenance_path": f"provenance/{sid}.json",
        }

    (ARC / "PROVENANCE_MANIFEST.json").write_text(
        json.dumps(master, indent=2, default=str), encoding="utf-8")

    n_chopped = sum(1 for s in master["series"].values() if s["has_chopped"])
    print(f"Wrote PROVENANCE_MANIFEST.json + {len(series)} per-series records")
    print(f"  Series with chopped output: {n_chopped}")
    print(f"  Output: {ARC}/PROVENANCE_MANIFEST.json")
    print(f"          {prov_dir}/")


if __name__ == "__main__":
    main()
