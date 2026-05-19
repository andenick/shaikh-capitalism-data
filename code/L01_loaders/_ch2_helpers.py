"""Chapter 2 shared loader helpers.

Centralizes the salvaged-chopped-table read patterns used by S202-S218.

All loaders in Ch2 read from one of the Appendix2_*.xlsx workbooks living
under SalvagedInputs/book_data/ShaikhChoppedTables/. Each helper here
returns the raw frame (no rebasing, no splicing - that lives in P02).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import book_data_path  # noqa: E402


def read_chopped(filename: str, header_row: int = 1, sheet: str | int = 0) -> pd.DataFrame:
    """Read a Ch2 chopped table. Row 0 is the long descriptive header,
    row 1 holds the short column names. Returns a frame with Year as int."""
    path = book_data_path(filename)
    df = pd.read_excel(path, sheet_name=sheet, header=header_row)
    df.columns = [str(c).strip() for c in df.columns]
    if "Year" not in df.columns:
        raise RuntimeError(f"{filename}: 'Year' column missing; cols={list(df.columns)}")
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def book_path(filename: str) -> Path:
    return book_data_path(filename)


def slice_column(
    chopped: pd.DataFrame,
    col: str,
    *,
    subseries_id: str,
    subsource_id: str,
    units: str,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
) -> pd.DataFrame:
    """Extract one column from a chopped table into a long-form frame.
    Filters to year_min/year_max if given. Drops NaNs in value."""
    if col not in chopped.columns:
        raise RuntimeError(f"column missing: {col}; cols={list(chopped.columns)}")
    out = chopped[["Year", col]].rename(columns={"Year": "year", col: "value"}).dropna(subset=["value"])
    if year_min is not None:
        out = out[out["year"] >= year_min]
    if year_max is not None:
        out = out[out["year"] <= year_max]
    out = out.copy()
    out["units"] = units
    out["subseries_id"] = subseries_id
    out["subsource_id"] = subsource_id
    return out[["year", "value", "units", "subseries_id", "subsource_id"]].reset_index(drop=True)


def fred_annual(series_id: str, start: str = "2005-01-01", end: str = "2025-12-31",
                aggregation_method: str = "avg") -> tuple[pd.DataFrame, bool, str | None]:
    """Convenience wrapper for FRED annual fetch with graceful degradation.

    Returns (df, ok, error_msg). df has columns [year, value]. ok=False means
    skipped/failed; caller writes no parquet in that case.
    """
    from S00_setup import S00_apis, S00_config
    if not S00_config.have_key("FRED_API_KEY"):
        return pd.DataFrame(), False, "FRED_API_KEY not set"
    try:
        df = S00_apis.fred_observations(
            series_id=series_id, frequency="a", aggregation_method=aggregation_method,
            observation_start=start, observation_end=end,
        )
    except S00_apis.ApiUnavailable as exc:
        return pd.DataFrame(), False, str(exc)
    df = df.copy()
    df["year"] = df["date"].dt.year.astype(int)
    return df[["year", "value"]].dropna(subset=["value"]).reset_index(drop=True), True, None
