"""P02_S402_construct — pass-through for S402 (per-hour cost columns)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S402"
IN = DATA_RAW / "S402_APPENDIX_4_2_T4.parquet"
OUT = DATA_PROCESSED / "S402.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw parquet missing: {IN}"}
    df = pd.read_parquet(IN)
    out = df.rename(columns={"row_index": "year"})[
        ["year", "value", "subseries_id", "source_id", "units", "XR"]
    ].copy()
    out = out.sort_values(["year", "subseries_id"]).reset_index(drop=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(out)),
        "non_null_values": int(out["value"].notna().sum()),
        "row_index_range": [int(out["year"].min()), int(out["year"].max())],
        "subseries_present": sorted(out["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_theoretical"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
