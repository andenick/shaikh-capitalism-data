"""L01_S210 - US and UK Wholesale Price Indexes, 1780-2010 (Fig 2.10, log scale).

Composite series with NO Appendix 2 chopped table. Per Phase 4 decision 0005,
we use the CD2-preserved consolidated data (S023, two columns US+UK both 1930=100)
as the salvaged book replica until the Jastram (1977) replica is hosted.

Design (folded A/B): both the US book series and its BLS-PPI extension live in the
CD2-preserved S023-A column (subsource JASTRAM_1977_T7_PLUS_BLS_PPI_EXT); UK is
S023-B (JASTRAM_1977_T2_PLUS_ONS_PLLU). The US column is capped at the last
complete calendar year (2026 is a partial-year annual mean and is dropped). The
legacy separate FRED WPU00000000 S210-C path was removed (DF-2, 2026-07-02): it
never appeared in the shipped chopped and only diverged code from output.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_EXT_BENCH  # noqa: E402

SALVAGED_USUK_WPI_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S023_us_and_uk_wholesale_price_indexes_1790_2010.xlsx"
OUT_US = DATA_RAW / "S210_US_WPI_BOOK.parquet"
OUT_UK = DATA_RAW / "S210_UK_WPI_BOOK.parquet"

# Last COMPLETE calendar year for the US BLS-PPI annual-average extension. The
# CD2-preserved S023-A column carries a partial-year 2026 value (an incomplete
# annual mean); it is capped so the shipped series ends on a full realized year.
# (T3.4/DF-2, 2026-07-02.)
LAST_COMPLETE_YEAR_US = 2025


def _load_s023() -> pd.DataFrame:
    df = pd.read_excel(SALVAGED_USUK_WPI_XLSX, sheet_name="Data")
    df = df.rename(columns={"Year": "year"})
    return df.dropna(subset=["year"]).astype({"year": int})


def run() -> dict:
    if not SALVAGED_USUK_WPI_XLSX.exists():
        return {"status": "FAIL", "error": f"S023 missing: {SALVAGED_USUK_WPI_XLSX}"}
    raw = _load_s023()
    us = raw[["year", "S023-A"]].rename(columns={"S023-A": "value"}).dropna(subset=["value"]).copy()
    # Cap the US column at the last complete calendar year (drop partial-year 2026).
    us = us[us["year"] <= LAST_COMPLETE_YEAR_US].copy()
    us["units"] = "index_1930=100"
    us["subseries_id"] = "S210-A"
    us["subsource_id"] = "JASTRAM_1977_T7_PLUS_BLS_PPI_EXT"
    uk = raw[["year", "S023-B"]].rename(columns={"S023-B": "value"}).dropna(subset=["value"]).copy()
    uk["units"] = "index_1930=100"
    uk["subseries_id"] = "S210-B"
    uk["subsource_id"] = "JASTRAM_1977_T2_PLUS_ONS_PLLU"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    us.to_parquet(OUT_US, index=False)
    uk.to_parquet(OUT_UK, index=False)
    # NOTE (DF-2, 2026-07-02): the legacy FRED WPU00000000 S210-C extension path was
    # removed. The shipped design is folded-A/B: the US BLS-PPI extension is already
    # embedded in the CD2-preserved S023-A column (subsource JASTRAM_1977_T7_PLUS_BLS_PPI_EXT),
    # so a separate S210-C FRED subseries was never in the chopped and only diverged the
    # code from the shipped output.
    return {
        "status": "OK",
        "rows_loaded": {"US_WPI": len(us), "UK_WPI": len(uk)},
        "sources_fetched": ["JASTRAM_1977_T7_PLUS_BLS_PPI_EXT", "JASTRAM_1977_T2_PLUS_ONS_PLLU"],
        "us_capped_at": LAST_COMPLETE_YEAR_US,
        "outputs": [str(OUT_US), str(OUT_UK)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
