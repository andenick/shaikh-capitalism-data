"""L01_S1601_load - US and UK Golden Waves long-run prices (Ch16 Fig 16.1).

Reads Shaikh Appendix 5 DATALRprices workbook and emits one parquet per
subseries:
  * S1601-A  USGoldWaveDetrended  (book-period 1786-2010, deviation 1930=100)
  * S1601-B  UKGoldWaveDetrended  (book-period 1786-2010, deviation 1930=100)
  * S1601-C  USPPIGold raw ratio (USWPI/USGoldprice) for cubic-trend re-fit
  * S1601-D  UKPPIGold raw ratio (UKWPI/UKGoldprice) for cubic-trend re-fit

Extension (FRED PPIACO + GOLDPMGBD228NLBM, ONS K646) is deferred to Phase 6
sensitivity: book-period reproduction (MAE=0 vs Appendix 5.3 columns) is the
Phase 5 priority per Ch16 fanout direction.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch16_helpers import read_appendix5_lrprices  # noqa: E402

SERIES_ID = "S1601"
BOOK_START = 1786
BOOK_END = 2010

OUT_A = DATA_RAW / "S1601_USGoldWaveDetrended.parquet"
OUT_B = DATA_RAW / "S1601_UKGoldWaveDetrended.parquet"
OUT_C = DATA_RAW / "S1601_USPPIGold.parquet"
OUT_D = DATA_RAW / "S1601_UKPPIGold.parquet"


def _save(df: pd.DataFrame, col: str, out: Path, subseries_id: str,
          subsource_id: str, units: str) -> int:
    sub = df[["year", col]].rename(columns={col: "value"}).dropna(subset=["value"])
    sub = sub[(sub["year"] >= BOOK_START) & (sub["year"] <= BOOK_END)].copy()
    sub["units"] = units
    sub["subseries_id"] = subseries_id
    sub["subsource_id"] = subsource_id
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(out, index=False)
    return int(len(sub))


def run() -> dict:
    panel = read_appendix5_lrprices()
    n_a = _save(panel, "USGoldWaveDetrended", OUT_A, "S1601-A",
                "SHAIKH_APPENDIX_5", "deviation_1930=100")
    n_b = _save(panel, "UKGoldWaveDetrended", OUT_B, "S1601-B",
                "SHAIKH_APPENDIX_5", "deviation_1930=100")
    n_c = _save(panel, "USPPIGold", OUT_C, "S1601-C",
                "SHAIKH_APPENDIX_5", "ratio_wpi_per_gold")
    n_d = _save(panel, "UKPPIGold", OUT_D, "S1601-D",
                "SHAIKH_APPENDIX_5", "ratio_wpi_per_gold")
    return {
        "status": "OK",
        "rows_loaded": {"USGoldWaveDetrended": n_a, "UKGoldWaveDetrended": n_b,
                         "USPPIGold": n_c, "UKPPIGold": n_d},
        "sources_fetched": ["SHAIKH_APPENDIX_5"],
        "extension_status": "deferred_to_phase6",
        "extension_note": ("FRED PPIACO + GOLDPMGBD228NLBM + ONS K646 extension "
                           "deferred per Ch16 fanout direction; book-period "
                           "reproduction is Phase 5 priority."),
        "outputs": [str(OUT_A), str(OUT_B), str(OUT_C), str(OUT_D)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
