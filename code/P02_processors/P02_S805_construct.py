"""P02_S805_construct — emit processed S805 (Demsetz 1963/1969 cross-sections)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, DATA_RAW  # noqa: E402

IN = DATA_RAW / "S805_DEMSETZ_TABLE_4.parquet"
OUT = DATA_PROCESSED / "S805.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    keep = ["year", "value", "subseries_id", "source_id", "units", "cr4_bin"]
    df = df[keep]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "content_type": "cross_sectional",
        "extension": {"extension_status": "not_applicable_cross_sectional"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
