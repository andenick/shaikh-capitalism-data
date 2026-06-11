"""P02_S217_construct - pass-through Maddison regions; no auto-extension."""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN = DATA_RAW / "S217_MADDISON_REGIONS.parquet"
OUT = DATA_PROCESSED / "S217.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": "raw missing"}
    df = pd.read_parquet(IN).rename(columns={"subsource_id": "source_id"})
    cols = ["year", "value", "subseries_id", "source_id", "units", "region"]
    df = df[cols]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "deferred",
                      "reason": "MPD 2023 1990GK->2011PPP base change + regional re-aggregation; manual splice needed"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
