"""Shared library for Ch7 validators.

Each validator re-reads the source xlsx and compares against the processed parquet
on the (year, industry) keys. PASS if max_pct_err < tolerance.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# Make sibling packages importable when loaded by run.py
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


def validate_against_panel(
    sid: str,
    processed_parquet: Path,
    chopped_xlsx: Path,
    tolerance_pct: float,
    is_deviation: bool = False,
    salter_table: bool = False,
) -> dict:
    """Compare processed parquet to xlsx by (year, industry) key.

    is_deviation: read *_Deviation/*_Dev columns instead of level columns
    salter_table: special handling for Salter cross-section tables
    """
    if not processed_parquet.exists():
        row = {"status": "FAIL", "error": f"processed missing: {processed_parquet}",
               "validated_at": datetime.now(timezone.utc).isoformat()}
        update_report(sid, row)
        return row
    if not chopped_xlsx.exists():
        row = {"status": "FAIL", "error": f"chopped table missing: {chopped_xlsx}",
               "validated_at": datetime.now(timezone.utc).isoformat()}
        update_report(sid, row)
        return row

    actual = pd.read_parquet(processed_parquet)
    if salter_table:
        return _validate_salter(sid, actual, chopped_xlsx, tolerance_pct)

    truth = pd.read_excel(chopped_xlsx, header=1)
    truth.columns = [str(c).strip() for c in truth.columns]
    truth = truth.dropna(subset=["Year"])
    truth["Year"] = pd.to_numeric(truth["Year"], errors="coerce")
    truth = truth.dropna(subset=["Year"]).astype({"Year": int})

    # Build (year, industry) -> expected
    from L01_loaders._ch7_xlsx_panels import _is_dev_col, _strip_dev_suffix, _is_aggregate  # noqa: E402

    rows = []
    for col in truth.columns:
        if col == "Year":
            continue
        if is_deviation:
            if not _is_dev_col(col):
                continue
            base = _strip_dev_suffix(col)
            if _is_aggregate(col):
                continue
        else:
            if _is_dev_col(col):
                continue
            base = col
        for _, r in truth.iterrows():
            val = pd.to_numeric(r[col], errors="coerce")
            if pd.isna(val):
                continue
            rows.append({"year": int(r["Year"]), "industry": base, "expected": float(val)})
    truth_long = pd.DataFrame(rows)

    merged = actual.merge(truth_long, on=["year", "industry"], how="inner")
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    # Avoid divide-by-zero for cells that equal zero exactly
    safe_denom = merged["expected"].abs().replace(0, pd.NA)
    merged["pct_err"] = (merged["abs_err"] / safe_denom * 100.0).fillna(0.0)

    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max()) if n else float("nan")
    divergence = merged[merged["pct_err"] > tolerance_pct]
    div_keys = [(int(r["year"]), str(r["industry"])) for _, r in divergence.iterrows()]
    status = "PASS" if len(div_keys) == 0 else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": tolerance_pct,
        "n_compared": n,
        "mae": round(mae, 8),
        "max_abs_err": round(max_abs, 8),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(div_keys),
        "divergence_keys": div_keys[:20],
        "is_deviation_panel": is_deviation,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    update_report(sid, row)
    return row


def _validate_salter(sid: str, actual: pd.DataFrame, chopped_xlsx: Path, tolerance_pct: float) -> dict:
    """Salter cross-section: compare (industry, axis) keys."""
    truth = pd.read_excel(chopped_xlsx, header=1)
    truth.columns = [str(c).strip() for c in truth.columns]
    # First col may be 'Industry' or descriptive — normalize
    first_col = truth.columns[0]
    truth = truth.rename(columns={first_col: "Industry"})
    truth["Industry"] = truth["Industry"].astype(str).str.strip()
    truth = truth[truth["Industry"].str.match(r"^\s*\d+", na=False)].reset_index(drop=True)

    rows = []
    for _, r in truth.iterrows():
        ind = str(r["Industry"]).strip()
        # 'Unit labour cost' axis
        ulc = pd.to_numeric(r.get("Unit labour cost"), errors="coerce")
        if pd.notna(ulc):
            rows.append({"industry": ind, "axis": "unit_labour_cost", "expected": float(ulc)})
        # 'Whole sale price' (S701) or 'Net price' (S702)
        for price_col in ("Whole sale price", "Net price"):
            if price_col in truth.columns:
                p = pd.to_numeric(r.get(price_col), errors="coerce")
                if pd.notna(p):
                    rows.append({"industry": ind, "axis": "selling_price", "expected": float(p)})
                break

    truth_long = pd.DataFrame(rows)
    merged = actual.merge(truth_long, on=["industry", "axis"], how="inner")
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    safe_denom = merged["expected"].abs().replace(0, pd.NA)
    merged["pct_err"] = (merged["abs_err"] / safe_denom * 100.0).fillna(0.0)

    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max()) if n else float("nan")
    divergence = merged[merged["pct_err"] > tolerance_pct]
    div_keys = [(str(r["industry"]), str(r["axis"])) for _, r in divergence.iterrows()]
    status = "PASS" if len(div_keys) == 0 else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": tolerance_pct,
        "n_compared": n,
        "mae": round(mae, 8),
        "max_abs_err": round(max_abs, 8),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(div_keys),
        "divergence_keys": div_keys[:20],
        "content_type": "cross_sectional",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    update_report(sid, row)
    return row


def pass_data_unavailable(sid: str, reason: str) -> dict:
    row = {
        "status": "PASS_DATA_UNAVAILABLE",
        "reason": reason,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    update_report(sid, row)
    return row
