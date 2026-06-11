"""P02_S1101_construct - pass-through processor for Fig 11.2 trade balances.

The book-truth X/M ratios are loaded directly from Appendix11_XMData.xlsx; no
re-derivation is needed. Schema:
  year, value, subseries_id, source_id, units (+ country for cross-sectional
  disambiguation when multiple country subseries share the same year).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1101"
IN = DATA_RAW / f"{SERIES_ID}_IMF_IFS_XM.parquet"
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
        "extension": {"extension_status": "not_attempted_v1",
                      "reason": "IMF DOTS extension deferred to Phase 9"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
