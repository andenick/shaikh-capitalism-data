"""V03_S203 - validate processed S203.

Two independent legs (Decision 0008 + Decision 0011):

1. Book round-trip: compare processed vs the salvaged Appendix2 MW Real-GDP-per-capita
   column at 1% tolerance — BUT excluding the corrupt Great-Depression span 1930-1944,
   which P02_S203 deliberately replaces with the re-based fresh MeasuringWorth re-pull
   (Decision 0008 / T1.2). Round-tripping the corrected span against the corrupt book
   column would falsely FAIL; the retained (non-corrupt) years still prove melt-fidelity.
   This breaks the legacy tautology (V03 re-reading the same corrupt workbook the loader
   read — see S203_MHR §5, F-01) by no longer asserting the corrected rows against the
   known-bad source.

2. Independent-anchor / plausibility suite (Decision 0011, wired per evidence_B2_wiring.md):
   the registry ``validation.plausibility_rules`` (Depression-must-fall: 1929->1933
   strictly falling) is asserted against the processed parquet. An anchor/plausibility RED
   FAILS this validator — this is the out-of-source sanity assertion the legacy V03 lacked.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402
from V03_validators._v03_anchor_lib import (  # noqa: E402
    RED, check_independent_anchor, check_level_plausibility,
    check_splice_continuity, _load_processed, _load_registry,
)

SERIES_ID = "S203"
PROCESSED = DATA_PROCESSED / "S203.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix2_MeasuringWorthGDP_1889-2010.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1889, 2010)
# Corrupt Great-Depression span replaced by P02 from the re-pull (Decision 0008 / T1.2).
# Excluded from the book-XLSX round-trip because the book source itself is corrupt here.
CORRECTED_SPAN = (1930, 1944)


def _anchor_section(sid: str) -> dict:
    """Load registry + processed parquet via the anchor lib's own readers (byte-identical
    to run_anchor_suite.py) and fold the three Decision-0011 checks. status=FAIL iff any RED.
    """
    reg = _load_registry()
    dfp = _load_processed(sid)
    anchors = check_independent_anchor(sid, dfp, reg)
    splice = check_splice_continuity(sid, dfp, reg)
    plaus = check_level_plausibility(sid, dfp, reg)
    red_checks = [name for name, blk in
                  (("anchors", anchors), ("splice", splice), ("plausibility", plaus))
                  if blk.get("status") == RED]
    return {"status": "FAIL" if red_checks else "PASS", "red_checks": red_checks,
            "anchors": anchors, "splice": splice, "plausibility": plaus}


def _book_truth() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    truth = df[["Year", "Real GDP per Capita_2005Dollars"]].rename(
        columns={"Year": "year", "Real GDP per Capita_2005Dollars": "expected"})
    return truth.dropna(subset=["expected"])


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S203"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = _book_truth()
    m = actual.merge(truth, on="year", how="inner")
    m = m[(m["year"] >= BOOK_OVERLAP[0]) & (m["year"] <= BOOK_OVERLAP[1])]
    # Exclude the corrected Depression span from the book round-trip: those rows were
    # deliberately replaced (Decision 0008); the book source is corrupt there.
    lo, hi = CORRECTED_SPAN
    m = m[~((m["year"] >= lo) & (m["year"] <= hi))]
    m["abs_err"] = (m["value"] - m["expected"]).abs()
    m["pct_err"] = m["abs_err"] / m["expected"].abs() * 100.0
    n = int(len(m))
    div_years = m[m["pct_err"] > VALIDATOR_TOL_PCT]["year"].astype(int).tolist()

    # Independent-anchor / plausibility suite (Decision 0011) — a RED FAILS the validator.
    anchor = _anchor_section(SERIES_ID)

    status = "PASS" if (not div_years and anchor["status"] == "PASS") else "FAIL"
    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": list(BOOK_OVERLAP),
        "excluded_corrected_span": list(CORRECTED_SPAN),
        "n_compared": n,
        "mae": round(float(m["abs_err"].mean()) if n else float("nan"), 6),
        "max_abs_err": round(float(m["abs_err"].max()) if n else float("nan"), 6),
        "max_pct_err": round(float(m["pct_err"].max()) if n else float("nan"), 6),
        "divergence_years": div_years, "divergence_count": len(div_years),
        "anchor_checks": anchor,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
