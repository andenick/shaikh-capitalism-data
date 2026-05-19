"""L01_ES2001_load — Shaikh (2020) Tables 1-2 aggregate price/value ratios.

Reads SalvagedInputs/book_data/Reconstructed/ES2001_aggregate_ratios.csv
and emits one long-form parquet with one row per (model, year, aggregate).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "ES2001"
SOURCE_ID = "SHAIKH_2020_SRAFFA_PRICES_T1T2"
CSV_PATH = SALVAGED_BOOK_DATA / "Reconstructed" / "ES2001_aggregate_ratios.csv"
OUT = DATA_RAW / f"{SERIES_ID}_AGG_RATIOS.parquet"

AGGREGATE_COLS = [
    "r_obs", "r_obs_over_R",
    "constant_capital", "variable_capital", "surplus_value",
    "value_added", "rate_surplus_value", "rate_profit",
    "max_rate_profit_R",
]


def run() -> dict:
    if not CSV_PATH.exists():
        return {"status": "FAIL", "error": f"missing CSV: {CSV_PATH}"}
    df = pd.read_csv(CSV_PATH)

    rows = []
    for _, r in df.iterrows():
        model = str(r["model"])
        year = int(r["year"])
        matrix_size = int(r["matrix_size"])
        model_short = "circ" if model.startswith("circ") else "fixed"
        for col in AGGREGATE_COLS:
            if pd.isna(r[col]):
                continue
            rows.append({
                "year": year,
                "value": float(r[col]),
                "subseries_id": f"{SERIES_ID}-{model_short}-{col}",
                "subsource_id": SOURCE_ID,
                "units": "dimensionless_ratio",
                "model": model,
                "aggregate": col,
                "matrix_size": matrix_size,
            })

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_loaded": int(len(out)),
        "year_range": [int(out["year"].min()), int(out["year"].max())],
        "subseries_count": int(out["subseries_id"].nunique()),
        "sources_fetched": [SOURCE_ID],
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
