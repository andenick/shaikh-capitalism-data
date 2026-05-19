"""L01_S401_load — load Appendix 4.2 Table 4 (per-worker cost columns) for S401.

Reads:
  SalvagedInputs/book_data/Reconstructed/Appendix_4_2_Table4.csv
Writes:
  Technical/data/raw/S401_APPENDIX_4_2_T4.parquet

Schema: row_index (int, synthetic 0..20), XR (float, cumulative output),
        component (str), value (float), source_id (str), units (str).

The per-worker cost columns reproduced: afc, ulc_prime, avc_prime, ac_prime,
tc_prime, mc_prime. The XR=0 row keeps afc=70 and tc_prime=70; all other
per-worker cost columns are null at XR=0 (cost-per-unit undefined at zero output).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "S401"
SOURCE_ID = "SHAIKH_APPENDIX_4_2"
CSV_PATH = SALVAGED_BOOK_DATA / "Reconstructed" / "Appendix_4_2_Table4.csv"
OUT = DATA_RAW / "S401_APPENDIX_4_2_T4.parquet"

# Per-worker cost components reproduced in Fig 4.16
COMPONENTS = ["afc", "ulc_prime", "avc_prime", "ac_prime", "tc_prime", "mc_prime"]
UNITS = "money_units_per_unit_output_illustrative"


def run() -> dict:
    if not CSV_PATH.exists():
        return {"status": "FAIL", "error": f"reconstructed CSV missing: {CSV_PATH}"}
    df = pd.read_csv(CSV_PATH)
    missing = [c for c in COMPONENTS + ["XR"] if c not in df.columns]
    if missing:
        return {"status": "FAIL", "error": f"columns missing in CSV: {missing}"}

    # Build long-form per (row_index, component) record.
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
