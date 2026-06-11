"""L01_S303_load — loader for S303 (theoretical).

See Technical/docs/series/S303_DPR.md for full documentation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch3_helpers import (  # noqa: E402
    C_CASE_I, x1min_case_i, make_curve_frame, write_parquet,
)

SERIES_ID = "S303"
OUT = DATA_RAW / f"{SERIES_ID}_THEORETICAL.parquet"
SUBSERIES = f"{SERIES_ID}-A"
SUBSOURCE = "SHAIKH_2016_EQ_3_4_3_11"
UNITS = "expenditure_on_necessaries_model_units"

Y_MIN, Y_MAX, N_POINTS = 0.0, 60.0, 121


def run() -> dict:
    y = np.linspace(Y_MIN, Y_MAX, N_POINTS)
    # eq (3.5): x1 = (1 - c) * x1min + c * y / p1   (p1=1 -> p1*x1 = x1)
    expenditure = (1.0 - C_CASE_I) * x1min_case_i(y) + C_CASE_I * y
    df = make_curve_frame(y, expenditure, subseries_id=SUBSERIES, subsource_id=SUBSOURCE, units=UNITS)
    n = write_parquet(df, OUT)
    return {"status": "OK", "rows_loaded": {"theoretical": n},
            "sources_fetched": [SUBSOURCE], "outputs": [str(OUT)],
            "calibration": {"c": C_CASE_I, "x1min_form": "y^0.5", "y_range": [Y_MIN, Y_MAX]}}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
