"""P02_S1005_construct — Dividend Yield vs Bond Yield.

Composite: dividend yield (book + Shiller ext), 10yr govt (book + FRED GS10 ext),
plus corporate yield inherited from S1002-A (book + ext).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_DIV_BOOK = DATA_RAW / "S1005_USLR_ys.parquet"
IN_GOV_BOOK = DATA_RAW / "S1005_USLR_ib10yr.parquet"
IN_DIV_EXT = DATA_RAW / "S1005_SHILLER_div_ext.parquet"
IN_GOV_EXT = DATA_RAW / "S1005_FRED_GS10.parquet"
IN_CORP_BOOK = DATA_RAW / "S1002_USLR_iblong.parquet"
IN_CORP_EXT = DATA_RAW / "S1002_FRED_AAA.parquet"
OUT = DATA_PROCESSED / "S1005.parquet"

BOOK_END = 2011


def _norm(df: pd.DataFrame, sub_id: str, ss_id: str) -> pd.DataFrame:
    p = df[["year", "value"]].copy()
    p["subseries_id"] = sub_id
    p["source_id"] = ss_id
    p["units"] = "percent"
    return p


def run() -> dict:
    if not (IN_DIV_BOOK.exists() and IN_GOV_BOOK.exists()):
        return {"status": "FAIL", "error": "book parquets missing"}
    parts = [
        _norm(pd.read_parquet(IN_DIV_BOOK), "S1005-A", "USLR_ys"),
        _norm(pd.read_parquet(IN_GOV_BOOK), "S1005-B", "USLR_ib10yr"),
    ]
    diag = {"extension_status": "book_only"}

    # Corporate composite (book + ext) inherited from S1002
    if IN_CORP_BOOK.exists():
        parts.append(_norm(pd.read_parquet(IN_CORP_BOOK), "S1005-C", "S1002_iblong"))
    if IN_CORP_EXT.exists():
        c_ext_raw = pd.read_parquet(IN_CORP_EXT)
        c_ext = c_ext_raw[c_ext_raw["year"] > BOOK_END].copy()
        if not c_ext.empty:
            ext = c_ext.groupby("year", as_index=False)["value"].mean()
            parts.append(_norm(ext, "S1005-C-ext", "FRED_AAA"))
            diag["corp_ext_years"] = int(len(ext))

    if IN_DIV_EXT.exists():
        d_ext = pd.read_parquet(IN_DIV_EXT)
        d_ext = d_ext[d_ext["year"] > BOOK_END]
        if not d_ext.empty:
            parts.append(_norm(d_ext, "S1005-A-ext", "SHILLER_div"))
            diag["div_ext_years"] = int(len(d_ext))
            diag["extension_status"] = "ok"
    if IN_GOV_EXT.exists():
        g_ext = pd.read_parquet(IN_GOV_EXT)
        g_ext = g_ext[g_ext["year"] > BOOK_END]
        if not g_ext.empty:
            parts.append(_norm(g_ext, "S1005-B-ext", "FRED_GS10"))
            diag["gs10_ext_years"] = int(len(g_ext))
            diag["extension_status"] = "ok"

    df = pd.concat(parts, ignore_index=True).sort_values(["year", "subseries_id"]).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": diag,
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
