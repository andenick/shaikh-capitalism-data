"""P02_S301_construct — pass-through processor for S301 theoretical curve.

Reads:
    Technical/data/raw/S301_THEORETICAL.parquet

Writes:
    Technical/data/processed/S301.parquet

For theoretical curves there is no construction (no rebase, no splice). The
processor copies raw -> processed with the canonical schema, renaming
subsource_id -> source_id.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S301"
IN = DATA_RAW / f"{SERIES_ID}_THEORETICAL.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw parquet missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df.rename(columns={"subsource_id": "source_id"})
    cols = ["year", "x_value", "value", "subseries_id", "source_id", "units"]
    df = df[cols].sort_values(["subseries_id", "x_value"]).reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "x_range": [float(df["x_value"].min()), float(df["x_value"].max())],
        "value_range": [float(df["value"].min()), float(df["value"].max())],
        "extension": {"extension_status": "not_applicable_theoretical"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
