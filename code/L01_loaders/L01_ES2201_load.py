"""L01_ES2201_load — Shaikh-Jacobo (2020) Table 1 five-parameter panel."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "ES2201"
SOURCE_ID = "SHAIKH_JACOBO_2020_TABLE1"
CSV_PATH = SALVAGED_BOOK_DATA / "Reconstructed" / "ES2201_fitted_parameters.csv"
OUT = DATA_RAW / f"{SERIES_ID}_TABLE1.parquet"

PARAMS = [
    ("G_prime", "G_prime", "dimensionless"),
    ("r_mean", "r_mean", "thousands_usd"),
    ("w_mean", "w_mean", "thousands_usd"),
    ("f_top3", "f_top3", "dimensionless"),
    ("alpha", "alpha", "dimensionless"),
]


def run() -> dict:
    if not CSV_PATH.exists():
        return {"status": "FAIL", "error": f"missing CSV: {CSV_PATH}"}
    df = pd.read_csv(CSV_PATH)
    rows = []
    for _, r in df.iterrows():
        year = int(r["year"])
        for col, key, units in PARAMS:
            v = r[col]
            if pd.isna(v):
                continue
            rows.append({
                "year": year,
                "value": float(v),
                "subseries_id": f"{SERIES_ID}-{key}",
                "subsource_id": SOURCE_ID,
                "units": units,
                "parameter": key,
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
