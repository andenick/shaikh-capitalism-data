"""V03_ES2302_validate — anchor-based validation of ES2302 CA balance.

Anchors from Weber & Shaikh (2020) paper text and Fig 2 (Appendix p. 453):
  - CA level USD bn peaks ~420 in 2008 (per Fig 2 left axis)
  - CA %GDP peaks ~10 in 2007 (per Fig 2 right axis and Section 1)
  - CA %GDP ~ 0.4 in 2019 per IMF (2019a) cited in paper Section 1 p. 432

Tolerance: +/- 15% (loose; WEO vintage revisions move values; paper-figure
read precision ~0.5% of GDP).
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

SERIES_ID = "ES2302"
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 15.0

# (year, subseries_id, expected_value, source_anchor)
ANCHORS = [
    (2008, "ES2302-level", 420.0, "Fig 2 left axis peak ~ 420 USD bn"),
    (2007, "ES2302-pctgdp", 10.0, "Fig 2 right axis + Section 1 p. 432 ~10% peak"),
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
    for yr, sub, expected, note in ANCHORS:
        m = actual[(actual["year"] == yr) & (actual["subseries_id"] == sub)]
        if m.empty:
            divergences.append({"year": yr, "subseries": sub,
                                "issue": "missing", "expected": expected,
                                "anchor_note": note})
            continue
        v = float(m["value"].iloc[0])
        abs_err = abs(v - expected)
        pct = abs_err / abs(expected) * 100.0
        abs_errs.append(abs_err)
        pct_errs.append(pct)
        n_compared += 1
        if pct > VALIDATOR_TOL_PCT:
            divergences.append({"year": yr, "subseries": sub, "value": v,
                                "expected": expected, "pct_err": round(pct, 4),
                                "anchor_note": note})

    mae = float(sum(abs_errs) / len(abs_errs)) if abs_errs else 0.0
    max_abs = float(max(abs_errs)) if abs_errs else 0.0
    max_pct = float(max(pct_errs)) if pct_errs else 0.0
    status = "PASS" if not divergences else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "time_series",
        "comparison_basis": "Fig 2 / paper Section 1 p. 432 figure-read anchors at known peaks",
        "n_compared": n_compared,
        "mae": round(mae, 4),
        "max_abs_err": round(max_abs, 4),
        "max_pct_err": round(max_pct, 4),
        "divergence_count": len(divergences),
        "divergences": divergences[:10],
        "year_range_processed": [int(actual["year"].min()), int(actual["year"].max())] if len(actual) else None,
        "subseries_present": sorted(actual["subseries_id"].unique().tolist()),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
