"""P02_S216_construct - pass-through 1972 cross-section; no extension."""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN = DATA_RAW / "S216_IO_1972_71_INDUSTRIES.parquet"
OUT = DATA_PROCESSED / "S216.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": "raw missing"}
    df = pd.read_parquet(IN).rename(columns={"subsource_id": "source_id"})
    cols = ["year", "value", "subseries_id", "source_id", "units", "industry_index", "x_tv_norm"]
    df = df[cols]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_cross_sectional",
                      "reason": "Single-year (1972) BEA benchmark; multi-year analysis requires separate registry rows"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
