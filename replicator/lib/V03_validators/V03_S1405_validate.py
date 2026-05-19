"""V03_S1405_validate - validate S1405 (HP100 wage-share Phillips) against Appendix 14.3.

Validates the HP100 time series and the published constrained-b=1 fitted curves
against Appendix columns. Additionally verifies the in-sample-fitted constrained
parameters (a, c) reproduced from data agree with Shaikh's published values to
within 0.05 absolute (numerical reproduction tolerance).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED  # noqa: E402
from V03_validators._ch14_validator_lib import (  # noqa: E402
    validate_against_appendix14, update_report,
)

SERIES_ID = "S1405"
VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1949, 2011)
PUBLISHED_ERA1 = {"a": -1.026431, "c": -0.010677, "r2": 0.931}
PUBLISHED_ERA2 = {"a": -1.010996, "c": -0.003709, "r2": 0.965}
PARAM_TOL_ABS = 0.05


def _phillips_fit_check() -> dict:
    p = DATA_PROCESSED / f"{SERIES_ID}_phillips_fits.json"
    if not p.exists():
        return {"status": "skipped", "reason": "no phillips_fits sidecar"}
    fits = json.loads(p.read_text(encoding="utf-8"))
    out = {}
    for era_key, pub in (("era1", PUBLISHED_ERA1), ("era2", PUBLISHED_ERA2)):
        cb1 = fits.get(era_key, {}).get("constrained_b1", {})
        a_diff = abs(cb1.get("a", float("nan")) - pub["a"]) if cb1 else None
        c_diff = abs(cb1.get("c", float("nan")) - pub["c"]) if cb1 else None
        r2_diff = abs(cb1.get("r2", float("nan")) - pub["r2"]) if cb1 else None
        out[era_key] = {
            "fitted": cb1,
            "published": pub,
            "a_abs_diff": a_diff,
            "c_abs_diff": c_diff,
            "r2_abs_diff": r2_diff,
            "param_tol_abs": PARAM_TOL_ABS,
            "matches_published": (a_diff is not None and a_diff < PARAM_TOL_ABS and
                                   c_diff is not None and c_diff < PARAM_TOL_ABS),
        }
        out[era_key]["unconstrained"] = fits.get(era_key, {}).get("unconstrained", {})
    return out


def run() -> dict:
    row = validate_against_appendix14(
        SERIES_ID,
        {
            f"{SERIES_ID}-A": "gwshhp100",
            f"{SERIES_ID}-B": "ulintensityhp100",
            f"{SERIES_ID}-FIT1": "GWSHHP100RAL8AF",
            f"{SERIES_ID}-FIT2": "GWSHHP100RAL8BP1F",
        },
        overlap_range=BOOK_OVERLAP,
        tol_pct=VALIDATOR_TOL_PCT,
    )
    row["phillips_fit_replication"] = _phillips_fit_check()
    row["validated_at"] = datetime.now(timezone.utc).isoformat()
    update_report(SERIES_ID, row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
