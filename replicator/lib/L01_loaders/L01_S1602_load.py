"""L01_S1602_load - Hourly Real Wages and Productivity, US Business Sector.

Reads Shaikh Appendix 16 WageProdData and emits one parquet per subseries:
  * S1602-A  Productivity 1982=100        (1947-2012)
  * S1602-B  Real Hrly EC 1982=100        (1947-2012)
  * S1602-C  Adj Real Hrly EC (ec_c)      (counterfactual, 1947-2012)
  * S1602-G  Productivity 1958=100        (cross-cadence variant)
  * S1602-H  Real Hrly EC 1958=100        (cross-cadence variant)

Extension (FRED OPHNFB / COMPRNFB rebased to 1982=100, plus re-run of
counterfactual regression) is deferred to Phase 6: book-period reproduction
is Phase 5 priority per Ch16 fanout direction.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch16_helpers import read_appendix16_wage_prod  # noqa: E402

SERIES_ID = "S1602"
BOOK_START = 1947
BOOK_END = 2012

OUTPUTS = {
    "S1602-A": (DATA_RAW / "S1602_Prod1982.parquet",
                "Productivity 1982=100", "index_1982=100"),
    "S1602-B": (DATA_RAW / "S1602_RealHrlyEC1982.parquet",
                "Real Hrly EC 1982=100", "index_1982=100"),
    "S1602-C": (DATA_RAW / "S1602_AdjRealHrlyEC.parquet",
                "Adj Real Hrly EC", "index_1982=100"),
    "S1602-G": (DATA_RAW / "S1602_Prod1958.parquet",
                "Productivity 1958=100", "index_1958=100"),
    "S1602-H": (DATA_RAW / "S1602_RealHrlyEC1958.parquet",
                "Real Hrly EC 1958=100", "index_1958=100"),
}


def _save(df: pd.DataFrame, col: str, out: Path, subseries_id: str, units: str) -> int:
    sub = df[["year", col]].rename(columns={col: "value"}).dropna(subset=["value"])
    sub = sub[(sub["year"] >= BOOK_START) & (sub["year"] <= BOOK_END)].copy()
    sub["units"] = units
    sub["subseries_id"] = subseries_id
    sub["subsource_id"] = "SHAIKH_APPENDIX_16_2"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(out, index=False)
    return int(len(sub))


def run() -> dict:
    panel = read_appendix16_wage_prod()
    rows: dict[str, int] = {}
    for sid, (path, col, units) in OUTPUTS.items():
        rows[sid] = _save(panel, col, path, sid, units)
    return {
        "status": "OK",
        "rows_loaded": rows,
        "sources_fetched": ["SHAIKH_APPENDIX_16_2"],
        "extension_status": "deferred_to_phase6",
        "extension_note": ("FRED OPHNFB+COMPRNFB rebase + counterfactual regression "
                           "deferred to Phase 6 sensitivity; Phase 5 reproduces "
                           "Appendix 16.2 columns exactly."),
        "outputs": [str(p) for (p, _, _) in OUTPUTS.values()],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
