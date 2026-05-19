"""P02_S1502_construct - emit processed S1502 (Panel A growth rates).

The loader writes long-form growth rates directly; the processor's job
is to filter to the book window 1988-2010, drop the 1987 NaN row, and
write the canonical schema (year, value, subseries_id, source_id, units).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, DATA_RAW  # noqa: E402

IN = DATA_RAW / "S1502_BEA_INDUSTRY_PANEL_A.parquet"
OUT = DATA_PROCESSED / "S1502.parquet"
BOOK_START = 1988
BOOK_END = 2010


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df[(df["year"] >= BOOK_START) & (df["year"] <= BOOK_END)].copy()
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "data_unavailable",
                      "reason": "BEA Industry API client not yet implemented; book period only"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
