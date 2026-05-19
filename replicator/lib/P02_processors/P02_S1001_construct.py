"""P02_S1001_construct — assemble S1001 from book IROP panel.

Composite of two parallel subseries (Banks, All Private), 1988-2005.
Pass-through; no transformation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_A = DATA_RAW / "S1001_BANKS.parquet"
IN_B = DATA_RAW / "S1001_ALL_PRIVATE.parquet"
OUT = DATA_PROCESSED / "S1001.parquet"


def run() -> dict:
    if not IN_A.exists() or not IN_B.exists():
        return {"status": "FAIL", "error": "raw parquet missing", "missing":
                [str(p) for p in (IN_A, IN_B) if not p.exists()]}
    a = pd.read_parquet(IN_A)
    b = pd.read_parquet(IN_B)
    df = pd.concat([a, b], ignore_index=True).rename(columns={"subsource_id": "source_id"})
    df = df.sort_values(["year", "subseries_id"]).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
