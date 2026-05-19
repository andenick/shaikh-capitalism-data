"""L01_S1401_load - Nominal GDP Growth and Level of Wage Share (Ch14 Fig 14.10).

Loads three subseries:
  - S1401-A: wage share level (wagesh) 1948-2011 from Appendix 14.3
  - S1401-B: nominal GDP growth (ggdp) 1948-2011 from Appendix 14.3 (NaN at 1948)
  - S1401-C: nominal GDP level via FRED GDP (annual avg of quarterly) for 1948-2024
  - S1401-D: Compensation of Employees via FRED A576RC1 (annual) for 1948-2024

The Appendix 14.3 spreadsheet is the canonical Shaikh-published reference. FRED
inputs power the post-2011 extension via re-derivation in the processor.

Writes raw parquets to Technical/data/raw/S1401_*.parquet.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch14_helpers import read_appendix14, fred_annual  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

SERIES_ID = "S1401"
OUT_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
OUT_FRED_GDP = DATA_RAW / f"{SERIES_ID}_FRED_GDP.parquet"
OUT_FRED_EC = DATA_RAW / f"{SERIES_ID}_FRED_A576RC1.parquet"


def _save_book(df: pd.DataFrame) -> int:
    sub = df[["year", "wagesh", "ggdp"]].copy()
    sub = sub.melt(id_vars="year", var_name="appendix_col", value_name="value")
    sub = sub.dropna(subset=["value"]).reset_index(drop=True)
    sub["subseries_id"] = sub["appendix_col"].map({
        "wagesh": f"{SERIES_ID}-A",
        "ggdp":   f"{SERIES_ID}-B",
    })
    sub["subsource_id"] = "SHAIKH_APPENDIX_14_3"
    sub["units"] = sub["appendix_col"].map({
        "wagesh": "decimal_ratio",  # EC/GDP
        "ggdp":   "decimal_annual_growth_rate",
    })
    sub["year"] = sub["year"].astype(int)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(OUT_BOOK, index=False)
    return len(sub)


def _save_fred_pair() -> tuple[int, int, bool, str | None]:
    try:
        gdp = fred_annual("GDP")           # billions USD, SAAR
        ec  = fred_annual("A576RC1")       # billions USD, NIPA T1.10 line 2
    except S00_apis.ApiUnavailable as exc:
        return 0, 0, False, str(exc)
    gdp = gdp.assign(units="billions_usd_saar",
                     subseries_id=f"{SERIES_ID}-C",
                     subsource_id="FRED_GDP")
    ec  = ec.assign(units="billions_usd",
                    subseries_id=f"{SERIES_ID}-D",
                    subsource_id="FRED_A576RC1")
    gdp.to_parquet(OUT_FRED_GDP, index=False)
    ec.to_parquet(OUT_FRED_EC, index=False)
    return len(gdp), len(ec), True, None


def run() -> dict:
    book = read_appendix14()
    n_book = _save_book(book)
    n_gdp, n_ec, fred_ok, fred_err = _save_fred_pair()
    sources = ["SHAIKH_APPENDIX_14_3"]
    if fred_ok:
        sources += ["FRED_GDP", "FRED_A576RC1"]
    return {
        "status": "OK",
        "rows_loaded": {"book": n_book, "fred_gdp": n_gdp, "fred_ec": n_ec},
        "sources_fetched": sources,
        "fred_status": "ok" if fred_ok else "skipped",
        "fred_error": fred_err,
        "outputs": [str(OUT_BOOK)] + ([str(OUT_FRED_GDP), str(OUT_FRED_EC)] if fred_ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
