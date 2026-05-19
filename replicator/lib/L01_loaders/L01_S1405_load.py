"""L01_S1405_load - HP(100) wage-share growth vs unemployment intensity (Ch14 Fig 14.14).

Loads:
  - S1405-A: gwshhp100 (HP100-filtered wage-share growth) from Appendix 14.3
  - S1405-B: ulintensityhp100 (HP100-filtered unemployment intensity)
  - S1405-FIT1: GWSHHP100RAL8AF (era-1 1949-1982 fitted curve, Phillips form)
  - S1405-FIT2: GWSHHP100RAL8BP1F (era-2 1994-2011 fitted curve, Phillips form)

The fitted-curve columns are Shaikh's published constrained (b=1) Phillips fits.
The processor will additionally compute both constrained and unconstrained fits
from the data per Phase 4 Q3 resolution, omitting the 1983-1993 transition
window (Q4 resolution).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch14_helpers import read_appendix14  # noqa: E402

SERIES_ID = "S1405"
OUT_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"


def _save_book(df: pd.DataFrame) -> int:
    cols = {
        "gwshhp100":         (f"{SERIES_ID}-A",    "decimal_hp100_growth_rate"),
        "ulintensityhp100":  (f"{SERIES_ID}-B",    "decimal_hp100"),
        "GWSHHP100RAL8AF":   (f"{SERIES_ID}-FIT1", "decimal_phillips_fit_era1_constrained_b1"),
        "GWSHHP100RAL8BP1F": (f"{SERIES_ID}-FIT2", "decimal_phillips_fit_era2_constrained_b1"),
    }
    sub = df[["year"] + list(cols.keys())].copy()
    sub = sub.melt(id_vars="year", var_name="appendix_col", value_name="value")
    sub = sub.dropna(subset=["value"]).reset_index(drop=True)
    sub["subseries_id"] = sub["appendix_col"].map(lambda k: cols[k][0])
    sub["units"]        = sub["appendix_col"].map(lambda k: cols[k][1])
    sub["subsource_id"] = "SHAIKH_APPENDIX_14_3"
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
        "fit_variants_emitted": ["constrained_b1", "unconstrained_b_free"],
        "era_windows": ["1949-1982", "1994-2011"],
        "transition_omitted": "1983-1993",
        "outputs": [str(OUT_BOOK)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
