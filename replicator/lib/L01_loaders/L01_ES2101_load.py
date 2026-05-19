"""L01_ES2101_load — Shaikh-Coronado-Nassif-Pires (2020) headline summary stats."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "ES2101"
SOURCE_ID = "SHAIKH_CORONADO_NASSIF_2020_S5_SUMMARY"
CSV_PATH = SALVAGED_BOOK_DATA / "Reconstructed" / "ES2101_summary_statistics.csv"
OUT = DATA_RAW / f"{SERIES_ID}_SUMMARY_STATS.parquet"


def run() -> dict:
    if not CSV_PATH.exists():
        return {"status": "FAIL", "error": f"missing CSV: {CSV_PATH}"}
    df = pd.read_csv(CSV_PATH)
    rows = []
    for _, r in df.iterrows():
        stat = str(r["statistic"])
        rows.append({
            "year": int(r["year"]),
            "value": float(r["value"]),
            "subseries_id": f"{SERIES_ID}-{stat}",
            "subsource_id": SOURCE_ID,
            "units": str(r["units"]),
            "statistic": stat,
        })
    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {"status": "OK", "rows_loaded": int(len(out)),
            "sources_fetched": [SOURCE_ID], "output": str(OUT)}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
