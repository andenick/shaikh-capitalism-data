"""P02_S903_construct - merge wage-profit curves + scalars (R_t, PWT anchors)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_CURVES = DATA_RAW / "S903_WAGE_PROFIT_CURVES.parquet"
IN_SCALARS = DATA_RAW / "S903_SCALARS_R_AND_PWT.parquet"
OUT = DATA_PROCESSED / "S903.parquet"


def run() -> dict:
    if not IN_CURVES.exists():
        return {"status": "FAIL", "error": f"raw curves missing: {IN_CURVES}"}
    curves = pd.read_parquet(IN_CURVES).rename(columns={"subsource_id": "source_id"})
    parts = [curves]
    if IN_SCALARS.exists():
        sc = pd.read_parquet(IN_SCALARS).rename(columns={"subsource_id": "source_id"})
        parts.append(sc)
    df = pd.concat(parts, ignore_index=True)
    # Drop 'r_value' to keep canonical chopped-writer columns; the x-axis info
    # is preserved in x_tv_norm.
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
                      "reason": "per-year wage-profit curves; PWT vintage splice for v2 extension"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
