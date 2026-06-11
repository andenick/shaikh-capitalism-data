"""P02_S1402_construct - construct S1402 from raw inputs.

Book period (1948-2011): pass-through of UNEMPLRATE, UNEMPDURATION, ulintensity
from Appendix 14.3.

Extension (2012+): re-derive from FRED UNRATE (annual mean) and UEMPMEAN
(annual mean), rebase duration to 1948-1951 annual mean (extracted from the
book period), intensity = unrate * (duration_index/100).

UEMPMEAN 2011 top-coding break: NO backward adjustment (Phase 4 Q2 resolution).
Annotated in metadata.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1402"
IN_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
IN_UNRATE   = DATA_RAW / f"{SERIES_ID}_FRED_UNRATE.parquet"
IN_UEMPMEAN = DATA_RAW / f"{SERIES_ID}_FRED_UEMPMEAN.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"
BOOK_END = 2011
BASE_WINDOW = (1948, 1951)


def _book_long(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={"subsource_id": "source_id"})[
        ["year", "value", "subseries_id", "source_id", "units"]
    ]


def _derive_extension(ur: pd.DataFrame, ud: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    # UNRATE comes in percent; convert to decimal to match Appendix
    ur = ur[["year", "value"]].copy().rename(columns={"value": "unrate_pct"})
    ur["unrate"] = ur["unrate_pct"] / 100.0
    ud = ud[["year", "value"]].copy().rename(columns={"value": "uempmean_w"})
    # Base period mean (1948-1951) computed from the FRED annual UEMPMEAN
    base_mask = (ud["year"] >= BASE_WINDOW[0]) & (ud["year"] <= BASE_WINDOW[1])
    base_mean = float(ud.loc[base_mask, "uempmean_w"].mean())
    if not np.isfinite(base_mean) or base_mean <= 0:
        return pd.DataFrame(), {"extension_status": "FAIL", "reason": "base_window_mean_invalid"}
    ud["duration_index"] = ud["uempmean_w"] / base_mean
    # intensity (Shaikh decimal convention): rate * (index_x100 / 100) == rate * index
    m = ur.merge(ud[["year", "duration_index"]], on="year", how="inner")
    m["ulintensity"] = m["unrate"] * m["duration_index"]
    ext = m[m["year"] > BOOK_END].copy()

    rows = []
    for _, r in ext.iterrows():
        y = int(r["year"])
        rows.extend([
            {"year": y, "value": float(r["unrate"]),
             "subseries_id": f"{SERIES_ID}-A", "source_id": "FRED_DERIVED_UNRATE",
             "units": "decimal_rate"},
            # Appendix duration column is index *100; FRED-derived index already in *100 scale (Appendix base ~1)
            {"year": y, "value": float(r["duration_index"]),
             "subseries_id": f"{SERIES_ID}-B", "source_id": "FRED_DERIVED_UEMPDURATION",
             "units": "index_1948_1951_avg=100"},
            {"year": y, "value": float(r["ulintensity"]),
             "subseries_id": f"{SERIES_ID}-C", "source_id": "FRED_DERIVED_ULINTENSITY",
             "units": "decimal"},
        ])
    diag = {
        "extension_status": "ok",
        "base_window": list(BASE_WINDOW),
        "base_window_mean_weeks": base_mean,
        "years_appended": int(ext["year"].nunique()) if not ext.empty else 0,
        "last_year": int(m["year"].max()),
        "methodological_break_2011-01": True,
        "treatment": "no_adjustment_documented_break",
    }
    return pd.DataFrame(rows), diag


def run() -> dict:
    if not IN_BOOK.exists():
        return {"status": "FAIL", "error": f"missing book parquet {IN_BOOK}"}
    book = _book_long(pd.read_parquet(IN_BOOK))
    ext_rows = pd.DataFrame()
    ext_diag = {"extension_status": "data_unavailable", "reason": "FRED not loaded"}
    if IN_UNRATE.exists() and IN_UEMPMEAN.exists():
        ur = pd.read_parquet(IN_UNRATE)
        ud = pd.read_parquet(IN_UEMPMEAN)
        ext_rows, ext_diag = _derive_extension(ur, ud)
    final = pd.concat([book, ext_rows], ignore_index=True).sort_values(
        ["subseries_id", "year"]
    ).reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": ext_diag,
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
