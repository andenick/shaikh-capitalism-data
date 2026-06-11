"""P02_S1102_construct - pass-through processor for Fig 11.3 REER (PPI-basis).

The book-truth rxr1 column is the canonical published value for S1102. No
re-derivation; extension to BIS PPI EER is deferred (see L01).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1102"
IN = DATA_RAW / f"{SERIES_ID}_BLS_REER_PPI.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df.rename(columns={"subsource_id": "source_id"})
    out = df[["year", "value", "subseries_id", "source_id", "units", "country"]].copy()
    out = out.sort_values(["year", "subseries_id"]).reset_index(drop=True)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_processed": int(len(out)),
        "year_range": [int(out["year"].min()), int(out["year"].max())],
        "subseries_present": sorted(out["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "data_unavailable_bls_ilc_discontinued",
                      "reason": "BLS ILC discontinued 2013; BIS PPI EER substitute deferred"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
