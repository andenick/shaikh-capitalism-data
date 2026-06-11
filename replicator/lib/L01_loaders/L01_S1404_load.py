"""L01_S1404_load - Raw wage-share-growth vs unemployment intensity (Ch14 Fig 14.13).

Direct read of Appendix 14.3 columns gwsh (wage-share growth) and ulintensity.
Extension via re-derivation in the processor from S1401 + S1402 components.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch14_helpers import read_appendix14  # noqa: E402

SERIES_ID = "S1404"
OUT_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"


def _save_book(df: pd.DataFrame) -> int:
    sub = df[["year", "gwsh", "ulintensity"]].copy()
    sub = sub.melt(id_vars="year", var_name="appendix_col", value_name="value")
    sub = sub.dropna(subset=["value"]).reset_index(drop=True)
    sub["subseries_id"] = sub["appendix_col"].map({
        "gwsh":        f"{SERIES_ID}-A",
        "ulintensity": f"{SERIES_ID}-B",
    })
    sub["subsource_id"] = "SHAIKH_APPENDIX_14_3"
    sub["units"] = sub["appendix_col"].map({
        "gwsh":        "decimal_annual_growth_rate",
        "ulintensity": "decimal",
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
        "gwsh_formula": "ln(wagesh_t) - ln(wagesh_{t-1}) -- first observation lost",
        "outputs": [str(OUT_BOOK)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
