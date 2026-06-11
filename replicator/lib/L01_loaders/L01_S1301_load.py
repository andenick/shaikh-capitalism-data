"""L01_S1301_load - render Fig 13.7 theoretical schematic (eq. 13.43).

S1301 is `theoretical` (Phase 4 ratified). Shaikh does not publish the
parameter values used to draw Fig 13.7, so we declare illustrative values
in the EPR:
  ln Y0 = 8.0
  alpha = 0.03   (3% per period equilibrium growth)
  sigma_epsilon = 0.015
  RNG seed = 42
  t in [0, 75] (matching the chart x-axis range)

The series is:
  ln Y(t) = ln Y0 + alpha * t + eta(t),  eta(t) = sum_{i=1..t} epsilon_i
  epsilon_i ~ N(0, sigma_epsilon^2)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402

SERIES_ID = "S1301"
OUT = DATA_RAW / f"{SERIES_ID}_THEORETICAL.parquet"

LN_Y0 = 8.0
ALPHA = 0.03
SIGMA = 0.015
SEED = 42
T_MAX = 75


def run() -> dict:
    rng = np.random.default_rng(SEED)
    eps = rng.normal(0.0, SIGMA, size=T_MAX + 1)
    eps[0] = 0.0  # eta(0) = 0
    eta = np.cumsum(eps)
    t = np.arange(0, T_MAX + 1)
    trend = LN_Y0 + ALPHA * t
    actual = trend + eta

    rows = []
    for tt, tr, ac in zip(t, trend, actual):
        rows.append({"year": int(tt), "value": float(tr),
                     "subseries_id": "S1301-EQ",
                     "subsource_id": "SHAIKH_2016_EQ_13_43",
                     "units": "ln_Y_model_units"})
        rows.append({"year": int(tt), "value": float(ac),
                     "subseries_id": "S1301-ACTUAL",
                     "subsource_id": "SHAIKH_2016_EQ_13_43",
                     "units": "ln_Y_model_units"})

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"theoretical_realization": len(out)},
        "params": {"ln_Y0": LN_Y0, "alpha": ALPHA,
                   "sigma_epsilon": SIGMA, "seed": SEED, "t_max": T_MAX},
        "sources_fetched": ["SHAIKH_2016_EQ_13_43"],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
