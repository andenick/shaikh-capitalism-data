"""V03_S801 — validate processed Eichner Fig 8.1 panel against the digitized source.

Round-trips the processed parquet against the level columns of the digitized panel xlsx.
Certifies loader/processor fidelity; underlying values are digitization-grade (provenance:
digitized, overlay-validated vs the book figure — see EXTRACTION_REPORT.md).

F-T2-01 (2026-07-10): the frozen digitized xlsx has its two industry columns TRANSPOSED vs
Shaikh Fig 8.1 (the volatile line is really *Competitive*, the smooth line *Oligopolistic* —
Shaikh p.372 "the smoother prices of the concentrated industries"). L01_S801 corrects the
labels at load; V03 applies the SAME relabel (COLUMN_RELABEL) to the truth xlsx so the
round-trip certifies the corrected mapping, and adds an INDEPENDENT variance sanity check so a
MAE-0.0 round-trip can no longer mask a label transposition.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402
from V03_validators._ch7_validator_lib import validate_against_panel  # noqa: E402

SERIES_ID = "S801"
VALIDATOR_TOL_PCT = 1.0
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
SRC_XLSX = SALVAGED_BOOK_DATA / "Reconstructed" / "Eichner_1973_Fig8_1_S801.xlsx"

# F-T2-01: correct the transposed labels in the frozen truth xlsx to match the figure.
COLUMN_RELABEL = {"Oligopolistic": "Competitive", "Competitive": "Oligopolistic"}


def _variance_sanity_check() -> dict:
    """Independent (round-trip-agnostic) label-assignment check.

    Shaikh p.372: the concentrated/oligopolistic line is the SMOOTHER one. So over the
    common window the *Competitive* series must have STRICTLY GREATER variance than the
    *Oligopolistic* series. This does not read the xlsx, so a transposition that a
    MAE-0.0 round-trip would accept still fails here.
    """
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    df = pd.read_parquet(PROCESSED)

    def _var(ind: str) -> float:
        v = df[df["industry"] == ind]["value"].astype(float)
        return float(v.var(ddof=0)) if len(v) >= 2 else float("nan")

    comp_var = _var("Competitive")
    oligo_var = _var("Oligopolistic")
    ok = comp_var > oligo_var
    return {
        "status": "PASS" if ok else "FAIL",
        "competitive_var": round(comp_var, 6),
        "oligopolistic_var": round(oligo_var, 6),
        "rule": "var(Competitive) > var(Oligopolistic) — concentrated line is smoother (Shaikh p.372)",
    }


def run() -> dict:
    result = validate_against_panel(
        sid=SERIES_ID,
        processed_parquet=PROCESSED,
        chopped_xlsx=SRC_XLSX,
        tolerance_pct=VALIDATOR_TOL_PCT,
        is_deviation=False,
        column_relabel=COLUMN_RELABEL,
    )
    sanity = _variance_sanity_check()
    result["label_variance_check"] = sanity
    if sanity["status"] != "PASS" and result.get("status") == "PASS":
        result["status"] = "FAIL"
        result["error"] = "label variance sanity check failed (possible Competitive/Oligopolistic transposition)"
    return result


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
