"""P02_S1606_construct - assemble S1606 household debt-service ratio.

Dual-cadence emission (Phase 4 ratified):
  * canonical annual parquet  (mean of four quarters; matches Ch16 cadence)
  * quarterly sidecar parquet (book-faithful Fig 16.10 axis)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

INPUTS = {
    "S1606-A": DATA_RAW / "S1606_FOR.parquet",
    "S1606-B": DATA_RAW / "S1606_DSR.parquet",
}
OUT = DATA_PROCESSED / "S1606.parquet"
QUARTERLY_SIDECAR_DIR = DATA_PROCESSED / "_sidecars"
QUARTERLY_OUT = QUARTERLY_SIDECAR_DIR / "S1606_quarterly.parquet"


def run() -> dict:
    missing = [str(p) for p in INPUTS.values() if not p.exists()]
    if missing:
        return {"status": "FAIL", "error": "raw parquet missing", "missing": missing}

    # --- Quarterly sidecar (book-faithful, Fig 16.10 axis) --------------------
    q_frames = [pd.read_parquet(p) for p in INPUTS.values()]
    quarterly = pd.concat(q_frames, ignore_index=True).rename(
        columns={"subsource_id": "source_id"})
    quarterly = quarterly.sort_values(["subseries_id", "qdate"]).reset_index(drop=True)
    quarterly = quarterly[["year", "quarter", "qdate", "value",
                            "subseries_id", "source_id", "units"]]
    QUARTERLY_SIDECAR_DIR.mkdir(parents=True, exist_ok=True)
    quarterly.to_parquet(QUARTERLY_OUT, index=False)

    # --- Annual primary parquet (mean of four quarters per year) -------------
    annual = (quarterly.groupby(["subseries_id", "year"], as_index=False)
                       .agg(value=("value", "mean"),
                            source_id=("source_id", "first"))
                       .copy())
    annual["units"] = "decimal_annual_mean_of_quarterly"
    annual = annual[["year", "value", "subseries_id", "source_id", "units"]]
    annual = annual.sort_values(["subseries_id", "year"]).reset_index(drop=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    annual.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_processed": int(len(annual)),
        "rows_quarterly_sidecar": int(len(quarterly)),
        "year_range": [int(annual["year"].min()), int(annual["year"].max())],
        "subseries_present": sorted(annual["subseries_id"].unique().tolist()),
        "output": str(OUT),
        "quarterly_sidecar": str(QUARTERLY_OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
