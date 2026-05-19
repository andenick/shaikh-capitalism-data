"""L01_S1406_load - Inflation and Productivity Growth (Ch14 Fig 14.15).

CONCEPT POLICING (Phase 4 Q5 resolution):
  Productivity = real GDP per FTE per Shaikh's exact formula
  yr = (GDP*100/p)/(FEE/1000). The loader REJECTS any per-hour substitute
  (OPHNFB, PRS85006092, OPHPBS, OPHMFG).

Loads:
  - S1406-A: inflrate (Appendix 14.3)
  - S1406-B: GPRODVTY (Appendix 14.3)
  - S1406-C: FRED GDP (annual avg of quarterly)
  - S1406-D: FRED GDPDEF (annual avg of quarterly, current vintage 2017=100)
  - S1406-E: FRED B4701C0A222NBEA (FTE all industries, annual, thousands of jobs)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch14_helpers import (  # noqa: E402
    read_appendix14, fred_annual, assert_no_per_hour_substitution,
)
from S00_setup import S00_apis  # noqa: E402

SERIES_ID = "S1406"
OUT_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
OUT_GDP    = DATA_RAW / f"{SERIES_ID}_FRED_GDP.parquet"
OUT_DEF    = DATA_RAW / f"{SERIES_ID}_FRED_GDPDEF.parquet"
OUT_FEE    = DATA_RAW / f"{SERIES_ID}_FRED_B4701C0A222NBEA.parquet"

# Hard concept-policing assertion: any future maintainer who adds a per-hour
# substitute to this list will fail import.
FRED_INPUTS = ["GDP", "GDPDEF", "B4701C0A222NBEA"]
assert_no_per_hour_substitution(FRED_INPUTS)


def _save_book(df: pd.DataFrame) -> int:
    sub = df[["year", "inflrate", "GPRODVTY"]].copy()
    sub = sub.melt(id_vars="year", var_name="appendix_col", value_name="value")
    sub = sub.dropna(subset=["value"]).reset_index(drop=True)
    sub["subseries_id"] = sub["appendix_col"].map({
        "inflrate":  f"{SERIES_ID}-A",
        "GPRODVTY":  f"{SERIES_ID}-B",
    })
    sub["subsource_id"] = "SHAIKH_APPENDIX_14_3"
    sub["units"] = sub["appendix_col"].map({
        "inflrate":  "decimal_annual_inflation_rate",
        "GPRODVTY":  "decimal_annual_productivity_growth_per_FTE",
    })
    sub["year"] = sub["year"].astype(int)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(OUT_BOOK, index=False)
    return len(sub)


def _save_fred() -> tuple[dict, bool, str | None]:
    try:
        gdp = fred_annual("GDP")
        defl = fred_annual("GDPDEF")
        fee = fred_annual("B4701C0A222NBEA")
    except S00_apis.ApiUnavailable as exc:
        return {}, False, str(exc)
    gdp.assign(units="billions_usd_saar",
               subseries_id=f"{SERIES_ID}-C",
               subsource_id="FRED_GDP").to_parquet(OUT_GDP, index=False)
    defl.assign(units="index_2017=100",
                subseries_id=f"{SERIES_ID}-D",
                subsource_id="FRED_GDPDEF").to_parquet(OUT_DEF, index=False)
    fee.assign(units="thousands_of_jobs",
               subseries_id=f"{SERIES_ID}-E",
               subsource_id="FRED_B4701C0A222NBEA").to_parquet(OUT_FEE, index=False)
    return {"gdp": len(gdp), "gdpdef": len(defl), "fee": len(fee)}, True, None


def run() -> dict:
    book = read_appendix14()
    n_book = _save_book(book)
    fred_rows, fred_ok, fred_err = _save_fred()
    sources = ["SHAIKH_APPENDIX_14_3"]
    if fred_ok:
        sources += ["FRED_GDP", "FRED_GDPDEF", "FRED_B4701C0A222NBEA"]
    return {
        "status": "OK",
        "rows_loaded": {"book": n_book, **fred_rows},
        "sources_fetched": sources,
        "fred_status": "ok" if fred_ok else "skipped",
        "fred_error": fred_err,
        "concept_policing_assertion": "productivity_per_FTE_not_per_hour",
        "rejected_substitutes": ["OPHNFB", "PRS85006092", "OPHPBS", "OPHMFG"],
        "productivity_formula": "(GDP*100/p)/(FEE/1000)  [Appendix 14.2 p. 892 verbatim]",
        "outputs": [str(OUT_BOOK)] + ([str(OUT_GDP), str(OUT_DEF), str(OUT_FEE)] if fred_ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
