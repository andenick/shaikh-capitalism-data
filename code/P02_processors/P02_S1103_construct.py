"""P02_S1103_construct - pass-through processor for Fig 11.6 LOP ratio.

S1103 is a formula construction: rxr1 / rulcadjratio1rescaled. The
processor preserves the book-truth rxrrulcratio1 column as `value` and
keeps the numerator and denominator inputs as auxiliary columns for the
V03 cell-by-cell derivation check.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1103"
IN = DATA_RAW / f"{SERIES_ID}_LOP_RATIO.parquet"
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
                      "reason": ("BLS ILC discontinued 2013. Per No-Lazy-Splices, "
                                 "extension requires re-computing rxr1/rulcadj from "
                                 "BIS PPI EER and OECD/Conference Board ULC. Deferred.")},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
