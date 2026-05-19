"""P02_S207_construct - emit S207-A (productivity) and S207-B (real compensation)
as two co-plotted series (one parquet, distinguished by subseries_id), plus
extensions reindexed at the most recent book overlap.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_PROD = DATA_RAW / "S207_PROD_BOOK.parquet"
IN_COMP = DATA_RAW / "S207_COMP_BOOK.parquet"
IN_FRED_PROD = DATA_RAW / "S207_FRED_OPHMFG.parquet"
IN_FRED_COMP = DATA_RAW / "S207_FRED_COMPRMS.parquet"
OUT = DATA_PROCESSED / "S207.parquet"
OVERLAP = 2009  # BLS FLS table ends 2009; safest overlap year for productivity


def _reindex_extension(book: pd.DataFrame, ext_raw: pd.DataFrame, overlap_year: int,
                       sub_label: str) -> tuple[pd.DataFrame, dict]:
    in_book = book[book["year"] == overlap_year]
    in_ext = ext_raw[ext_raw["year"] == overlap_year]
    if in_book.empty or in_ext.empty:
        # try 2010 then 2008 etc.
        for y in [2010, 2008, 2007]:
            in_book = book[book["year"] == y]
            in_ext = ext_raw[ext_raw["year"] == y]
            if not in_book.empty and not in_ext.empty:
                overlap_year = y
                break
        else:
            return pd.DataFrame(), {"extension_status": "no_overlap", "label": sub_label}
    book_val = float(in_book["value"].iloc[0])
    ext_val = float(in_ext["value"].iloc[0])
    if ext_val == 0:
        return pd.DataFrame(), {"extension_status": "zero_anchor"}
    scale = book_val / ext_val
    ext = ext_raw[ext_raw["year"] > overlap_year].copy()
    ext["value"] = ext["value"] * scale
    ext["units"] = "index_1889=100"
    ext = ext.rename(columns={"subsource_id": "source_id"})
    diag = {"extension_status": "ok", "overlap_year": overlap_year, "scale_factor": scale,
            "years_appended": int(len(ext)), "label": sub_label}
    return ext[["year", "value", "units", "subseries_id", "source_id"]], diag


def run() -> dict:
    if not IN_PROD.exists() or not IN_COMP.exists():
        return {"status": "FAIL", "error": "book raw missing"}
    prod = pd.read_parquet(IN_PROD).rename(columns={"subsource_id": "source_id"})
    comp = pd.read_parquet(IN_COMP).rename(columns={"subsource_id": "source_id"})
    prod = prod[["year", "value", "units", "subseries_id", "source_id"]]
    comp = comp[["year", "value", "units", "subseries_id", "source_id"]]
    parts = [prod, comp]
    diags = []
    if IN_FRED_PROD.exists():
        ext, d = _reindex_extension(prod, pd.read_parquet(IN_FRED_PROD), OVERLAP, "productivity")
        if not ext.empty:
            parts.append(ext)
        diags.append(d)
    if IN_FRED_COMP.exists():
        ext, d = _reindex_extension(comp, pd.read_parquet(IN_FRED_COMP), OVERLAP, "compensation")
        if not ext.empty:
            parts.append(ext)
        diags.append(d)
    final = pd.concat(parts, ignore_index=True).sort_values(["subseries_id", "year"]).reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": diags, "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
