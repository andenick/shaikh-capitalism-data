"""L01_S503_load - UK WPI in Gold + UK Gold Price, 1790-2010 (Fig 5.5).

Reads pre-computed Shaikh columns UKPPIGold (= p'_UK = UKWPI/pG_UK rebased)
and UKGoldpriceindex (= pG_UK rebased), both 1930=100. Extension not attempted
in v1 (requires UK PPI 2011+ and UK gold price helper, neither implemented).

WW2 wartime years 1939-1945 are flagged as proxy_flag=ww2_gold_suspension_interpolated_measuringworth
per Phase 4 ratification.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch5_helpers import load_datalrprices  # noqa: E402

SERIES_ID = "S503"
YEAR_MIN, YEAR_MAX = 1790, 2010
WW2_YEARS = set(range(1939, 1946))
OUT_PPRIME = DATA_RAW / f"{SERIES_ID}_UK_WPI_in_GOLD.parquet"
OUT_PG = DATA_RAW / f"{SERIES_ID}_UK_GOLD_PRICE_IDX.parquet"


def _slice(df: pd.DataFrame, col: str, sub_id: str) -> pd.DataFrame:
    sub = df[(df["Year"] >= YEAR_MIN) & (df["Year"] <= YEAR_MAX)][["Year", col]].copy()
    sub = sub.rename(columns={"Year": "year", col: "value"}).dropna(subset=["value"])
    sub["units"] = "index_1930=100"
    sub["subseries_id"] = sub_id
    sub["subsource_id"] = "SHAIKH_APPENDIX_5_DATALRPRICES"
    sub["proxy_flag"] = sub["year"].map(
        lambda y: "ww2_gold_suspension_interpolated_measuringworth"
        if int(y) in WW2_YEARS else None)
    return sub


def run() -> dict:
    try:
        df = load_datalrprices()
    except FileNotFoundError as exc:
        return {"status": "FAIL", "error": str(exc)}

    pprime = _slice(df, "UKPPIGold", "S503-A")
    pg = _slice(df, "UKGoldpriceindex", "S503-B")

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    pprime.to_parquet(OUT_PPRIME, index=False)
    pg.to_parquet(OUT_PG, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"S503-A_pprime_UK": int(len(pprime)),
                        "S503-B_pG_UK": int(len(pg))},
        "year_range_book": [YEAR_MIN, YEAR_MAX],
        "sources_fetched": ["SHAIKH_APPENDIX_5_DATALRPRICES"],
        "outputs": [str(OUT_PPRIME), str(OUT_PG)],
        "wartime_proxy_flagged_years": sorted(int(y) for y in WW2_YEARS),
        "extension_status": "not_attempted_v1",
        "extension_reasons": {
            "uk_wpi": "api_unavailable_ons_pllu_cdn_502",
            "uk_gold_price": "missing_lbma_helper_and_boe_fx_helper",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
