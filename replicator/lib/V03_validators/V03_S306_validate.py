"""V03_S306_validate — validator for S306.

See S306_DPR.md §9 for tolerance and shape checks.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402
from V03_validators._ch3_helpers import update_report, validate_cross_sectional_unavailable  # noqa: E402

SERIES_ID = "S306"
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 0.5
Y_BOUND_LO, Y_BOUND_HI = 56.0, 70.0
UNITS = "pct_total_weekly_expenditure_on_food"


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    df = pd.read_parquet(PROCESSED)
    row = validate_cross_sectional_unavailable(
        df, sid=SERIES_ID, year=1904,
        y_bound_lo=Y_BOUND_LO, y_bound_hi=Y_BOUND_HI, units=UNITS,
    )
    update_report(REPORT, SERIES_ID, row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
