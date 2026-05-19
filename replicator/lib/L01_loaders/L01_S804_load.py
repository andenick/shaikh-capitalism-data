"""L01_S804_load — load Stigler 1963 Table 17 (concentrated vs unconcentrated profit rates).

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_StiglerRatesOfProfit.xlsx
Six time bins x two industry groups = 12 data points. Plus an "Average" row that is
NOT loaded into the time series but is preserved as a sanity-check informational note.

Writes Technical/data/raw/S804_STIGLER_TABLE_17.parquet

Year label per bin uses the integer floor of bin midpoint:
  1939-41 -> 1940
  1942-44 -> 1943
  1945-47 -> 1946
  1948-50 -> 1949
  1951-54 -> 1952 (int floor of 1952.5)
  1955-57 -> 1956
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix8_StiglerRatesOfProfit.xlsx")
OUT = DATA_RAW / "S804_STIGLER_TABLE_17.parquet"

BINS = [
    ("1939-41", 1939, 1941, 1940),
    ("1942-44", 1942, 1944, 1943),
    ("1945-47", 1945, 1947, 1946),
    ("1948-50", 1948, 1950, 1949),
    ("1951-54", 1951, 1954, 1952),
    ("1955-57", 1955, 1957, 1956),
]


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=None)
    # Layout: row 0 title, row 1 headers, rows 2-7 data, row 8 Average
    data = raw.iloc[2:8, :3].reset_index(drop=True)
    data.columns = ["time_period", "unconc", "conc"]
    rows = []
    by_label = {row["time_period"]: row for _, row in data.iterrows()}
    for label, bstart, bend, ylabel in BINS:
        if label not in by_label:
            return {"status": "FAIL", "error": f"missing bin {label} in xlsx"}
        r = by_label[label]
        rows.append({
            "year": int(ylabel), "value": float(r["unconc"]),
            "subseries_id": "S804-UNCONC", "source_id": "STIGLER_1963_TABLE_17",
            "units": "percent", "bin_label": label, "bin_start": bstart, "bin_end": bend,
        })
        rows.append({
            "year": int(ylabel), "value": float(r["conc"]),
            "subseries_id": "S804-CONC", "source_id": "STIGLER_1963_TABLE_17",
            "units": "percent", "bin_label": label, "bin_start": bstart, "bin_end": bend,
        })
    df = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)

    # Sanity check: computed group means vs Stigler's reported averages
    mean_unconc = df.loc[df["subseries_id"] == "S804-UNCONC", "value"].mean()
    mean_conc = df.loc[df["subseries_id"] == "S804-CONC", "value"].mean()
    stigler_avg_row = raw.iloc[8, :3].tolist()
    sanity = {
        "computed_mean_unconc": round(float(mean_unconc), 6),
        "computed_mean_conc": round(float(mean_conc), 6),
        "stigler_published_avg_row": [str(x) for x in stigler_avg_row],
        "book_reported_unconc_pct": 6.9,
        "book_reported_conc_pct": 7.1,
    }
    return {
        "status": "OK",
        "rows_loaded": int(len(df)),
        "subseries": sorted(df["subseries_id"].unique().tolist()),
        "sources_fetched": ["STIGLER_1963_TABLE_17"],
        "sanity_check": sanity,
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
