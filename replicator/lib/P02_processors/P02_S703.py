"""P02_S703 — pass-through processor for the digitized WORLDAVG aggregate line.

The L01 loader already emits canonical long-form (year, value, subseries_id, source_id,
units); this single-line series needs no construction, so P02 is a schema-preserving
pass-through from data/raw/ to data/processed/ (the stage the chopped writer + V03 read).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S703"
IN = DATA_RAW / "S703_MACHINE_FIG7_13_WORLDAVG.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"

_COLS = ["year", "value", "subseries_id", "source_id", "units"]


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "sid": SERIES_ID, "error": f"raw parquet missing: {IN}"}
    df = pd.read_parquet(IN)[_COLS].sort_values("year").reset_index(drop=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "sid": SERIES_ID,
        "rows": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
