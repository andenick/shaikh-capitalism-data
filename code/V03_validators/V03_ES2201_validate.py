"""V03_ES2201_validate — verify ES2201 matches reconstructed Table 1."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "ES2201"
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
CSV_PATH = SALVAGED_BOOK_DATA / "Reconstructed" / "ES2201_fitted_parameters.csv"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 0.5
PARAMS = ["G_prime", "r_mean", "w_mean", "f_top3", "alpha"]


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
        return {"status": "FAIL", "error": f"truth missing: {CSV_PATH}"}

    actual = pd.read_parquet(PROCESSED)
    truth = pd.read_csv(CSV_PATH)

    abs_errs: list[float] = []
    pct_errs: list[float] = []
    divergences: list[dict] = []
    n = 0
    for _, t in truth.iterrows():
        year = int(t["year"])
        for param in PARAMS:
            expected = float(t[param])
            sub_id = f"{SERIES_ID}-{param}"
            m = actual[(actual["year"] == year) & (actual["subseries_id"] == sub_id)]
            if m.empty:
                divergences.append({"year": year, "subseries": sub_id, "issue": "missing"})
                continue
            v = float(m["value"].iloc[0])
            abs_err = abs(v - expected)
            denom = abs(expected) if abs(expected) > 1e-12 else 1.0
            pct = abs_err / denom * 100.0
            abs_errs.append(abs_err)
            pct_errs.append(pct)
            n += 1
            if pct > VALIDATOR_TOL_PCT:
                divergences.append({"year": year, "subseries": sub_id, "value": v,
                                    "expected": expected, "pct_err": round(pct, 6)})

    mae = float(sum(abs_errs) / len(abs_errs)) if abs_errs else 0.0
    max_abs = float(max(abs_errs)) if abs_errs else 0.0
    max_pct = float(max(pct_errs)) if pct_errs else 0.0
    status = "PASS" if not divergences else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "time_series",
        "comparison_basis": "Reconstructed ES2201_fitted_parameters.csv (verbatim Shaikh-Jacobo 2020 Table 1)",
        "n_compared": n,
        "mae": round(mae, 6),
        "max_abs_err": round(max_abs, 6),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(divergences),
        "divergences": divergences[:10],
        "extension_status": "v1_1_deferred_mle_refit_2017_2022",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
