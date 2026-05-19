"""V03_S1506_validate - verify S1506 is an exact slice of S1505 (1948-1981)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402

CHILD = DATA_PROCESSED / "S1506.parquet"
PARENT = DATA_PROCESSED / "S1505.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 1.0
WINDOW = (1948, 1981)
SERIES_ID = "S1506"


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[SERIES_ID] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not CHILD.exists() or not PARENT.exists():
        return {"status": "FAIL", "error": "missing processed parquet (child or parent)"}
    child = pd.read_parquet(CHILD)
    parent = pd.read_parquet(PARENT)
    # Map child subseries to parent subseries
    child = child.copy()
    child["parent_sub"] = child["subseries_id"].str.replace("S1506-", "S1505-", regex=False)
    parent_sub = parent.rename(columns={"value": "expected"})
    merged = child.merge(parent_sub, left_on=["year", "parent_sub"],
                         right_on=["year", "subseries_id"], suffixes=("", "_p"))
    merged = merged[(merged["year"] >= WINDOW[0]) & (merged["year"] <= WINDOW[1])]
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    merged["pct_err"] = merged["abs_err"] / merged["expected"].abs().clip(lower=1e-9) * 100.0
    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max()) if n else float("nan")
    bad = merged[(merged["abs_err"] > 1e-10) & (merged["pct_err"] > VALIDATOR_TOL_PCT)]
    status = "PASS" if bad.empty else "FAIL"
    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": list(WINDOW),
        "n_compared": n,
        "mae": round(mae, 12),
        "max_abs_err": round(max_abs, 12),
        "max_pct_err": round(max_pct, 8),
        "divergence_count": int(len(bad)),
        "parent_series": "S1505",
        "construction": "derived_subperiod",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
