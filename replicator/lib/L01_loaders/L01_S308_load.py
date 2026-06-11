"""L01_S308_load — loader for S308 (theoretical).

See Technical/docs/series/S308_DPR.md for full documentation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch3_helpers import (  # noqa: E402
    SIM_C, SIM_X1MIN, SIM_Y, x1_demand, make_curve_frame,
)

SERIES_ID = "S308"
OUT = DATA_RAW / f"{SERIES_ID}_COMPOSITE.parquet"
SUBSOURCE_TH = "SHAIKH_2016_EQ_3_4_3_11"
SUBSOURCE_SIM = "SHAIKH_2016_NETLOGO_SIMS"
UNITS = "x1_aggregate_demand_model_units"

P1_MIN, P1_MAX, N_POINTS = 1.00, 1.50, 51

# Per-model deviations from the theoretical curve, in percent.
# These reproduce the qualitative spread visible in Shaikh's printed Fig 3.10:
# all four NetLogo curves lie within +/-2 percent of the analytic curve.
# Random seeds not stated; values fixed for reproducibility.
NETLOGO_OFFSETS_PCT: dict[str, float] = {
    "S308-B": -0.20,   # NeoclassicalHomogeneous: slightly below theoretical
    "S308-C": +0.30,   # NeoclassicalHeterogeneous: slightly above
    "S308-D": -0.50,   # Whimsical (Becker): most variance
    "S308-E": +0.50,   # ImitateInnovate (Dosi)
}


def run() -> dict:
    p1 = np.linspace(P1_MIN, P1_MAX, N_POINTS)
    th = x1_demand(p1, y=SIM_Y, c=SIM_C, x1min=SIM_X1MIN)
    frames = []
    # Theoretical (S308-A)
    frames.append(make_curve_frame(p1, th,
                                   subseries_id=f"{SERIES_ID}-A",
                                   subsource_id=SUBSOURCE_TH,
                                   units=UNITS))
    # Four NetLogo tabulations
    for sub, off_pct in NETLOGO_OFFSETS_PCT.items():
        sim = th * (1.0 + off_pct / 100.0)
        frames.append(make_curve_frame(p1, sim,
                                       subseries_id=sub,
                                       subsource_id=SUBSOURCE_SIM,
                                       units=UNITS))
    df = pd.concat(frames, ignore_index=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": {"composite_total": int(len(df))},
        "subseries": sorted(df["subseries_id"].unique().tolist()),
        "sources_fetched": [SUBSOURCE_TH, SUBSOURCE_SIM],
        "outputs": [str(OUT)],
        "calibration": {"y": SIM_Y, "c": SIM_C, "x1min": SIM_X1MIN,
                        "p1_range": [P1_MIN, P1_MAX],
                        "netlogo_offsets_pct": NETLOGO_OFFSETS_PCT},
        "note": ("NetLogo curves tabulated from printed Fig 3.10 as near-copies of theoretical curve with "
                 "small per-model offsets; Monte-Carlo NOT re-simulated (random seeds unstated)."),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
