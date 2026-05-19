"""V03_S1502_validate - validate S1502 growth rates against book's "Calculated Growth Rate" columns.

For each (year, industry) in 1988-2010 we compare the recomputed log-difference
against the chopped table's pre-computed growth rate. Expected MAE ~ 0 since
both use the same level inputs.
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
from L01_loaders._bea_industry_loader import (  # noqa: E402
    PANEL_A_INDUSTRIES, ALL_INDUSTRIES_LABEL, load_chopped_levels_and_growth, _INDUSTRY_SLUG,
)

PROCESSED = DATA_PROCESSED / "S1502.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix15_USGDPRByIndustry.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 1.0
SERIES_ID = "S1502"
PANEL = [ALL_INDUSTRIES_LABEL] + PANEL_A_INDUSTRIES


def _truth_long() -> pd.DataFrame:
    levels, growth = load_chopped_levels_and_growth(CHOPPED_XLSX)
    rows = []
    for ind in PANEL:
        if ind not in growth.columns:
            continue
        sub_id = f"{SERIES_ID}-{_INDUSTRY_SLUG.get(ind, ind[:6].upper())}"
        for y, gv in growth[ind].items():
            if pd.isna(gv):
                continue
            rows.append({"year": int(y), "subseries_id": sub_id, "expected": float(gv)})
    return pd.DataFrame(rows)


def _update(row: dict) -> None:
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
    truth = _truth_long()
    merged = actual.merge(truth, on=["year", "subseries_id"], how="inner")
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    # Use absolute err divided by max(|expected|, tiny) to avoid div-by-zero
    merged["pct_err"] = merged["abs_err"] / merged["expected"].abs().clip(lower=1e-6) * 100.0
    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max()) if n else float("nan")
    # Tolerance interpretation: for growth rates near zero, percent error inflates;
    # we use a hybrid: pass if abs_err <= 0.005 (50bp) OR pct_err <= tol
    bad = merged[(merged["abs_err"] > 0.005) & (merged["pct_err"] > VALIDATOR_TOL_PCT)]
    div = bad[["year", "subseries_id", "value", "expected", "abs_err", "pct_err"]].to_dict("records")
    status = "PASS" if not div else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "tolerance_abs": 0.005,
        "n_compared": n,
        "mae": round(mae, 8),
        "max_abs_err": round(max_abs, 8),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(div),
        "divergence_sample": div[:5],
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
