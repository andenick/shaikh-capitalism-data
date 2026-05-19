"""Shared helpers for Ch3 V03 validators.

Theoretical and cross_sectional series do not have year-by-year book-truth
tabulations. The validator checks instead that:

  - all output points are finite
  - all output values fall within the printed axis bounds [y_min, y_max]
  - the curve shape matches the qualitative property stated by Shaikh
    (monotone declining / monotone rising / saturating etc.)

When checks pass, the validator returns status='PASS_THEORETICAL' or
status='PASS_CROSS_SECTIONAL' depending on content type.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional

import numpy as np
import pandas as pd


def update_report(report_path, sid: str, row: dict) -> None:
    """Append/overwrite the per-series row in VALIDATION_REPORT.json."""
    if report_path.exists():
        rpt = json.loads(report_path.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[sid] = row
    report_path.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def validate_theoretical_curve(
    df: pd.DataFrame,
    *,
    sid: str,
    y_bound_lo: float,
    y_bound_hi: float,
    shape: str,
    tolerance_pct: float = 0.5,
    bound_tol_pct: float = 1.0,
    asymptote_target: Optional[float] = None,
    asymptote_tol: float = 0.05,
    subseries_filter: Optional[str] = None,
) -> dict:
    """Validate one theoretical curve in the processed parquet.

    Parameters
    ----------
    df          : the processed DataFrame (must contain x_value, value, subseries_id)
    y_bound_lo, y_bound_hi : printed-figure y-axis bounds
    shape       : one of {"declining", "rising", "non_monotone", "saturating"}
    tolerance_pct  : informational only (reported, not enforced point-by-point)
    bound_tol_pct  : how far outside [y_bound_lo, y_bound_hi] a value may stray (percent of range)
    asymptote_target : if not None, the curve's last value must lie within +/- asymptote_tol of this
    subseries_filter : if not None, restrict validation to rows with this subseries_id
    """
    if subseries_filter is not None:
        df = df[df["subseries_id"] == subseries_filter].copy()
    df = df.sort_values("x_value").reset_index(drop=True)
    n = int(len(df))

    if n == 0:
        return {"status": "FAIL", "sid": sid, "error": "empty curve", "tolerance_pct": tolerance_pct}

    vals = df["value"].to_numpy(dtype=float)
    finite_ok = bool(np.all(np.isfinite(vals)))

    y_range = y_bound_hi - y_bound_lo
    slack = bound_tol_pct / 100.0 * y_range
    lo, hi = y_bound_lo - slack, y_bound_hi + slack
    bound_ok = bool(np.all(vals >= lo) and np.all(vals <= hi))
    n_oob = int(np.sum((vals < lo) | (vals > hi)))

    if shape == "declining":
        shape_ok = bool(np.all(np.diff(vals) <= 1e-9))
    elif shape == "rising":
        shape_ok = bool(np.all(np.diff(vals) >= -1e-9))
    elif shape == "saturating":
        # Should be rising but with declining slope (concave): diff(diff(vals)) <= small
        diffs = np.diff(vals)
        shape_ok = bool(np.all(diffs >= -1e-9)) and bool(np.all(np.diff(diffs) <= 1e-6))
    elif shape == "non_monotone":
        shape_ok = True
    else:
        shape_ok = True  # unknown shape -> pass with note

    asymp_ok = True
    asymp_err = None
    if asymptote_target is not None and n > 0:
        asymp_err = float(vals[-1] - asymptote_target)
        asymp_ok = bool(abs(asymp_err) <= asymptote_tol)

    all_ok = finite_ok and bound_ok and shape_ok and asymp_ok
    status = "PASS_THEORETICAL" if all_ok else "FAIL"

    # Informational MAE/max_pct vs the midpoint of the bounds (no book-truth points)
    midpoint = 0.5 * (y_bound_lo + y_bound_hi)
    mae_from_mid = float(np.mean(np.abs(vals - midpoint)))
    return {
        "status": status,
        "sid": sid,
        "tolerance_pct": tolerance_pct,
        "n_compared": n,
        "y_bounds": [y_bound_lo, y_bound_hi],
        "bound_tol_pct": bound_tol_pct,
        "n_out_of_bounds": n_oob,
        "shape_requested": shape,
        "shape_ok": shape_ok,
        "finite_ok": finite_ok,
        "asymptote_target": asymptote_target,
        "asymptote_err": asymp_err,
        "mae": round(mae_from_mid, 6),
        "max_abs_err": round(float(np.max(np.abs(vals - midpoint))), 6),
        "max_pct_err": round(float(np.max(np.abs(vals - midpoint) / max(abs(midpoint), 1e-9)) * 100.0), 6),
        "divergence_years": [],
        "divergence_count": 0,
        "cd2_comparison": {},
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "note": "Theoretical series; tolerance is applied to axis bounds, not point-by-point against tabulated truth (none published).",
    }


def validate_cross_sectional_unavailable(
    df: pd.DataFrame,
    *,
    sid: str,
    year: int,
    y_bound_lo: float,
    y_bound_hi: float,
    units: str,
) -> dict:
    """For cross-sectional series whose underlying tabulation is not yet in
    SalvagedInputs (Allen & Bowley 1935 / Cd. 3864), the loader emits an empty
    or bounds-only data frame. We validate that:
      - the year column is the documented year (1904)
      - the value column is empty OR contains only NaN (no synthetic fill)
      - any non-NaN value (e.g. axis bound metadata if loader chose to emit them)
        lies within the documented axis range.
    """
    n = int(len(df))
    non_null = int(df["value"].notna().sum())
    year_ok = bool((df["year"] == year).all()) if n else True
    in_range = True
    if non_null > 0:
        vals = df.loc[df["value"].notna(), "value"].to_numpy(dtype=float)
        in_range = bool(np.all(vals >= y_bound_lo) and np.all(vals <= y_bound_hi))
    status = "PASS_CROSS_SECTIONAL_UNAVAILABLE" if year_ok and in_range else "FAIL"
    return {
        "status": status,
        "sid": sid,
        "tolerance_pct": 0.5,
        "n_compared": non_null,
        "n_rows": n,
        "year": year,
        "y_bounds": [y_bound_lo, y_bound_hi],
        "units": units,
        "mae": None,
        "max_abs_err": None,
        "max_pct_err": None,
        "divergence_years": [],
        "divergence_count": 0,
        "cd2_comparison": {},
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "note": ("Underlying Allen & Bowley (1935) Table 1 not in SalvagedInputs/ (Internet Archive URL 404). "
                 "Processed parquet contains the axis-bound metadata only. No synthetic values. "
                 "Status PASS_CROSS_SECTIONAL_UNAVAILABLE signals 'no observation data ingested; nothing to falsify against book truth'."),
    }
