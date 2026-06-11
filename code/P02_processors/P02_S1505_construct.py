"""P02_S1505_construct - construct processed S1505 (Phillips-curve dataset)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, DATA_RAW  # noqa: E402

IN = DATA_RAW / "S1505_USINFLATION_CHOPPED.parquet"
OUT = DATA_PROCESSED / "S1505.parquet"
BOOK_START = 1948
BOOK_END = 2010


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df[(df["year"] >= BOOK_START) & (df["year"] <= BOOK_END)].copy()
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    df = df.sort_values(["year", "subseries_id"]).reset_index(drop=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "data_unavailable",
                      "reason": "BEA NIPA API client not yet implemented; book period only"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
