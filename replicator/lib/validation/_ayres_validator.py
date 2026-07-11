"""Shared Ayres validator: compare every (year, month, value) to the raw
Appendix2_Ayres.xlsx values for the appropriate window.
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

CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix2_Ayres.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
TOL_PCT = 1.0
MONTH_TO_NUM = {"Jan": 1, "Jan.": 1, "January": 1,
                "Feb": 2, "Feb.": 2, "February": 2,
                "Mar": 3, "Mar.": 3, "March": 3,
                "Apr": 4, "Apr.": 4, "April": 4,
                "May": 5,
                "Jun": 6, "June": 6,
                "Jul": 7, "July": 7,
                "Aug": 8, "Aug.": 8, "August": 8,
                "Sep": 9, "Sep.": 9, "Sept": 9, "September": 9,
                "Oct": 10, "Oct.": 10, "October": 10,
                "Nov": 11, "Nov.": 11, "November": 11,
                "Dec": 12, "Dec.": 12, "December": 12}


def _book_truth(year_min: int, year_max: int) -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year", "Month", "AyresCycle"]).copy()
    df["year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df["month"] = df["Month"].map(MONTH_TO_NUM)
    df = df.dropna(subset=["year", "month"])
    df["year"] = df["year"].astype(int)
    df["month"] = df["month"].astype(int)
    df = df[(df["year"] >= year_min) & (df["year"] <= year_max)]
    return df[["year", "month", "AyresCycle"]].rename(columns={"AyresCycle": "expected"})


def _update(sid: str, row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[sid] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def validate(sid: str, year_min: int, year_max: int) -> dict:
    processed = DATA_PROCESSED / f"{sid}.parquet"
    if not processed.exists():
        return {"status": "FAIL", "error": f"processed missing: {processed}"}
    actual = pd.read_parquet(processed)
    truth = _book_truth(year_min, year_max)
    m = actual.merge(truth, on=["year", "month"], how="inner")
    # Abs/percent err -- Ayres values are signed deviations, can be near zero; guard div
    m["abs_err"] = (m["value"] - m["expected"]).abs()
    safe = m["expected"].abs().clip(lower=1e-6)
    m["pct_err"] = m["abs_err"] / safe * 100.0
    # For near-zero expected (< 1.0), treat divergence by abs_err threshold instead of pct
    is_div = ((m["expected"].abs() >= 1.0) & (m["pct_err"] > TOL_PCT)) | \
             ((m["expected"].abs() < 1.0) & (m["abs_err"] > 0.5))
    div_rows = m[is_div]
    div_years = sorted(set(div_rows["year"].astype(int).tolist()))
    n = int(len(m))
    row = {
        "status": "PASS" if not div_years else "FAIL", "tolerance_pct": TOL_PCT,
        "compare_range": [year_min, year_max], "n_compared": n,
        "mae": round(float(m["abs_err"].mean()) if n else float("nan"), 6),
        "max_abs_err": round(float(m["abs_err"].max()) if n else float("nan"), 6),
        "max_pct_err": round(float(m["pct_err"].max()) if n else float("nan"), 6),
        "divergence_years": div_years, "divergence_count": len(div_years),
        "frequency": "monthly", "extension_status": "not_applicable_discontinued",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(sid, row)
    return row
