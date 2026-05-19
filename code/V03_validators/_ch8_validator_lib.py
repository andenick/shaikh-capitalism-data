"""Shared library for Ch8 validators.

Provides:
  - update_report(sid, row): write/refresh VALIDATION_REPORT.json row
  - pass_data_unavailable(sid, reason): canonical S801 helper
  - validate_long_form(sid, processed, truth_long, tolerance_pct, join_keys, content_type)
        generic compare-by-key validator used by S802/S803/S804/S805
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402

REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"


def update_report(sid: str, row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[sid] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def pass_data_unavailable(sid: str, reason: str) -> dict:
    row = {
        "status": "PASS_DATA_UNAVAILABLE",
        "reason": reason,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    update_report(sid, row)
    return row


def validate_long_form(
    sid: str,
    processed_parquet: Path,
    truth_long: pd.DataFrame,
    tolerance_pct: float,
    join_keys: list[str],
    content_type: str = "cross_sectional",
) -> dict:
    """Compare processed parquet to a long-form truth DataFrame on join_keys.

    truth_long must contain `expected` column plus all join_keys.
    processed parquet must contain `value` column plus all join_keys.
    """
    if not processed_parquet.exists():
        row = {"status": "FAIL", "error": f"processed missing: {processed_parquet}",
               "validated_at": datetime.now(timezone.utc).isoformat()}
        update_report(sid, row)
        return row

    actual = pd.read_parquet(processed_parquet)
    missing = [k for k in join_keys if k not in actual.columns]
    if missing:
        row = {"status": "FAIL", "error": f"join keys missing in processed: {missing}",
               "validated_at": datetime.now(timezone.utc).isoformat()}
        update_report(sid, row)
        return row

    merged = actual.merge(truth_long, on=join_keys, how="inner")
    if len(merged) == 0:
        row = {"status": "FAIL", "error": "no rows matched on join_keys",
               "join_keys": join_keys,
               "validated_at": datetime.now(timezone.utc).isoformat()}
        update_report(sid, row)
        return row

    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    safe_denom = merged["expected"].abs().replace(0, pd.NA)
    merged["pct_err"] = (merged["abs_err"] / safe_denom * 100.0).fillna(0.0)

    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max()) if n else float("nan")
    bad = merged[(merged["abs_err"] > 1e-6) & (merged["pct_err"] > tolerance_pct)]
    status = "PASS" if bad.empty else "FAIL"

    div_keys = [
        {k: (int(r[k]) if isinstance(r[k], (int, float)) and not isinstance(r[k], bool) else str(r[k]))
         for k in join_keys}
        for _, r in bad.iterrows()
    ]

    row = {
        "status": status,
        "tolerance_pct": tolerance_pct,
        "content_type": content_type,
        "n_compared": n,
        "mae": round(mae, 10),
        "max_abs_err": round(max_abs, 10),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": int(len(bad)),
        "divergence_keys": div_keys[:20],
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    update_report(sid, row)
    return row
