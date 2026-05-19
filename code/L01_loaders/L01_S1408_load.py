"""L01_S1408_load - HP(100) nominal-wage growth vs unemployment intensity (Ch14 Fig 14.17).

Loads:
  - S1408-A: GMWAGEHP100 from Appendix 14.3
  - S1408-B: ulintensityhp100 from Appendix 14.3

Inherits productivity concept-policing from S1406 (nominal wage w = EC*100/FEE
uses the same FEE denominator).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch14_helpers import read_appendix14, assert_no_per_hour_substitution  # noqa: E402

SERIES_ID = "S1408"
OUT_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"

assert_no_per_hour_substitution([])  # no FRED inputs here (S1406 holds them)


def _save_book(df: pd.DataFrame) -> int:
    sub = df[["year", "GMWAGEHP100", "ulintensityhp100"]].copy()
    sub = sub.melt(id_vars="year", var_name="appendix_col", value_name="value")
    sub = sub.dropna(subset=["value"]).reset_index(drop=True)
    sub["subseries_id"] = sub["appendix_col"].map({
        "GMWAGEHP100":      f"{SERIES_ID}-A",
        "ulintensityhp100": f"{SERIES_ID}-B",
    })
    sub["subsource_id"] = "SHAIKH_APPENDIX_14_3"
    sub["units"] = sub["appendix_col"].map({
        "GMWAGEHP100":      "decimal_hp100_nominal_wage_growth_rate",
        "ulintensityhp100": "decimal_hp100",
    })
    sub["year"] = sub["year"].astype(int)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(OUT_BOOK, index=False)
    return len(sub)


def run() -> dict:
    book = read_appendix14()
    n = _save_book(book)
    return {
        "status": "OK",
        "rows_loaded": {"book": n},
        "sources_fetched": ["SHAIKH_APPENDIX_14_3"],
        "hp_lambda": 100,
        "concept_policing_inherited_from": "S1406",
        "nominal_wage_formula": "EC*100/FEE  -- per-FTE not per-hour",
        "sample_windows_table_14_3": ["1949-1982", "1994-2011"],
        "outputs": [str(OUT_BOOK)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
