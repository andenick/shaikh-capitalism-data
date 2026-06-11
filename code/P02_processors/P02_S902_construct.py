"""P02_S902_construct - merge standard-price industry vectors + observed profit rates."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_PRICES = DATA_RAW / "S902_STD_PRICES_AND_LABOR_VALUES.parquet"
IN_ROBS = DATA_RAW / "S902_OBSERVED_PROFIT_RATES.parquet"
OUT = DATA_PROCESSED / "S902.parquet"


def run() -> dict:
    if not IN_PRICES.exists():
        return {"status": "FAIL", "error": f"raw prices missing: {IN_PRICES}"}
    prices = pd.read_parquet(IN_PRICES).rename(columns={"subsource_id": "source_id"})
    parts = [prices]
    if IN_ROBS.exists():
        robs = pd.read_parquet(IN_ROBS).rename(columns={"subsource_id": "source_id"})
        parts.append(robs)
    df = pd.concat(parts, ignore_index=True)
    cols = ["year", "value", "subseries_id", "source_id", "units",
            "industry_index", "x_tv_norm", "model"]
    df = df[cols]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_cross_sectional",
                      "reason": "eigensystem per benchmark; no time-series splice"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
