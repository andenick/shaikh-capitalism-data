"""L01_S211_load - US and UK Wholesale Price Indexes, 1780-1940 (Fig 2.11, log scale).

Windowed view of S210 truncated at 1940 by analytical design. We source from
CD2's S022 (the 1790-1940 window), which matches Jastram (1977) Table 2/Table 7.

No extension by design (per Phase 4 adequacy and dossier).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_EXT_BENCH  # noqa: E402

S022_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S022_us_and_uk_wholesale_price_indexes_1790_1940.xlsx"
OUT_US = DATA_RAW / "S211_US_WPI_1790_1940.parquet"
OUT_UK = DATA_RAW / "S211_UK_WPI_1790_1940.parquet"


def run() -> dict:
    if not S022_XLSX.exists():
        return {"status": "FAIL", "error": f"S022 missing: {S022_XLSX}"}
    df = pd.read_excel(S022_XLSX, sheet_name="Data").rename(columns={"Year": "year"})
    df = df.dropna(subset=["year"]).astype({"year": int})
    df = df[(df["year"] >= 1780) & (df["year"] <= 1940)]
    us = df[["year", "S022-A"]].rename(columns={"S022-A": "value"}).dropna(subset=["value"]).copy()
    us["units"] = "index_1930=100"
    us["subseries_id"] = "S211-A"
    us["subsource_id"] = "JASTRAM_1977_T7_US_WPI"
    uk = df[["year", "S022-B"]].rename(columns={"S022-B": "value"}).dropna(subset=["value"]).copy()
    uk["units"] = "index_1930=100"
    uk["subseries_id"] = "S211-B"
    uk["subsource_id"] = "JASTRAM_1977_T2_UK_WPI"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    us.to_parquet(OUT_US, index=False)
    uk.to_parquet(OUT_UK, index=False)
    return {
        "status": "OK",
        "rows_loaded": {"US_WPI": len(us), "UK_WPI": len(uk)},
        "sources_fetched": ["JASTRAM_1977_T7_US_WPI", "JASTRAM_1977_T2_UK_WPI"],
        "extension_status": "not_applicable_windowed",
        "outputs": [str(OUT_US), str(OUT_UK)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
