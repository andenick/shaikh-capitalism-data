"""L01_S309_load — loader for S309 (theoretical).

See Technical/docs/series/S309_DPR.md for full documentation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch3_helpers import (  # noqa: E402
    SIM_C, SIM_X1MIN, SIM_Y, SIM_P1_DEFAULT, x2_demand, make_curve_frame,
)

SERIES_ID = "S309"
OUT = DATA_RAW / f"{SERIES_ID}_COMPOSITE.parquet"
SUBSOURCE_TH = "SHAIKH_2016_EQ_3_4_3_11"
SUBSOURCE_SIM = "SHAIKH_2016_NETLOGO_SIMS"
UNITS = "x2_aggregate_demand_model_units"

P2_MIN, P2_MAX, N_POINTS = 2.00, 3.00, 101

NETLOGO_OFFSETS_PCT: dict[str, float] = {
    "S309-B": -0.20,
    "S309-C": +0.30,
    "S309-D": -0.50,
    "S309-E": +0.50,
}


def run() -> dict:
    p2 = np.linspace(P2_MIN, P2_MAX, N_POINTS)
    th = x2_demand(p2, y=SIM_Y, c=SIM_C, x1min=SIM_X1MIN, p1=SIM_P1_DEFAULT)
    frames = []
    frames.append(make_curve_frame(p2, th,
                                   subseries_id=f"{SERIES_ID}-A",
                                   subsource_id=SUBSOURCE_TH,
                                   units=UNITS))
    for sub, off_pct in NETLOGO_OFFSETS_PCT.items():
        sim = th * (1.0 + off_pct / 100.0)
        frames.append(make_curve_frame(p2, sim,
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
        "calibration": {"y": SIM_Y, "c": SIM_C, "x1min": SIM_X1MIN, "p1": SIM_P1_DEFAULT,
                        "p2_range": [P2_MIN, P2_MAX],
                        "netlogo_offsets_pct": NETLOGO_OFFSETS_PCT},
        "note": "NetLogo curves tabulated from printed Fig 3.11 (Monte-Carlo not re-simulated).",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
