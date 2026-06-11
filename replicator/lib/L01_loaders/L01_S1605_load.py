"""L01_S1605_load - Household Debt-to-Income Ratio (Ch16 Fig 16.9).

Reads Shaikh Appendix 16 DebtIncRatio and emits one parquet per published
subseries:
  * S1605-A  HHDebt         (book period, billions USD)
  * S1605-B  HHDispPersInc  (book period, billions USD SAAR)
  * S1605-C  HHDebtIncRatio (book period, decimal)

PHASE 4 CANONICAL SUBSTITUTION (RATIFIED): the extension subseries (S1605-D,
-E, -F) replace CD2's CMDEBT/PI wrong-concept proxies with HCCSDODNS/DPI
matching Shaikh's stated book spec (Z.1 D.3 line 2 + NIPA T2.1 line 27).
Extension is deferred to Phase 6.  See P02_S1605_construct.py for the
unit-conversion dimensional-analysis comment that pins down the
ratio = HCCSDODNS_millions / (DPI_billions * 1000) recipe.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch16_helpers import read_appendix16_debt_inc_ratio  # noqa: E402

SERIES_ID = "S1605"
BOOK_START = 1975
BOOK_END = 2012

OUTPUTS = {
    "S1605-A": (DATA_RAW / "S1605_HHDebt.parquet",
                "HHDebt", "billions_usd"),
    "S1605-B": (DATA_RAW / "S1605_DPI.parquet",
                "HHDispPersInc", "billions_usd_saar"),
    "S1605-C": (DATA_RAW / "S1605_Ratio.parquet",
                "HHDebtIncRatio", "decimal_ratio"),
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
    panel = read_appendix16_debt_inc_ratio()
    rows: dict[str, int] = {}
    for sid, (path, col, units) in OUTPUTS.items():
        rows[sid] = _save(panel, col, path, sid, units)
    return {
        "status": "OK",
        "rows_loaded": rows,
        "sources_fetched": ["SHAIKH_APPENDIX_16_2"],
        "extension_status": "deferred_to_phase6",
        "extension_note": ("S1605-D (FRED HCCSDODNS millions) + S1605-E (FRED DPI "
                           "billions) + S1605-F (computed ratio with explicit unit "
                           "conversion HCCSDODNS_millions / (DPI_billions * 1000)) "
                           "deferred to Phase 6.  Substitution from CD2 CMDEBT/PI "
                           "ratified by Phase 4 to restore Shaikh's Z.1 D.3 line 2 "
                           "+ NIPA T2.1 line 27 book spec."),
        "outputs": [str(p) for (p, _, _) in OUTPUTS.values()],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
