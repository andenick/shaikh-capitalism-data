"""Shared helpers for Chapter 16 loaders / processors / validators.

Centralises the Appendix 16 + Appendix 5 chopped-table readers and the FRED
helpers used across S1601-S1606 so each per-series script stays small.

Conventions
-----------
- Salvaged spreadsheets are the canonical "book truth" reference:
    * ``Appendix5_DATALRprices.xlsx`` -> S1601 golden waves (US/UK)
    * ``Appendix16_WageProdData.xlsx`` -> S1602 wages/productivity + ec_c trend
    * ``Appendix16_RXRRULCOECD.xlsx`` -> S1603 US + OECD + EU rates (annual %)
    * ``Appendix16_ProfitRates.xlsx`` -> S1604 profit rates and r_net components
    * ``Appendix16_DebtIncRatio.xlsx`` -> S1605 HHDebt / DPI ratio
    * ``Appendix16_HouseholdDebtService.xlsx`` -> S1606 FOR + DSR quarterly
- HP filtering for S1604 uses lambda=100 (Shaikh's explicit choice for annual
  data); Ravn-Uhlig 6.25 is emitted as a sensitivity variant only.
- S1605 unit conversion (HCCSDODNS millions / (DPI billions * 1000)) is
  implemented in P02_S1605_construct.py with an explicit dimensional comment.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


HP_LAMBDA_ANNUAL_CH16 = 100        # Shaikh's choice for Fig 16.8
HP_LAMBDA_SENSITIVITY = 6.25       # Ravn-Uhlig sensitivity variant


def book_data_dir() -> Path:
    from utils.paths import SALVAGED_BOOK_DATA  # local to avoid circular import
    return SALVAGED_BOOK_DATA / "ShaikhChoppedTables"


# ---------------------------------------------------------------------------
# Appendix 5 — long-run prices (S1601)
# ---------------------------------------------------------------------------
def read_appendix5_lrprices() -> pd.DataFrame:
    """Read Appendix 5 DATALRprices into a year-indexed DataFrame.

    Row 1 is the real header (the workbook has a descriptive banner at row 0).
    The returned DataFrame is clipped to years where the published golden-wave
    residual columns (USGoldWaveDetrended, UKGoldWaveDetrended) exist, plus the
    raw PPI/gold ratios (USPPIGold, UKPPIGold) used for the cubic-trend re-fit.
    """
    p = book_data_dir() / "Appendix5_DATALRprices.xlsx"
    df = pd.read_excel(p, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    if "Year" not in df.columns:
        # Some vintages put year in first column unnamed
        df = df.rename(columns={df.columns[0]: "Year"})
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).copy()
    df["year"] = df["Year"].astype(int)
    return df


# ---------------------------------------------------------------------------
# Appendix 16 — Wages / Productivity (S1602)
# ---------------------------------------------------------------------------
def read_appendix16_wage_prod() -> pd.DataFrame:
    """Read Appendix 16 wage/productivity data (header=1; Year column present).

    Returns DataFrame with original Appendix column names plus a clean ``year``
    integer column. Values include Productivity, Real Hrly EC, indexed and
    rebased variants, plus the published ec_c (Adj Real Hrly EC) counterfactual.
    """
    p = book_data_dir() / "Appendix16_WageProdData.xlsx"
    df = pd.read_excel(p, sheet_name="Data", header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).copy()
    df["year"] = df["Year"].astype(int)
    return df


# ---------------------------------------------------------------------------
# Appendix 16 — OECD/US/EU rates (S1603)
# ---------------------------------------------------------------------------
def read_appendix16_rxrrulcoecd() -> pd.DataFrame:
    """Read Appendix 16 RXRRULC OECD rates table (header=1).

    Columns: Year, US (rate, decimal), OECD (rate, decimal), EU, OECD/EU, US.1
    (US.1 is a sometimes-percent variant near the end). Annual 1960-2012.
    """
    p = book_data_dir() / "Appendix16_RXRRULCOECD.xlsx"
    df = pd.read_excel(p, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).copy()
    df["year"] = df["Year"].astype(int)
    return df


# ---------------------------------------------------------------------------
# Appendix 16 — Profit Rates (S1604)
# ---------------------------------------------------------------------------
def read_appendix16_profit_rates() -> pd.DataFrame:
    """Read Appendix 16 ProfitRates table (header=1).

    Columns of interest:
      Year, Corporate Average Rate of Profit (rcorp),
      Current (Real) Incremental Profit Rate (iroprcorp),
      Current (Real) Incremental Profit Rate (HP100), HP100 lag(1),
      Interest Rate (3-mo. T-Bill) [decimal],
      Net Corporate Rate of Profit (rcorp - i),
      Net Incremental Real Corporate Rate of Profit (HP100), HP100 lag(1).
    """
    p = book_data_dir() / "Appendix16_ProfitRates.xlsx"
    df = pd.read_excel(p, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).copy()
    df["year"] = df["Year"].astype(int)
    return df


# ---------------------------------------------------------------------------
# Appendix 16 — Debt/Income Ratio (S1605)
# ---------------------------------------------------------------------------
def read_appendix16_debt_inc_ratio() -> pd.DataFrame:
    """Read Appendix 16 HHDebt/DPI ratio table (header=1).

    Columns: Date (year, 1975-2012), HHDebt (billions USD),
             HHDispPersInc (billions USD SAAR), HHDebtIncRatio (decimal).
    """
    p = book_data_dir() / "Appendix16_DebtIncRatio.xlsx"
    df = pd.read_excel(p, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df["Date"] = pd.to_numeric(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).copy()
    df["year"] = df["Date"].astype(int)
    return df


# ---------------------------------------------------------------------------
# Appendix 16 — Household Debt Service (S1606)
# ---------------------------------------------------------------------------
def read_appendix16_debt_service() -> pd.DataFrame:
    """Read Appendix 16 Household Debt Service table (header=1).

    Returns DataFrame with columns:
      Time Period (e.g. '1980Q1'),
      'Financial obligations ratio, seasonally adjusted' (FOR, decimal),
      'Debt service ratio, seasonally adjusted' (DSR, decimal),
      plus a parsed (year, quarter, qdate) triple.
    """
    p = book_data_dir() / "Appendix16_HouseholdDebtService.xlsx"
    df = pd.read_excel(p, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Time Period"]).copy()
    df["Time Period"] = df["Time Period"].astype(str)
    # Parse 1980Q1 -> year=1980, quarter=1
    parts = df["Time Period"].str.extract(r"(\d{4})Q([1-4])")
    df["year"] = pd.to_numeric(parts[0], errors="coerce").astype("Int64")
    df["quarter"] = pd.to_numeric(parts[1], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year", "quarter"]).copy()
    df["year"] = df["year"].astype(int)
    df["quarter"] = df["quarter"].astype(int)
    month_first = (df["quarter"] - 1) * 3 + 1
    df["qdate"] = pd.to_datetime(
        df["year"].astype(str) + "-" + month_first.astype(str).str.zfill(2) + "-01"
    )
    return df


# ---------------------------------------------------------------------------
# FRED helpers (annual / quarterly)
# ---------------------------------------------------------------------------
def fred_annual(series_id: str, *, start: str = "1947-01-01",
                end: str = "2025-12-31",
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


def fred_quarterly(series_id: str, *, start: str = "1947-01-01",
                   end: str = "2025-12-31",
                   aggregation_method: str = "avg") -> pd.DataFrame:
    """Fetch a FRED series at quarterly frequency.

    Returns DataFrame with columns ``date``, ``year``, ``quarter``, ``value``.
    """
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


# ---------------------------------------------------------------------------
# HP filter (shared with Ch14 helper but re-stated for clarity)
# ---------------------------------------------------------------------------
def hp_filter(series: "np.ndarray | pd.Series", lam: float = HP_LAMBDA_ANNUAL_CH16) -> np.ndarray:
    """Two-sided Hodrick-Prescott filter; returns the TREND component.

    Default lambda=100 matches Shaikh's Ch16 (Fig 16.8) choice for annual data.
    Use ``lam=6.25`` for the Ravn-Uhlig sensitivity variant.
    """
    try:
        from statsmodels.tsa.filters.hp_filter import hpfilter
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("statsmodels is required for HP filter") from exc
    arr = np.asarray(series, dtype=float)
    if np.isnan(arr).all():
        return np.full_like(arr, np.nan, dtype=float)
    s = pd.Series(arr).interpolate(method="linear", limit_direction="both")
    _cycle, trend = hpfilter(s.to_numpy(), lamb=lam)
    return np.asarray(trend, dtype=float)


# ---------------------------------------------------------------------------
# Cubic-trend de-trender (S1601 golden waves construction)
# ---------------------------------------------------------------------------
def fit_cubic_trend(years: np.ndarray, values: np.ndarray) -> tuple[np.ndarray, dict]:
    """Fit OLS cubic on ln(values) ~ years + years^2 + years^3.

    Returns (residuals_array_aligned_to_years_input, fit_diagnostics_dict).
    Residuals are in log-points; the caller is responsible for rebasing to
    1930=100 in deviation-percent form.

    NaNs in ``values`` are dropped before fit; residuals at those positions
    are NaN in the returned array.
    """
    years = np.asarray(years, dtype=float)
    values = np.asarray(values, dtype=float)
    mask = np.isfinite(values) & (values > 0)
    if mask.sum() < 4:
        return np.full_like(values, np.nan), {"n_fit": int(mask.sum()), "converged": False}
    y = np.log(values[mask])
    t = years[mask]
    X = np.column_stack([np.ones_like(t), t, t ** 2, t ** 3])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    Xfull = np.column_stack([np.ones_like(years), years, years ** 2, years ** 3])
    yhat_full = Xfull @ coef
    resid = np.full_like(values, np.nan, dtype=float)
    resid[mask] = y - yhat_full[mask]
    diag = {
        "n_fit": int(mask.sum()),
        "converged": True,
        "coef_const": float(coef[0]),
        "coef_t": float(coef[1]),
        "coef_t2": float(coef[2]),
        "coef_t3": float(coef[3]),
    }
    return resid, diag


def rebase_residuals_to_year(residuals: np.ndarray, years: np.ndarray,
                             base_year: int = 1930) -> np.ndarray:
    """Convert log-residuals into (1 + resid)/(1 + resid_base) * 100 style
    deviation-from-trend, where 100 corresponds to base_year's trend value.

    Shaikh's Fig 16.1 plots residuals such that 1930 = 100 on a "deviation
    from cubic trend" axis. The convention is: residual_t = trend_dev_t -
    trend_dev_{1930}, then re-expressed as 100 * exp(adj_resid).
    """
    residuals = np.asarray(residuals, dtype=float)
    years = np.asarray(years, dtype=int)
    if base_year not in years:
        # Use nearest available year (graceful)
        avail = years[np.isfinite(residuals)]
        if avail.size == 0:
            return np.full_like(residuals, np.nan, dtype=float)
        base_year = int(avail[np.argmin(np.abs(avail - base_year))])
    base_resid = float(residuals[years == base_year][0])
    adj = residuals - base_resid
    return 100.0 * np.exp(adj)
