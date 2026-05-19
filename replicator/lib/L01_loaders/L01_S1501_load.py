"""L01_S1501_load - fetch raw inputs for S1501 (U.S. CPI 1774-2025).

Fetches two inputs:
  - MeasuringWorth USCPI 1774-2011 from the salvaged chopped table
    written to Technical/data/raw/S1501_MEASURINGWORTH_USCPI.parquet
  - FRED CPIAUCNS 2010-2025 via API (annual avg of monthly CPI-U)
    written to Technical/data/raw/S1501_FRED_CPIAUCNS.parquet

Graceful degradation: if FRED_API_KEY missing or API fails, only the book
segment is published downstream.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from S00_setup import S00_apis, S00_config  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix15_MeasuringWorthCPI.xlsx")
OUT_MW = DATA_RAW / "S1501_MEASURINGWORTH_USCPI.parquet"
OUT_FRED = DATA_RAW / "S1501_FRED_CPIAUCNS.parquet"
FRED_SERIES_ID = "CPIAUCNS"
BOOK_END_YEAR = 2011


def _load_chopped() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def _save_mw(chopped: pd.DataFrame) -> int:
    mw = (
        chopped[chopped["Year"] <= BOOK_END_YEAR]
        [["Year", "U.S. Consumer Price Index"]]
        .rename(columns={"Year": "year", "U.S. Consumer Price Index": "value"})
        .dropna(subset=["value"])
    )
    mw["units"] = "index_1982_84=100"
    mw["subseries_id"] = "S1501-A"
    mw["subsource_id"] = "MEASURINGWORTH_USCPI"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    mw.to_parquet(OUT_MW, index=False)
    return len(mw)


def _save_fred() -> tuple[int, bool, str | None]:
    if not S00_config.have_key("FRED_API_KEY"):
        return 0, False, "FRED_API_KEY not set"
    try:
        df = S00_apis.fred_observations(
            series_id=FRED_SERIES_ID,
            frequency="a",
            aggregation_method="avg",
            observation_start="2005-01-01",
            observation_end="2025-12-31",
        )
    except S00_apis.ApiUnavailable as exc:
        return 0, False, str(exc)
    df = df.copy()
    df["year"] = df["date"].dt.year.astype(int)
    df = df[["year", "value"]]
    df["units"] = "index_1982_84=100"
    df["subseries_id"] = "S1501-B"
    df["subsource_id"] = "FRED_CPIAUCNS"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT_FRED, index=False)
    return len(df), True, None


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}
    chopped = _load_chopped()
    n_mw = _save_mw(chopped)
    n_fred, fred_ok, fred_err = _save_fred()
    sources = ["MEASURINGWORTH_USCPI"]
    if fred_ok:
        sources.append("FRED_CPIAUCNS")
    return {
        "status": "OK",
        "rows_loaded": {"MW": n_mw, "FRED": n_fred},
        "sources_fetched": sources,
        "fred_status": "ok" if fred_ok else "skipped",
        "fred_error": fred_err,
        "outputs": [str(OUT_MW)] + ([str(OUT_FRED)] if fred_ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
