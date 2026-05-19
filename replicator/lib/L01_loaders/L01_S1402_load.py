"""L01_S1402_load - Unemployment Measures, US 1948-2011 (Ch14 Fig 14.11).

Loads four subseries:
  - S1402-A: UNEMPLRATE (unemployment rate, decimal) from Appendix 14.3
  - S1402-B: UNEMPDURATION (duration index 1948-51=100) from Appendix 14.3
  - S1402-C: ulintensity (rate * duration_index/100) from Appendix 14.3
  - S1402-D: FRED UNRATE (annual avg of monthly, percent) 1948-2024
  - S1402-E: FRED UEMPMEAN (annual avg of monthly, weeks) 1948-2024

The UEMPMEAN series has a documented 2011-01 top-coding break (raised from
104w to 260w). Per Phase 4 Q2 resolution, no backward adjustment is applied;
the break is annotated in the registry.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch14_helpers import read_appendix14, fred_annual  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

SERIES_ID = "S1402"
OUT_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
OUT_UNRATE = DATA_RAW / f"{SERIES_ID}_FRED_UNRATE.parquet"
OUT_UEMPMEAN = DATA_RAW / f"{SERIES_ID}_FRED_UEMPMEAN.parquet"


def _save_book(df: pd.DataFrame) -> int:
    sub = df[["year", "UNEMPLRATE", "UNEMPDURATION", "ulintensity"]].copy()
    sub = sub.melt(id_vars="year", var_name="appendix_col", value_name="value")
    sub = sub.dropna(subset=["value"]).reset_index(drop=True)
    sub["subseries_id"] = sub["appendix_col"].map({
        "UNEMPLRATE":    f"{SERIES_ID}-A",
        "UNEMPDURATION": f"{SERIES_ID}-B",
        "ulintensity":   f"{SERIES_ID}-C",
    })
    sub["subsource_id"] = "SHAIKH_APPENDIX_14_3"
    sub["units"] = sub["appendix_col"].map({
        "UNEMPLRATE":    "decimal_rate",
        "UNEMPDURATION": "index_1948_1951_avg=100",
        "ulintensity":   "decimal",
    })
    sub["year"] = sub["year"].astype(int)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(OUT_BOOK, index=False)
    return len(sub)


def _save_fred_pair() -> tuple[int, int, bool, str | None]:
    try:
        ur = fred_annual("UNRATE")        # percent, SA
        ud = fred_annual("UEMPMEAN")      # weeks, SA
    except S00_apis.ApiUnavailable as exc:
        return 0, 0, False, str(exc)
    ur = ur.assign(units="percent",
                   subseries_id=f"{SERIES_ID}-D",
                   subsource_id="FRED_UNRATE")
    ud = ud.assign(units="weeks",
                   subseries_id=f"{SERIES_ID}-E",
                   subsource_id="FRED_UEMPMEAN")
    ur.to_parquet(OUT_UNRATE, index=False)
    ud.to_parquet(OUT_UEMPMEAN, index=False)
    return len(ur), len(ud), True, None


def run() -> dict:
    book = read_appendix14()
    n_book = _save_book(book)
    n_ur, n_ud, fred_ok, fred_err = _save_fred_pair()
    sources = ["SHAIKH_APPENDIX_14_3"]
    if fred_ok:
        sources += ["FRED_UNRATE", "FRED_UEMPMEAN"]
    return {
        "status": "OK",
        "rows_loaded": {"book": n_book, "fred_unrate": n_ur, "fred_uempmean": n_ud},
        "sources_fetched": sources,
        "fred_status": "ok" if fred_ok else "skipped",
        "fred_error": fred_err,
        "methodological_break_2011-01": True,
        "break_description": "BLS raised UEMPMEAN top-coding from 104w to 260w in 2011-01",
        "break_treatment": "no_adjustment_documented_break",
        "outputs": [str(OUT_BOOK)] + ([str(OUT_UNRATE), str(OUT_UEMPMEAN)] if fred_ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
