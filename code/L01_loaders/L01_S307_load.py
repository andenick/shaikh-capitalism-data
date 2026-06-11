"""L01_S307_load — loader for S307 (cross_sectional).

See Technical/docs/series/S307_DPR.md for full documentation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "S307"
OUT = DATA_RAW / f"{SERIES_ID}_CROSS_SECTION.parquet"
SUBSERIES = f"{SERIES_ID}-A"
SUBSOURCE = "ALLEN_BOWLEY_1935_TABLE1"
UNITS = "shillings_per_week_food_expenditure"

CANDIDATE_PATHS = [
    SALVAGED_BOOK_DATA / "AllenBowley1935_Table1.csv",
    SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix3_AllenBowley1904.xlsx",
    SALVAGED_BOOK_DATA / "UK_BoT_1908_Cd3864_workingclass_budgets.csv",
]

AXIS_X_MIN, AXIS_X_MAX = 0.0, 60.0     # shillings/week income
AXIS_Y_MIN, AXIS_Y_MAX = 0.0, 35.0     # shillings/week food expenditure


def _maybe_load_tabulation() -> pd.DataFrame | None:
    for p in CANDIDATE_PATHS:
        if p.exists():
            try:
                if p.suffix == ".csv":
                    tab = pd.read_csv(p)
                else:
                    tab = pd.read_excel(p)
                if {"income_shillings", "food_shillings"}.issubset(tab.columns):
                    return tab.rename(columns={
                        "income_shillings": "x_value",
                        "food_shillings": "value",
                    })[["x_value", "value"]]
            except Exception:
                continue
    return None


def run() -> dict:
    tab = _maybe_load_tabulation()
    if tab is None:
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
            "note": "Allen & Bowley Table 1 not in SalvagedInputs/; metadata row only. No synthetic interpolation.",
        }
    df = tab.copy()
    df["year"] = 1904
    df["subseries_id"] = SUBSERIES
    df["subsource_id"] = SUBSOURCE
    df["units"] = UNITS
    df = df[["year", "x_value", "value", "subseries_id", "subsource_id", "units"]]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {"status": "OK", "data_status": "loaded_from_tabulation",
            "rows_loaded": {"observations": int(len(df))},
            "sources_fetched": [SUBSOURCE], "outputs": [str(OUT)]}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
