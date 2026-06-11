"""V03_S401_validate — compare processed S401 against the reconstructed
Appendix 4.2 Table 4 (per-worker cost columns).

Since the loader/processor pass through the CSV directly, this validator
verifies pipeline integrity: every non-null value in the processed parquet
matches the CSV cell to within VALIDATOR_TOL_PCT = 0.5% (chapter playbook
standard for `derived`).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "S401"
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
CSV_PATH = SALVAGED_BOOK_DATA / "Reconstructed" / "Appendix_4_2_Table4.csv"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 0.5
COMPONENTS = ["afc", "ulc_prime", "avc_prime", "ac_prime", "tc_prime", "mc_prime"]


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
    if not CSV_PATH.exists():
        return {"status": "FAIL", "error": f"book truth missing: {CSV_PATH}"}

    actual = pd.read_parquet(PROCESSED)
    truth = pd.read_csv(CSV_PATH).reset_index(drop=True)

    abs_errs: list[float] = []
    pct_errs: list[float] = []
    divergences: list[dict] = []
    n_compared = 0

    for row_idx, truth_row in truth.iterrows():
        for comp in COMPONENTS:
            expected = truth_row[comp]
            if pd.isna(expected):
                continue
            sub_id = f"{SERIES_ID}-{comp}"
            match = actual[(actual["year"] == row_idx) & (actual["subseries_id"] == sub_id)]
            if match.empty:
                divergences.append({"row_index": int(row_idx), "component": comp,
                                    "issue": "missing row in processed"})
                continue
            v = match["value"].iloc[0]
            if pd.isna(v):
                divergences.append({"row_index": int(row_idx), "component": comp,
                                    "issue": "processed value is null but truth is not"})
                continue
            abs_err = abs(float(v) - float(expected))
            denom = abs(float(expected)) if abs(float(expected)) > 1e-12 else 1.0
            pct_err = abs_err / denom * 100.0
            abs_errs.append(abs_err)
            pct_errs.append(pct_err)
            n_compared += 1
            if pct_err > VALIDATOR_TOL_PCT:
                divergences.append({
                    "row_index": int(row_idx), "component": comp,
                    "value": float(v), "expected": float(expected),
                    "pct_err": round(pct_err, 6),
                })

    mae = float(sum(abs_errs) / len(abs_errs)) if abs_errs else 0.0
    max_abs = float(max(abs_errs)) if abs_errs else 0.0
    max_pct = float(max(pct_errs)) if pct_errs else 0.0
    status = "PASS" if not divergences else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "derived",
        "comparison_basis": "Reconstructed Appendix_4_2_Table4.csv (verbatim from book pp. 779-780)",
        "n_compared": n_compared,
        "mae": round(mae, 6),
        "max_abs_err": round(max_abs, 6),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(divergences),
        "divergences": divergences[:10],
        "cd2_comparison": {"note": "no CD/CD2 predecessor for Ch4 series"},
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
