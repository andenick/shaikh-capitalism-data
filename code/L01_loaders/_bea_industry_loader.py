"""Shared helper for S1502/S1503 - read the BEA GDP-by-Industry chopped table.

The same Appendix15_USGDPRByIndustry.xlsx supplies both panels. Splitting
the panel assignment into a helper avoids duplicate parse code.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

# Industry labels as they appear in the BEA chopped table header (row 1 of multi-index)
PANEL_A_INDUSTRIES = [
    "Agriculture, forestry, fishing, and hunting",
    "Mining",
    "Utilities",
    "Construction",
    "Durable Mfg. goods",
    "Nondurable Mfg. goods",
    "Wholesale trade",
    "Retail trade",
]
PANEL_B_INDUSTRIES = [
    "Transportation and warehousing",
    "Information",
    "Finance, insurance, real estate, rental, and leasing",
    "Professional and business services",
    "Educational services, health care, and social assistance",
    "Arts, entertainment, recreation, accommodation, and food services",
    "Other services, except government",
    "Federal government",
    "State and local government",
]
ALL_INDUSTRIES_LABEL = "All industries"


def load_chopped_levels_and_growth(xlsx_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (levels_df, growth_df), both indexed by year, columns = industry labels.

    Levels are BEA chain-type quantity indices (2005=100 vintage).
    Growth are Shaikh's precomputed log-differences (used as validation ground truth).
    """
    raw = pd.read_excel(xlsx_path, sheet_name="Data", header=[0, 1])
    # The first column is Year; relabel
    raw.columns = [
        ("Year", "Year") if str(c[1]).strip() == "Year" else (str(c[0]).strip(), str(c[1]).strip())
        for c in raw.columns
    ]
    raw = raw.dropna(subset=[("Year", "Year")])
    raw[("Year", "Year")] = pd.to_numeric(raw[("Year", "Year")], errors="coerce")
    raw = raw.dropna(subset=[("Year", "Year")])
    raw[("Year", "Year")] = raw[("Year", "Year")].astype(int)

    years = raw[("Year", "Year")].values
    level_cols = [c for c in raw.columns if c[0] == "BEA"]
    growth_cols = [c for c in raw.columns if c[0] == "Calculated Growth Rate"]

    levels = pd.DataFrame({c[1]: raw[c].values for c in level_cols}, index=years)
    growth = pd.DataFrame({c[1]: raw[c].values for c in growth_cols}, index=years)
    levels.index.name = "year"
    growth.index.name = "year"
    return levels, growth


def panel_to_long(
    levels: pd.DataFrame,
    growth: pd.DataFrame,
    industries: list[str],
    series_id: str,
    subsource_id: str,
    include_all_ref: bool = True,
) -> pd.DataFrame:
    """Build a long-form DataFrame with year, value (growth rate), subseries_id, source_id, units.

    Recomputes growth rates from levels using simple percent change
    `(x_t - x_{t-1}) / x_{t-1}` to match Shaikh's book convention (verified
    against Appendix15_USGDPRByIndustry.xlsx Calculated Growth Rate columns).
    """
    rows = []
    industries_with_ref = list(industries)
    if include_all_ref and ALL_INDUSTRIES_LABEL not in industries_with_ref:
        industries_with_ref = [ALL_INDUSTRIES_LABEL] + industries_with_ref

    for ind in industries_with_ref:
        if ind not in levels.columns:
            continue
        lvl = levels[ind]
        # Shaikh uses simple percent change, not log-difference
        recomputed = (lvl - lvl.shift(1)) / lvl.shift(1)
        for y in lvl.index:
            g_recomputed = float(recomputed.loc[y]) if not pd.isna(recomputed.loc[y]) else None
            g_book = float(growth.loc[y, ind]) if ind in growth.columns and not pd.isna(growth.loc[y, ind]) else None
            # Prefer recomputed; fall back to book if recomputed is NaN
            value = g_recomputed if g_recomputed is not None else g_book
            if value is None:
                continue
            sub_id = f"{series_id}-{_industry_slug(ind, ind == ALL_INDUSTRIES_LABEL)}"
            rows.append({
                "year": int(y),
                "value": value,
                "subseries_id": sub_id,
                "source_id": subsource_id,
                "units": "rate_decimal_log_diff",
                "industry": ind,
            })
    return pd.DataFrame(rows)


_INDUSTRY_SLUG = {
    "All industries": "ALL",
    "Agriculture, forestry, fishing, and hunting": "AGRI",
    "Mining": "MINE",
    "Utilities": "UTIL",
    "Construction": "CONS",
    "Durable Mfg. goods": "DURMFG",
    "Nondurable Mfg. goods": "NONDURMFG",
    "Wholesale trade": "WHOLE",
    "Retail trade": "RETAIL",
    "Transportation and warehousing": "TRANS",
    "Information": "INFO",
    "Finance, insurance, real estate, rental, and leasing": "FIRE",
    "Professional and business services": "PROF",
    "Educational services, health care, and social assistance": "EDUHEALTH",
    "Arts, entertainment, recreation, accommodation, and food services": "ARTSFOOD",
    "Other services, except government": "OTHERSVC",
    "Federal government": "FEDGOV",
    "State and local government": "SLGOV",
}


def _industry_slug(label: str, is_ref: bool) -> str:
    return _INDUSTRY_SLUG.get(label, label.split(",")[0].split(" ")[0].upper()[:6])
