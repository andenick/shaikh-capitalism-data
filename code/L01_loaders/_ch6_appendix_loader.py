"""Shared helper: load Shaikh (2016) Appendix 6.8 chopped tables in long form.

The 10 Appendix 6.8.I.{1,2,3} and 6.8.II.{1..7} workbooks in
``SalvagedInputs/book_data/ShaikhChoppedTables/`` are Shaikh's own verbatim
construction-pipeline tables: each row is a named variable, each column from
column index 4 onward is a calendar year. Header is on row 1 (zero-indexed).

This helper is invoked by all Ch6 / AS L01 loaders. It exists so that:

* Vintage-stability is preserved: every AS series and S60x series reads its
  variables from the same canonical Shaikh workbook (which itself documents the
  2011 NIPA / BEA FA vintage). Phase 6 extension is delegated to per-series
  EPRs, which describe how to re-fetch each underlying NIPA / BEA / IRS series
  and re-compute the formula end-to-end, never splicing a derived rate.

* The 10 chopped tables are the canonical Shaikh book-truth values (Appendix
  Tables 6.7.* and 6.8.*) for the construction internals, so V03 validators
  validate against the same Excel sheet they loaded from. This is intentional
  for ingestion-phase fanout: extension/divergence behaviour is encoded in
  S00_apis-based extension loaders that the EPR documents.

Layout of every workbook (single sheet "Sheet1"):

    Row 0 : prose description of the table
    Row 1 : header row (used as columns) -- Table | Description | Source | Variable | <years>
            (II.7 has an extra leftmost "Table" col, others start at "Description")
    Row 2+: data rows keyed by 'Variable'

Variables found in each table are listed in CH6_GPIM_SUMMARY.md and in the
README in SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import SALVAGED_BOOK_DATA  # noqa: E402

APPENDIX_DIR = SALVAGED_BOOK_DATA / "ShaikhChoppedTables"


def appendix_path(name: str) -> Path:
    """e.g. appendix_path('II3') -> Appendix6_Table68II3.xlsx"""
    return APPENDIX_DIR / f"Appendix6_Table68{name}.xlsx"


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def load_variables(
    table_name: str,
    variables: Iterable[str],
    *,
    source_label: str | None = None,
) -> pd.DataFrame:
    """Return long-form DataFrame(year, variable, value, source_id) for given vars.

    Parameters
    ----------
    table_name : e.g. 'II3' for Appendix6_Table68II3.xlsx.
    variables  : iterable of Variable-column strings to extract.
    source_label : optional override for the source_id column (default: table_name).
    """
    p = appendix_path(table_name)
    if not p.exists():
        raise FileNotFoundError(f"Appendix table missing: {p}")
    df = _normalize_columns(pd.read_excel(p, header=1))
    if "Variable" not in df.columns:
        raise ValueError(f"{p.name}: 'Variable' column not found; have {list(df.columns)[:5]}")
    # Strip leading/trailing whitespace from Variable cells
    df["Variable"] = df["Variable"].astype(str).str.strip()

    # Year columns are everything that parses as an integer
    year_cols: list[tuple[str, int]] = []
    for c in df.columns:
        try:
            # II.7 has a duplicated '1946.1' — only keep the first '1946'
            if c.endswith(".1") and c[:-2].isdigit():
                continue
            yi = int(float(c))
            if 1900 <= yi <= 2100:
                year_cols.append((c, yi))
        except (ValueError, TypeError):
            continue

    requested = list(variables)
    out_rows: list[dict] = []
    for var in requested:
        sel = df[df["Variable"] == var]
        if sel.empty:
            continue  # caller can decide whether to FAIL; helper stays liberal
        # If duplicates (rare), take the first row
        row = sel.iloc[0]
        for col_str, year_int in year_cols:
            v = row[col_str]
            if pd.isna(v):
                continue
            try:
                fv = float(v)
            except (ValueError, TypeError):
                continue
            out_rows.append({
                "year": year_int,
                "variable": var,
                "value": fv,
                "source_id": source_label or f"SHAIKH_APP_6_8_{table_name}",
            })

    return pd.DataFrame(out_rows)


def variable_year_range(df_long: pd.DataFrame, variable: str) -> tuple[int, int]:
    sub = df_long[df_long["variable"] == variable]
    if sub.empty:
        raise ValueError(f"variable {variable!r} not present in DataFrame")
    return int(sub["year"].min()), int(sub["year"].max())


def pivot_wide(df_long: pd.DataFrame) -> pd.DataFrame:
    """Reshape (year, variable, value) -> wide DataFrame indexed by year."""
    return df_long.pivot_table(index="year", columns="variable", values="value", aggfunc="first").sort_index()
