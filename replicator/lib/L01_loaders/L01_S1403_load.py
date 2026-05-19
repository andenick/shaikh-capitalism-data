"""L01_S1403_load - Wage Share vs Unemployment Intensity (Ch14 Fig 14.12).

Quarterly phase plot. Loads the inputs needed to construct quarterly
HP(100)-filtered wage share and unemployment intensity.

Phase 4 substitutions / decisions:
  - Dead FRED W270RE1Q156NBEA (404) replaced by W209RC1 + GDP at quarterly
    frequency (within-FRED routing update; same underlying NIPA T1.10 line 2).
  - Quarterly intensity (per Q1 resolution): aggregate monthly UNRATE and
    UEMPMEAN to quarterly means; rebase duration to 1948Q1-1951Q4 (16-quarter)
    base; intensity = quarterly_UNRATE * (quarterly_duration_index/100).
  - HP lambda=100 (NOT 1600 for quarterly) per Shaikh Appendix 14.2 p. 893.

Falls back gracefully if FRED key absent: in that case, only the Appendix 14.3
annual reference values (subseries S1403-A/B) are emitted; the quarterly phase
plot is not constructed.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch14_helpers import (  # noqa: E402
    read_appendix14, fred_quarterly, fred_monthly_to_quarterly,
)
from S00_setup import S00_apis  # noqa: E402

SERIES_ID = "S1403"
OUT_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
OUT_GDP_Q = DATA_RAW / f"{SERIES_ID}_FRED_GDP_Q.parquet"
OUT_EC_Q  = DATA_RAW / f"{SERIES_ID}_FRED_W209RC1_Q.parquet"
OUT_UNRATE_Q = DATA_RAW / f"{SERIES_ID}_FRED_UNRATE_Q.parquet"
OUT_UEMPMEAN_Q = DATA_RAW / f"{SERIES_ID}_FRED_UEMPMEAN_Q.parquet"


def _save_book_annual_reference(df: pd.DataFrame) -> int:
    # Phase plot has no per-year "value", but we keep the annual HP-filtered
    # series from the Appendix as a reference axis for validation.
    sub = df[["year", "wageshhp100", "ulintensityhp100"]].copy()
    sub = sub.melt(id_vars="year", var_name="appendix_col", value_name="value")
    sub = sub.dropna(subset=["value"]).reset_index(drop=True)
    sub["subseries_id"] = sub["appendix_col"].map({
        "wageshhp100":      f"{SERIES_ID}-A",
        "ulintensityhp100": f"{SERIES_ID}-B",
    })
    sub["subsource_id"] = "SHAIKH_APPENDIX_14_3"
    sub["units"] = sub["appendix_col"].map({
        "wageshhp100":      "decimal_ratio_hp100",
        "ulintensityhp100": "decimal_hp100",
    })
    sub["year"] = sub["year"].astype(int)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(OUT_BOOK, index=False)
    return len(sub)


def _save_quarterly() -> tuple[dict, bool, str | None]:
    try:
        gdp_q = fred_quarterly("GDP")               # billions USD SAAR
        ec_q  = fred_quarterly("W209RC1")           # billions USD SAAR
        ur_q  = fred_monthly_to_quarterly("UNRATE")     # percent
        ud_q  = fred_monthly_to_quarterly("UEMPMEAN")   # weeks
    except S00_apis.ApiUnavailable as exc:
        return {}, False, str(exc)
    gdp_q.assign(units="billions_usd_saar",
                 subseries_id=f"{SERIES_ID}-Q_GDP",
                 subsource_id="FRED_GDP_Q").to_parquet(OUT_GDP_Q, index=False)
    ec_q.assign(units="billions_usd_saar",
                subseries_id=f"{SERIES_ID}-Q_EC",
                subsource_id="FRED_W209RC1_Q").to_parquet(OUT_EC_Q, index=False)
    ur_q.assign(units="percent",
                subseries_id=f"{SERIES_ID}-Q_UNRATE",
                subsource_id="FRED_UNRATE_Q_FROM_MONTHLY").to_parquet(OUT_UNRATE_Q, index=False)
    ud_q.assign(units="weeks",
                subseries_id=f"{SERIES_ID}-Q_UEMPMEAN",
                subsource_id="FRED_UEMPMEAN_Q_FROM_MONTHLY").to_parquet(OUT_UEMPMEAN_Q, index=False)
    return {"gdp_q": len(gdp_q), "ec_q": len(ec_q), "unrate_q": len(ur_q), "uempmean_q": len(ud_q)}, True, None


def run() -> dict:
    book = read_appendix14()
    n_book = _save_book_annual_reference(book)
    q_rows, fred_ok, fred_err = _save_quarterly()
    sources = ["SHAIKH_APPENDIX_14_3"]
    if fred_ok:
        sources += ["FRED_GDP_Q", "FRED_W209RC1_Q", "FRED_UNRATE_Q_FROM_MONTHLY",
                    "FRED_UEMPMEAN_Q_FROM_MONTHLY"]
    return {
        "status": "OK",
        "rows_loaded": {"book_annual_ref": n_book, **q_rows},
        "sources_fetched": sources,
        "fred_status": "ok" if fred_ok else "skipped",
        "fred_error": fred_err,
        "url_substitution": {
            "deprecated": "W270RE1Q156NBEA",
            "active": "W209RC1 + GDP (quarterly pair)",
            "rationale": "W270RE1Q156NBEA returns HTTP 404; W209RC1/GDP reconstructs same NIPA T1.10 line 2 wage share",
        },
        "hp_lambda": 100,
        "intensity_construction": "quarterly_UNRATE * (quarterly_duration_index_rebased_1948Q1-1951Q4/100)",
        "outputs": [str(OUT_BOOK)] + ([str(OUT_GDP_Q), str(OUT_EC_Q), str(OUT_UNRATE_Q), str(OUT_UEMPMEAN_Q)] if fred_ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
