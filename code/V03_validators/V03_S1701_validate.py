"""V03_S1701_validate - validate S1701 against Appendix5_DATALRprices.xlsx.

Cell-by-cell check that each subseries' value matches the corresponding
salvage workbook column.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, book_data_path  # noqa: E402

SERIES_ID = "S1701"
VALIDATOR_TOL_PCT = 0.5
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
TRUTH_XLSX = book_data_path("Appendix5_DATALRprices.xlsx")
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

SUB_TO_COL = {
    "S1701-A": "USPPIGOLDHP100",
    "S1701-B": "UKPPIGOLDHP100",
    "S1701-C": "USUKAVGWAVE",
}


def _update_report(row: dict) -> None:
    rpt = (json.loads(REPORT.read_text(encoding="utf-8"))
           if REPORT.exists() else
           {"schema_version": "anu-validation-v1.0", "series": {}})
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[SERIES_ID] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    if not TRUTH_XLSX.exists():
        return {"status": "FAIL", "error": f"book truth missing: {TRUTH_XLSX}"}

    actual = pd.read_parquet(PROCESSED)
    truth = pd.read_excel(TRUTH_XLSX, header=1)
    truth = truth.dropna(subset=["Year"])
    truth["Year"] = pd.to_numeric(truth["Year"], errors="coerce").astype("Int64")
    truth = truth.dropna(subset=["Year"]).astype({"Year": int})

    abs_errs = []
    pct_errs = []
    divs = []
    n_compared = 0

    for sub_id, col in SUB_TO_COL.items():
        sub_act = actual[actual["subseries_id"] == sub_id]
        sub_truth = truth[["Year", col]].rename(
            columns={"Year": "year", col: "expected"}).dropna()
        merged = sub_act.merge(sub_truth, on="year", how="inner")
        for _, r in merged.iterrows():
            v = float(r["value"])
            e = float(r["expected"])
            ae = abs(v - e)
            pe = ae / abs(e) * 100.0 if abs(e) > 1e-12 else 0.0
            abs_errs.append(ae)
            pct_errs.append(pe)
            n_compared += 1
            if pe > VALIDATOR_TOL_PCT:
                divs.append({"sub": sub_id, "year": int(r["year"]),
                             "pct_err": round(pe, 6),
                             "value": v, "expected": e})

    mae = float(sum(abs_errs) / len(abs_errs)) if abs_errs else 0.0
    max_pct = max(pct_errs) if pct_errs else 0.0
    status = "PASS" if not divs else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "time_series",
        "comparison_basis": "Appendix5_DATALRprices.xlsx columns USPPIGOLDHP100, UKPPIGOLDHP100, USUKAVGWAVE",
        "n_compared": n_compared,
        "mae": round(mae, 6),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(divs),
        "divergences": divs[:10],
        "cd2_comparison": {"note": "CD2 S102 was actually the IRS-2011 table (now S1702/S1703); long-wave figure had no CD2 predecessor under S102."},
        "forecast_layer_note": "Post-2011 USUKAVGWAVE values are forecast; preserved with is_forecast=True flag in processed parquet.",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
