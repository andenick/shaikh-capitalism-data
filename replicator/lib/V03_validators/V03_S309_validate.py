"""V03_S309_validate — validator for S309.

See S309_DPR.md §9 for tolerance and shape checks.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402
from V03_validators._ch3_helpers import update_report, validate_theoretical_curve  # noqa: E402

SERIES_ID = "S309"
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 0.5
Y_BOUND_LO, Y_BOUND_HI = 30.0, 50.0
SHAIKH_TOL_PCT = 2.0


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    df = pd.read_parquet(PROCESSED)
    rows: dict = {}
    overall_status = "PASS_THEORETICAL"
    for sub in sorted(df["subseries_id"].unique().tolist()):
        r = validate_theoretical_curve(
            df, sid=f"{SERIES_ID}/{sub}",
            y_bound_lo=Y_BOUND_LO, y_bound_hi=Y_BOUND_HI,
            shape="declining",
            tolerance_pct=VALIDATOR_TOL_PCT, bound_tol_pct=1.0,
            subseries_filter=sub,
        )
        rows[sub] = r
        if r["status"] != "PASS_THEORETICAL":
            overall_status = "FAIL"
    th = df[df["subseries_id"] == f"{SERIES_ID}-A"].sort_values("x_value")
    crosscurve_ok = True
    crosscurve_details = {}
    for sub in [f"{SERIES_ID}-B", f"{SERIES_ID}-C", f"{SERIES_ID}-D", f"{SERIES_ID}-E"]:
        sim = df[df["subseries_id"] == sub].sort_values("x_value")
        merged = th.merge(sim, on="x_value", suffixes=("_th", "_sim"))
        pct_diff = np.abs((merged["value_sim"] - merged["value_th"]) / merged["value_th"]) * 100.0
        max_pct = float(pct_diff.max())
        crosscurve_details[sub] = round(max_pct, 4)
        if max_pct > SHAIKH_TOL_PCT:
            crosscurve_ok = False
    if not crosscurve_ok:
        overall_status = "FAIL"
    row = {
        "status": overall_status,
        "sid": SERIES_ID,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "n_compared": int(len(df)),
        "subseries_results": {k: v["status"] for k, v in rows.items()},
        "shaikh_central_claim_tolerance_pct": SHAIKH_TOL_PCT,
        "netlogo_vs_theoretical_max_pct_diff": crosscurve_details,
        "netlogo_within_tolerance": crosscurve_ok,
        "y_bounds": [Y_BOUND_LO, Y_BOUND_HI],
        "mae": rows.get(f"{SERIES_ID}-A", {}).get("mae"),
        "max_abs_err": rows.get(f"{SERIES_ID}-A", {}).get("max_abs_err"),
        "max_pct_err": rows.get(f"{SERIES_ID}-A", {}).get("max_pct_err"),
        "divergence_years": [],
        "divergence_count": 0,
        "cd2_comparison": {},
        "validated_at": rows.get(f"{SERIES_ID}-A", {}).get("validated_at"),
        "note": ("Composite theoretical series for luxury good x2; 5 subseries. Validates shape/bounds "
                 "per subseries AND Shaikh's central claim (NetLogo within +/-2 percent of theoretical)."),
    }
    update_report(REPORT, SERIES_ID, row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
