"""L01_S1606_load - Household Debt-Service Ratio (Ch16 Fig 16.10).

Reads Shaikh Appendix 16 HouseholdDebtService (quarterly 1980Q1-2012Q4) and
emits one parquet per published subseries:
  * S1606-A  Financial Obligations Ratio (FOR), quarterly decimal
  * S1606-B  Debt Service Ratio          (DSR), quarterly decimal

PHASE 4 DUAL-CADENCE EMISSION: P02 produces a quarterly sidecar plus the
annual-average primary parquet so the canonical Ch16 cadence is preserved
and the book-faithful quarterly view is available downstream.

Extension subseries (S1606-C FRED FODSP, S1606-D FRED TDSP) deferred to
Phase 6; book period is the Phase 5 priority.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch16_helpers import read_appendix16_debt_service  # noqa: E402

SERIES_ID = "S1606"
BOOK_START = 1980
BOOK_END = 2012

OUTPUTS = {
    "S1606-A": (DATA_RAW / "S1606_FOR.parquet",
                "Financial obligations ratio, seasonally adjusted",
                "decimal_quarterly"),
    "S1606-B": (DATA_RAW / "S1606_DSR.parquet",
                "Debt service ratio, seasonally adjusted",
                "decimal_quarterly"),
}


def _save(df: pd.DataFrame, col: str, out: Path, subseries_id: str, units: str) -> int:
    sub = df[["year", "quarter", "qdate", col]].rename(columns={col: "value"})
    sub = sub.dropna(subset=["value"])
    sub = sub[(sub["year"] >= BOOK_START) & (sub["year"] <= BOOK_END)].copy()
    sub["units"] = units
    sub["subseries_id"] = subseries_id
    sub["subsource_id"] = "SHAIKH_APPENDIX_16_2"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(out, index=False)
    return int(len(sub))


def run() -> dict:
    panel = read_appendix16_debt_service()
    rows: dict[str, int] = {}
    for sid, (path, col, units) in OUTPUTS.items():
        rows[sid] = _save(panel, col, path, sid, units)
    return {
        "status": "OK",
        "rows_loaded": rows,
        "sources_fetched": ["SHAIKH_APPENDIX_16_2"],
        "extension_status": "deferred_to_phase6",
        "extension_note": ("S1606-C (FRED FODSP) and S1606-D (FRED TDSP) "
                           "extension deferred to Phase 6; remember to "
                           "convert FRED percent -> decimal at splice."),
        "outputs": [str(p) for (p, _, _) in OUTPUTS.values()],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
