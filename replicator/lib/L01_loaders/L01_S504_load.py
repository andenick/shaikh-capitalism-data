"""L01_S504_load - US WPI in Gold + US Gold Price, 1800-2010 (Fig 5.6).

Reads Shaikh's pre-computed USPPIGold and USGoldpriceindex (both 1930=100).
Extension not attempted in v1: requires US gold price helper (no LBMA helper).
USWPI extension to 2025 is available via S502-C but is not re-fetched here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch5_helpers import load_datalrprices  # noqa: E402

SERIES_ID = "S504"
YEAR_MIN, YEAR_MAX = 1800, 2010
OUT_PPRIME = DATA_RAW / f"{SERIES_ID}_US_WPI_in_GOLD.parquet"
OUT_PG = DATA_RAW / f"{SERIES_ID}_US_GOLD_PRICE_IDX.parquet"


def _slice(df: pd.DataFrame, col: str, sub_id: str) -> pd.DataFrame:
    sub = df[(df["Year"] >= YEAR_MIN) & (df["Year"] <= YEAR_MAX)][["Year", col]].copy()
    sub = sub.rename(columns={"Year": "year", col: "value"}).dropna(subset=["value"])
    sub["units"] = "index_1930=100"
    sub["subseries_id"] = sub_id
    sub["subsource_id"] = "SHAIKH_APPENDIX_5_DATALRPRICES"
    sub["proxy_flag"] = None
    return sub


def run() -> dict:
    try:
        df = load_datalrprices()
    except FileNotFoundError as exc:
        return {"status": "FAIL", "error": str(exc)}

    pprime = _slice(df, "USPPIGold", "S504-A")
    pg = _slice(df, "USGoldpriceindex", "S504-B")

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    pprime.to_parquet(OUT_PPRIME, index=False)
    pg.to_parquet(OUT_PG, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"S504-A_pprime_US": int(len(pprime)),
                        "S504-B_pG_US": int(len(pg))},
        "year_range_book": [YEAR_MIN, YEAR_MAX],
        "sources_fetched": ["SHAIKH_APPENDIX_5_DATALRPRICES"],
        "outputs": [str(OUT_PPRIME), str(OUT_PG)],
        "extension_status": "not_attempted_v1",
        "extension_reasons": {
            "us_wpi": "available_via_S502-C_but_not_re_fetched_here",
            "us_gold_price": "missing_lbma_helper",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
