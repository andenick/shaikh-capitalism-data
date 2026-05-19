"""P02_S1404_construct - construct S1404 raw scatter (Ch14 Fig 14.13).

Pass-through of Appendix 14.3 gwsh and ulintensity (annual, unfiltered).
Extension via re-derivation is left to a downstream rebuild if S1401/S1402 are
extended; we do not splice extended values here because Fig 14.13 is the raw
1949-2011 scatter that the chapter describes.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1404"
IN_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"


def run() -> dict:
    if not IN_BOOK.exists():
        return {"status": "FAIL", "error": f"missing book parquet {IN_BOOK}"}
    df = pd.read_parquet(IN_BOOK).rename(columns={"subsource_id": "source_id"})
    df = df[["year", "value", "subseries_id", "source_id", "units"]].sort_values(
        ["subseries_id", "year"]).reset_index(drop=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "derive_from_S1401_S1402_if_extended",
                      "note": "Raw scatter is per Shaikh's 1949-2011 sample; extension is the responsibility of S1401/S1402 plus a Phase 6 re-derivation pass."},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
