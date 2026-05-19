"""V03_S1501_validate - validate processed S1501 against the book chopped table.

Compares Technical/data/processed/S1501.parquet 'value' against the
'U.S. Consumer Price Index' column of Appendix15_MeasuringWorthCPI.xlsx
on overlap 1774-2011.
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

PROCESSED = DATA_PROCESSED / "S1501.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix15_MeasuringWorthCPI.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1774, 2011)
CD2_SPOTCHECK = {1774: 7.82, 1899: 8.04, 1949: 23.85, 1999: 166.60}


def _load_book_truth() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df[["Year", "U.S. Consumer Price Index"]].rename(
        columns={"Year": "year", "U.S. Consumer Price Index": "expected"}
    ).dropna(subset=["expected"])


def _update_report(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S1501"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = _load_book_truth()
    merged = actual.merge(truth, on="year", how="inner")
    merged = merged[(merged["year"] >= BOOK_OVERLAP[0]) & (merged["year"] <= BOOK_OVERLAP[1])]
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    merged["pct_err"] = merged["abs_err"] / merged["expected"].abs() * 100.0
    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max()) if n else float("nan")
    div_years = merged[merged["pct_err"] > VALIDATOR_TOL_PCT]["year"].astype(int).tolist()
    status = "PASS" if not div_years else "FAIL"

    cd2_info = {}
    for y, expected in CD2_SPOTCHECK.items():
        row = actual[actual["year"] == y]
        if not row.empty:
            v = float(row["value"].iloc[0])
            cd2_info[y] = {"expected_cd2": expected, "actual": v,
                           "diff_pct": abs(v - expected) / expected * 100.0}

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": list(BOOK_OVERLAP),
        "n_compared": n,
        "mae": round(mae, 6),
        "max_abs_err": round(max_abs, 6),
        "max_pct_err": round(max_pct, 6),
        "divergence_years": div_years,
        "divergence_count": len(div_years),
        "cd2_spotcheck": cd2_info,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
