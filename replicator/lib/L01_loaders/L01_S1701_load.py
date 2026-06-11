"""L01_S1701_load - load Shaikh's HP-smoothed gold-deflated price indexes.

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix5_DATALRprices.xlsx
which is the canonical Appendix 5.3 spreadsheet (same source backs Ch5 series).

Emits three subseries:
  S1701-A US PPI in gold (HP-100 smoothed)   = USPPIGOLDHP100 (1800-2007)
  S1701-B UK PPI in gold (HP-100 smoothed)   = UKPPIGOLDHP100 (covers 1801-2007)
  S1701-C USUKAVGWAVE                        = average-of-past-two-waves overlay
                                                (1983-2025; per Phase 4 the
                                                post-2011 portion is forecast)

Per Phase 4 CH17 adequacy, anwarshaikhecon.org is DEAD; the local salvage
file IS canonical (IA snapshot recorded in registry).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

SERIES_ID = "S1701"
CHOPPED_XLSX = book_data_path("Appendix5_DATALRprices.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_LONGWAVES.parquet"


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}

    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})

    rows = []
    for sub_id, col, label in [
        ("S1701-A", "USPPIGOLDHP100", "US PPI in gold (HP-100)"),
        ("S1701-B", "UKPPIGOLDHP100", "UK PPI in gold (HP-100)"),
        ("S1701-C", "USUKAVGWAVE", "Average of past two waves (data+forecast)"),
    ]:
        sub = df[["Year", col]].dropna()
        for _, r in sub.iterrows():
            yr = int(r["Year"])
            # Mark the post-2011 portion of USUKAVGWAVE as forecast
            is_forecast = (sub_id == "S1701-C") and (yr > 2011)
            rows.append({
                "year": yr,
                "value": float(r[col]),
                "subseries_id": sub_id,
                "subsource_id": "SHAIKH_APPENDIX_5_3_DATALRPRICES",
                "units": "index_dimensionless_HP100_smoothed",
                "is_forecast": bool(is_forecast),
                "label": label,
            })

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_loaded": {
            "S1701-A": int((out["subseries_id"] == "S1701-A").sum()),
            "S1701-B": int((out["subseries_id"] == "S1701-B").sum()),
            "S1701-C": int((out["subseries_id"] == "S1701-C").sum()),
        },
        "year_range": [int(out["year"].min()), int(out["year"].max())],
        "sources_fetched": ["SHAIKH_APPENDIX_5_3_DATALRPRICES"],
        "outputs": [str(OUT)],
        "extension_note": ("Post-2007 US/UK WPI-in-gold extension requires recomputing "
                           "WPI/gold then re-applying HP(100); MeasuringWorth USWP URL "
                           "404; NBER m04051a + BLS WPU00000000 substitute documented. "
                           "Deferred to Phase 9."),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
