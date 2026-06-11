"""P02_S1506_construct - emit processed S1506 (1948-1981 slice of S1505)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, DATA_RAW  # noqa: E402

IN = DATA_RAW / "S1506_S1505_SLICE.parquet"
OUT = DATA_PROCESSED / "S1506.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())] if len(df) else [None, None],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_closed_subperiod",
                      "rationale": "S1506 is the closed pre-Volcker sub-period of S1505 by design"},
        "output": str(OUT),
        "derived_from": "S1505",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
