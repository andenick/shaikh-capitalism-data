"""Shared Ayres processor: pass through monthly raw to processed, no transforms.

The book figure plots monthly values; the chopped CSV likewise should hold one
row per (year, month). For the standard year/value processed schema we keep
month as a separate column when present.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402


def process(sid: str, raw_filename: str) -> dict:
    raw = DATA_RAW / raw_filename
    if not raw.exists():
        return {"status": "FAIL", "error": f"raw missing: {raw}"}
    df = pd.read_parquet(raw)
    df = df.rename(columns={"subsource_id": "source_id"})
    # Final schema: year, value, subseries_id, source_id, units, month
    cols = ["year", "value", "subseries_id", "source_id", "units"]
    if "month" in df.columns:
        cols.append("month")
    out_df = df[cols].copy()
    out = DATA_PROCESSED / f"{sid}.parquet"
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out_df.to_parquet(out, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(out_df)),
        "year_range": [int(out_df["year"].min()), int(out_df["year"].max())],
        "subseries_present": sorted(out_df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_discontinued",
                      "reason": "Ayres (1939) has no modern continuation"},
        "output": str(out),
    }
