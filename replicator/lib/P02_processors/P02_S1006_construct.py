"""P02_S1006_construct — Bond and Equity Returns.

Three subseries (Equity, LT Corp, LT Gov) over 1926-present. Book period from
Ibbotson; extension from Damodaran (Equity + LT Gov) and FRED AAA (LT Corp
PROXY). proxy:true flagged on S1006-B-ext only.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_BOOK = DATA_RAW / "S1006_IBBOTSON_book.parquet"
IN_DAM = DATA_RAW / "S1006_DAMODARAN_ext.parquet"
IN_AAA = DATA_RAW / "S1006_FRED_AAA_ext.parquet"
OUT = DATA_PROCESSED / "S1006.parquet"


def run() -> dict:
    if not IN_BOOK.exists():
        return {"status": "FAIL", "error": "Ibbotson book parquet missing"}
    book = pd.read_parquet(IN_BOOK).rename(columns={"subsource_id": "source_id"})
    parts = [book]
    diag = {"extension_status": "book_only"}

    if IN_DAM.exists():
        dam = pd.read_parquet(IN_DAM).rename(columns={"subsource_id": "source_id"})
        parts.append(dam)
        diag["damodaran_rows"] = int(len(dam))
    if IN_AAA.exists():
        aaa = pd.read_parquet(IN_AAA).rename(columns={"subsource_id": "source_id"})
        parts.append(aaa)
        diag["aaa_proxy_rows"] = int(len(aaa))

    if len(parts) > 1:
        diag["extension_status"] = "ok"

    df = pd.concat(parts, ignore_index=True)
    df = df.sort_values(["year", "subseries_id"]).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": diag,
        "proxy_flags": {"S1006-B-ext": True},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
