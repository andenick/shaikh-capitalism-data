"""L01_S305 — loader for S305 (theoretical).

Engel Curve of Necessaries, Case II (Shaikh 2016, Figure 3.7, printed p. 95).

Book-stated model
-----------------
The Engel curve for the necessary good is eq (3.5) with the discretionary
propensity c allowed to decline with income (Case II):

    p1*x1 = (1 - c(y)) * p1*x1min + c(y) * y          (p1 = 1)

Shaikh states the qualitative form (c declines with income; the curve "gets
flatter" as c falls — saturation, printed p. 93) but does NOT give an explicit
algebraic c(y). However he *plots* the exact c(y) he used in Figure 3.6
("Discretionary Propensity to Consume, Case II"), which is directly readable:
c falls gently from ~0.70 at y=10 to ~0.40 at y=50. Feeding that plotted
profile through the stated Engel equation reproduces his Figure 3.7
(rising ~10 -> ~26 over y = 10 -> 50). x1min = 10 is pinned by both Engel
curves (Fig 3.5 Case I and Fig 3.7 Case II) starting at E = 10 at y = 10, and
matches the chapter's simulation minimum (eq 3.5, x1min = 10).

Calibration of c(y) here matches Shaikh's plotted Figure 3.6 to within read-off
tolerance: c(y) = 0.80 * exp(-0.014 * y) gives c(10..50) = 0.70, 0.61, 0.53,
0.46, 0.40. The earlier calibration (c0=0.7, k=0.05, x1min=5) decayed far too
fast and collapsed the Engel curve into a non-monotone hump ~3x too low; it was
not consistent with Shaikh's own Figure 3.6/3.7. These parameters are local to
S305 (they do not touch the shared Case II c(y) used by S304).

See Technical/docs/series/S305_DPR.md for full documentation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch3_helpers import make_curve_frame, write_parquet  # noqa: E402

SERIES_ID = "S305"
OUT = DATA_RAW / f"{SERIES_ID}_THEORETICAL.parquet"
SUBSERIES = f"{SERIES_ID}-A"
SUBSOURCE = "SHAIKH_2016_EQ_3_4_3_11"
UNITS = "expenditure_on_necessaries_model_units"

Y_MIN, Y_MAX, N_POINTS = 0.0, 60.0, 121

# --- Case II calibration matched to Shaikh's plotted Figure 3.6 (p. 95) ------
# c(y) = C0 * exp(-K * y), reproducing the read-off c-curve (0.70 @ y=10 ->
# 0.40 @ y=50). x1min pinned to 10 by the Engel-curve start point (E=10 @ y=10)
# shared with Fig 3.5 (Case I) and the chapter's simulation minimum.
C0_S305 = 0.80
K_S305 = 0.014
X1MIN_S305 = 10.0
P1_S305 = 1.0


def c_s305(y: np.ndarray) -> np.ndarray:
    """Case II discretionary propensity matched to Shaikh's Figure 3.6 profile."""
    return C0_S305 * np.exp(-K_S305 * y)


def run() -> dict:
    y = np.linspace(Y_MIN, Y_MAX, N_POINTS)
    c = c_s305(y)
    # eq (3.5) with c -> c(y), p1 = 1:  p1*x1 = (1 - c(y)) * p1*x1min + c(y)*y
    expenditure = (1.0 - c) * (P1_S305 * X1MIN_S305) + c * y
    df = make_curve_frame(y, expenditure, subseries_id=SUBSERIES, subsource_id=SUBSOURCE, units=UNITS)
    n = write_parquet(df, OUT)
    return {"status": "OK", "rows_loaded": {"theoretical": n},
            "sources_fetched": [SUBSOURCE], "outputs": [str(OUT)],
            "calibration": {"functional_form": "p1*x1=(1-c(y))*p1*x1min + c(y)*y, c(y)=0.80*exp(-0.014*y)",
                            "x1min": X1MIN_S305, "p1": P1_S305, "c0": C0_S305, "k": K_S305,
                            "y_range": [Y_MIN, Y_MAX]}}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
