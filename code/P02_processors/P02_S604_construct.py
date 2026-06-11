"""P02_S604_construct — construct S604 from raw parquet (pass-through with cleaning).

Reads Technical/data/raw/S604_raw.parquet (one row per (year, subseries_id))
and writes Technical/data/processed/S604.parquet with the canonical
``year, value, subseries_id, source_id, units`` columns.

Construction: the Shaikh Appendix 6.8 chopped tables already contain the
finished S604 columns; the loader applied unit normalization at fetch time
(AS007/AS009 thousands->billions; others identity). The processor enforces
the 5-column schema, deduplicates, and sorts.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S604"
IN = DATA_RAW / f"{SERIES_ID}_raw.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df[["year", "value", "subseries_id", "source_id", "units"]].copy()
    df = df.drop_duplicates(subset=["year", "subseries_id"], keep="first")
    df = df.sort_values(["subseries_id", "year"]).reset_index(drop=True)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
