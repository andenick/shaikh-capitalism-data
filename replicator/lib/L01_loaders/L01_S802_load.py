"""L01_S802_load — load Semmler 1984 Table 3.3 (Weston et al. 1974) cross-sections.

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_Semmler19843.3.xlsx
Three CR4 midpoints (20, 50, 80) crossed with three NBER-dated US contractions:
  - 1957-07 to 1958-04 (label: 1957)
  - 1960-01 to 1961-01 (label: 1960)
  - 1969-11 to 1970-11 (label: 1969)

Writes:
  Technical/data/raw/S802_SEMMLER_TABLE_3_3.parquet

Columns: year (int contraction-start), value (percent), subseries_id, source_id, units,
         cr4_midpoint (int)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix8_Semmler19843.3.xlsx")
OUT = DATA_RAW / "S802_SEMMLER_TABLE_3_3.parquet"

CONTRACTION_YEARS = (1957, 1960, 1969)
CONTRACTION_LABELS = {
    1957: "Contraction 7/57-4/58",
    1960: "Contraction 1/60-1/61",
    1969: "Contraction 11/69-11/70",
}
CR4_MIDPOINTS = (20, 50, 80)


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=None)
    # Row 1 contains contraction headers; row 0 is figure title; data rows 2,3,4
    data = raw.iloc[2:5, :].reset_index(drop=True)
    data.columns = ["cr4_midpoint", "C1957", "C1960", "C1969"]
    rows = []
    for _, r in data.iterrows():
        cr = int(float(r["cr4_midpoint"]))
        for yr, col in zip(CONTRACTION_YEARS, ("C1957", "C1960", "C1969")):
            v = float(r[col])
            rows.append({
                "year": int(yr),
                "value": v,
                "subseries_id": f"S802-C{yr}",
                "source_id": "SEMMLER_1984_TABLE_3_3",
                "units": "percent",
                "cr4_midpoint": cr,
            })
    df = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": int(len(df)),
        "subseries": sorted(df["subseries_id"].unique().tolist()),
        "sources_fetched": ["SEMMLER_1984_TABLE_3_3"],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
