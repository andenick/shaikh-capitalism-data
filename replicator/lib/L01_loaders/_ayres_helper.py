"""Shared loader for the Ayres (1939) monthly business-cycle index.

The Appendix2_Ayres.xlsx workbook contains monthly observations 1831-1939
for a single column 'AyresCycle'. Figures 2.4A/B/C in Shaikh (2016) are
three subperiod windows of the same underlying series. We load it once
and slice per series.

Per Phase 4 adequacy: no modern continuation -- historical-only. The
processor and validator therefore mark extension_status as not_applicable.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED = book_data_path("Appendix2_Ayres.xlsx")
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


def load_ayres_monthly() -> pd.DataFrame:
    """Return long-form Ayres monthly frame: year, month, value."""
    df = pd.read_excel(CHOPPED, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year", "Month", "AyresCycle"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df["month"] = df["Month"].map(MONTH_TO_NUM)
    df = df.dropna(subset=["Year", "month"]).copy()
    df["Year"] = df["Year"].astype(int)
    df["month"] = df["month"].astype(int)
    return df.rename(columns={"Year": "year", "AyresCycle": "value"})[["year", "month", "value"]]


def slice_window(year_min: int, year_max: int, subseries_id: str) -> pd.DataFrame:
    df = load_ayres_monthly()
    df = df[(df["year"] >= year_min) & (df["year"] <= year_max)].copy()
    df["units"] = "percent_deviation_from_trend"
    df["subseries_id"] = subseries_id
    df["subsource_id"] = "AYRES_1939_T9_APP_A"
    return df[["year", "month", "value", "units", "subseries_id", "subsource_id"]].reset_index(drop=True)


def save_window(year_min: int, year_max: int, sid: str, out_name: str) -> int:
    df = slice_window(year_min, year_max, f"{sid}-A")
    out = DATA_RAW / out_name
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    return len(df)
