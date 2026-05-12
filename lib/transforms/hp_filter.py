"""Statistical filters and transforms for figure-level post-processing.

These transforms are applied during the figure export phase, not during
core P## processing.  The P## scripts produce raw replicated values;
transforms here produce the derived series that specific book figures
display (HP-smoothed trends, normal-capacity adjustments, etc.).
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def hp_filter(
    series: pd.Series,
    lamb: float = 100,
) -> tuple[pd.Series, pd.Series]:
    """Hodrick-Prescott filter.

    Parameters
    ----------
    series : pd.Series
        Input series (index = years, values = numeric).
    lamb : float
        Smoothing parameter.  Common values in Shaikh (2016):
        - 100 for annual macro data (wage share, Phillips curves, long waves)
        - 40 for alternative bandwidth (unemployment intensity)
        - 3 for interest rate trends

    Returns
    -------
    trend : pd.Series
        HP trend component.
    cycle : pd.Series
        HP cyclical component (original minus trend).
    """
    from statsmodels.tsa.filters.hp_filter import hpfilter

    clean = series.dropna()
    if len(clean) < 4:
        return clean.copy(), pd.Series(0.0, index=clean.index)

    cycle_vals, trend_vals = hpfilter(clean.values, lamb=lamb)
    trend = pd.Series(trend_vals, index=clean.index, name=f"{series.name}_trend")
    cycle = pd.Series(cycle_vals, index=clean.index, name=f"{series.name}_cycle")
    return trend, cycle


def normal_capacity(
    profit_rate: pd.Series,
    capacity_util: pd.Series,
) -> pd.Series:
    """Normal-capacity profit rate: r_nc = r / uK.

    Used in Shaikh (2016) Figures 6.5 and 6.6 to adjust the observed
    profit rate for capacity utilization fluctuations.

    Parameters
    ----------
    profit_rate : pd.Series
        Observed profit rate series.
    capacity_util : pd.Series
        Capacity utilization rate (decimal, e.g. 0.85).

    Returns
    -------
    pd.Series
        Normal-capacity profit rate.
    """
    common_idx = profit_rate.index.intersection(capacity_util.index)
    r = profit_rate.reindex(common_idx)
    u = capacity_util.reindex(common_idx)

    u_safe = u.replace(0, np.nan)
    result = r / u_safe
    result.name = f"{profit_rate.name}_nc" if profit_rate.name else "r_nc"
    return result


def cubic_detrend(series: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Fit a cubic time trend and return deviations.

    Used in Shaikh (2016) Figure 16.1 for long-wave analysis.

    Parameters
    ----------
    series : pd.Series
        Input series (index = years).

    Returns
    -------
    trend : pd.Series
        Fitted cubic polynomial trend.
    deviations : pd.Series
        Original minus trend.
    """
    clean = series.dropna()
    if len(clean) < 5:
        return clean.copy(), pd.Series(0.0, index=clean.index)

    x = clean.index.values.astype(float)
    y = clean.values.astype(float)

    x_centered = x - x.mean()
    coeffs = np.polyfit(x_centered, y, 3)
    trend_vals = np.polyval(coeffs, x_centered)

    trend = pd.Series(trend_vals, index=clean.index, name=f"{series.name}_trend")
    deviations = pd.Series(y - trend_vals, index=clean.index, name=f"{series.name}_dev")
    return trend, deviations


TRANSFORM_REGISTRY: dict[str, dict] = {
    "hp_filter": {
        "fn": hp_filter,
        "inputs": ["input"],
        "params": {"lamb": ("lambda", 100)},
        "outputs": ["output_trend", "output_cycle"],
        "default_suffixes": ["_trend", "_cycle"],
    },
    "normal_capacity": {
        "fn": normal_capacity,
        "inputs": ["input", "capacity"],
        "params": {},
        "outputs": ["output"],
        "default_suffixes": ["_nc"],
    },
    "cubic_detrend": {
        "fn": cubic_detrend,
        "inputs": ["input"],
        "params": {},
        "outputs": ["output_trend", "output_dev"],
        "default_suffixes": ["_trend", "_dev"],
    },
}
