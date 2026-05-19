"""L01_ES2303_load — China FX reserves ex-gold from World Bank WDI.

Fetches WDI indicator FI.RES.XGLD.CD for country CHN, 1990-2024, via the
open World Bank Data API. Writes one parquet to Technical/data/raw/.

Source: Weber & Shaikh (2020) Fig 3 (Appendix p. 454).
License: CC-BY-4.0 (World Bank Open Data Terms).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

SERIES_ID = "ES2303"
COUNTRY = "CHN"
INDICATOR = "FI.RES.XGLD.CD"
OUT = DATA_RAW / f"{SERIES_ID}_WB_FI_RES_XGLD_CD.parquet"
START_YEAR = 1990
END_YEAR = 2024


def run() -> dict:
    try:
        df = S00_apis.worldbank_indicator(
            country=COUNTRY, indicator=INDICATOR,
            start=START_YEAR, end=END_YEAR,
        )
    except S00_apis.ApiUnavailable as exc:
        return {"status": "FAIL", "error": f"WDI unavailable: {exc}",
                "wb_status": "api_error"}

    # Convert current USD -> Billion USD (paper presentation unit)
    df = df.copy()
    df["value"] = df["value"] / 1e9
    df["units"] = "billion_usd"
    df["subseries_id"] = f"{SERIES_ID}-A"
    df["subsource_id"] = "WB_FI_RES_XGLD_CD_CHN"
    df = df.dropna(subset=["value"]).reset_index(drop=True)

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"wb_wdi": int(len(df))},
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "sources_fetched": ["WB_FI_RES_XGLD_CD_CHN"],
        "wb_status": "ok",
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
