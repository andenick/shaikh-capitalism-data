"""L01_S203 - US Real GDP per Capita (MeasuringWorth).

Direct port of MeasuringWorth's Real GDP per Capita series from the salvaged
Appendix2_MeasuringWorthGDP_1889-2010.xlsx (column 'Real GDP per Capita_2005Dollars').

Extension: MeasuringWorth uscompensation->uswage rename applies to S207; for S203
the canonical /datasets/usgdp/ remains live (HTTP 200). MeasuringWorth doesn't
publish a JSON API; we use the salvaged chopped table as canonical book data
and rely on annual MW workbook refresh as the extension path. For automated
extension we use FRED A939RX0Q048SBEA (Real GDP per capita, chained 2017 $)
reindexed at 2010 overlap.

Source-corruption remediation (Decision 0008 / campaign backlog T1.2):
    The salvaged book column ('Real GDP per Capita_2005Dollars') is corrupt across
    the Great Depression — real GDP/capita RISES through 1929-1934 (economically
    impossible). The salvaged workbook itself is left untouched as historical
    evidence; the correction lives in the pipeline. This loader additionally loads a
    FRESH re-pull of the MeasuringWorth 'usgdp' Real-GDP-per-capita series
    (2026 vintage, year-2017 dollars), retrieved 2026-07-01 from
    https://www.measuringworth.com/datasets/usgdp/ and committed verbatim at
    ``data/raw/S203_MEASURINGWORTH_USGDP_repull_20260701.csv``. P02_S203 re-bases the
    re-pull to the book's 2005$ level (overlap reindex) and replaces ONLY the corrupt
    1930-1944 rows. The book column is still loaded byte-faithfully below so the
    corruption remains inspectable and V03 can round-trip the retained (non-corrupt)
    years against it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch2_helpers import read_chopped, slice_column, fred_annual  # noqa: E402
from utils.vintage_manifest import realtime_window  # noqa: E402

CHOPPED = "Appendix2_MeasuringWorthGDP_1889-2010.xlsx"
OUT_MW = DATA_RAW / "S203_MEASURINGWORTH_USGDP.parquet"
OUT_REPULL = DATA_RAW / "S203_MEASURINGWORTH_REPULL.parquet"
OUT_FRED = DATA_RAW / "S203_FRED_RGDPPC.parquet"
FRED_SERIES_ID = "A939RX0Q048SBEA"   # Real GDP per Capita, chained 2017 $
# Fresh MeasuringWorth usgdp re-pull committed as a raw input (Decision 0008).
REPULL_CSV = DATA_RAW / "S203_MEASURINGWORTH_USGDP_repull_20260701.csv"
REPULL_COL = "Real GDP per capita (year 2017 dollars)"
REPULL_RETRIEVED = "2026-07-01"


def _load_repull() -> pd.DataFrame:
    """Load the committed MeasuringWorth re-pull CSV as a long-form raw frame
    (native year-2017 dollars, untransformed). P02 handles the re-base."""
    raw = pd.read_csv(REPULL_CSV, skiprows=1, thousands=",")
    raw.columns = [str(c).strip() for c in raw.columns]
    out = raw[["Year", REPULL_COL]].rename(columns={"Year": "year", REPULL_COL: "value"})
    out["year"] = pd.to_numeric(out["year"], errors="coerce")
    out["value"] = pd.to_numeric(out["value"], errors="coerce")
    out = out.dropna(subset=["year", "value"]).copy()
    out["year"] = out["year"].astype(int)
    out["units"] = "real_dollars_2017"
    out["subseries_id"] = "S203-A"
    out["subsource_id"] = "MEASURINGWORTH_USGDP"
    out["retrieved"] = REPULL_RETRIEVED
    return out[["year", "value", "units", "subseries_id", "subsource_id", "retrieved"]].reset_index(drop=True)


def run() -> dict:
    chopped = read_chopped(CHOPPED)
    mw = slice_column(
        chopped, "Real GDP per Capita_2005Dollars",
        subseries_id="S203-A", subsource_id="MEASURINGWORTH_USGDP",
        units="real_dollars_2005",
    )
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    mw.to_parquet(OUT_MW, index=False)
    repull = _load_repull()
    repull.to_parquet(OUT_REPULL, index=False)
    df, ok, err = fred_annual(FRED_SERIES_ID, start="2005-01-01",
                              realtime=realtime_window("S203", FRED_SERIES_ID))
    if ok and not df.empty:
        df = df.copy()
        df["units"] = "chained_2017_dollars"
        df["subseries_id"] = "S203-B"
        df["subsource_id"] = "FRED_RGDPPC"
        df.to_parquet(OUT_FRED, index=False)
    sources = ["MEASURINGWORTH_USGDP"] + (["FRED_RGDPPC"] if ok else [])
    return {
        "status": "OK",
        "rows_loaded": {"MW": len(mw), "REPULL": int(len(repull)),
                        "FRED": int(len(df)) if ok else 0},
        "sources_fetched": sources + ["MEASURINGWORTH_USGDP_REPULL"],
        "repull_retrieved": REPULL_RETRIEVED,
        "fred_status": "ok" if ok else "skipped",
        "fred_error": err,
        "outputs": [str(OUT_MW), str(OUT_REPULL)] + ([str(OUT_FRED)] if ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
