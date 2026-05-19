"""L01_S203_load - US Real GDP per Capita (MeasuringWorth).

Direct port of MeasuringWorth's Real GDP per Capita series from the salvaged
Appendix2_MeasuringWorthGDP_1889-2010.xlsx (column 'Real GDP per Capita_2005Dollars').

Extension: MeasuringWorth uscompensation->uswage rename applies to S207; for S203
the canonical /datasets/usgdp/ remains live (HTTP 200). MeasuringWorth doesn't
publish a JSON API; we use the salvaged chopped table as canonical book data
and rely on annual MW workbook refresh as the extension path. For automated
extension we use FRED A939RX0Q048SBEA (Real GDP per capita, chained 2017 $)
reindexed at 2010 overlap.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch2_helpers import read_chopped, slice_column, fred_annual  # noqa: E402

CHOPPED = "Appendix2_MeasuringWorthGDP_1889-2010.xlsx"
OUT_MW = DATA_RAW / "S203_MEASURINGWORTH_USGDP.parquet"
OUT_FRED = DATA_RAW / "S203_FRED_RGDPPC.parquet"
FRED_SERIES_ID = "A939RX0Q048SBEA"   # Real GDP per Capita, chained 2017 $


def run() -> dict:
    chopped = read_chopped(CHOPPED)
    mw = slice_column(
        chopped, "Real GDP per Capita_2005Dollars",
        subseries_id="S203-A", subsource_id="MEASURINGWORTH_USGDP",
        units="real_dollars_2005",
    )
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    mw.to_parquet(OUT_MW, index=False)
    df, ok, err = fred_annual(FRED_SERIES_ID, start="2005-01-01")
    if ok and not df.empty:
        df = df.copy()
        df["units"] = "chained_2017_dollars"
        df["subseries_id"] = "S203-B"
        df["subsource_id"] = "FRED_RGDPPC"
        df.to_parquet(OUT_FRED, index=False)
    sources = ["MEASURINGWORTH_USGDP"] + (["FRED_RGDPPC"] if ok else [])
    return {
        "status": "OK",
        "rows_loaded": {"MW": len(mw), "FRED": int(len(df)) if ok else 0},
        "sources_fetched": sources,
        "fred_status": "ok" if ok else "skipped",
        "fred_error": err,
        "outputs": [str(OUT_MW)] + ([str(OUT_FRED)] if ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
