"""V03_S408_validate — verify S408 processed parquet matches book-quoted
Eiteman & Guthrie 1952 survey percentages.

Two truth rows (verbatim from Shaikh 2016 p. 163):
  subseries S408-A: 94.0% (charts 6 or 7)
  subseries S408-B: 94.3% (charts 6, 7, or 8)

Tolerance 0.5% (cross_sectional default).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402

SERIES_ID = "S408"
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 0.5

# Verbatim from book p. 163.
TRUTH = {
    "S408-A": 94.0,
    "S408-B": 94.3,
}


def _update_report(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[SERIES_ID] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)

    abs_errs, pct_errs, divergences = [], [], []
    n_compared = 0
    for sub_id, expected in TRUTH.items():
        match = actual[(actual["subseries_id"] == sub_id) & (actual["year"] == 1952)]
        if match.empty:
            divergences.append({"subseries_id": sub_id, "issue": "missing"})
            continue
        v = float(match["value"].iloc[0])
        abs_err = abs(v - expected)
        pct_err = abs_err / abs(expected) * 100.0
        abs_errs.append(abs_err); pct_errs.append(pct_err); n_compared += 1
        if pct_err > VALIDATOR_TOL_PCT:
            divergences.append({"subseries_id": sub_id, "value": v,
                                "expected": expected, "pct_err": round(pct_err, 6)})

    mae = float(sum(abs_errs) / len(abs_errs)) if abs_errs else 0.0
    max_abs = float(max(abs_errs)) if abs_errs else 0.0
    max_pct = float(max(pct_errs)) if pct_errs else 0.0
    status = "PASS" if not divergences else "FAIL"

    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "cross_sectional",
        "comparison_basis": "Verbatim Shaikh 2016 p. 163 (Eiteman & Guthrie 1952 survey)",
        "n_compared": n_compared, "mae": round(mae, 6),
        "max_abs_err": round(max_abs, 6), "max_pct_err": round(max_pct, 6),
        "divergence_count": len(divergences), "divergences": divergences,
        "cd2_comparison": {"note": "no CD/CD2 predecessor"},
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
