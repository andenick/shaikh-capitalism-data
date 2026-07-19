"""Independent-anchor + structural-guard validator library (Decision 0011 / T4.1 / SI-4).

Style-matched to ``_ch14_validator_lib.py``. This library implements the machinery
that breaks the project's *tautological-V03* pattern: the legacy V03 scripts re-read
the same book workbook the L01 loader read, clipped to book years, so MAE≈0 proves
melt-fidelity only and is structurally blind to wrong-source and corrupt-source bugs.

Three independent check types are provided, each driven by new ``validation`` blocks in
``series_registry.json`` and each operating on the *processed* long-form parquet
(columns: ``year, value, subseries_id, source_id, units``):

1. ``check_independent_anchor``   — asserts book-published anchor values that are
   independent of the round-trip (Decision 0011's six authoritative anchors).
2. ``check_splice_continuity``    — flags a book->extension level break at the splice year.
3. ``check_level_plausibility``   — asserts MHR §5/§6 economic-sanity rules (monotonic/sign/range).

A suite runner (``run_anchor_suite``) runs all three across every series that carries
anchors, plausibility rules, or a book->extension splice, and writes
``Technical/remediation_campaign/ANCHOR_SUITE_REPORT.json``.

This library is NOT auto-discovered by ``run.py`` (leading underscore) and does NOT
modify run.py's per-series flow. Individual ``V03_<sid>.py`` files (a later wave) import
these functions; for now the suite is runnable standalone::

    python code/V03_validators/_v03_anchor_lib.py --run
    python code/run_anchor_suite.py

--------------------------------------------------------------------------------
REGISTRY SCHEMA (authored by B1 per Decision 0011)
--------------------------------------------------------------------------------

``series[<sid>].validation.independent_anchors``  (list[dict]) — each entry::

    {
      "anchor_id":          str,     # unique, e.g. "S903_T918_1998"
      "anchor_type":        "point" | "derived_statistic",
      "source_description": str,     # human: book table/page + what the value is
      "source_file":        str,     # SalvagedInputs path (or printed-book reference)
      "source_sheet":       str,     # optional — workbook sheet
      "source_cell":        str,     # optional — cell / row-col / quote locator
      "subseries_id":       str,     # subseries the anchor asserts against
      "tolerance_pct":      float,   # optional, default 1.0 (registry 1% canon)

      # anchor_type == "point" (time-series selection):
      "year":               int,
      "expected_value":     float,   # in the SAME numeric scale as parquet `value`
      # anchor_type == "point" (cross-sectional selection — e.g. country panels):
      "key_column":         str,     # optional, e.g. "country_key"; selects by row key not year
      "key_value":          str,     # optional, the value of key_column to select

      # anchor_type == "derived_statistic":
      "statistic":          "mean" | "std" | "cov" | "count" | "ols_a" | "ols_c" | "r2" | "ratio",
      "expected_value":     float,
      "spec": {
        "from_year":  int,           # optional (None = full span)
        "to_year":    int,           # optional
        # for ratio (P2.1 extension, 2026-07-10 — book fold-increase claims):
        "num_year":   int,           # value[num_year] / value[den_year] of anchor subseries_id
        "den_year":   int,
        # for ols_a / ols_c / r2 only:
        "y_subseries": str,          # dependent variable subseries
        "x_subseries": str,          # independent variable subseries
        "transform":   str,          # "none" | "log_y" | "log_x" | "log_both"
        "model":       str,          # "linear" (default, np.polyfit) | "power_b1" | "quadratic"
                                     #   power_b1 fits Shaikh's constrained Phillips form
                                     #   y = a + x^c (b=1) by NLLS (scipy.curve_fit); a->ols_a, c->ols_c
                                     #   quadratic (P2.1) fits y = a + c*x + q*x^2; a->ols_a, c->ols_c
        # P2.1 cross-sectional extensions (optional):
        "join_on":     str,          # join y/x on this column instead of year (e.g. "industry")
        "y_filter":    dict,         # row filter for y, e.g. {"axis": "ROE"} (long layouts where
        "x_filter":    dict          #   y and x share a subseries_id, split by an axis column)
      }
    }

``series[<sid>].validation.plausibility_rules``  (list[dict]) — each entry::

    {
      "rule_id":   str,
      "rule_type": "strictly_falling" | "strictly_rising" | "range" | "sign",
      "subseries": str,
      "from_year": int,     # optional (defaults to full span)
      "to_year":   int,     # optional
      # rule_type == "range":
      "min": float, "max": float,
      # rule_type == "sign":
      "sign": "positive" | "negative" | "nonnegative" | "nonpositive",
      "grounding": str      # REQUIRED: MHR §5/§6 or review-report citation of the economic fact
    }

Splice continuity is driven by the series' ``extension`` block (``splice_year``) when
present, otherwise inferred from ``year_range_book`` / ``year_range_extension``.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, REGISTRY  # noqa: E402

# ---------------------------------------------------------------------------
# Status vocabulary
# ---------------------------------------------------------------------------
GREEN = "GREEN"   # check ran and passed
RED = "RED"       # check ran and a genuine defect was detected
NA = "NA"         # check not applicable / insufficient data to assert

DEFAULT_TOL_PCT = 1.0                 # registry 1% canonical tolerance (Decision 0011)
SPLICE_FLOOR_PCT = 5.0                # absolute floor for the splice threshold
SPLICE_SIGMA_MULT = 3.0               # multiplier on trailing within-book sigma
SPLICE_TRAILING_N = 5                 # number of trailing within-book yoy changes

REPORT_PATH = paths.TECHNICAL / "remediation_campaign" / "ANCHOR_SUITE_REPORT.json"


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def _load_registry(registry_path: Path | str = REGISTRY) -> dict:
    with Path(registry_path).open(encoding="utf-8") as fh:
        return json.load(fh)


def _entry(registry: dict, sid: str) -> dict:
    return (registry.get("series") or {}).get(sid, {}) or {}


def _validation(registry: dict, sid: str) -> dict:
    return _entry(registry, sid).get("validation") or {}


def _load_processed(sid: str, processed_dir: Path | str = DATA_PROCESSED) -> pd.DataFrame | None:
    p = Path(processed_dir) / f"{sid}.parquet"
    if not p.exists():
        return None
    df = pd.read_parquet(p)
    if "year" in df.columns:
        df = df.copy()
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


def _subseries_series(df: pd.DataFrame, subseries_id: str,
                      from_year: int | None = None,
                      to_year: int | None = None) -> pd.Series:
    """Return a year-indexed value Series for one subseries, sorted by year."""
    sub = df[df["subseries_id"] == subseries_id][["year", "value"]].dropna()
    if from_year is not None:
        sub = sub[sub["year"] >= from_year]
    if to_year is not None:
        sub = sub[sub["year"] <= to_year]
    sub = sub.sort_values("year")
    return pd.Series(sub["value"].values, index=sub["year"].astype(int).values)


def _pct_diff(actual: float, expected: float) -> float:
    if expected == 0:
        return float("inf") if actual != 0 else 0.0
    return abs(actual - expected) / abs(expected) * 100.0


# ---------------------------------------------------------------------------
# 1. Independent anchors
# ---------------------------------------------------------------------------
def _select_point_value(df: pd.DataFrame, anchor: dict) -> tuple[float | None, str]:
    """Select the single processed value a point anchor asserts.

    Time-series anchors select by (subseries_id, year). Cross-sectional anchors
    (e.g. Harberger country panels) select by (subseries_id, key_column==key_value),
    optionally further narrowed by year.
    """
    sub = anchor["subseries_id"]
    rows = df[df["subseries_id"] == sub]
    key_col = anchor.get("key_column")
    if key_col:
        if key_col not in rows.columns:
            return None, f"key_column '{key_col}' absent from processed data"
        rows = rows[rows[key_col].astype(str) == str(anchor.get("key_value"))]
        if "year" in anchor and "year" in rows.columns:
            rows = rows[rows["year"] == int(anchor["year"])]
        vals = pd.to_numeric(rows["value"], errors="coerce").dropna().unique().tolist()
        if not vals:
            return None, f"no row for {sub} where {key_col}={anchor.get('key_value')}"
        if len(vals) > 1:
            return None, f"ambiguous: {len(vals)} distinct values for {sub}/{key_col}={anchor.get('key_value')}"
        return float(vals[0]), f"{key_col}={anchor.get('key_value')}"
    # time-series selection by year
    s = _subseries_series(df, sub)
    year = int(anchor["year"])
    if year not in s.index:
        return None, f"no processed value for {sub} @ {year}"
    return float(s.loc[year]), f"year={year}"


def _eval_point_anchor(df: pd.DataFrame, anchor: dict) -> dict:
    expected = float(anchor["expected_value"])
    tol = float(anchor.get("tolerance_pct", DEFAULT_TOL_PCT))
    actual, detail = _select_point_value(df, anchor)
    if actual is None:
        # P2.1 hardening (2026-07-10, closes the S903-exemption note): an anchor is
        # an ASSERTION that a book-printed value exists in the pipeline output. If
        # the anchored row cannot be selected at all, the assertion FAILS (RED) —
        # NA here previously let year-shift corruption pass point anchors silently.
        return {"status": RED, "detail": f"anchor not evaluable: {detail}",
                "expected": expected, "actual": None, "tolerance_pct": tol}
    pd_ = _pct_diff(actual, expected)
    return {"status": RED if pd_ > tol else GREEN,
            "expected": expected, "actual": actual, "detail": detail,
            "abs_pct_diff": round(pd_, 6), "tolerance_pct": tol}


def _filtered_pairs(df: pd.DataFrame, subseries_id: str, row_filter: dict | None,
                    join_col: str, fy: int | None, ty: int | None) -> pd.Series:
    """Return a join_col-indexed value Series for one subseries, optionally
    row-filtered (e.g. {"axis": "ROE"} in a long cross-sectional layout).

    P2.1 extension (2026-07-10): generalizes _subseries_series so regressions can
    join y/x on a non-year key (e.g. `industry`, `industry_index`) and select rows
    by an auxiliary column. join_col="year" + no filter reproduces legacy behavior.
    """
    sub = df[df["subseries_id"] == subseries_id]
    if row_filter:
        for col, val in row_filter.items():
            if col not in sub.columns:
                return pd.Series(dtype=float)
            sub = sub[sub[col].astype(str) == str(val)]
    if "year" in sub.columns:
        if fy is not None:
            sub = sub[sub["year"] >= fy]
        if ty is not None:
            sub = sub[sub["year"] <= ty]
    if join_col not in sub.columns:
        return pd.Series(dtype=float)
    sub = sub[[join_col, "value"]].dropna().sort_values(join_col)
    return pd.Series(sub["value"].values, index=sub[join_col].values)


def _compute_statistic(df: pd.DataFrame, anchor: dict) -> tuple[float | None, str]:
    stat = anchor["statistic"]
    spec = anchor.get("spec") or {}
    fy, ty = spec.get("from_year"), spec.get("to_year")

    if stat in ("mean", "std", "cov", "count"):
        s = _subseries_series(df, anchor["subseries_id"], fy, ty).dropna()
        if stat == "count":
            return float(len(s)), f"n={len(s)}"
        if len(s) == 0:
            return None, "no data in window"
        if stat == "mean":
            return float(s.mean()), f"n={len(s)}"
        if stat == "std":
            return float(s.std(ddof=1)), f"n={len(s)}"
        if stat == "cov":
            m = float(s.mean())
            return (float(s.std(ddof=1) / m) if m else float("inf")), f"n={len(s)}"

    if stat == "ratio":
        # P2.1 extension (2026-07-10): book-printed fold-increase claims
        # ("rose fifty-eight-fold"): value[num_year] / value[den_year].
        s = _subseries_series(df, anchor["subseries_id"]).dropna()
        ny, dy = int(spec["num_year"]), int(spec["den_year"])
        if ny not in s.index or dy not in s.index:
            return None, f"missing year for ratio ({ny} or {dy})"
        den = float(s.loc[dy])
        if den == 0:
            return None, f"zero denominator @ {dy}"
        return float(s.loc[ny]) / den, f"{ny}/{dy}"

    if stat in ("ols_a", "ols_c", "r2"):
        join_col = spec.get("join_on", "year")
        y_filter = spec.get("y_filter")
        x_filter = spec.get("x_filter")
        if join_col != "year" or y_filter or x_filter:
            # P2.1 extension: cross-sectional join (e.g. industry scatter) and/or
            # row-filtered y/x drawn from the same subseries via an axis column.
            ys = _filtered_pairs(df, spec["y_subseries"], y_filter, join_col, fy, ty)
            xs = _filtered_pairs(df, spec["x_subseries"], x_filter, join_col, fy, ty)
        else:
            ys = _subseries_series(df, spec["y_subseries"], fy, ty)
            xs = _subseries_series(df, spec["x_subseries"], fy, ty)
        joined = pd.DataFrame({"y": ys, "x": xs}).dropna()
        transform = spec.get("transform_ops", spec.get("transform", "none"))
        if transform in ("log_y", "log_both"):
            joined = joined[joined["y"] > 0]
            joined["y"] = np.log(joined["y"])
        if transform in ("log_x", "log_both"):
            joined = joined[joined["x"] > 0]
            joined["x"] = np.log(joined["x"])
        joined = joined.dropna()
        if len(joined) < 3:
            return None, f"insufficient paired obs (n={len(joined)})"
        x = joined["x"].to_numpy(dtype=float)
        y = joined["y"].to_numpy(dtype=float)

        model = spec.get("model", "linear")
        if model == "power_b1":
            # Shaikh's constrained Phillips form y = a + x^c (implicit b=1),
            # fit by nonlinear least squares (matches the book's EViews NLLS).
            from scipy.optimize import curve_fit  # lazy import — only S1405-style anchors need it
            def _f(xx, a_, c_):
                return a_ + np.power(xx, c_)
            p0 = spec.get("p0", [-1.0, -0.01])
            popt, _ = curve_fit(_f, x, y, p0=p0, maxfev=100000)
            a, c = float(popt[0]), float(popt[1])
            yhat = _f(x, a, c)
            model_tag = "power_b1(NLLS)"
        elif model == "quadratic":
            # P2.1 extension (2026-07-10): book-printed quadratic fits
            # (e.g. Fig 8.3 ROE = a + c*CR8 + q*CR8^2). ols_a -> intercept a,
            # ols_c -> linear coefficient c; r2 as usual.
            q, c, a = np.polyfit(x, y, 2)
            yhat = a + c * x + q * x * x
            model_tag = f"quadratic(OLS q={q:.6f})"
        else:
            c, a = np.polyfit(x, y, 1)        # slope (c), intercept (a)
            yhat = a + c * x
            model_tag = "linear(OLS)"

        ss_res = float(np.sum((y - yhat) ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot else float("nan")
        detail = f"{model_tag} n={len(joined)} a={a:.6f} c={c:.6f} r2={r2:.6f}"
        if stat == "ols_a":
            return float(a), detail
        if stat == "ols_c":
            return float(c), detail
        return float(r2), detail

    return None, f"unknown statistic '{stat}'"


def _eval_derived_anchor(df: pd.DataFrame, anchor: dict) -> dict:
    expected = float(anchor["expected_value"])
    tol = float(anchor.get("tolerance_pct", DEFAULT_TOL_PCT))
    actual, detail = _compute_statistic(df, anchor)
    if actual is None or (isinstance(actual, float) and not np.isfinite(actual)):
        # P2.1 hardening (2026-07-10): same assertion semantics as point anchors —
        # a derived-statistic anchor that cannot be computed (empty window, missing
        # ratio years, insufficient regression pairs) is a FAILED assertion (RED).
        return {"status": RED, "detail": f"anchor not evaluable: {detail}",
                "expected": expected, "actual": actual, "tolerance_pct": tol}
    pd_ = _pct_diff(actual, expected)
    return {"status": RED if pd_ > tol else GREEN,
            "expected": expected, "actual": round(actual, 8),
            "abs_pct_diff": round(pd_, 6), "tolerance_pct": tol, "detail": detail}


def check_independent_anchor(sid: str, df: pd.DataFrame, registry: dict) -> dict:
    """Assert registry ``validation.independent_anchors[]`` against processed data.

    Returns {status, sid, n_anchors, anchors:[{anchor_id, ...per-anchor result}]}.
    status = RED if any anchor RED; GREEN if >=1 anchor and all pass; NA if no anchors.
    """
    anchors = _validation(registry, sid).get("independent_anchors") or []
    if not anchors:
        return {"status": NA, "sid": sid, "n_anchors": 0, "anchors": [],
                "detail": "no independent_anchors registered"}
    if df is None:
        return {"status": NA, "sid": sid, "n_anchors": len(anchors), "anchors": [],
                "detail": "processed parquet missing"}

    results = []
    for a in anchors:
        atype = a.get("anchor_type", "point")
        res = (_eval_derived_anchor(df, a) if atype == "derived_statistic"
               else _eval_point_anchor(df, a))
        results.append({"anchor_id": a.get("anchor_id"), "anchor_type": atype,
                        "subseries_id": a.get("subseries_id"),
                        "source_description": a.get("source_description"), **res})

    reds = [r for r in results if r["status"] == RED]
    greens = [r for r in results if r["status"] == GREEN]
    status = RED if reds else (GREEN if greens else NA)
    return {"status": status, "sid": sid, "n_anchors": len(anchors),
            "n_red": len(reds), "n_green": len(greens),
            "n_na": len(results) - len(reds) - len(greens), "anchors": results}


# ---------------------------------------------------------------------------
# 2. Splice continuity
# ---------------------------------------------------------------------------
def _last_book_year(entry: dict) -> int | None:
    yrb = entry.get("year_range_book")
    if isinstance(yrb, (list, tuple)) and len(yrb) == 2 and yrb[1] is not None:
        try:
            return int(yrb[1])
        except (TypeError, ValueError):
            return None
    return None


def _splice_year(entry: dict) -> int | None:
    ext = entry.get("extension") or {}
    if isinstance(ext, dict) and ext.get("splice_year"):
        try:
            return int(ext["splice_year"])
        except (TypeError, ValueError):
            pass
    lby = _last_book_year(entry)
    if lby is not None and entry.get("year_range_extension"):
        return lby + 1
    return None


def _is_splice_eligible(entry: dict) -> bool:
    ext = entry.get("extension") or {}
    if isinstance(ext, dict) and ext.get("splice_year"):
        return True
    return bool(_last_book_year(entry) is not None and entry.get("year_range_extension"))


def _eval_subseries_splice(s: pd.Series, splice_year: int) -> dict | None:
    """Evaluate one subseries' splice break. Returns None if it doesn't span the splice."""
    last_book = splice_year - 1
    if last_book not in s.index or splice_year not in s.index:
        return None
    v0 = float(s.loc[last_book])
    v1 = float(s.loc[splice_year])
    jump_pct = _pct_diff(v1, v0) if v0 != 0 else float("inf")
    signed_jump = ((v1 - v0) / abs(v0) * 100.0) if v0 != 0 else float("inf")

    # trailing within-book yoy pct changes (consecutive years up to and incl. last_book)
    within = s[s.index <= last_book].sort_index()
    yoy = []
    idx = list(within.index)
    for i in range(1, len(idx)):
        y_prev, y_cur = idx[i - 1], idx[i]
        if y_cur - y_prev != 1:
            continue
        pv = float(within.loc[y_prev])
        if pv == 0:
            continue
        yoy.append((float(within.loc[y_cur]) - pv) / abs(pv) * 100.0)
    trailing = yoy[-SPLICE_TRAILING_N:]
    sigma = float(np.std(trailing, ddof=1)) if len(trailing) >= 2 else 0.0
    threshold = max(SPLICE_SIGMA_MULT * sigma, SPLICE_FLOOR_PCT)
    return {
        "last_book_year": last_book, "splice_year": splice_year,
        "value_last_book": v0, "value_splice": v1,
        "jump_pct": round(signed_jump, 4), "abs_jump_pct": round(jump_pct, 4),
        "trailing_sigma_pct": round(sigma, 4), "n_trailing": len(trailing),
        "threshold_pct": round(threshold, 4),
        "status": RED if jump_pct > threshold else GREEN,
    }


def check_splice_continuity(sid: str, df: pd.DataFrame, registry: dict) -> dict:
    """Flag a book->extension level break at the splice year.

    RED if |pct change across splice| > max(3 x std(trailing 5 within-book yoy pct
    changes), 5%). Returns {status, jump_pct, threshold_pct, detail, splice_year, ...}.
    """
    entry = _entry(registry, sid)
    if not _is_splice_eligible(entry):
        return {"status": NA, "sid": sid, "detail": "no extension / no book+extension ranges"}
    sy = _splice_year(entry)
    if sy is None:
        return {"status": NA, "sid": sid, "detail": "could not determine splice year"}
    if df is None:
        return {"status": NA, "sid": sid, "splice_year": sy, "detail": "processed parquet missing"}

    per_sub = {}
    for sub in sorted(df["subseries_id"].dropna().unique().tolist()):
        s = _subseries_series(df, sub)
        r = _eval_subseries_splice(s, sy)
        if r is not None:
            per_sub[sub] = r

    if not per_sub:
        return {"status": NA, "sid": sid, "splice_year": sy,
                "detail": f"no subseries spans {sy - 1}->{sy}"}

    worst_sub = max(per_sub, key=lambda k: per_sub[k]["abs_jump_pct"])
    worst = per_sub[worst_sub]
    reds = [k for k, v in per_sub.items() if v["status"] == RED]
    status = RED if reds else GREEN
    return {
        "status": status, "sid": sid, "splice_year": sy,
        "worst_subseries": worst_sub,
        "jump_pct": worst["jump_pct"], "abs_jump_pct": worst["abs_jump_pct"],
        "threshold_pct": worst["threshold_pct"],
        "red_subseries": reds,
        "detail": (f"{worst_sub}: {worst['jump_pct']:+.2f}% across {sy - 1}->{sy} "
                   f"vs threshold {worst['threshold_pct']:.2f}%"),
        "per_subseries": per_sub,
    }


# ---------------------------------------------------------------------------
# 3. Level plausibility
# ---------------------------------------------------------------------------
def _eval_rule(df: pd.DataFrame, rule: dict) -> dict:
    rtype = rule.get("rule_type")
    sub = rule.get("subseries")
    fy, ty = rule.get("from_year"), rule.get("to_year")
    s = _subseries_series(df, sub, fy, ty).dropna()
    base = {"rule_id": rule.get("rule_id"), "rule_type": rtype, "subseries": sub,
            "from_year": fy, "to_year": ty, "grounding": rule.get("grounding"),
            "n": int(len(s))}
    if len(s) == 0:
        return {**base, "status": NA, "detail": "no data in window"}

    years = list(s.index)
    vals = [float(v) for v in s.values]

    if rtype in ("strictly_falling", "strictly_rising"):
        violations = []
        for i in range(1, len(vals)):
            rising = vals[i] > vals[i - 1]
            falling = vals[i] < vals[i - 1]
            if rtype == "strictly_falling" and not falling:
                violations.append({"year": years[i], "prev_year": years[i - 1],
                                   "value": vals[i], "prev_value": vals[i - 1]})
            if rtype == "strictly_rising" and not rising:
                violations.append({"year": years[i], "prev_year": years[i - 1],
                                   "value": vals[i], "prev_value": vals[i - 1]})
        status = RED if violations else GREEN
        return {**base, "status": status, "n_violations": len(violations),
                "violations": violations[:10],
                "detail": (f"{len(violations)} non-{'decreasing' if rtype=='strictly_falling' else 'increasing'} "
                           f"step(s) over {years[0]}-{years[-1]}")}

    if rtype == "range":
        lo, hi = rule.get("min"), rule.get("max")
        violations = [{"year": years[i], "value": vals[i]}
                      for i in range(len(vals))
                      if (lo is not None and vals[i] < lo) or (hi is not None and vals[i] > hi)]
        status = RED if violations else GREEN
        return {**base, "status": status, "min": lo, "max": hi,
                "n_violations": len(violations), "violations": violations[:10],
                "detail": f"{len(violations)} value(s) outside [{lo}, {hi}]"}

    if rtype == "sign":
        want = rule.get("sign", "positive")
        def ok(v: float) -> bool:
            if want == "positive":
                return v > 0
            if want == "negative":
                return v < 0
            if want == "nonnegative":
                return v >= 0
            if want == "nonpositive":
                return v <= 0
            return True
        violations = [{"year": years[i], "value": vals[i]} for i in range(len(vals)) if not ok(vals[i])]
        status = RED if violations else GREEN
        return {**base, "status": status, "sign": want,
                "n_violations": len(violations), "violations": violations[:10],
                "detail": f"{len(violations)} value(s) violate sign={want}"}

    return {**base, "status": NA, "detail": f"unknown rule_type '{rtype}'"}


def check_level_plausibility(sid: str, df: pd.DataFrame, registry: dict) -> dict:
    """Evaluate registry ``validation.plausibility_rules[]`` against processed data.

    Returns {status, sid, n_rules, rules:[...]}. status = RED if any rule RED.
    """
    rules = _validation(registry, sid).get("plausibility_rules") or []
    if not rules:
        return {"status": NA, "sid": sid, "n_rules": 0, "rules": [],
                "detail": "no plausibility_rules registered"}
    if df is None:
        return {"status": NA, "sid": sid, "n_rules": len(rules), "rules": [],
                "detail": "processed parquet missing"}

    results = [_eval_rule(df, r) for r in rules]
    reds = [r for r in results if r["status"] == RED]
    greens = [r for r in results if r["status"] == GREEN]
    status = RED if reds else (GREEN if greens else NA)
    return {"status": status, "sid": sid, "n_rules": len(rules),
            "n_red": len(reds), "n_green": len(greens),
            "n_na": len(results) - len(reds) - len(greens), "rules": results}


# ---------------------------------------------------------------------------
# Suite runner
# ---------------------------------------------------------------------------
def run_anchor_suite(registry_path: Path | str = REGISTRY,
                     processed_dir: Path | str = DATA_PROCESSED,
                     write: bool = True) -> dict:
    """Run all three checks across every series that carries anchors, plausibility
    rules, or a book->extension splice. Writes ANCHOR_SUITE_REPORT.json and returns it.
    """
    registry = _load_registry(registry_path)
    series = registry.get("series") or {}

    targets: list[str] = []
    for sid, entry in series.items():
        val = entry.get("validation") or {}
        if val.get("independent_anchors") or val.get("plausibility_rules") or _is_splice_eligible(entry):
            targets.append(sid)
    targets.sort()

    series_reports: dict[str, dict] = {}
    splice_red, plausibility_red, anchor_red = [], [], []

    for sid in targets:
        df = _load_processed(sid, processed_dir)
        anchors_res = check_independent_anchor(sid, df, registry)
        splice_res = check_splice_continuity(sid, df, registry)
        plaus_res = check_level_plausibility(sid, df, registry)
        series_reports[sid] = {"anchors": anchors_res, "splice": splice_res,
                               "plausibility": plaus_res}
        if anchors_res["status"] == RED:
            anchor_red.append(sid)
        if splice_res["status"] == RED:
            splice_red.append(sid)
        if plaus_res["status"] == RED:
            plausibility_red.append(sid)

    report = {
        "schema_version": "anu-anchor-suite-v1.0",
        "decision": "0011",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "registry": str(registry_path),
        "processed_dir": str(processed_dir),
        "summary": {
            "series_checked": len(targets),
            "anchor_red": anchor_red,
            "splice_red": splice_red,
            "plausibility_red": plausibility_red,
            "total_red_series": len(set(anchor_red) | set(splice_red) | set(plausibility_red)),
        },
        "series": series_reports,
    }

    if write:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
        report["report_path"] = str(REPORT_PATH)
    return report


def _print_summary(report: dict) -> None:
    s = report["summary"]
    print("=== ANCHOR SUITE (Decision 0011) ===")
    print(f"series checked : {s['series_checked']}")
    print(f"anchor RED      : {s['anchor_red']}")
    print(f"splice RED      : {s['splice_red']}")
    print(f"plausibility RED: {s['plausibility_red']}")
    print(f"report          : {report.get('report_path', REPORT_PATH)}")


def main() -> int:
    ap = argparse.ArgumentParser(prog="_v03_anchor_lib.py",
                                 description="Run the independent-anchor validation suite (Decision 0011)")
    ap.add_argument("--run", action="store_true", help="run the full anchor suite and write the report")
    ap.add_argument("--no-write", action="store_true", help="do not write the report file")
    args = ap.parse_args()
    if args.run:
        report = run_anchor_suite(write=not args.no_write)
        _print_summary(report)
        # F-6D-02 fix: propagate RED -> exit 1 so `--run` gates CI/callers.
        # Previously this always returned 0, silently masking anchor RED.
        n_red = report["summary"]["total_red_series"]
        if n_red:
            print(f"RESULT          : FAIL ({n_red} series RED)")
            return 1
        print("RESULT          : PASS (0 RED)")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
