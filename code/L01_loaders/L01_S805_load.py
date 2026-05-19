"""L01_S805_load — load Demsetz 1973b Table 4 (CR4 bins x 1963/1969 profit rates).

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_DemsetzRatesOfReturn.xlsx
6 CR4 bins x 2 years = 12 data points.

Writes Technical/data/raw/S805_DEMSETZ_TABLE_4.parquet
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix8_DemsetzRatesOfReturn.xlsx")
OUT = DATA_RAW / "S805_DEMSETZ_TABLE_4.parquet"

BINS = ["10-20", "20-30", "30-40", "40-50", "50-60", "60+"]
YEARS = (1963, 1969)


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=None)
    # Layout: row 0 title, row 1 header (CR4 Ranges, 1963, 1969), rows 2-7 data
    data = raw.iloc[2:8, :3].reset_index(drop=True)
    data.columns = ["cr4_bin", "y1963", "y1969"]
    rows = []
    for _, r in data.iterrows():
        bin_label = str(r["cr4_bin"]).strip()
        for yr, col in ((1963, "y1963"), (1969, "y1969")):
            rows.append({
                "year": int(yr),
                "value": float(r[col]),
                "subseries_id": f"S805-{yr}",
                "source_id": "DEMSETZ_1973B_TABLE_4",
                "units": "percent",
                "cr4_bin": bin_label,
            })
    df = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": int(len(df)),
        "subseries": sorted(df["subseries_id"].unique().tolist()),
        "sources_fetched": ["DEMSETZ_1973B_TABLE_4"],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
