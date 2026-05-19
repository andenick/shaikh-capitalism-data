"""L01_S301_load — generate the theoretical marginal-share curve for Fig 3.3.

Series S301: d(p1*x1)/dy = (1 - c) * d(x1min)/dy + c, Case I (x1min sub-linear in y).

Writes:
    Technical/data/raw/S301_THEORETICAL.parquet

Schema: year (int sequence), x_value (income y), value (marginal share),
        subseries_id, subsource_id, units.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch3_helpers import (  # noqa: E402
    C_CASE_I, dx1min_dy_case_i, make_curve_frame, write_parquet,
)

SERIES_ID = "S301"
OUT = DATA_RAW / f"{SERIES_ID}_THEORETICAL.parquet"
SUBSERIES = f"{SERIES_ID}-A"
SUBSOURCE = "SHAIKH_2016_EQ_3_4_3_11"
UNITS = "marginal_share_dimensionless"

# Income grid: y in [1.0, 60], 119 points. Skip y<1 to keep curve within Fig 3.3
# printed y-axis bound of 0.8 (square-root tail diverges as y -> 0).
Y_MIN, Y_MAX, N_POINTS = 1.0, 60.0, 119


def run() -> dict:
    y = np.linspace(Y_MIN, Y_MAX, N_POINTS)
    # d(p1*x1)/dy = (1 - c) * d(x1min)/dy + c    (p1 = 1, so p1*x1min = x1min)
    val = (1.0 - C_CASE_I) * dx1min_dy_case_i(y) + C_CASE_I
    df = make_curve_frame(y, val, subseries_id=SUBSERIES, subsource_id=SUBSOURCE, units=UNITS)
    n = write_parquet(df, OUT)
    return {
        "status": "OK",
        "rows_loaded": {"theoretical": n},
        "sources_fetched": [SUBSOURCE],
        "outputs": [str(OUT)],
        "calibration": {
            "c": C_CASE_I, "x1min_form": "y^0.5", "y_range": [Y_MIN, Y_MAX],
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
