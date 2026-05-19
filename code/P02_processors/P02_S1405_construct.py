"""P02_S1405_construct - HP(100) wage-share growth vs intensity (Ch14 Fig 14.14).

Pass-through of Appendix 14.3 columns:
  - gwshhp100           -> S1405-A
  - ulintensityhp100    -> S1405-B
  - GWSHHP100RAL8AF     -> S1405-FIT1 (era-1 constrained b=1 Phillips fit)
  - GWSHHP100RAL8BP1F   -> S1405-FIT2 (era-2 constrained b=1 Phillips fit)

ADDITIONALLY computes BOTH constrained (b=1) and unconstrained Phillips fits
from the data over the two era windows (1949-1982, 1994-2011), omitting the
1983-1993 transition, per Phase 4 Q3 + Q4 resolutions. Fit parameters are
emitted as a sidecar JSON, NOT as additional time-series rows (per-axis fits
are scalar objects, not annual values).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402
from L01_loaders._ch14_helpers import (  # noqa: E402
    phillips_fit_constrained, phillips_fit_unconstrained,
)

SERIES_ID = "S1405"
IN_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"
OUT_FITS = DATA_PROCESSED / f"{SERIES_ID}_phillips_fits.json"

ERA1 = (1949, 1982)
ERA2 = (1994, 2011)
PUBLISHED = {
    "era1_constrained": {"a": -1.026431, "c": -0.010677, "r2": 0.931},
    "era2_constrained": {"a": -1.010996, "c": -0.003709, "r2": 0.965},
}


def _fit_era(x: pd.Series, y: pd.Series, era: tuple[int, int],
             years: pd.Series) -> dict:
    mask = (years >= era[0]) & (years <= era[1])
    x_, y_ = x[mask].to_numpy(dtype=float), y[mask].to_numpy(dtype=float)
    return {
        "era_window": [int(era[0]), int(era[1])],
        "constrained_b1": phillips_fit_constrained(x_, y_),
        "unconstrained":  phillips_fit_unconstrained(x_, y_),
    }


def run() -> dict:
    if not IN_BOOK.exists():
        return {"status": "FAIL", "error": f"missing book parquet {IN_BOOK}"}
    df = pd.read_parquet(IN_BOOK).rename(columns={"subsource_id": "source_id"})
    out = df[["year", "value", "subseries_id", "source_id", "units"]].sort_values(
        ["subseries_id", "year"]).reset_index(drop=True)

    # Reshape to wide for Phillips fitting
    wide = out.pivot_table(index="year", columns="subseries_id", values="value", aggfunc="first")
    wide = wide.reset_index()
    fits = {}
    if f"{SERIES_ID}-A" in wide.columns and f"{SERIES_ID}-B" in wide.columns:
        y = wide[f"{SERIES_ID}-A"]   # gwshhp100
        x = wide[f"{SERIES_ID}-B"]   # ulintensityhp100
        years = wide["year"]
        fits["era1"] = _fit_era(x, y, ERA1, years)
        fits["era2"] = _fit_era(x, y, ERA2, years)
        # Phase 6 third-regime check: era 2 over 1994-2007 (pre-GFC) for stability
        fits["era2_pre2008"] = _fit_era(x, y, (1994, 2007), years)
    fits["published_reference"] = PUBLISHED
    fits["transition_window_omitted"] = [1983, 1993]
    fits["hp_lambda"] = 100
    OUT_FITS.parent.mkdir(parents=True, exist_ok=True)
    OUT_FITS.write_text(json.dumps(fits, indent=2, default=str), encoding="utf-8")

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(out)),
        "year_range": [int(out["year"].min()), int(out["year"].max())],
        "subseries_present": sorted(out["subseries_id"].unique().tolist()),
        "phillips_fits_sidecar": str(OUT_FITS),
        "fits_summary": {k: v for k, v in fits.items()
                         if k in ("era1", "era2", "era2_pre2008")},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json as _json
    print(_json.dumps(run(), indent=2, default=str))
