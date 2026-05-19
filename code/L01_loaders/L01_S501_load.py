"""L01_S501_load - US and UK Wholesale Price Indexes, 1790-1940 (Fig 5.3).

Direct chronological slice of S502 (same Appendix5 columns, narrower window).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch5_helpers import load_datalrprices, country_wpi_proxy_flag  # noqa: E402

SERIES_ID = "S501"
YEAR_MIN = 1790
YEAR_MAX = 1940
OUT_US = DATA_RAW / f"{SERIES_ID}_US_WPI_1790_1940.parquet"
OUT_UK = DATA_RAW / f"{SERIES_ID}_UK_WPI_1790_1940.parquet"


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

    us = _slice(df, "USWPI", "S501-A", "US")
    uk = _slice(df, "UKWPI", "S501-B", "UK")

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    us.to_parquet(OUT_US, index=False)
    uk.to_parquet(OUT_UK, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"US": int(len(us)), "UK": int(len(uk))},
        "year_range": [YEAR_MIN, YEAR_MAX],
        "sources_fetched": ["SHAIKH_APPENDIX_5_DATALRPRICES"],
        "outputs": [str(OUT_US), str(OUT_UK)],
        "proxy_flag_counts": {
            "S501-A_pre1800": int(us["proxy_flag"].notna().sum()),
            "S501-B_wartime_1939_1940": int(uk["proxy_flag"].notna().sum()),
        },
        "extension_status": "not_applicable_chronological_slice",
        "notes": "S501 is a fixed 1790-1940 window onto S502; no extension applies.",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
