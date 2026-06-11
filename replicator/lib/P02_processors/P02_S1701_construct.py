"""P02_S1701_construct - pass-through processor for the long-wave chart.

Reads the three subseries from raw and writes the canonical processed parquet.
Preserves the is_forecast flag for the post-2011 portion of S1701-C.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1701"
IN = DATA_RAW / f"{SERIES_ID}_LONGWAVES.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df.rename(columns={"subsource_id": "source_id"})
    cols = ["year", "value", "subseries_id", "source_id", "units", "is_forecast"]
    out = df[cols].copy().sort_values(["year", "subseries_id"]).reset_index(drop=True)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_processed": int(len(out)),
        "year_range": [int(out["year"].min()), int(out["year"].max())],
        "subseries_present": sorted(out["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "deferred",
                      "reason": "WPI/gold/HP-100 recomposition deferred to Phase 9"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
