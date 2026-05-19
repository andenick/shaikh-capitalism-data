"""L01_S402_load — load Appendix 4.2 Table 4 (per-hour cost columns) for S402.

Reads:
  SalvagedInputs/book_data/Reconstructed/Appendix_4_2_Table4.csv
Writes:
  Technical/data/raw/S402_APPENDIX_4_2_T4.parquet

Per-hour cost columns reproduced: afc, ulc, avc, ac, tc, mc. (afc is shared with
S401; we re-emit here so S402's parquet is self-contained.)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "S402"
SOURCE_ID = "SHAIKH_APPENDIX_4_2"
CSV_PATH = SALVAGED_BOOK_DATA / "Reconstructed" / "Appendix_4_2_Table4.csv"
OUT = DATA_RAW / "S402_APPENDIX_4_2_T4.parquet"

COMPONENTS = ["afc", "ulc", "avc", "ac", "tc", "mc"]
UNITS = "money_units_per_unit_output_illustrative"


def run() -> dict:
    if not CSV_PATH.exists():
        return {"status": "FAIL", "error": f"reconstructed CSV missing: {CSV_PATH}"}
    df = pd.read_csv(CSV_PATH)
    missing = [c for c in COMPONENTS + ["XR"] if c not in df.columns]
    if missing:
        return {"status": "FAIL", "error": f"columns missing in CSV: {missing}"}

    rows = []
    for row_idx, r in df.reset_index(drop=True).iterrows():
        for comp in COMPONENTS:
            v = r[comp]
            rows.append({
                "row_index": int(row_idx),
                "XR": float(r["XR"]),
                "component": comp,
                "value": float(v) if pd.notna(v) else None,
                "source_id": SOURCE_ID,
                "units": UNITS,
                "subseries_id": f"{SERIES_ID}-{comp}",
            })
    out_df = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out_df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": int(len(out_df)),
        "row_index_range": [int(out_df["row_index"].min()), int(out_df["row_index"].max())],
        "components": COMPONENTS,
        "sources_fetched": [SOURCE_ID],
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
