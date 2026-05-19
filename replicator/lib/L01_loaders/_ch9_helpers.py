"""Chapter 9 loader helpers — shared Appendix9 workbook readers.

The historical IO workbooks (1947, 1958, 1963, 1967, 1972) share a 12-column
schema with `Index`, `tpm`, `td`, `tv`, `tp(r)` plus 4 normalized variants and
3 quotient columns. The 1998 workbooks (Circ + Fixed) share a 9-column schema
with the same first 8 columns.

`normalize_industry_frame` re-derives the normalized columns from the raw
absolute values so the loader output is exact (the workbook's own normalized
columns are rounded to 6-7 decimals).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import book_data_path  # noqa: E402


# 7 benchmark-year files used by S901 + S902. Each entry:
#   (display_year, label_suffix, filename, expected_industries, capital_model)
APPENDIX9_BENCHMARKS = [
    (1947, "1947F", "Appendix9_1947fixed.xlsx", 71, "fixed"),
    (1958, "1958F", "Appendix9_1958fixed.xlsx", 71, "fixed"),
    (1963, "1963F", "Appendix9_1963fixed.xlsx", 71, "fixed"),
    (1967, "1967F", "Appendix9_1967fixed.xlsx", 71, "fixed"),
    (1972, "1972F", "Appendix9_1972fixed.xlsx", 71, "fixed"),
    (1998, "1998C", "Appendix9_1998Circ.xlsx", 65, "circulating"),
    (1998, "1998F", "Appendix9_1998Fixed.xlsx", 65, "fixed"),
]


REQUIRED_COLS = {"Index", "tpm", "td", "tv", "tp(r)"}


def read_benchmark(filename: str) -> pd.DataFrame:
    """Read an Appendix9_*fixed.xlsx or Appendix9_1998*.xlsx workbook.

    Header row index is 1 (row 0 is the LTVCalc banner). Filters to rows where
    `Index` is a finite positive integer (the industry rows).
    """
    path = book_data_path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    df = pd.read_excel(path, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise RuntimeError(f"{filename}: missing columns {missing}; have {list(df.columns)[:12]}")
    df = df.dropna(subset=["Index"]).copy()
    df["Index"] = pd.to_numeric(df["Index"], errors="coerce")
    df = df.dropna(subset=["Index"])
    df["Index"] = df["Index"].astype(int)
    df = df[df["Index"] >= 1].copy()
    return df


def normalize_industry_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Add normalized variants of tpm, td, tv, tp(r). All sum to 1."""
    out = df.copy()
    for raw, norm in [("tpm", "tpm_norm"), ("td", "td_norm"),
                      ("tv", "tv_norm"), ("tp(r)", "tpr_norm")]:
        col_sum = out[raw].sum()
        out[norm] = out[raw] / col_sum
    return out
