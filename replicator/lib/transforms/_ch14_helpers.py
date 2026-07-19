"""Shared helpers for Chapter 14 loaders / processors / validators.

Centralises the Appendix-14 chopped-table reader and the FRED-fetch helpers
used across S1401-S1408 so each per-series script stays small.

Conventions
-----------
- The Shaikh Appendix 14.3 spreadsheet
  ``SalvagedInputs/book_data/ShaikhChoppedTables/Appendix14_InflationULdata.xlsx``
  is the canonical "book truth" reference for all 8 Chapter 14 series. Its row 0
  is a descriptive header, row 1 is the year column (Year, 1948, 1949, ...,
  2012). The first data row (1948) is also the first observation in the chapter.
- All HP filtering in Chapter 14 uses ``lambda = 100`` (Shaikh's explicit
  Appendix 14.2 p. 893 choice — even for quarterly Fig 14.12, where the
  textbook quarterly value would otherwise be 1600). DO NOT substitute.
- Productivity is per-FTE-EMPLOYEE per Shaikh's exact formula
  ``yr = (GDP*100/p)/(FEE/1000)`` where FEE = full-time equivalent employment
  (NIPA Tables 6.5A-D). Both per-hour BLS substitutes (OPHNFB, PRS85006092,
  OPHPBS, OPHMFG) AND BEA hours-worked denominators (B4701C0*, e.g.
  B4701C0A222NBEA, NIPA T6.9) are REJECTED via a hard concept-policing
  assertion in any loader that constructs productivity (SWEEP-ch1417-01).
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# Concept-policing list — kept here so any loader can import the same list.
# These are BLS *per-hour* productivity indices (output-per-hour is a different
# labor-input concept than Shaikh's real-GDP-per-FTE-employee).
PER_HOUR_PROHIBITED_FRED_IDS = (
    "OPHNFB",       # Output per hour, nonfarm business (BLS)
    "PRS85006092",  # Nonfarm business sector labor productivity index (BLS)
    "OPHPBS",       # Output per hour, business sector (BLS)
    "OPHMFG",       # Manufacturing output per hour (BLS)
)

# Hours-worked denominators (BEA NIPA T6.9) that are NOT an employee count.
# Feeding hours into yr = (GDP*100/p)/(FEE/1000) yields output-per-HOUR growth,
# not output-per-FTE-EMPLOYEE growth (SWEEP-ch1417-01, remediated 2026-07-01).
# The `B4701C0` prefix covers B4701C0A222NBEA ("Hours worked by full-time and
# part-time employees") and its NIPA-6.9 siblings.
HOURS_WORKED_PROHIBITED_FRED_ID_PREFIXES = (
    "B4701C0",
)
HOURS_WORKED_PROHIBITED_FRED_IDS = (
    "B4701C0A222NBEA",  # Hours worked by full-time and part-time employees (BEA NIPA T6.9)
)

# Canonical total-compensation series for the Chapter-14 wage-share numerator.
# Shaikh's wage share = Compensation of Employees (NIPA T1.10 line 2) / GDP.
# This is FRED W209RC1 — the SAME series S1403 uses for its quarterly wage share.
COMPENSATION_T110_LINE2_FRED_ID = "W209RC1"

# Wage-and-salary-only subsets that are ~20% low and must NEVER be used as the
# wage-share numerator (they exclude employer supplements — pensions, insurance).
WAGE_SHARE_NUMERATOR_PROHIBITED_FRED_IDS = (
    "A576RC1",  # Compensation of Employees, Received: Wage & Salary Disbursements (NIPA T2.1)
    "A576RC1A027NBEA",  # annual variant of the same wage-and-salary-only subset
)

HP_LAMBDA_CH14 = 100  # Shaikh Appendix 14.2 p. 893; annual AND quarterly


def appendix14_path() -> Path:
    """Resolve the canonical Appendix 14.3 chopped table path."""
    from utils.paths import SALVAGED_BOOK_DATA  # local import to avoid circular
    return SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix14_InflationULdata.xlsx"


def read_appendix14() -> pd.DataFrame:
    """Read the Appendix 14.3 data table into a year-indexed DataFrame.

    The workbook's row 0 is a descriptive header; row 1 onward holds the data.
    The first column is unnamed but contains the year. We promote it to ``year``
    and drop the descriptive header row. NaN rows (e.g. the 2012 incomplete row
    that exists for some columns but not others) are preserved.

    Returns
    -------
    DataFrame with columns: ``year`` (Int64), then the original Appendix column
    names: ``inflrate``, ``inflrateHP100``, ``GPRODVTY``, ``GPRODVTYHP100``,
    ``ggdp``, ``ggdphp100``, ``grgdp``, ``grgdphp100``, ``wagesh``,
    ``wageshhp100``, ``gwsh``, ``gwshhp100``, ``UNEMPLRATE``,
    ``UNEMPLRATEHP100``, ``UNEMPDURATION``, ``UNEMPDURHP100``,
    ``ulintensity``, ``ulintensityhp100``, ``GULINTENSITY``, ``GULINTENSITYHP``,
    ``GMWAGEHP100``, ``GRWAGEHP100``, ``GWSHHP100RAL8AF`` (era-1 Phillips fit),
    ``GWSHHP100RAL8BP1F`` (era-2 Phillips fit), plus three "Unnamed" passthrough
    columns we leave as-is.
    """
    raw = pd.read_excel(appendix14_path())
    # First row (index 0) is descriptive header — drop. Data starts at index 1.
    df = raw.iloc[1:].reset_index(drop=True)
    df = df.rename(columns={"Unnamed: 0": "year"})
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year"]).reset_index(drop=True)
    # Strip whitespace on any string-named columns (some Appendix headers have
    # trailing spaces, e.g. 'GMWAGEHP100 ').
    df.columns = [str(c).strip() for c in df.columns]
    # Coerce all data columns to float (Appendix occasionally writes ints)
    for col in df.columns:
        if col == "year":
            continue
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # Strict book-period clip: Shaikh's chapter scope is 1948-2011. The Appendix
    # spreadsheet has a partial 2012 row with leftover values that we
    # intentionally drop so the extension takes over cleanly at 2012.
    df = df[df["year"] <= 2011].reset_index(drop=True)
    return df


def hp_filter(series: np.ndarray | pd.Series, lam: float = HP_LAMBDA_CH14) -> np.ndarray:
    """Apply the Hodrick-Prescott two-sided filter and return the trend.

    Shaikh's Appendix 14.2 uses ``lambda = 100`` for both annual and quarterly
    data — do NOT substitute the textbook quarterly value of 1600.

    Returns the trend component as a numpy array.
    """
    try:
        from statsmodels.tsa.filters.hp_filter import hpfilter  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("statsmodels is required for HP filter") from exc
    arr = np.asarray(series, dtype=float)
    # statsmodels does not accept NaNs — return NaN trend for all-NaN input
    if np.isnan(arr).all():
        return np.full_like(arr, np.nan, dtype=float)
    # Mask interior NaNs by filling with linear interpolation, then refit
    s = pd.Series(arr).interpolate(method="linear", limit_direction="both")
    cycle, trend = hpfilter(s.to_numpy(), lamb=lam)
    return np.asarray(trend, dtype=float)


def assert_no_per_hour_substitution(series_ids: list[str]) -> None:
    """Concept-policing assertion. Raise ValueError if any prohibited per-hour
    OR hours-worked series ID appears in ``series_ids``.

    Shaikh's productivity = real GDP per FULL-TIME-EQUIVALENT EMPLOYEE per
    Appendix 14.2 p. 892 (FEE = full-time equivalent employment from Tables
    6.5A-D). Two distinct wrong-concept classes are blocked:

    (a) BLS per-hour productivity indices (OPHNFB / PRS85006092 / OPHPBS /
        OPHMFG) — output-per-hour, a different labor-input concept;
    (b) BEA hours-worked denominators (B4701C0*, e.g. B4701C0A222NBEA "Hours
        worked by full-time and part-time employees", NIPA T6.9) — HOURS, not
        an employee count. Dividing GDP by hours yields output-per-HOUR growth
        mislabeled per-FTE (the SWEEP-ch1417-01 defect, remediated 2026-07-01).

    Either substitution silently breaks Shaikh's wage-share decomposition
    wr = w/p, gwsh = wr - yr (Eq. 14.18-14.19).
    """
    upper = [sid.upper() for sid in series_ids]
    per_hour = {s.upper() for s in PER_HOUR_PROHIBITED_FRED_IDS}
    hours_exact = {s.upper() for s in HOURS_WORKED_PROHIBITED_FRED_IDS}
    hours_prefixes = tuple(p.upper() for p in HOURS_WORKED_PROHIBITED_FRED_ID_PREFIXES)

    per_hour_offenders = [sid for sid, u in zip(series_ids, upper) if u in per_hour]
    if per_hour_offenders:
        raise ValueError(
            "Productivity concept-policing failure: per-hour substitute(s) "
            f"detected: {per_hour_offenders}. Shaikh Ch14 productivity is real "
            "GDP per FTE employee (Appendix 14.2 p. 892 formula "
            "yr = (GDP*100/p)/(FEE/1000)); per-hour BLS series are prohibited "
            "substitutes."
        )

    hours_offenders = [
        sid for sid, u in zip(series_ids, upper)
        if u in hours_exact or u.startswith(hours_prefixes)
    ]
    if hours_offenders:
        raise ValueError(
            "Productivity concept-policing failure: hours-worked denominator(s) "
            f"detected: {hours_offenders}. Shaikh Ch14 productivity divides real "
            "GDP by FULL-TIME-EQUIVALENT EMPLOYEES (FEE, NIPA T6.5A-D, a count), "
            "NOT by hours worked (NIPA T6.9, B4701C0*). Use A4301C0A173NBEA "
            "(Full-time equivalent employees). Feeding hours yields "
            "output-per-HOUR growth mislabeled per-FTE (SWEEP-ch1417-01)."
        )


def assert_compensation_is_total(series_id: str) -> None:
    """Concept-policing assertion for Chapter-14 wage-share numerators.

    Shaikh's wage share (Appendix 14.2 p. 892; NIPA T1.10 line 2) uses TOTAL
    Compensation of Employees — FRED ``W209RC1`` — which includes wages, salaries
    AND employer supplements (pension/insurance). The wage-and-salary-disbursements
    subset (``A576RC1``, NIPA T2.1) omits supplements and understates the wage
    share by ~20%, producing a spurious downward break at the book->extension
    splice. Raise ``ValueError`` unless the numerator series is exactly the
    canonical total-compensation concept, so ``A576RC1`` can never silently
    return in place of ``W209RC1``.
    """
    sid = series_id.upper()
    if sid in {s.upper() for s in WAGE_SHARE_NUMERATOR_PROHIBITED_FRED_IDS}:
        raise ValueError(
            "Wage-share numerator concept-policing failure: wage-and-salary-only "
            f"substitute detected: {series_id!r}. Shaikh Ch14 wage share is TOTAL "
            "Compensation of Employees (NIPA T1.10 line 2 = FRED W209RC1); "
            "A576RC1 (Wage & Salary Disbursements, NIPA T2.1) excludes employer "
            "supplements and is ~20% low. Use W209RC1 (matches S1403)."
        )
    if sid != COMPENSATION_T110_LINE2_FRED_ID:
        raise ValueError(
            "Wage-share numerator concept-policing failure: expected the canonical "
            f"total-compensation series {COMPENSATION_T110_LINE2_FRED_ID!r} (NIPA "
            f"T1.10 line 2) but got {series_id!r}. Any substitution must be "
            "justified in the EPR and this guard updated deliberately."
        )


def fred_annual(series_id: str, *, start: str = "1947-01-01", end: str = "2025-12-31",
                aggregation_method: str = "avg",
                realtime: tuple[str | None, str | None] | None = None) -> pd.DataFrame:
    """Fetch a FRED series at annual frequency. Returns DataFrame[year, value].

    ``realtime`` is the ALFRED ``(realtime_start, realtime_end)`` vintage window
    resolved by ``utils.vintage_manifest.realtime_window`` (SI-1 pinning). When
    ``None`` the loader has not routed a pin and the LATEST vintage is fetched.
    """
    from S00_setup import S00_apis, S00_config
    if not S00_config.have_key("FRED_API_KEY"):
        raise S00_apis.ApiUnavailable("FRED_API_KEY not set")
    rs, re = realtime if realtime else (None, None)
    df = S00_apis.fred_observations(
        series_id=series_id, frequency="a", aggregation_method=aggregation_method,
        observation_start=start, observation_end=end,
        realtime_start=rs, realtime_end=re,
    )
    df = df.copy()
    df["year"] = df["date"].dt.year.astype(int)
    return df[["year", "value"]].reset_index(drop=True)


def fred_quarterly(series_id: str, *, start: str = "1947-01-01", end: str = "2025-12-31",
                   aggregation_method: str = "avg",
                   realtime: tuple[str | None, str | None] | None = None) -> pd.DataFrame:
    """Fetch a FRED series at quarterly frequency. Returns DataFrame[date, value,
    year, quarter]. ``realtime`` = ALFRED vintage window (SI-1 pinning)."""
    from S00_setup import S00_apis, S00_config
    if not S00_config.have_key("FRED_API_KEY"):
        raise S00_apis.ApiUnavailable("FRED_API_KEY not set")
    rs, re = realtime if realtime else (None, None)
    df = S00_apis.fred_observations(
        series_id=series_id, frequency="q", aggregation_method=aggregation_method,
        observation_start=start, observation_end=end,
        realtime_start=rs, realtime_end=re,
    )
    df = df.copy()
    df["year"] = df["date"].dt.year.astype(int)
    df["quarter"] = df["date"].dt.quarter.astype(int)
    return df[["date", "year", "quarter", "value"]].reset_index(drop=True)


def fred_monthly_to_quarterly(series_id: str, *, start: str = "1947-01-01",
                              end: str = "2025-12-31",
                              aggregation_method: str = "avg",
                              realtime: tuple[str | None, str | None] | None = None) -> pd.DataFrame:
    """Fetch a FRED monthly series and aggregate to quarterly means.

    Used by S1403 quarterly intensity construction per Phase 4 Q1 resolution
    (aggregate monthly UNRATE/UEMPMEAN to quarterly means). ``realtime`` =
    ALFRED vintage window (SI-1 pinning).
    """
    from S00_setup import S00_apis, S00_config
    if not S00_config.have_key("FRED_API_KEY"):
        raise S00_apis.ApiUnavailable("FRED_API_KEY not set")
    rs, re = realtime if realtime else (None, None)
    df = S00_apis.fred_observations(
        series_id=series_id, frequency="m", aggregation_method=aggregation_method,
        observation_start=start, observation_end=end,
        realtime_start=rs, realtime_end=re,
    )
    df = df.copy()
    df["year"] = df["date"].dt.year.astype(int)
    df["quarter"] = df["date"].dt.quarter.astype(int)
    qd = df.groupby(["year", "quarter"], as_index=False)["value"].mean()
    qd["date"] = pd.to_datetime(
        qd["year"].astype(str) + "-" + ((qd["quarter"] - 1) * 3 + 1).astype(str).str.zfill(2) + "-01"
    )
    return qd[["date", "year", "quarter", "value"]].reset_index(drop=True)


def phillips_fit_constrained(x: np.ndarray, y: np.ndarray) -> dict:
    """Fit y = a + x^c (Shaikh's published form, constrained b=1).

    Returns dict with keys: a, c, r2, n, converged.
    """
    from scipy.optimize import curve_fit
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0)
    x_, y_ = x[mask], y[mask]
    if len(x_) < 3:
        return {"a": float("nan"), "c": float("nan"), "r2": float("nan"),
                "n": int(len(x_)), "converged": False}

    def f(x, a, c):
        return a + np.power(x, c)

    try:
        popt, _ = curve_fit(f, x_, y_, p0=[-1.0, -0.01], maxfev=20000)
        a, c = float(popt[0]), float(popt[1])
        yhat = f(x_, a, c)
        ss_res = float(np.sum((y_ - yhat) ** 2))
        ss_tot = float(np.sum((y_ - y_.mean()) ** 2))
        r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
        return {"a": a, "c": c, "r2": r2, "n": int(len(x_)), "converged": True}
    except Exception as exc:  # pragma: no cover
        return {"a": float("nan"), "c": float("nan"), "r2": float("nan"),
                "n": int(len(x_)), "converged": False, "error": str(exc)}


def phillips_fit_unconstrained(x: np.ndarray, y: np.ndarray) -> dict:
    """Fit y = a + b * x^c (Phillips's original 3-parameter form).

    Returns dict with keys: a, b, c, r2, n, converged.
    """
    from scipy.optimize import curve_fit
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0)
    x_, y_ = x[mask], y[mask]
    if len(x_) < 4:
        return {"a": float("nan"), "b": float("nan"), "c": float("nan"),
                "r2": float("nan"), "n": int(len(x_)), "converged": False}

    def f(x, a, b, c):
        return a + b * np.power(x, c)

    try:
        popt, _ = curve_fit(f, x_, y_, p0=[-1.0, 1.0, -0.01], maxfev=20000)
        a, b, c = float(popt[0]), float(popt[1]), float(popt[2])
        yhat = f(x_, a, b, c)
        ss_res = float(np.sum((y_ - yhat) ** 2))
        ss_tot = float(np.sum((y_ - y_.mean()) ** 2))
        r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
        return {"a": a, "b": b, "c": c, "r2": r2,
                "n": int(len(x_)), "converged": True}
    except Exception as exc:  # pragma: no cover
        return {"a": float("nan"), "b": float("nan"), "c": float("nan"),
                "r2": float("nan"), "n": int(len(x_)), "converged": False,
                "error": str(exc)}
