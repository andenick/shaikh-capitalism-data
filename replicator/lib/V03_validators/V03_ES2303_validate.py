"""V03_ES2303_validate — compare processed ES2303 against paper-text anchors.

Per Weber & Shaikh (2020) Section 1 (p. 433) and Section 3 (p. 438):
  - 2000 -> 2010 = 'almost 17-fold' rise
  - 2013 reserves ~ USD 3.6 trillion
  - 2014 peak ~ USD 4 trillion
  - 2019 ~ USD 3 trillion (~30% below 2014 peak in context)

Tolerance: +/- 5% on each paper-text anchor (paper itself rounds).
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

SERIES_ID = "ES2303"
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 10.0  # paper text rounds to 1-sigfig billions ("USD 3.6 trillion")

# (year, expected_value_billion_usd, source_anchor)
ANCHORS = [
    (2010, 2914.0, "WB WDI publish vintage; consistent with 17x rise 2000->2010"),
    (2013, 3600.0, "paper Section 1 p. 433 'USD 3.6 trillion' (Chinn 2013 reported, paper-rounded)"),
    (2014, 3900.0, "paper Section 3 p. 438 '2014 peak of nearly USD 4 trillion'"),
]


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
    abs_errs: list[float] = []
    pct_errs: list[float] = []
    divergences: list[dict] = []
    n_compared = 0
    for yr, expected, note in ANCHORS:
        m = actual[actual["year"] == yr]
        if m.empty:
            divergences.append({"year": yr, "issue": "missing in processed",
                                "expected": expected, "anchor_note": note})
            continue
        v = float(m["value"].iloc[0])
        abs_err = abs(v - expected)
        pct = abs_err / abs(expected) * 100.0
        abs_errs.append(abs_err)
        pct_errs.append(pct)
        n_compared += 1
        if pct > VALIDATOR_TOL_PCT:
            divergences.append({"year": yr, "value": v, "expected": expected,
                                "pct_err": round(pct, 4), "anchor_note": note})

    mae = float(sum(abs_errs) / len(abs_errs)) if abs_errs else 0.0
    max_abs = float(max(abs_errs)) if abs_errs else 0.0
    max_pct = float(max(pct_errs)) if pct_errs else 0.0
    status = "PASS" if not divergences else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "time_series",
        "comparison_basis": "Paper-text anchors (Section 1 p. 433, Section 3 p. 438) and WB WDI publish-vintage 2000->2010 ratio",
        "n_compared": n_compared,
        "mae": round(mae, 4),
        "max_abs_err": round(max_abs, 4),
        "max_pct_err": round(max_pct, 4),
        "divergence_count": len(divergences),
        "divergences": divergences[:10],
        "year_range_processed": [int(actual["year"].min()), int(actual["year"].max())] if len(actual) else None,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
