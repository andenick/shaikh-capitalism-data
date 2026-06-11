"""P02_S218_construct - pass-through Maddison richest/poorest 4; no auto-extension."""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN = DATA_RAW / "S218_MADDISON_RICHEST_POOREST_4.parquet"
OUT = DATA_PROCESSED / "S218.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": "raw missing"}
    df = pd.read_parquet(IN).rename(columns={"subsource_id": "source_id"})
    cols = ["year", "value", "subseries_id", "source_id", "units", "label"]
    df = df[cols]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "deferred",
                      "reason": "MPD 2023 extension requires Shaikh exclusion rule reapplication (and possibly new exclusions); manual Phase 9 work"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
