"""P02_S1604_construct - assemble S1604 profit-rate panel.

Pass-through composite of five Appendix-16.2 derived columns.  HP100 smoothing
is already applied in the Appendix (columns -C, -D) using Shaikh's lambda=100
choice for annual data.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

INPUTS = {
    "S1604-A": DATA_RAW / "S1604_NetCorp.parquet",
    "S1604-B": DATA_RAW / "S1604_NetIncRealCorp.parquet",
    "S1604-C": DATA_RAW / "S1604_NetIncRealCorpHP100.parquet",
    "S1604-D": DATA_RAW / "S1604_NetIncRealCorpHP100Lag1.parquet",
    "S1604-E": DATA_RAW / "S1604_RcorpAlt.parquet",
}
OUT = DATA_PROCESSED / "S1604.parquet"


def run() -> dict:
    missing = [str(p) for p in INPUTS.values() if not p.exists()]
    if missing:
        return {"status": "FAIL", "error": "raw parquet missing", "missing": missing}
    frames = [pd.read_parquet(p) for p in INPUTS.values()]
    df = pd.concat(frames, ignore_index=True).rename(columns={"subsource_id": "source_id"})
    df = df.sort_values(["subseries_id", "year"]).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
