"""P02_S201_construct — construct S201 from raw inputs.

Reads:
  Technical/data/raw/S201_BEA_LTEG_A173.parquet
  Technical/data/raw/S201_FRB_G17_BOOK.parquet
  Technical/data/raw/S201_FRED_INDPRO.parquet  (may be absent if FRED degraded)

Writes:
  Technical/data/processed/S201.parquet
  Columns: year (int), value (float), subseries_id (str), source_id (str), units (str)
  Units: 'index_1958=100' throughout (post-reindex).

Construction (per S201_DPR.md and S201_EPR.md):
  1. Rebase BEA from native 1913=100 to 1958=100 (anchor: BEA[1958])
  2. Rebase FRB-book from native 2007=100 to 1958=100 (anchor: FRB[1958])
  3. Splice at 1919: use BEA for 1860-1918, FRB for 1919-2010
  4. If FRED INDPRO present: reindex to 1958=100 at 2010 overlap, append 2011-2025
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_BEA = DATA_RAW / "S201_BEA_LTEG_A173.parquet"
IN_FRB = DATA_RAW / "S201_FRB_G17_BOOK.parquet"
IN_FRED = DATA_RAW / "S201_FRED_INDPRO.parquet"
OUT = DATA_PROCESSED / "S201.parquet"

ANCHOR_BEA = 1958
ANCHOR_FRB = 1958
BOOK_SPLICE_YEAR = 1919   # FRB takes over at this year
EXT_OVERLAP_YEAR = 2010   # FRED anchored to S201_book[2010]


def _rebase(df: pd.DataFrame, anchor_year: int) -> pd.DataFrame:
    """Scale df.value so that value[anchor_year] == 100. Returns a copy."""
    if anchor_year not in df["year"].values:
        raise ValueError(f"anchor year {anchor_year} not in series")
    anchor_val = float(df.loc[df["year"] == anchor_year, "value"].iloc[0])
    if anchor_val == 0 or pd.isna(anchor_val):
        raise ValueError(f"anchor value at {anchor_year} is {anchor_val}")
    scale = 100.0 / anchor_val
    out = df.copy()
    out["value"] = out["value"] * scale
    out["units"] = "index_1958=100"
    return out


def _splice_book(bea_rebased: pd.DataFrame, frb_rebased: pd.DataFrame) -> pd.DataFrame:
    """Combine BEA (1860-1918) and FRB (1919-2010) into a single book-period series."""
    bea_part = bea_rebased[bea_rebased["year"] < BOOK_SPLICE_YEAR][["year", "value", "units", "subseries_id", "subsource_id"]].copy()
    frb_part = frb_rebased[frb_rebased["year"] >= BOOK_SPLICE_YEAR][["year", "value", "units", "subseries_id", "subsource_id"]].copy()
    book = pd.concat([bea_part, frb_part], ignore_index=True)
    book = book.sort_values("year").reset_index(drop=True)
    book = book.rename(columns={"subsource_id": "source_id"})
    return book


def _extend_with_fred(book: pd.DataFrame, fred_raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Reindex FRED to 1958=100 at the overlap year and append post-book years."""
    diag: dict = {}
    overlap_year = EXT_OVERLAP_YEAR
    # Fallback if 2010 missing (very unlikely): walk back to 2005
    while overlap_year >= 2005:
        in_book = book[book["year"] == overlap_year]
        in_fred = fred_raw[fred_raw["year"] == overlap_year]
        if not in_book.empty and not in_fred.empty:
            book_val = float(in_book["value"].iloc[0])
            fred_val = float(in_fred["value"].iloc[0])
            if not pd.isna(book_val) and not pd.isna(fred_val) and fred_val != 0:
                break
        overlap_year -= 1
    else:
        return book, {"extension_status": "no_overlap", "overlap_attempted": "2005-2010"}

    scale = book_val / fred_val
    diag["overlap_year"] = overlap_year
    diag["scale_factor"] = scale
    diag["book_at_overlap"] = book_val
    diag["fred_at_overlap"] = fred_val

    ext = fred_raw[fred_raw["year"] > EXT_OVERLAP_YEAR].copy()
    ext["value"] = ext["value"] * scale
    ext["units"] = "index_1958=100"
    ext = ext.rename(columns={"subsource_id": "source_id"})
    ext = ext[["year", "value", "units", "subseries_id", "source_id"]]

    extended = pd.concat([book, ext], ignore_index=True).sort_values("year").reset_index(drop=True)
    diag["extension_status"] = "ok"
    diag["years_appended"] = int(len(ext))
    diag["last_year"] = int(extended["year"].max())
    return extended, diag


def run() -> dict:
    if not IN_BEA.exists() or not IN_FRB.exists():
        return {"status": "FAIL", "error": "raw parquet missing — run loader first",
                "missing": [str(p) for p in (IN_BEA, IN_FRB) if not p.exists()]}

    bea_raw = pd.read_parquet(IN_BEA)
    frb_raw = pd.read_parquet(IN_FRB)

    bea_rebased = _rebase(bea_raw, ANCHOR_BEA)
    frb_rebased = _rebase(frb_raw, ANCHOR_FRB)

    book = _splice_book(bea_rebased, frb_rebased)
    diag: dict = {}
    if IN_FRED.exists():
        fred_raw = pd.read_parquet(IN_FRED)
        final, diag = _extend_with_fred(book, fred_raw)
    else:
        final = book
        diag = {"extension_status": "data_unavailable", "reason": "FRED not loaded"}

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    # Final schema: year, value, subseries_id, source_id, units
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    final.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": diag,
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
