"""V03_S1101_validate - validate S1101 against Appendix11_XMData.xlsx.

The processed parquet IS the book-truth pass-through, so this validator
verifies pipeline integrity (round-trip match within tolerance).
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

SERIES_ID = "S1101"
VALIDATOR_TOL_PCT = 0.5
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
TRUTH_XLSX = book_data_path("Appendix11_XMData.xlsx")
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"


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
    truth = truth.dropna(subset=["Year"])
    truth["Year"] = truth["Year"].astype(int)
    truth = truth.rename(columns={"Year": "year",
                                  "X/M (Trade Balance)": "expected",
                                  "Country": "country"})
    truth = truth[["year", "country", "expected"]].dropna(subset=["expected"])

    merged = actual.merge(truth, on=["year", "country"], how="inner",
                          suffixes=("", "_truth"))
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    merged["pct_err"] = merged["abs_err"] / merged["expected"].abs() * 100.0

    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else 0.0
    max_abs = float(merged["abs_err"].max()) if n else 0.0
    max_pct = float(merged["pct_err"].max()) if n else 0.0
    divergence = merged[merged["pct_err"] > VALIDATOR_TOL_PCT]
    div_years = divergence[["year", "country", "pct_err"]].to_dict("records")
    status = "PASS" if len(div_years) == 0 else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "time_series",
        "comparison_basis": "Appendix11_XMData.xlsx X/M (Trade Balance) column",
        "n_compared": n,
        "mae": round(mae, 6),
        "max_abs_err": round(max_abs, 6),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(div_years),
        "divergences": div_years[:10],
        "cd2_comparison": {"note": "CD2 S060 only cross-checked US; this validator checks all 15 countries."},
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
