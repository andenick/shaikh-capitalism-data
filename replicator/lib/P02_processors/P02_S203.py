"""P02_S203 - emit MeasuringWorth book-period values; correct the corrupt Great-
Depression span with a re-based fresh MeasuringWorth re-pull; optionally append a
FRED-based real GDP per capita extension reindexed at 2010 overlap.

Source-corruption remediation (Decision 0008 / campaign backlog T1.2)
--------------------------------------------------------------------
The salvaged book column ('Real GDP per Capita_2005Dollars', 2005$) RISES through
the Great Depression (1929=8187.56 -> 1934=14705.52), which is economically
impossible. Diagnosis (compare vs the fresh 2026 MeasuringWorth re-pull, which falls
-28.6% 1929->1933 as history requires): the corrupt span is 1930-1944 inclusive; pre-
1930 and post-1944 book values are sound (they differ from the current vintage only by
ordinary MeasuringWorth re-estimation/base drift, not by the Depression-rise defect).

Fix (pipeline, not hand-edit): re-base the fresh re-pull (native year-2017 dollars)
to the book's 2005$ level by an OVERLAP REINDEX, then replace ONLY the 1930-1944 rows.
Decision 0008 specifies "overlap reindex at 2010", but the book MeasuringWorth column
ends at 2000 (2001-2010 are NaN in the salvaged workbook), so 2010 is not an available
overlap. Per the decision's intent (tie the re-pull to the book 2005$ level at a
trustworthy overlap adjacent to the replaced span), the reindex anchor is 1929 - the
last realized, non-corrupt year immediately preceding the corrupt span. Continuity at
the far boundary (1945) is verified: reindexed(1945) vs book(1945) = -1.05% (absorbed by
ordinary vintage drift). Every replaced value = round(repull_2017 * scale, 2) where
scale = book(1929) / repull_2017(1929); nothing is fabricated.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_MW = DATA_RAW / "S203_MEASURINGWORTH_USGDP.parquet"
IN_REPULL = DATA_RAW / "S203_MEASURINGWORTH_REPULL.parquet"
IN_FRED = DATA_RAW / "S203_FRED_RGDPPC.parquet"
OUT = DATA_PROCESSED / "S203.parquet"
OVERLAP = 2010

# Depression source-corruption remediation (Decision 0008).
CORRUPT_SPAN = (1930, 1944)   # inclusive years replaced by the re-based re-pull
REINDEX_ANCHOR = 1929         # last non-corrupt year before the span; overlap anchor


def _correct_depression(mw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Replace the corrupt 1930-1944 book rows with the re-based fresh re-pull.

    Returns (corrected_mw, diagnostics). If the re-pull is unavailable the book
    values are returned unchanged with a flagged status (no silent fabrication).
    """
    if not IN_REPULL.exists():
        return mw, {"depression_fix": "SKIPPED", "reason": "re-pull raw missing"}
    repull = pd.read_parquet(IN_REPULL)[["year", "value"]].set_index("year")["value"]
    book = mw.set_index("year")["value"]
    if REINDEX_ANCHOR not in book.index or REINDEX_ANCHOR not in repull.index:
        return mw, {"depression_fix": "SKIPPED", "reason": "reindex anchor absent"}
    scale = float(book.loc[REINDEX_ANCHOR]) / float(repull.loc[REINDEX_ANCHOR])
    lo, hi = CORRUPT_SPAN
    replaced = {}
    out = mw.copy()
    for yr in range(lo, hi + 1):
        if yr in repull.index and (out["year"] == yr).any():
            new_val = round(float(repull.loc[yr]) * scale, 2)
            old_val = float(out.loc[out["year"] == yr, "value"].iloc[0])
            out.loc[out["year"] == yr, "value"] = new_val
            replaced[yr] = {"old": old_val, "new": new_val}
    # far-boundary continuity check (informational)
    far = hi + 1
    cont = None
    if far in repull.index and far in book.index:
        pred = float(repull.loc[far]) * scale
        cont = round((pred / float(book.loc[far]) - 1) * 100, 4)
    diag = {
        "depression_fix": "APPLIED",
        "corrupt_span": [lo, hi],
        "reindex_anchor": REINDEX_ANCHOR,
        "scale_factor": scale,
        "n_replaced": len(replaced),
        "far_boundary_continuity_pct": cont,
        "trough_1933_vs_1929_pct": round(
            (out.loc[out["year"] == 1933, "value"].iloc[0] /
             out.loc[out["year"] == 1929, "value"].iloc[0] - 1) * 100, 2),
        "replaced": replaced,
    }
    return out, diag


def run() -> dict:
    if not IN_MW.exists():
        return {"status": "FAIL", "error": "MW raw missing"}
    mw = pd.read_parquet(IN_MW).rename(columns={"subsource_id": "source_id"})
    mw = mw[["year", "value", "units", "subseries_id", "source_id"]]
    mw, depression_diag = _correct_depression(mw)
    diag: dict = {"extension_status": "data_unavailable", "reason": "FRED not loaded"}
    if IN_FRED.exists():
        fred = pd.read_parquet(IN_FRED)
        in_mw = mw[mw["year"] == OVERLAP]
        in_fred = fred[fred["year"] == OVERLAP]
        if not in_mw.empty and not in_fred.empty:
            mw_val = float(in_mw["value"].iloc[0])
            fred_val = float(in_fred["value"].iloc[0])
            scale = mw_val / fred_val
            ext = fred[fred["year"] > OVERLAP].copy()
            ext["value"] = ext["value"] * scale
            ext["units"] = "real_dollars_2005"
            ext = ext.rename(columns={"subsource_id": "source_id"})
            ext = ext[["year", "value", "units", "subseries_id", "source_id"]]
            mw = pd.concat([mw, ext], ignore_index=True).sort_values("year").reset_index(drop=True)
            diag = {"extension_status": "ok", "overlap_year": OVERLAP, "scale_factor": scale,
                    "years_appended": int(len(ext)), "last_year": int(mw["year"].max())}
        else:
            diag = {"extension_status": "no_overlap", "overlap_attempted": OVERLAP}
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    mw.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(mw)),
        "year_range": [int(mw["year"].min()), int(mw["year"].max())],
        "subseries_present": sorted(mw["subseries_id"].unique().tolist()),
        "depression_correction": depression_diag,
        "extension": diag, "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
