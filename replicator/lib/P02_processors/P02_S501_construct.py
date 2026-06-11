"""P02_S501_construct - concat US + UK WPI sliced parquets into S501."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_US = DATA_RAW / "S501_US_WPI_1790_1940.parquet"
IN_UK = DATA_RAW / "S501_UK_WPI_1790_1940.parquet"
OUT = DATA_PROCESSED / "S501.parquet"


def run() -> dict:
    for p in (IN_US, IN_UK):
        if not p.exists():
            return {"status": "FAIL", "error": f"missing {p}"}
    us = pd.read_parquet(IN_US).rename(columns={"subsource_id": "source_id"})
    uk = pd.read_parquet(IN_UK).rename(columns={"subsource_id": "source_id"})
    final = pd.concat([us, uk], ignore_index=True).sort_values(
        ["year", "subseries_id"]).reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_chronological_slice"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
