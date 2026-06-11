"""L01_S212_load - US and UK Wholesale Prices in Ounces of Gold, 1790-2010 (Fig 2.12).

Formula series: WPI_in_gold = WPI / gold_price, both rebased to 1930=100.

Source data via CD2's S024 (UK WPI in gold + UK gold price) and S025 (US WPI in
gold + US gold price), themselves derived from Jastram (1977) Golden Constant
Tables 1, 2, 7 + MeasuringWorth gold prices.

Per Phase 4: extension recomputes WPI/gold from extended WPI (FRED WPU) +
extended gold price (MeasuringWorth gold dataset, FRED GOLDPMGBD228NLBM as proxy).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_EXT_BENCH  # noqa: E402
from L01_loaders._ch2_helpers import fred_annual  # noqa: E402

S024_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S024_uk_wpi_in_gold_and_uk_gold_price.xlsx"
S025_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S025_us_wpi_in_gold_and_us_gold_price.xlsx"
OUT_US_GOLD = DATA_RAW / "S212_US_WPI_IN_GOLD.parquet"
OUT_UK_GOLD = DATA_RAW / "S212_UK_WPI_IN_GOLD.parquet"
OUT_GOLD_PRICE = DATA_RAW / "S212_FRED_GOLD_PRICE.parquet"


def run() -> dict:
    if not S024_XLSX.exists() or not S025_XLSX.exists():
        return {"status": "FAIL", "error": "CD2 S024/S025 missing"}
    us_df = pd.read_excel(S025_XLSX, sheet_name="Data").rename(columns={"Year": "year"})
    us_df = us_df.dropna(subset=["year"]).astype({"year": int})
    us = us_df[["year", "S025-A"]].rename(columns={"S025-A": "value"}).dropna(subset=["value"]).copy()
    us["units"] = "index_1930=100"
    us["subseries_id"] = "S212-A"
    us["subsource_id"] = "JASTRAM_1977_T1_MW_US_WPI_GOLD"
    uk_df = pd.read_excel(S024_XLSX, sheet_name="Data").rename(columns={"Year": "year"})
    uk_df = uk_df.dropna(subset=["year"]).astype({"year": int})
    uk = uk_df[["year", "S024-A"]].rename(columns={"S024-A": "value"}).dropna(subset=["value"]).copy()
    uk["units"] = "index_1930=100"
    uk["subseries_id"] = "S212-B"
    uk["subsource_id"] = "JASTRAM_1977_MW_UK_WPI_GOLD"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    us.to_parquet(OUT_US_GOLD, index=False)
    uk.to_parquet(OUT_UK_GOLD, index=False)
    # FRED gold price (London PM fix, USD per oz) for post-2010 extension cross-check
    df_g, ok, err = fred_annual("GOLDPMGBD228NLBM", start="2005-01-01")
    sources = ["JASTRAM_1977_T1_MW_US_WPI_GOLD", "JASTRAM_1977_MW_UK_WPI_GOLD"]
    if ok and not df_g.empty:
        df_g["units"] = "usd_per_oz"
        df_g["subseries_id"] = "S212-X-GOLD"
        df_g["subsource_id"] = "FRED_GOLDPMGBD228NLBM"
        df_g.to_parquet(OUT_GOLD_PRICE, index=False)
        sources.append("FRED_GOLDPMGBD228NLBM")
    return {
        "status": "OK",
        "rows_loaded": {"US_GOLD": len(us), "UK_GOLD": len(uk),
                        "FRED_GOLD": int(len(df_g)) if ok else 0},
        "sources_fetched": sources,
        "fred_status": "ok" if ok else "skipped", "fred_error": err,
        "outputs": [str(OUT_US_GOLD), str(OUT_UK_GOLD)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
