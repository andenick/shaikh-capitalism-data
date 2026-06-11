"""P02_S209_construct - splice BEA LTEG (1890-1947) + ERP (1948-2010); extend with FRED UNRATE.

The chopped table holds 'TotUnempl' already-spliced. We reproduce by taking
BEA for years where ERP is NaN, and ERP otherwise (ERP wins from 1948 onward).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_A = DATA_RAW / "S209_BEA_LTEG_B1_B2.parquet"
IN_B = DATA_RAW / "S209_ERP_T_B40.parquet"
IN_C = DATA_RAW / "S209_FRED_UNRATE.parquet"
OUT = DATA_PROCESSED / "S209.parquet"
SPLICE_YEAR = 1948
EXT_OVERLAP = 2010


def run() -> dict:
    if not IN_A.exists() or not IN_B.exists():
        return {"status": "FAIL", "error": "raw missing"}
    a = pd.read_parquet(IN_A).rename(columns={"subsource_id": "source_id"})
    b = pd.read_parquet(IN_B).rename(columns={"subsource_id": "source_id"})
    book = pd.concat([
        a[a["year"] < SPLICE_YEAR][["year", "value", "units", "subseries_id", "source_id"]],
        b[b["year"] >= SPLICE_YEAR][["year", "value", "units", "subseries_id", "source_id"]],
    ], ignore_index=True).sort_values("year").reset_index(drop=True)
    diag = {"extension_status": "data_unavailable"}
    if IN_C.exists():
        c = pd.read_parquet(IN_C).rename(columns={"subsource_id": "source_id"})
        ext = c[c["year"] > EXT_OVERLAP][["year", "value", "units", "subseries_id", "source_id"]]
        book = pd.concat([book, ext], ignore_index=True).sort_values("year").reset_index(drop=True)
        diag = {"extension_status": "ok", "years_appended": int(len(ext)),
                "last_year": int(book["year"].max()),
                "note": "UNRATE level-equivalent to ERP; no rescale needed"}
    book = book[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    book.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(book)),
        "year_range": [int(book["year"].min()), int(book["year"].max())],
        "subseries_present": sorted(book["subseries_id"].unique().tolist()),
        "extension": diag, "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
