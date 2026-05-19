"""P02_S802_construct — emit processed S802 (Weston et al. cross-sections)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, DATA_RAW  # noqa: E402

IN = DATA_RAW / "S802_SEMMLER_TABLE_3_3.parquet"
OUT = DATA_PROCESSED / "S802.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    # cross_sectional: keep canonical columns + cr4_midpoint as extra disambiguator
    keep = ["year", "value", "subseries_id", "source_id", "units", "cr4_midpoint"]
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
