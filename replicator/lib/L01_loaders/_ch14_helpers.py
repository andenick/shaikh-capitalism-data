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
- Productivity is per-FTE per Shaikh's exact formula
  ``yr = (GDP*100/p)/(FEE/1000)``. Per-hour BLS substitutes (OPHNFB,
  PRS85006092, OPHPBS, OPHMFG) are REJECTED via a hard concept-policing
  assertion in any loader that constructs productivity.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# Concept-policing list — kept here so any loader can import the same list
PER_HOUR_PROHIBITED_FRED_IDS = (
    "OPHNFB",       # Output per hour, nonfarm business (BLS)
    "PRS85006092",  # Nonfarm business sector labor productivity index (BLS)
    "OPHPBS",       # Output per hour, business sector (BLS)
    "OPHMFG",       # Manufacturing output per hour (BLS)
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
    series ID appears in ``series_ids``.

    Shaikh's productivity = real GDP per FTE per Appendix 14.2 p. 892.
    Substituting BLS per-hour productivity silently breaks his wage-share
    decomposition wr = w/p, gwsh = wr - yr (Eq. 14.18-14.19).
    """
    offenders = [sid for sid in series_ids if sid.upper() in {s.upper() for s in PER_HOUR_PROHIBITED_FRED_IDS}]
    if offenders:
        raise ValueError(
            "Productivity concept-policing failure: per-hour substitute(s) "
            f"detected: {offenders}. Shaikh Ch14 productivity is real GDP per "
            "FTE (Appendix 14.2 p. 892 formula yr = (GDP*100/p)/(FEE/1000)); "
            "per-hour BLS series are prohibited substitutes."
        )


def fred_annual(series_id: str, *, start: str = "1947-01-01", end: str = "2025-12-31",
                aggregation_method: str = "avg") -> pd.DataFrame:
    """Fetch a FRED series at annual frequency. Returns DataFrame[year, value]."""
    from S00_setup import S00_apis, S00_config
    if not S00_config.have_key("FRED_API_KEY"):
        raise S00_apis.ApiUnavailable("FRED_API_KEY not set")
    df = S00_apis.fred_observations(
        series_id=series_id, frequency="a", aggregation_method=aggregation_method,
        observation_start=start, observation_end=end,
    )
    df = df.copy()
    df["year"] = df["date"].dt.year.astype(int)
    return df[["year", "value"]].reset_index(drop=True)


def fred_quarterly(series_id: str, *, start: str = "1947-01-01", end: str = "2025-12-31",
                   aggregation_method: str = "avg") -> pd.DataFrame:
    """Fetch a FRED series at quarterly frequency. Returns DataFrame[date, value,
    year, quarter]."""
    from S00_setup import S00_apis, S00_config
    if not S00_config.have_key("FRED_API_KEY"):
        raise S00_apis.ApiUnavailable("FRED_API_KEY not set")
    df = S00_apis.fred_observations(
        series_id=series_id, frequency="q", aggregation_method=aggregation_method,
        observation_start=start, observation_end=end,
    )
    df = df.copy()
    df["year"] = df["date"].dt.year.astype(int)
    df["quarter"] = df["date"].dt.quarter.astype(int)
    return df[["date", "year", "quarter", "value"]].reset_index(drop=True)


def fred_monthly_to_quarterly(series_id: str, *, start: str = "1947-01-01",
                              end: str = "2025-12-31",
                              aggregation_method: str = "avg") -> pd.DataFrame:
    """Fetch a FRED monthly series and aggregate to quarterly means.

    Used by S1403 quarterly intensity construction per Phase 4 Q1 resolution
    (aggregate monthly UNRATE/UEMPMEAN to quarterly means).
    """
    from S00_setup import S00_apis, S00_config
    if not S00_config.have_key("FRED_API_KEY"):
        raise S00_apis.ApiUnavailable("FRED_API_KEY not set")
    df = S00_apis.fred_observations(
        series_id=series_id, frequency="m", aggregation_method=aggregation_method,
        observation_start=start, observation_end=end,
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
