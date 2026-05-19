"""P02_S1501_construct - construct S1501 from MeasuringWorth + FRED CPIAUCNS.

Reads:
  Technical/data/raw/S1501_MEASURINGWORTH_USCPI.parquet  (1774-2011)
  Technical/data/raw/S1501_FRED_CPIAUCNS.parquet         (2005-2025; optional)

Writes Technical/data/processed/S1501.parquet with
columns year, value, subseries_id, source_id, units (index_1982_84=100).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, DATA_RAW  # noqa: E402

IN_MW = DATA_RAW / "S1501_MEASURINGWORTH_USCPI.parquet"
IN_FRED = DATA_RAW / "S1501_FRED_CPIAUCNS.parquet"
OUT = DATA_PROCESSED / "S1501.parquet"

BOOK_END_YEAR = 2011
EXT_OVERLAP_YEAR_DEFAULT = 2011


def _extend_with_fred(book: pd.DataFrame, fred_raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    diag: dict = {}
    overlap_year = EXT_OVERLAP_YEAR_DEFAULT
    while overlap_year >= 2005:
        b = book[book["year"] == overlap_year]
        f = fred_raw[fred_raw["year"] == overlap_year]
        if not b.empty and not f.empty:
            bv = float(b["value"].iloc[0]); fv = float(f["value"].iloc[0])
            if not pd.isna(bv) and not pd.isna(fv) and fv != 0:
                break
        overlap_year -= 1
    else:
        return book, {"extension_status": "no_overlap"}
    scale = bv / fv
    ext = fred_raw[fred_raw["year"] > BOOK_END_YEAR].copy()
    ext["value"] = ext["value"] * scale
    ext["units"] = "index_1982_84=100"
    ext = ext.rename(columns={"subsource_id": "source_id"})
    ext = ext[["year", "value", "units", "subseries_id", "source_id"]]
    extended = pd.concat([book, ext], ignore_index=True).sort_values("year").reset_index(drop=True)
    diag = {
        "extension_status": "ok",
        "overlap_year": int(overlap_year),
        "scale_factor": float(scale),
        "book_at_overlap": float(bv),
        "fred_at_overlap": float(fv),
        "years_appended": int(len(ext)),
        "last_year": int(extended["year"].max()),
    }
    return extended, diag


def run() -> dict:
    if not IN_MW.exists():
        return {"status": "FAIL", "error": "MW raw parquet missing - run loader first"}
    mw = pd.read_parquet(IN_MW)
    book = mw.rename(columns={"subsource_id": "source_id"})[
        ["year", "value", "units", "subseries_id", "source_id"]
    ].copy()

    diag: dict
    if IN_FRED.exists():
        fred = pd.read_parquet(IN_FRED)
        final, diag = _extend_with_fred(book, fred)
    else:
        final = book
        diag = {"extension_status": "data_unavailable", "reason": "FRED not loaded"}

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    final.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": diag,
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
