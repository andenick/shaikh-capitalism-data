"""P02_S408_construct — pass-through for S408 (cross_sectional 1952 snapshot)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S408"
IN = DATA_RAW / "S408_EITEMAN_GUTHRIE_1952.parquet"
OUT = DATA_PROCESSED / "S408.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw parquet missing: {IN}"}
    df = pd.read_parquet(IN)
    out = df[["year", "value", "subseries_id", "source_id", "units"]].copy()
    out = out.sort_values(["year", "subseries_id"]).reset_index(drop=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(out)),
        "year_range": [int(out["year"].min()), int(out["year"].max())],
        "subseries_present": sorted(out["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_cross_sectional",
                      "reason": "single 1952 survey snapshot; no recurring series"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
