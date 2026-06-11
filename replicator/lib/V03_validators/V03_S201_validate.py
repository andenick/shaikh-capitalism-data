"""V03_S201_validate — validate processed S201 against the book chopped table.

Compares Technical/data/processed/S201.parquet (column 'value') against the
'IndProd_Final' column of the salvaged chopped table
SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_IndustrialProduction.xlsx
on the overlap range 1860-2010.

Tolerance: +/- 1.0% per year (configurable via VALIDATOR_TOL_PCT).
A year is a 'divergence_year' if abs(actual - expected) / expected > tol.

Emits:
  - returns dict {status: PASS|FAIL, mae, max_abs_err, n_compared, divergence_years, ...}
  - writes/updates Technical/VALIDATION_REPORT.json with the S201 row
  - also reports CD2 divergence (informational, never affects status)
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA, SALVAGED_EXT_BENCH  # noqa: E402

PROCESSED = DATA_PROCESSED / "S201.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix2_IndustrialProduction.xlsx"
CD2_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S001_us_industrial_production_index.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 1.0   # +/- 1% per year
BOOK_OVERLAP = (1860, 2010)


def _load_book_truth() -> pd.DataFrame:
    """Read the chopped table; return DataFrame[year, expected]."""
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    out = df[["Year", "IndProd_Final"]].rename(columns={"Year": "year", "IndProd_Final": "expected"})
    out = out.dropna(subset=["expected"])
    return out


def _load_cd2() -> pd.DataFrame | None:
    """Optional informational comparison against CD2's S001."""
    if not CD2_XLSX.exists():
        return None
    try:
        df = pd.read_excel(CD2_XLSX, sheet_name="Data")
        # CD2 final = S001-B for 1860-1918, S001-D for 1919-2010
        df = df.rename(columns={"Year": "year"})
        # Take whichever rebased column is non-NaN (B for early, D for late)
        df["cd2"] = df["S001-D [R:1958]"].fillna(df["S001-B [R:1958]"])
        return df[["year", "cd2"]].dropna()
    except Exception:
        return None


def _update_report(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S201"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed file missing: {PROCESSED}"}
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"book truth missing: {CHOPPED_XLSX}"}

    actual_df = pd.read_parquet(PROCESSED)
    truth_df = _load_book_truth()

    merged = actual_df.merge(truth_df, on="year", how="inner")
    merged = merged[(merged["year"] >= BOOK_OVERLAP[0]) & (merged["year"] <= BOOK_OVERLAP[1])]

    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    merged["pct_err"] = merged["abs_err"] / merged["expected"].abs() * 100.0

    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max()) if n else float("nan")
    divergence = merged[merged["pct_err"] > VALIDATOR_TOL_PCT][["year", "value", "expected", "pct_err"]]
    div_years = divergence["year"].astype(int).tolist()

    status = "PASS" if len(div_years) == 0 else "FAIL"

    # Informational CD2 divergence
    cd2_info: dict = {}
    cd2_df = _load_cd2()
    if cd2_df is not None:
        cd2_merge = actual_df.merge(cd2_df, on="year", how="inner")
        cd2_merge = cd2_merge[(cd2_merge["year"] >= BOOK_OVERLAP[0]) & (cd2_merge["year"] <= BOOK_OVERLAP[1])]
        cd2_merge["abs_err"] = (cd2_merge["value"] - cd2_merge["cd2"]).abs()
        cd2_merge["pct_err"] = cd2_merge["abs_err"] / cd2_merge["cd2"].abs() * 100.0
        cd2_info = {
            "n": int(len(cd2_merge)),
            "mae": float(cd2_merge["abs_err"].mean()),
            "max_pct_err": float(cd2_merge["pct_err"].max()),
            "note": "Informational. CD2 used a different FRB reindex anchor; ~1-2% divergence expected and acceptable.",
        }

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
        "cd2_comparison": cd2_info,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
