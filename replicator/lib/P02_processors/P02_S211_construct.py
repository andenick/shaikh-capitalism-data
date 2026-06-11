"""P02_S211_construct - pass-through US+UK WPI 1780-1940; no extension."""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_US = DATA_RAW / "S211_US_WPI_1790_1940.parquet"
IN_UK = DATA_RAW / "S211_UK_WPI_1790_1940.parquet"
OUT = DATA_PROCESSED / "S211.parquet"


def run() -> dict:
    if not IN_US.exists() or not IN_UK.exists():
        return {"status": "FAIL", "error": "raw missing"}
    us = pd.read_parquet(IN_US).rename(columns={"subsource_id": "source_id"})
    uk = pd.read_parquet(IN_UK).rename(columns={"subsource_id": "source_id"})
    final = pd.concat([us, uk], ignore_index=True).sort_values(["subseries_id", "year"]).reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_windowed",
                      "reason": "Truncated at 1940 by design"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
