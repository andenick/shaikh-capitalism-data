"""P02_S804_construct — emit processed S804 (Stigler concentrated vs unconcentrated)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, DATA_RAW  # noqa: E402

IN = DATA_RAW / "S804_STIGLER_TABLE_17.parquet"
OUT = DATA_PROCESSED / "S804.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    keep = ["year", "value", "subseries_id", "source_id", "units",
            "bin_label", "bin_start", "bin_end"]
    df = df[keep]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "content_type": "time_series",
        "extension": {"extension_status": "data_unavailable",
                       "reason": "SIC->NAICS break + Census CR discontinuity; treat as historical illustration per Phase 4 recommendation"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
