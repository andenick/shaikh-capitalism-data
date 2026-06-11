"""L01_S1604_load - Net Average and Real Incremental Profit Rates (Ch16 Fig 16.8).

Reads Shaikh Appendix 16 ProfitRates and emits one parquet per published
subseries.  The HP100 lambda is pinned at 100 (Shaikh's choice for annual
data); see _ch16_helpers.HP_LAMBDA_ANNUAL_CH16.

Subseries:
  * S1604-A  Net Corporate Rate of Profit                   (rcorp - i)
  * S1604-B  Net Incremental Real Corporate Rate of Profit  (raw)
  * S1604-C  Net Incremental Real Corporate Rate (HP100)
  * S1604-D  Net Incremental Real Corporate Rate (HP100 lag(1))
  * S1604-E  Counterfactual Rate of Profit                  (rcorpalt)

Extension subseries (S1604-F, -G) re-derive from S0608 + FRED TB3MS + S1602
ec_c; deferred to Phase 6 per Ch16 fanout direction.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch16_helpers import (  # noqa: E402
    read_appendix16_profit_rates, HP_LAMBDA_ANNUAL_CH16,
)

SERIES_ID = "S1604"
BOOK_START = 1946
BOOK_END = 2011

# Module-level HP lambda constant per Phase 4 ratification (Shaikh's choice
# for annual data; Ravn-Uhlig 6.25 documented as sensitivity-only variant).
HP_LAMBDA = HP_LAMBDA_ANNUAL_CH16  # == 100

OUTPUTS = {
    "S1604-A": (DATA_RAW / "S1604_NetCorp.parquet",
                "Net Corporate Rate of Profit", "decimal_rate"),
    "S1604-B": (DATA_RAW / "S1604_NetIncRealCorp.parquet",
                "Net Incremental Real Corporate Rate of Profit", "decimal_rate"),
    "S1604-C": (DATA_RAW / "S1604_NetIncRealCorpHP100.parquet",
                "Net Incremental Real Corporate Rate of Profit (HP100)",
                "decimal_rate_hp100"),
    "S1604-D": (DATA_RAW / "S1604_NetIncRealCorpHP100Lag1.parquet",
                "Net Incremental Real Corporate Rate of Profit (HP100 lag(1))",
                "decimal_rate_hp100_lag1"),
    "S1604-E": (DATA_RAW / "S1604_RcorpAlt.parquet",
                "Counterfactual Rate of Profit", "decimal_rate"),
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
    assert HP_LAMBDA == 100, "Ch16 HP lambda must be 100 (Shaikh's annual choice)"
    panel = read_appendix16_profit_rates()
    rows: dict[str, int] = {}
    for sid, (path, col, units) in OUTPUTS.items():
        rows[sid] = _save(panel, col, path, sid, units)
    return {
        "status": "OK",
        "rows_loaded": rows,
        "sources_fetched": ["SHAIKH_APPENDIX_16_2"],
        "hp_lambda": HP_LAMBDA,
        "extension_status": "deferred_to_phase6",
        "extension_note": ("S1604-F (S0608 + FRED TB3MS extension) and S1604-G "
                           "(rcorpalt with S1602 ec_c extension) deferred to "
                           "Phase 6; book-period values read directly from "
                           "Appendix 16.2 columns."),
        "outputs": [str(p) for (p, _, _) in OUTPUTS.values()],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
