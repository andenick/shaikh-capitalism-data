"""P02_S202_construct - splice BEA 1977 Table B4 (rebased to 1958=100 via 1901 anchor)
with BEA Wealth Table 4.8 line 1 at 1901, then re-index to 1958=100.

Per book p. 763: 'The two series were rebased to 1958 = 100 and spliced at 1901.'

Extension: append BEA NIPA T1.1.6 line 9 (Real Nonresidential Fixed Investment),
reindexed to S202_book at 2010 overlap (overlap_anchor strategy).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_A = DATA_RAW / "S202_BEA_1977_T_B4.parquet"
IN_B = DATA_RAW / "S202_BEA_WEALTH_T48.parquet"
IN_C = DATA_RAW / "S202_BEA_NIPA_T116_L9.parquet"
OUT = DATA_PROCESSED / "S202.parquet"

SPLICE_YEAR = 1901   # BEA_WEALTH takes over here per Appendix 2.1
REBASE_YEAR = 1958   # final base
EXT_OVERLAP_YEAR = 2010


def _rebase_to_anchor(df: pd.DataFrame, year: int) -> pd.DataFrame:
    if year not in df["year"].values:
        raise ValueError(f"anchor {year} not in series; have {df['year'].min()}-{df['year'].max()}")
    anchor = float(df.loc[df["year"] == year, "value"].iloc[0])
    out = df.copy()
    out["value"] = out["value"] * (100.0 / anchor)
    out["units"] = f"index_{year}=100"
    return out


def _splice_two_series_at(early: pd.DataFrame, late: pd.DataFrame, splice_year: int,
                          rebase_year: int) -> pd.DataFrame:
    """Rebase both to splice_year=100, splice, then re-anchor to rebase_year=100."""
    early_r = _rebase_to_anchor(early, splice_year)
    late_r = _rebase_to_anchor(late, splice_year)
    early_part = early_r[early_r["year"] < splice_year]
    late_part = late_r[late_r["year"] >= splice_year]
    spliced = pd.concat([early_part, late_part], ignore_index=True).sort_values("year")
    # Re-anchor to rebase_year=100 if present
    if rebase_year in spliced["year"].values:
        anchor = float(spliced.loc[spliced["year"] == rebase_year, "value"].iloc[0])
        spliced["value"] = spliced["value"] * (100.0 / anchor)
        spliced["units"] = f"index_{rebase_year}=100"
    return spliced.reset_index(drop=True)


def _extend(book: pd.DataFrame, ext_raw: pd.DataFrame, overlap_year: int) -> tuple[pd.DataFrame, dict]:
    diag: dict = {}
    in_book = book[book["year"] == overlap_year]
    in_ext = ext_raw[ext_raw["year"] == overlap_year]
    if in_book.empty or in_ext.empty:
        return book, {"extension_status": "no_overlap", "overlap_attempted": overlap_year}
    book_val = float(in_book["value"].iloc[0])
    ext_val = float(in_ext["value"].iloc[0])
    if ext_val == 0:
        return book, {"extension_status": "zero_anchor"}
    scale = book_val / ext_val
    ext = ext_raw[ext_raw["year"] > overlap_year].copy()
    ext["value"] = ext["value"] * scale
    ext["units"] = f"index_{REBASE_YEAR}=100"
    ext = ext.rename(columns={"subsource_id": "source_id"})
    ext = ext[["year", "value", "units", "subseries_id", "source_id"]]
    book_x = book.rename(columns={"subsource_id": "source_id"})[
        ["year", "value", "units", "subseries_id", "source_id"]]
    combined = pd.concat([book_x, ext], ignore_index=True).sort_values("year").reset_index(drop=True)
    diag.update({
        "extension_status": "ok",
        "overlap_year": overlap_year,
        "scale_factor": scale,
        "book_at_overlap": book_val,
        "ext_at_overlap": ext_val,
        "years_appended": int(len(ext)),
        "last_year": int(combined["year"].max()),
    })
    return combined, diag


def run() -> dict:
    if not IN_A.exists() or not IN_B.exists():
        return {"status": "FAIL", "error": "raw parquet missing", "missing": [str(p) for p in [IN_A, IN_B] if not p.exists()]}
    a = pd.read_parquet(IN_A)
    b = pd.read_parquet(IN_B)
    book = _splice_two_series_at(a, b, SPLICE_YEAR, REBASE_YEAR)
    if IN_C.exists():
        ext_raw = pd.read_parquet(IN_C)
        final, diag = _extend(book, ext_raw, EXT_OVERLAP_YEAR)
    else:
        final = book.rename(columns={"subsource_id": "source_id"})[
            ["year", "value", "units", "subseries_id", "source_id"]]
        diag = {"extension_status": "data_unavailable", "reason": "BEA NIPA not loaded"}
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
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
