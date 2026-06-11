"""P02_S1407_construct - HP(100) real-wage growth vs intensity (Ch14 Fig 14.16).

Pass-through of Appendix 14.3 GRWAGEHP100 and ulintensityhp100.

Additionally fits the two Phillips-form era curves (1949-1982, 1994-2011)
both as (a) DIRECT refit of GRWAGEHP100 vs ulintensityhp100 and (b) ALGEBRAIC
decomposition = S1405-era-fit + HP100(productivity-growth) -- emitting both
variants per Phase 4 Q3/Q4 and the S1407 dossier open question.

(b) is emitted as additional rows ONLY if the S1405 fits sidecar is present
and S1406 is processed (GPRODVTY HP100 series).
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

SERIES_ID = "S1407"
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


def run() -> dict:
    if not IN_BOOK.exists():
        return {"status": "FAIL", "error": f"missing book parquet {IN_BOOK}"}
    df = pd.read_parquet(IN_BOOK).rename(columns={"subsource_id": "source_id"})
    out = df[["year", "value", "subseries_id", "source_id", "units"]].sort_values(
        ["subseries_id", "year"]).reset_index(drop=True)

    wide = out.pivot_table(index="year", columns="subseries_id", values="value", aggfunc="first").reset_index()
    fits = {}
    if f"{SERIES_ID}-A" in wide.columns and f"{SERIES_ID}-B" in wide.columns:
        y = wide[f"{SERIES_ID}-A"]   # GRWAGEHP100
        x = wide[f"{SERIES_ID}-B"]   # ulintensityhp100
        years = wide["year"]
        fits["direct_refit_era1"] = _fit_era(x, y, ERA1, years)
        fits["direct_refit_era2"] = _fit_era(x, y, ERA2, years)
    # Algebraic decomposition variant: requires S1405 fits + HP100(productivity growth)
    if S1405_FITS.exists():
        s1405 = json.loads(S1405_FITS.read_text(encoding="utf-8"))
        fits["algebraic_variant_note"] = (
            "Per Eq. 14.18: real-wage Phillips curve = wage-share Phillips curve "
            "+ HP100(productivity growth). The S1405 fits sidecar provides era 1 "
            "and era 2 wage-share curves; combine with HP100(GPRODVTY) from "
            "Appendix 14.3 (column GPRODVTYHP100) at the implementation site."
        )
        fits["s1405_era1_constrained_b1"] = s1405.get("era1", {}).get("constrained_b1", {})
        fits["s1405_era2_constrained_b1"] = s1405.get("era2", {}).get("constrained_b1", {})

    fits["hp_lambda"] = 100
    fits["transition_omitted"] = [1983, 1993]
    fits["concept_policing_inherited_from"] = "S1406"
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
                         if k.startswith("direct_refit_")},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json as _json
    print(_json.dumps(run(), indent=2, default=str))
