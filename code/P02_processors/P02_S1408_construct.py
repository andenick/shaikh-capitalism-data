"""P02_S1408_construct - HP(100) nominal-wage growth vs intensity (Ch14 Fig 14.17).

Pass-through of Appendix 14.3 GMWAGEHP100 and ulintensityhp100.

Additionally fits the two Phillips-form era curves (1949-1982, 1994-2011) both
as DIRECT refit of GMWAGEHP100 vs ulintensityhp100 and ALGEBRAIC decomposition
= S1405-era-fit + HP100(inflation) + HP100(productivity-growth) per Eq. 14.19.

Also runs the Table 14.3 secondary regression of residual nominal-wage growth on
inflation + productivity growth, separately by era.

Sample windows per Phase 4 resolution: 1949-1982 / 1994-2011 (Appendix-documented
windows; first-difference loses 1948). Off-by-one with chapter-text 1948-1982 noted.
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
    phillips_fit_constrained, phillips_fit_unconstrained, read_appendix14,
)

SERIES_ID = "S1408"
IN_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"
OUT_FITS = DATA_PROCESSED / f"{SERIES_ID}_phillips_fits.json"
S1405_FITS = DATA_PROCESSED / "S1405_phillips_fits.json"

ERA1 = (1949, 1982)
ERA2 = (1994, 2011)


def _fit_era(x: pd.Series, y: pd.Series, era: tuple[int, int], years: pd.Series) -> dict:
    mask = (years >= era[0]) & (years <= era[1])
    return {
        "era_window": [int(era[0]), int(era[1])],
        "constrained_b1": phillips_fit_constrained(x[mask].to_numpy(dtype=float),
                                                   y[mask].to_numpy(dtype=float)),
        "unconstrained":  phillips_fit_unconstrained(x[mask].to_numpy(dtype=float),
                                                     y[mask].to_numpy(dtype=float)),
    }


def _table_14_3(years: pd.Series, gmwage_hp: pd.Series, infl_hp: pd.Series,
                gprod_hp: pd.Series, era: tuple[int, int]) -> dict:
    """OLS: GMWAGEHP100 = const + b_p * inflrateHP100 + b_y * GPRODVTYHP100."""
    mask = (years >= era[0]) & (years <= era[1])
    y = gmwage_hp[mask].to_numpy(dtype=float)
    X = np.column_stack([np.ones(mask.sum()), infl_hp[mask].to_numpy(dtype=float),
                         gprod_hp[mask].to_numpy(dtype=float)])
    keep = np.isfinite(y) & np.isfinite(X).all(axis=1)
    y_, X_ = y[keep], X[keep]
    if len(y_) < 4:
        return {"era_window": list(era), "n": int(len(y_)), "converged": False}
    beta, *_ = np.linalg.lstsq(X_, y_, rcond=None)
    yhat = X_ @ beta
    ss_res = float(np.sum((y_ - yhat) ** 2))
    ss_tot = float(np.sum((y_ - y_.mean()) ** 2))
    r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
    return {
        "era_window": list(era),
        "n": int(len(y_)),
        "const": float(beta[0]),
        "inflation_coef": float(beta[1]),
        "productivity_growth_coef": float(beta[2]),
        "r2": r2,
        "converged": True,
    }


def run() -> dict:
    if not IN_BOOK.exists():
        return {"status": "FAIL", "error": f"missing book parquet {IN_BOOK}"}
    df = pd.read_parquet(IN_BOOK).rename(columns={"subsource_id": "source_id"})
    out = df[["year", "value", "subseries_id", "source_id", "units"]].sort_values(
        ["subseries_id", "year"]).reset_index(drop=True)

    wide = out.pivot_table(index="year", columns="subseries_id", values="value", aggfunc="first").reset_index()
    fits: dict = {}
    if f"{SERIES_ID}-A" in wide.columns and f"{SERIES_ID}-B" in wide.columns:
        y = wide[f"{SERIES_ID}-A"]   # GMWAGEHP100
        x = wide[f"{SERIES_ID}-B"]   # ulintensityhp100
        years = wide["year"]
        fits["direct_refit_era1"] = _fit_era(x, y, ERA1, years)
        fits["direct_refit_era2"] = _fit_era(x, y, ERA2, years)

    # Table 14.3 secondary regression
    appx = read_appendix14()
    if "GMWAGEHP100" in appx.columns and "inflrateHP100" in appx.columns and "GPRODVTYHP100" in appx.columns:
        fits["table_14_3_era1"] = _table_14_3(
            appx["year"].astype(float), appx["GMWAGEHP100"],
            appx["inflrateHP100"], appx["GPRODVTYHP100"], ERA1,
        )
        fits["table_14_3_era2"] = _table_14_3(
            appx["year"].astype(float), appx["GMWAGEHP100"],
            appx["inflrateHP100"], appx["GPRODVTYHP100"], ERA2,
        )
        fits["table_14_3_published_era1_inflation_coef"] = "slightly below 1.0 (book p. 672)"
        fits["table_14_3_published_era1_productivity_growth_coef"] = 0.82

    if S1405_FITS.exists():
        s1405 = json.loads(S1405_FITS.read_text(encoding="utf-8"))
        fits["algebraic_variant_note"] = (
            "Per Eq. 14.19: nominal-wage Phillips curve = wage-share Phillips curve "
            "+ HP100(inflation) + HP100(productivity growth)."
        )
        fits["s1405_era1_constrained_b1"] = s1405.get("era1", {}).get("constrained_b1", {})
        fits["s1405_era2_constrained_b1"] = s1405.get("era2", {}).get("constrained_b1", {})

    fits["hp_lambda"] = 100
    fits["sample_window_resolution"] = ("Use 1949-1982 / 1994-2011 (Appendix 14.2 "
                                         "documented). Chapter-text 1948-1982 reflects "
                                         "the level-data start year, but the regression "
                                         "first observation is 1949 (differencing loses 1948).")
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
                         if k.startswith(("direct_refit_", "table_14_3_era"))},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json as _json
    print(_json.dumps(run(), indent=2, default=str))
