"""L01_S1507_load - derived_subperiod loader: reads parent S1505 processed parquet.

S1507 covers 1982-2010 (post-Volcker era; forward-extendable when S1505 is extended).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

PARENT_PROCESSED = DATA_PROCESSED / "S1505.parquet"
OUT = DATA_RAW / "S1507_S1505_SLICE.parquet"
SUBPERIOD_START = 1982
SUBPERIOD_END_DEFAULT = 2010  # extended forward as S1505 extends


def run() -> dict:
    if not PARENT_PROCESSED.exists():
        return {"status": "FAIL",
                "error": f"parent S1505 processed parquet missing: {PARENT_PROCESSED}; "
                         f"run S1505 pipeline first"}
    parent = pd.read_parquet(PARENT_PROCESSED)
    # Extend window to whatever S1505 actually contains past 2010
    upper = max(SUBPERIOD_END_DEFAULT, int(parent["year"].max()) if len(parent) else SUBPERIOD_END_DEFAULT)
    sliced = parent[(parent["year"] >= SUBPERIOD_START) & (parent["year"] <= upper)].copy()
    sliced["subseries_id"] = sliced["subseries_id"].str.replace("S1505-", "S1507-", regex=False)
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
        "subperiod_years": [SUBPERIOD_START, upper],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
