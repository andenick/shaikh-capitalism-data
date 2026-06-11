"""L01_S502_load - US and UK Wholesale Price Indexes, 1790-2010 (Fig 5.4).

Book period from Appendix5_DATALRprices (USWPI, UKWPI columns), plus optional
US extension 2011+ from FRED WPU00000000 (BLS PPI All Commodities; successor
to legacy WPS00000000 frozen 1974). UK extension is not fetched (ONS PLLU CDN
unavailable per Phase 4); UK 2011+ left NaN with documented status.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch5_helpers import load_datalrprices, country_wpi_proxy_flag  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

SERIES_ID = "S502"
YEAR_MIN, YEAR_MAX = 1790, 2010
OUT_US = DATA_RAW / f"{SERIES_ID}_US_WPI_BOOK.parquet"
OUT_UK = DATA_RAW / f"{SERIES_ID}_UK_WPI_BOOK.parquet"
OUT_US_EXT = DATA_RAW / f"{SERIES_ID}_FRED_PPIACO.parquet"


def _fred_ppiaco_annual() -> tuple:
    """Annual-avg PPIACO from FRED no-key CSV endpoint (FRED's mirror of BLS WPU00000000).

    Returns (df_year_value, ok, err).
    """
    try:
        df = S00_apis.fred_csv_observations("PPIACO", ttl_days=30)
    except S00_apis.ApiUnavailable as exc:
        return None, False, str(exc)
    df = df.copy()
    df["year"] = df["date"].dt.year.astype(int)
    annual = df.groupby("year", as_index=False)["value"].mean()
    annual = annual.dropna(subset=["value"]).reset_index(drop=True)
    return annual, True, None


def _slice(df: pd.DataFrame, col: str, sub_id: str, country: str) -> pd.DataFrame:
    sub = df[(df["Year"] >= YEAR_MIN) & (df["Year"] <= YEAR_MAX)][["Year", col]].copy()
    sub = sub.rename(columns={"Year": "year", col: "value"}).dropna(subset=["value"])
    sub["units"] = "index_1930=100"
    sub["subseries_id"] = sub_id
    sub["subsource_id"] = "SHAIKH_APPENDIX_5_DATALRPRICES"
    sub["proxy_flag"] = sub["year"].map(lambda y: country_wpi_proxy_flag(int(y), country))
    return sub


def run() -> dict:
    try:
        df = load_datalrprices()
    except FileNotFoundError as exc:
        return {"status": "FAIL", "error": str(exc)}

    us = _slice(df, "USWPI", "S502-A", "US")
    uk = _slice(df, "UKWPI", "S502-B", "UK")
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    us.to_parquet(OUT_US, index=False)
    uk.to_parquet(OUT_UK, index=False)

    # US extension via FRED PPIACO (FRED's mirror of BLS PPI All Commodities = WPU00000000)
    fred_df, fred_ok, fred_err = _fred_ppiaco_annual()
    sources = ["SHAIKH_APPENDIX_5_DATALRPRICES"]
    if fred_ok and fred_df is not None and not fred_df.empty:
        fred_df = fred_df.copy()
        fred_df["units"] = "index_1982=100"
        fred_df["subseries_id"] = "S502-C"
        fred_df["subsource_id"] = "FRED_PPIACO"
        fred_df["proxy_flag"] = None
        fred_df.to_parquet(OUT_US_EXT, index=False)
        sources.append("FRED_PPIACO")

    return {
        "status": "OK",
        "rows_loaded": {"US_book": int(len(us)), "UK_book": int(len(uk)),
                        "US_ext_FRED_PPIACO": int(len(fred_df)) if fred_ok else 0},
        "year_range_book": [YEAR_MIN, YEAR_MAX],
        "sources_fetched": sources,
        "fred_status": "ok" if fred_ok else "skipped", "fred_error": fred_err,
        "uk_extension_status": "api_unavailable_ons_pllu_cdn_502",
        "uk_extension_note": ("ONS PLLU CDN returns 502 from our IP "
                              "(Phase 4 reachability 2026-05-18); UK 2011+ left NaN."),
        "outputs": [str(OUT_US), str(OUT_UK)] + ([str(OUT_US_EXT)] if fred_ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
