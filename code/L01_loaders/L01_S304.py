"""L01_S304 — loader for S304 (theoretical).

See Technical/docs/series/S304_DPR.md for full documentation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch3_helpers import make_curve_frame, write_parquet  # noqa: E402

SERIES_ID = "S304"
OUT = DATA_RAW / f"{SERIES_ID}_THEORETICAL.parquet"
SUBSERIES = f"{SERIES_ID}-A"
SUBSOURCE = "SHAIKH_2016_EQ_3_4_3_11"
UNITS = "discretionary_propensity_dimensionless"

Y_MIN, Y_MAX, N_POINTS = 0.0, 60.0, 121


def run() -> dict:
    y = np.linspace(Y_MIN, Y_MAX, N_POINTS)
    # Case-II discretionary propensity, calibrated to Shaikh's plotted Fig 3.6 read-off
    # (c = 0.70 at y=10 -> 0.40 at y=50). The shared c_case_ii (c0=0.7, k=0.05) decayed far
    # too fast (~0.06 by y=50), mismatching the book. Localized 2026-05-27 PC-fix (cf S305).
    c = 0.80 * np.exp(-0.014 * y)
    df = make_curve_frame(y, c, subseries_id=SUBSERIES, subsource_id=SUBSOURCE, units=UNITS)
    n = write_parquet(df, OUT)
    return {"status": "OK", "rows_loaded": {"theoretical": n},
            "sources_fetched": [SUBSOURCE], "outputs": [str(OUT)],
            "calibration": {"functional_form": "c(y)=c0*exp(-k*y)", "c0": 0.80, "k": 0.014,
                            "y_range": [Y_MIN, Y_MAX], "note": "calibrated to book Fig 3.6 (0.70@y10->0.40@y50)"}}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
