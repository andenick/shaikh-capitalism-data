"""V03_S301_validate — validate the S301 marginal-share curve.

Theoretical series; no point-by-point book truth exists. We validate axis
bounds, monotone-decline, and approach to the asymptote c=0.5.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402
from V03_validators._ch3_helpers import update_report, validate_theoretical_curve  # noqa: E402

SERIES_ID = "S301"
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 0.5  # axis-bound tolerance for theoretical Ch3 series
Y_BOUND_LO, Y_BOUND_HI = 0.0, 0.8  # Fig 3.3 printed y-axis bounds


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    df = pd.read_parquet(PROCESSED)
    row = validate_theoretical_curve(
        df, sid=SERIES_ID,
        y_bound_lo=Y_BOUND_LO, y_bound_hi=Y_BOUND_HI,
        shape="declining",
        tolerance_pct=VALIDATOR_TOL_PCT,
        bound_tol_pct=1.0,
        asymptote_target=0.5, asymptote_tol=0.05,
        subseries_filter=f"{SERIES_ID}-A",
    )
    update_report(REPORT, SERIES_ID, row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
