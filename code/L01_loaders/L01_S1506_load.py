"""L01_S1506_load - derived_subperiod loader: reads parent S1505 processed parquet.

S1506 is a deterministic sub-period view of S1505 (1948-1981). No independent
fetch. We write a "raw" parquet that is simply the S1505 processed slice; this
keeps the L01/P02/V03/O06 contract consistent across the pipeline.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

PARENT_PROCESSED = DATA_PROCESSED / "S1505.parquet"
OUT = DATA_RAW / "S1506_S1505_SLICE.parquet"
SUBPERIOD_START = 1948
SUBPERIOD_END = 1981


def run() -> dict:
    if not PARENT_PROCESSED.exists():
        return {"status": "FAIL",
                "error": f"parent S1505 processed parquet missing: {PARENT_PROCESSED}; "
                         f"run S1505 pipeline first"}
    parent = pd.read_parquet(PARENT_PROCESSED)
    sliced = parent[(parent["year"] >= SUBPERIOD_START) & (parent["year"] <= SUBPERIOD_END)].copy()
    # Rename subseries IDs to S1506-* and source_id to indicate derivation
    sliced["subseries_id"] = sliced["subseries_id"].str.replace("S1505-", "S1506-", regex=False)
    sliced["source_id"] = "DERIVED_FROM_S1505"
    sliced = sliced[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sliced.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": int(len(sliced)),
        "subseries": sorted(sliced["subseries_id"].unique().tolist()),
        "year_range": [int(sliced["year"].min()), int(sliced["year"].max())] if len(sliced) else [None, None],
        "sources_fetched": ["DERIVED_FROM_S1505"],
        "derived_from": "S1505",
        "subperiod_years": [SUBPERIOD_START, SUBPERIOD_END],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
