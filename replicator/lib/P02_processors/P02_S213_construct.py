"""P02_S213_construct - emit book corporate profit rate; BEA-based extension is
documented but not executed by default (extension requires correctly identifying
NOS and K-net line numbers in T1.14 / T4.1 which is non-trivial; we leave it
for a focused Phase 9 effort and mark extension as data_unavailable here).
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN = DATA_RAW / "S213_BOOK_CORP_PROFIT_RATE.parquet"
OUT = DATA_PROCESSED / "S213.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": "raw missing"}
    df = pd.read_parquet(IN).rename(columns={"subsource_id": "source_id"})
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "data_unavailable",
                      "reason": "BEA T1.14/T4.1 line-mapping under review (Phase 3 open question still open)"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
