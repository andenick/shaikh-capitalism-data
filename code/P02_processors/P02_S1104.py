"""P02_S1104 - pass-through processor for Fig 11.7 US 3-line overlay.

S1104-A net-trade ratio (X-M)/(X+M), S1104-B REER PPI, and S1104-C US/EU12
relative real GDP index (2002=100) are all emitted from the L01 raw parquet.
S1104-C is now BUILT (FU-1 / campaign C6) from WDI NY.GDP.MKTP.KD with the
fixed pre-1995 EU12 basket (see L01_S1104.py notes).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1104"
IN = DATA_RAW / f"{SERIES_ID}_US_BOP_REER_RELGDP.parquet"
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
        "extension": {"extension_status": "partial",
                      "S1104-A": "IMF DOTS extension feasible (deferred)",
                      "S1104-B": "BIS PPI EER extension deferred",
                      "S1104-C": "built (WDI NY.GDP.MKTP.KD, fixed EU12 basket, 2002=100)"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
