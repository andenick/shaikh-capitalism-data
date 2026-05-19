"""L01_S306_load — loader for S306 (cross_sectional).

See Technical/docs/series/S306_DPR.md for full documentation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "S306"
OUT = DATA_RAW / f"{SERIES_ID}_CROSS_SECTION.parquet"
SUBSERIES = f"{SERIES_ID}-A"
SUBSOURCE = "ALLEN_BOWLEY_1935_TABLE1"
UNITS = "pct_total_weekly_expenditure_on_food"

CANDIDATE_PATHS = [
    SALVAGED_BOOK_DATA / "AllenBowley1935_Table1.csv",
    SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix3_AllenBowley1904.xlsx",
    SALVAGED_BOOK_DATA / "UK_BoT_1908_Cd3864_workingclass_budgets.csv",
]

# Printed-figure axis bounds (Fig 3.8 in Shaikh 2016 p. 95). These are NOT
# observation values; they are the verifiable range bounds that the loader
# records as metadata when no underlying tabulation has been digitised.
AXIS_X_MIN, AXIS_X_MAX = 0.0, 60.0    # shillings/week income
AXIS_Y_MIN, AXIS_Y_MAX = 56.0, 70.0   # percent food expenditure


def _maybe_load_tabulation() -> pd.DataFrame | None:
    """Return DataFrame[x_value, value] if a tabulation is present, else None."""
    for p in CANDIDATE_PATHS:
        if p.exists():
            # Schema expected (future): columns income_shillings, food_share_pct
            try:
                if p.suffix == ".csv":
                    tab = pd.read_csv(p)
                else:
                    tab = pd.read_excel(p)
                if {"income_shillings", "food_share_pct"}.issubset(tab.columns):
                    return tab.rename(columns={
                        "income_shillings": "x_value",
                        "food_share_pct": "value",
                    })[["x_value", "value"]]
            except Exception:
                continue
    return None


def run() -> dict:
    tab = _maybe_load_tabulation()
    if tab is None:
        # Emit metadata-only parquet
        df = pd.DataFrame({
            "year": [1904],
            "x_value": [np.nan],
            "value": [np.nan],
            "subseries_id": [SUBSERIES],
            "subsource_id": [SUBSOURCE],
            "units": [UNITS],
        })
        OUT.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(OUT, index=False)
        return {
            "status": "OK",
            "data_status": "data_unavailable_pending_digitization",
            "rows_loaded": {"observations": 0, "metadata_rows": 1},
            "sources_fetched": [SUBSOURCE],
            "outputs": [str(OUT)],
            "axis_bounds": {"x": [AXIS_X_MIN, AXIS_X_MAX], "y": [AXIS_Y_MIN, AXIS_Y_MAX]},
            "note": ("Allen & Bowley (1935) Table 1 not in SalvagedInputs/; loader emitted metadata row only. "
                     "Per anu-framework: no synthetic interpolation. Future: library scan of Cd. 3864 (1908) preferred."),
        }
    # Real tabulation found
    df = tab.copy()
    df["year"] = 1904
    df["subseries_id"] = SUBSERIES
    df["subsource_id"] = SUBSOURCE
    df["units"] = UNITS
    df = df[["year", "x_value", "value", "subseries_id", "subsource_id", "units"]]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "data_status": "loaded_from_tabulation",
        "rows_loaded": {"observations": int(len(df))},
        "sources_fetched": [SUBSOURCE],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
