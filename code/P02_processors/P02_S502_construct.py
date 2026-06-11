"""P02_S502_construct - assemble US+UK WPI book + US extension via FRED WPU.

Splice strategy (US only): overlap-anchor on 2010 (same as S210).
US extended segment: FRED_WPU * (USWPI[2010] / FRED_WPU[2010]).
UK extended segment: NaN (ONS PLLU not fetched in v1).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_US = DATA_RAW / "S502_US_WPI_BOOK.parquet"
IN_UK = DATA_RAW / "S502_UK_WPI_BOOK.parquet"
IN_FRED = DATA_RAW / "S502_FRED_PPIACO.parquet"
OUT = DATA_PROCESSED / "S502.parquet"
ANCHOR_YEAR = 2010


def _extend_us(us_book: pd.DataFrame, fred: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Overlap-anchor on 2010; walk back to 2005 if missing."""
    diag: dict = {}
    overlap = ANCHOR_YEAR
    book_val = fred_val = None
    while overlap >= 2005:
        bv = us_book[us_book["year"] == overlap]["value"]
        fv = fred[fred["year"] == overlap]["value"]
        if not bv.empty and not fv.empty and float(fv.iloc[0]) != 0:
            book_val = float(bv.iloc[0])
            fred_val = float(fv.iloc[0])
            break
        overlap -= 1
    if book_val is None:
        return us_book.copy(), {"extension_status": "no_overlap_2005_2010"}
    scale = book_val / fred_val
    ext = fred[fred["year"] > ANCHOR_YEAR].copy()
    if ext.empty:
        return us_book.copy(), {"extension_status": "no_post_2010_obs",
                                "overlap_year": overlap}
    ext["value"] = ext["value"] * scale
    ext["units"] = "index_1930=100"
    ext = ext[["year", "value", "units", "subseries_id", "subsource_id"]]
    out = pd.concat([us_book[["year", "value", "units", "subseries_id", "subsource_id"]],
                     ext], ignore_index=True)
    diag = {"extension_status": "ok", "overlap_year": int(overlap),
            "scale_factor": float(scale), "us_appended_years": int(len(ext)),
            "last_year_us": int(ext["year"].max())}
    return out, diag


def run() -> dict:
    if not (IN_US.exists() and IN_UK.exists()):
        return {"status": "FAIL", "error": "raw US/UK missing"}
    us_book = pd.read_parquet(IN_US)
    uk_book = pd.read_parquet(IN_UK)

    if IN_FRED.exists():
        fred = pd.read_parquet(IN_FRED)
        us_ext, diag_us = _extend_us(us_book, fred)
    else:
        us_ext = us_book[["year", "value", "units", "subseries_id", "subsource_id"]].copy()
        diag_us = {"extension_status": "data_unavailable_no_fred"}

    uk_final = uk_book[["year", "value", "units", "subseries_id", "subsource_id"]].copy()

    final = pd.concat([us_ext, uk_final], ignore_index=True)
    final = final.rename(columns={"subsource_id": "source_id"})
    final = final.sort_values(["year", "subseries_id"]).reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": {"us": diag_us,
                      "uk": {"extension_status": "api_unavailable_ons_pllu_cdn_502"}},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
