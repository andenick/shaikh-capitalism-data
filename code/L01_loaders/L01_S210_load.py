"""L01_S210_load - US and UK Wholesale Price Indexes, 1780-2010 (Fig 2.10, log scale).

Composite series with NO Appendix 2 chopped table. Per Phase 4 decision 0005,
we use the CD2-preserved consolidated data (S023, two columns US+UK both 1930=100)
as the salvaged book replica until the Jastram (1977) replica is hosted.

Phase 4 substitutions:
  - NBER macrohistory URL updated to https://www.nber.org/research/data/nber-macrohistory-database
  - BLS WPS00000000 frozen 1974 -> we use WPU00000000 via FRED for post-1974 US extension
  - ONS PLLU for UK PPI extension (frequency=annual via FRED's UKPPI proxy unavailable;
    we use FRED PPIACO as a US-only continuation and document UK gap in EPR)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_EXT_BENCH  # noqa: E402
from L01_loaders._ch2_helpers import fred_annual  # noqa: E402

S023_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S023_us_and_uk_wholesale_price_indexes_1790_2010.xlsx"
OUT_US = DATA_RAW / "S210_US_WPI_BOOK.parquet"
OUT_UK = DATA_RAW / "S210_UK_WPI_BOOK.parquet"
OUT_US_EXT = DATA_RAW / "S210_FRED_WPU00000000.parquet"


def _load_s023() -> pd.DataFrame:
    df = pd.read_excel(S023_XLSX, sheet_name="Data")
    df = df.rename(columns={"Year": "year"})
    return df.dropna(subset=["year"]).astype({"year": int})


def run() -> dict:
    if not S023_XLSX.exists():
        return {"status": "FAIL", "error": f"S023 missing: {S023_XLSX}"}
    raw = _load_s023()
    us = raw[["year", "S023-A"]].rename(columns={"S023-A": "value"}).dropna(subset=["value"]).copy()
    us["units"] = "index_1930=100"
    us["subseries_id"] = "S210-A"
    us["subsource_id"] = "JASTRAM_1977_T7_PLUS_BLS_PPI_EXT"
    uk = raw[["year", "S023-B"]].rename(columns={"S023-B": "value"}).dropna(subset=["value"]).copy()
    uk["units"] = "index_1930=100"
    uk["subseries_id"] = "S210-B"
    uk["subsource_id"] = "JASTRAM_1977_T2_PLUS_ONS_PLLU"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    us.to_parquet(OUT_US, index=False)
    uk.to_parquet(OUT_UK, index=False)
    # FRED WPU00000000 (PPI All Commodities) for US extension post-2010
    # Phase 4 substitution: BLS froze WPS00000000 in 1974; WPU is the live successor
    df_us, ok, err = fred_annual("WPU00000000", start="2005-01-01")
    sources = ["JASTRAM_1977_T7_PLUS_BLS_PPI_EXT", "JASTRAM_1977_T2_PLUS_ONS_PLLU"]
    if ok and not df_us.empty:
        df_us["units"] = "index_1982=100"
        df_us["subseries_id"] = "S210-C"
        df_us["subsource_id"] = "FRED_WPU00000000"
        df_us.to_parquet(OUT_US_EXT, index=False)
        sources.append("FRED_WPU00000000")
    return {
        "status": "OK",
        "rows_loaded": {"US_WPI": len(us), "UK_WPI": len(uk),
                        "FRED_WPU": int(len(df_us)) if ok else 0},
        "sources_fetched": sources,
        "fred_status": "ok" if ok else "skipped", "fred_error": err,
        "outputs": [str(OUT_US), str(OUT_UK)] + ([str(OUT_US_EXT)] if ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
