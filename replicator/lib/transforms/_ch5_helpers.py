"""Chapter 5 loader helpers — shared Appendix5_DATALRprices reader.

S501-S504 all read the same Shaikh workbook
SalvagedInputs/book_data/ShaikhChoppedTables/Appendix5_DATALRprices.xlsx
(header row 1; row 0 is the DATALRprices banner).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import book_data_path  # noqa: E402

APPENDIX5_XLSX = book_data_path("Appendix5_DATALRprices.xlsx")

# Per Phase 4 / DPR §7: years where a value is a historical fill rather than
# a raw Jastram observation. The loader stamps a proxy_flag on these rows so
# downstream Anu pipeline ledger can audit them.
US_PRE_1800_PROXY_YEARS = set(range(1790, 1800))     # USWPI imputed from CPI
UK_WW2_PROXY_YEARS = set(range(1939, 1946))           # NBER m04053 fill


def load_datalrprices() -> pd.DataFrame:
    """Return the cleaned DATALRprices frame with `Year` as int.

    Caller is responsible for selecting columns (USWPI, UKWPI, USPPIGold,
    UKPPIGold, USGoldpriceindex, UKGoldpriceindex, etc.).
    """
    if not APPENDIX5_XLSX.exists():
        raise FileNotFoundError(f"Appendix5_DATALRprices.xlsx missing: {APPENDIX5_XLSX}")
    df = pd.read_excel(APPENDIX5_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    if "Year" not in df.columns:
        raise RuntimeError(f"DATALRprices: 'Year' column missing; cols={list(df.columns)[:8]}")
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def country_wpi_proxy_flag(year: int, country: str) -> str | None:
    """Return a proxy_flag string for years that are documented historical fills.

    `country` is 'US' or 'UK'.
    """
    if country == "US" and year in US_PRE_1800_PROXY_YEARS:
        return "pre1800_uswpi_via_uscpi"
    if country == "UK" and year in UK_WW2_PROXY_YEARS:
        return "wartime_interpolated_NBER_m04053"
    return None
