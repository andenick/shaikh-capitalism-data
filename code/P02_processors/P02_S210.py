"""P02_S210 - emit US and UK WPI on 1930=100 base (folded-A/B design).

The US BLS-PPI extension is already embedded in the S023-A book column (subsource
JASTRAM_1977_T7_PLUS_BLS_PPI_EXT), capped at the last complete year in L01. The
legacy FRED WPU00000000 S210-C extension path was removed (DF-2, 2026-07-02): it
never shipped in the chopped and only diverged the code from the shipped output.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_US = DATA_RAW / "S210_US_WPI_BOOK.parquet"
IN_UK = DATA_RAW / "S210_UK_WPI_BOOK.parquet"
OUT = DATA_PROCESSED / "S210.parquet"


def run() -> dict:
    if not IN_US.exists() or not IN_UK.exists():
        return {"status": "FAIL", "error": "raw missing"}
    us = pd.read_parquet(IN_US).rename(columns={"subsource_id": "source_id"})
    uk = pd.read_parquet(IN_UK).rename(columns={"subsource_id": "source_id"})
    us = us[["year", "value", "units", "subseries_id", "source_id"]]
    uk = uk[["year", "value", "units", "subseries_id", "source_id"]]
    final = pd.concat([us, uk], ignore_index=True).sort_values(["subseries_id", "year"]).reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
