"""Shared helpers for the Ch7 BEA / OECD industry-panel loaders.

The Shaikh Appendix 7.2 xlsx files for ROP/IROP/OECD all share the same shape:
  - Row 0: descriptive title (e.g. 'Average Rate of Profit, US Indusries, 1987-2005')
  - Row 1: column names ('Year', then N industry names, an aggregate, then *_Deviation
           columns mirroring the industry columns)
  - Rows 2..end: annual values

These helpers read the xlsx, split level vs deviation columns, and emit long-form
DataFrames suitable for processor union.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


DEV_SUFFIXES = ("_Deviation", "_Dev")
AGGREGATE_KEYS = ("All Private", "All Industries", "All_Private", "All_Industries")


def _is_dev_col(col: str) -> bool:
    return any(col.endswith(sfx) for sfx in DEV_SUFFIXES)


def _strip_dev_suffix(col: str) -> str:
    for sfx in DEV_SUFFIXES:
        if col.endswith(sfx):
            return col[: -len(sfx)]
    return col


def _is_aggregate(col: str) -> bool:
    base = _strip_dev_suffix(col)
    return base in AGGREGATE_KEYS


def read_panel(xlsx_path: Path) -> pd.DataFrame:
    """Read header-row-1 xlsx; return DataFrame indexed by Year (int) with cleaned cols."""
    df = pd.read_excel(xlsx_path, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def _sanitize_industry_label(s: str) -> str:
    """Sanitize industry name into a safe subseries_id suffix (alnum + dashes)."""
    return "".join(ch if ch.isalnum() else "-" for ch in s).strip("-")


def levels_long(panel: pd.DataFrame, subseries_id: str, subsource_id: str,
                units: str, include_aggregate: bool = True) -> pd.DataFrame:
    """Convert level columns (non-_Dev) to long form: (year, value, subseries_id, source_id, units, industry).

    The subseries_id is suffixed per industry so that (year, subseries_id) is unique
    (required by O06_chopped_writer's no-dupe check).
    """
    rows = []
    for col in panel.columns:
        if col == "Year":
            continue
        if _is_dev_col(col):
            continue
        if not include_aggregate and _is_aggregate(col):
            continue
        ind_safe = _sanitize_industry_label(col)
        for _, r in panel.iterrows():
            val = pd.to_numeric(r[col], errors="coerce")
            if pd.isna(val):
                continue
            rows.append({
                "year": int(r["Year"]),
                "value": float(val),
                "subseries_id": f"{subseries_id}-{ind_safe}",
                "source_id": subsource_id,
                "units": units,
                "industry": col,
            })
    return pd.DataFrame(rows)


def deviations_long(panel: pd.DataFrame, subseries_id: str, subsource_id: str,
                    units: str, include_aggregate: bool = False) -> pd.DataFrame:
    """Convert _Deviation / _Dev columns to long form, with industry-suffixed subseries_id."""
    rows = []
    for col in panel.columns:
        if not _is_dev_col(col):
            continue
        base = _strip_dev_suffix(col)
        if not include_aggregate and _is_aggregate(col):
            continue
        ind_safe = _sanitize_industry_label(base)
        for _, r in panel.iterrows():
            val = pd.to_numeric(r[col], errors="coerce")
            if pd.isna(val):
                continue
            rows.append({
                "year": int(r["Year"]),
                "value": float(val),
                "subseries_id": f"{subseries_id}-{ind_safe}",
                "source_id": subsource_id,
                "units": units,
                "industry": base,
            })
    return pd.DataFrame(rows)


def industries_in_panel(panel: pd.DataFrame, include_deviations: bool = False,
                        include_aggregate: bool = True) -> Iterable[str]:
    out = []
    for col in panel.columns:
        if col == "Year":
            continue
        if _is_dev_col(col) and not include_deviations:
            continue
        if not include_aggregate and _is_aggregate(col):
            continue
        out.append(col)
    return out
