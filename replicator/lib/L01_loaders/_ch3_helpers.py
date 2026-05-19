"""Shared helpers for Ch3 theoretical/cross-sectional loaders.

All loaders write a parquet with the same minimal schema:
    year (int)        — sequence index; for theoretical curves this is the
                        point index 1..N; for cross-sectional 1904 it is 1904.
    x_value (float)   — the natural abscissa (income y; price p1/p2)
    value (float)     — the curve ordinate
    subseries_id (str)
    subsource_id (str)
    units (str)

Note the addition of `x_value` beyond the canonical Anu schema. The chopped
writer (O06_chopped_writer.py) accepts extra columns silently — it requires
year/value/subseries_id/source_id/units present and treats others as
informational.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


# --- Case I (x1min sub-linear) -----------------------------------------------
# x1min(y) = y^0.5, c = 0.5, p1 = 1, p2 = 2 (the latter two are book-stated for the simulations)

C_CASE_I = 0.5
ALPHA_X1MIN_CASE_I = 1.0   # multiplicative scale on y^beta
BETA_X1MIN_CASE_I = 0.5    # exponent (sub-linear -> beta < 1)

# --- Case II (c declining) ---------------------------------------------------
# c(y) = c0 * exp(-k * y), x1min held constant
C0_CASE_II = 0.7
K_CASE_II = 0.05
X1MIN_CASE_II = 5.0   # constant minimum (in expenditure-on-necessaries units when p1=1)


def x1min_case_i(y: np.ndarray) -> np.ndarray:
    """Sub-linear necessary minimum under Case I."""
    return ALPHA_X1MIN_CASE_I * np.power(y, BETA_X1MIN_CASE_I)


def dx1min_dy_case_i(y: np.ndarray) -> np.ndarray:
    """Derivative of x1min(y) under Case I (square-root path)."""
    # d/dy (y^0.5) = 0.5 * y^(-0.5); avoid singularity at y=0 (callers should trim)
    return ALPHA_X1MIN_CASE_I * BETA_X1MIN_CASE_I * np.power(y, BETA_X1MIN_CASE_I - 1.0)


def c_case_ii(y: np.ndarray) -> np.ndarray:
    """Discretionary propensity declining in income under Case II."""
    return C0_CASE_II * np.exp(-K_CASE_II * y)


# --- Demand curves from eqs (3.5) and (3.6) for the simulation studies -------
# eq (3.5):  x1 = (1 - c) * x1min + c * y / p1
# eq (3.6):  x2 = c * (y - p1*x1min) / p2
# parameters: y = 200, c = 0.5, x1min = 10, p1 default 1, p2 default 2


SIM_Y = 200.0
SIM_C = 0.50
SIM_X1MIN = 10.0
SIM_P1_DEFAULT = 1.0
SIM_P2_DEFAULT = 2.0


def x1_demand(p1: np.ndarray, y: float = SIM_Y, c: float = SIM_C, x1min: float = SIM_X1MIN) -> np.ndarray:
    """Necessary-good demand x1 as a function of p1, holding y nominal."""
    # eq (3.5): x1 = (1 - c) * x1min + c * y / p1
    # multiplied by 5000 / 200 because Shaikh's simulation aggregates over 5000 agents with mean income 200,
    # but the Figure 3.10 axes report aggregate demand normalised to per-capita units (range x1 in [70, 110]).
    # We keep the per-agent formula (range matches the printed axis when c=0.5, x1min=10).
    return (1.0 - c) * x1min + c * y / p1


def x2_demand(p2: np.ndarray, y: float = SIM_Y, c: float = SIM_C, x1min: float = SIM_X1MIN,
              p1: float = SIM_P1_DEFAULT) -> np.ndarray:
    """Luxury-good demand x2 as a function of p2."""
    # eq (3.6): x2 = c * (y - p1 * x1min) / p2
    return c * (y - p1 * x1min) / p2


# --- Standard parquet writer for Ch3 theoretical/CS curves -------------------

def make_curve_frame(x_values: np.ndarray, y_values: np.ndarray, *,
                     subseries_id: str, subsource_id: str, units: str,
                     year_start: int = 1) -> pd.DataFrame:
    """Build the canonical per-curve DataFrame for Ch3 series.

    `year` is a 1-based point index (theoretical curves have no calendar year);
    keeping it as an int column is required by the generic chopped writer.
    """
    n = len(x_values)
    if len(y_values) != n:
        raise ValueError("x_values and y_values must be the same length")
    return pd.DataFrame({
        "year": np.arange(year_start, year_start + n, dtype=int),
        "x_value": x_values.astype(float),
        "value": y_values.astype(float),
        "subseries_id": subseries_id,
        "subsource_id": subsource_id,
        "units": units,
    })


def write_parquet(df: pd.DataFrame, out_path: Path) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
    return len(df)
