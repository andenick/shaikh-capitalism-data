"""V03_S1403_validate - validate S1403 annual HP100 reference axes against Appendix 14.3.

The quarterly phase-plot axes (S1403-WSH_*_HP100, S1403-ULINT_*_HP100) cannot
be validated against the Appendix because the Appendix only publishes annual
HP100 series; the quarterly data Shaikh used was not redistributed. We instead
validate (a) S1403-A wageshhp100 and S1403-B ulintensityhp100 against the
Appendix as pass-through references, and (b) loosely compare the FRED-derived
annual-collapsed quarterly axes (subseries ending _ANNUALAVG_HP100) against
the Appendix at the 3% level (annual mean of quarterly HP-filtered values is
not identically equal to annual HP-filtered values).

Tolerance for S1403-A/B is the standard 1.0% pass-through; the annual-collapse
informational comparison is reported but does not fail the validator.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED  # noqa: E402
from V03_validators._ch14_validator_lib import (  # noqa: E402
    validate_against_appendix14, load_appendix14, update_report,
)

SERIES_ID = "S1403"
VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1948, 2011)


def _informational_quarterly_collapse_check() -> dict:
    proc = DATA_PROCESSED / f"{SERIES_ID}.parquet"
    if not proc.exists():
        return {"status": "skipped", "reason": "processed missing"}
    df = pd.read_parquet(proc)
    info: dict = {}
    truth = load_appendix14()
    for sub, appx_col in [
        (f"{SERIES_ID}-WSH_ANNUALAVG_HP100",   "wageshhp100"),
        (f"{SERIES_ID}-ULINT_ANNUALAVG_HP100", "ulintensityhp100"),
    ]:
        a = df[df["subseries_id"] == sub][["year", "value"]].rename(columns={"value": "actual"})
        if a.empty:
            info[sub] = {"status": "absent"}
            continue
        t = truth[["year", appx_col]].rename(columns={appx_col: "expected"}).dropna(subset=["expected"])
        m = a.merge(t, on="year", how="inner")
        m = m[(m["year"] >= BOOK_OVERLAP[0]) & (m["year"] <= BOOK_OVERLAP[1])]
        m["abs_err"] = (m["actual"] - m["expected"]).abs()
        m["pct_err"] = m["abs_err"] / m["expected"].abs() * 100.0
        info[sub] = {
            "n": int(len(m)),
            "mae": float(m["abs_err"].mean()) if len(m) else None,
            "max_pct_err": float(m["pct_err"].max()) if len(m) else None,
            "note": "Annual mean of quarterly HP100 series; expected to differ "
                    "modestly from annual HP100 of annual data (different filter "
                    "input + endpoint effects).",
        }
    return info


def run() -> dict:
    row = validate_against_appendix14(
        SERIES_ID,
        {
            f"{SERIES_ID}-A": "wageshhp100",
            f"{SERIES_ID}-B": "ulintensityhp100",
        },
        overlap_range=BOOK_OVERLAP,
        tol_pct=VALIDATOR_TOL_PCT,
    )
    row["informational_quarterly_collapse_check"] = _informational_quarterly_collapse_check()
    row["validated_at"] = datetime.now(timezone.utc).isoformat()
    update_report(SERIES_ID, row)
    return row


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
