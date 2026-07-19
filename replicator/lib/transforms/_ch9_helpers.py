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


# ---------------------------------------------------------------------------
# classification_vintage (Decision 0014 / SI-3, CH9-F4 fix)
# ---------------------------------------------------------------------------
# The ch9 I-O benchmark cross-sections span two industry-classification eras:
#   1947/1958/1963/1967/1972 -> Ochoa 71-order on a SIC basis        = SIC71
#   1998                      -> BEA 65-order on a NAICS basis        = NAICS65
# These orders are NOT conformable; silently concatenating rows across them is a
# latent splice error. classification_vintage tags each cross-section so the
# chopped-writer guard can refuse a mixed-vintage concat.
VINTAGE_BY_YEAR: dict[int, str] = {
    1947: "SIC71", 1958: "SIC71", 1963: "SIC71", 1967: "SIC71", 1972: "SIC71",
    1998: "NAICS65",
}

# Persistent subseries-id suffixes -> vintage. Benchmark cross-section subseries only;
# cross-benchmark aggregates/derived (e.g. S902-ROBS, S903-R-*, S903-PWT-*) return ""
# (guard-not-applicable) so they are never flagged by the per-subseries vintage guard.
_SIC71_SUFFIXES = ("_1947F", "_1958F", "_1963F", "_1967F", "_1972F",
                   "-47", "-58", "-63", "-67", "-72")
_NAICS65_SUFFIXES = ("_1998C", "_1998F", "-98CIRC", "-98FIX")


def assert_benchmark_vintage(year: int, label: str = "") -> str:
    """Return the known classification_vintage for a benchmark year; raise on mismatch.

    The CH9-F4 loader assertion (Decision 0014): a benchmark year must resolve to its
    registered classification era. Raises AssertionError if the year is unknown or the
    label's embedded year disagrees.
    """
    if year not in VINTAGE_BY_YEAR:
        raise AssertionError(
            f"ch9 benchmark year {year} has no registered classification_vintage "
            f"(known: {sorted(VINTAGE_BY_YEAR)})"
        )
    vintage = VINTAGE_BY_YEAR[year]
    if label:
        # label embeds the year (e.g. '1947F', '1998C'); sanity-check it agrees.
        expect_naics = str(year) == "1998"
        is_naics = vintage == "NAICS65"
        if expect_naics != is_naics:  # pragma: no cover - defensive
            raise AssertionError(f"ch9 label {label!r} vs year {year} vintage mismatch")
    return vintage


def classification_vintage_for_subseries(subseries_id: str) -> str:
    """Map an I-O subseries_id to its classification_vintage by suffix ("" if aggregate)."""
    s = subseries_id.upper()
    if s.endswith(_NAICS65_SUFFIXES):
        return "NAICS65"
    if s.endswith(_SIC71_SUFFIXES):
        return "SIC71"
    return ""


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
