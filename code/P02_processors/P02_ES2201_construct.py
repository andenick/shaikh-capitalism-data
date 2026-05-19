"""P02_ES2201_construct — pass-through for ES2201 five-parameter panel."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "ES2201"
IN = DATA_RAW / f"{SERIES_ID}_TABLE1.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df.rename(columns={"subsource_id": "source_id"})
    df = df[["year", "value", "subseries_id", "source_id", "units"]].copy()
    df = df.sort_values(["subseries_id", "year"]).reset_index(drop=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_count": int(df["subseries_id"].nunique()),
        "extension": {"extension_status": "v1_1_deferred",
                      "reason": "Requires IRS SOI 2017+ re-fit via paper MLE protocol"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
