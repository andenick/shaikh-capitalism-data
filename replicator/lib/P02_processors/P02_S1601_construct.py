"""P02_S1601_construct - assemble S1601 golden-wave residuals.

Composite of four subseries. Pass-through for the two published residual
columns (S1601-A, S1601-B); raw ratios (S1601-C, S1601-D) preserved for the
cubic-trend re-fit variant if Phase 6 extension is enabled.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN = {
    "S1601-A": DATA_RAW / "S1601_USGoldWaveDetrended.parquet",
    "S1601-B": DATA_RAW / "S1601_UKGoldWaveDetrended.parquet",
    "S1601-C": DATA_RAW / "S1601_USPPIGold.parquet",
    "S1601-D": DATA_RAW / "S1601_UKPPIGold.parquet",
}
OUT = DATA_PROCESSED / "S1601.parquet"


def run() -> dict:
    missing = [str(p) for p in IN.values() if not p.exists()]
    if missing:
        return {"status": "FAIL", "error": "raw parquet missing", "missing": missing}
    frames = [pd.read_parquet(p) for p in IN.values()]
    df = pd.concat(frames, ignore_index=True).rename(columns={"subsource_id": "source_id"})
    df = df.sort_values(["subseries_id", "year"]).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
