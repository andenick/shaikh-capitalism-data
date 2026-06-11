"""P02_S1702_construct - pass-through processor for Fig 17.2 bottom-97% income."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1702"
IN = DATA_RAW / f"{SERIES_ID}_IRS_2011_BOTTOM97.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df.rename(columns={"subsource_id": "source_id"})
    out = df[["year", "value", "subseries_id", "source_id", "units",
              "country", "country_key", "agi_midpoint_usd", "agi_label"]].copy()
    out = out.sort_values(["year", "subseries_id", "agi_midpoint_usd"]).reset_index(drop=True)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_processed": int(len(out)),
        "subseries_present": sorted(out["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_cross_sectional"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
