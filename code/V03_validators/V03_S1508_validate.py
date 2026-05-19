"""V03_S1508_validate - validate S1508 cell-by-cell against the Harberger chopped table."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

PROCESSED = DATA_PROCESSED / "S1508.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix15_WorldInflationDataLambda.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 0.5
SERIES_ID = "S1508"


def _truth() -> pd.DataFrame:
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="HarbergerTable12", header=1)
    raw = raw.dropna(how="all").reset_index(drop=True)
    rows = []
    for i, r in raw.iterrows():
        country_key = f"H{i+1:02d}"
        rows.append({"country_key": country_key, "subseries_id": "S1508-lambda",
                     "expected": float(r.iloc[0])})
        rows.append({"country_key": country_key, "subseries_id": "S1508-pi",
                     "expected": float(r.iloc[1])})
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
    truth = _truth()
    merged = actual.merge(truth, on=["country_key", "subseries_id"], how="inner")
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    merged["pct_err"] = merged["abs_err"] / merged["expected"].abs().clip(lower=1e-9) * 100.0
    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max()) if n else float("nan")
    bad = merged[(merged["abs_err"] > 1e-6) & (merged["pct_err"] > VALIDATOR_TOL_PCT)]
    status = "PASS" if bad.empty else "FAIL"
    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "n_compared": n,
        "n_countries": int(merged["country_key"].nunique()),
        "mae": round(mae, 10),
        "max_abs_err": round(max_abs, 10),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": int(len(bad)),
        "content_type": "cross_sectional",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
