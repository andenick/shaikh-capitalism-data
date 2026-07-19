"""L01_S1603 - US and OECD Short-Term Interest Rates (Ch16 Fig 16.7).

Emits one parquet per published subseries:
  * S1603-A  US    3-month T-Bill rate (decimal, annual avg, 1960-2011)
  * S1603-B  OECD  (Ragab-Shaikh weighted avg, decimal rate, 1960-2012)
  * S1603-C  EU    (Euro-area aggregate, decimal rate, where present)

SOURCE CORRECTION (P2.6 / F-P2.1-01, 2026-07-10)
------------------------------------------------
S1603-A is the US **3-month T-Bill** rate the book plots in Fig 16.6 and Fig
16.7 ("the 3-month T-Bill interest rate in the United States ... 14.03% in 1981
... As of 2011 the US rate stood at 0.0006 (i.e., 0.06%)", KB ch16 L390-392,
L465-466, L483-484). It is now read from Shaikh's own Appendix 16 ProfitRates
workbook column ``Interest Rate (3-mo. T-Bill)`` (= ERP Table 73 / FRED TB3MS:
1981=0.14029, 2011=0.00060), which reproduces the book's printed values exactly
and splices continuously to the FRED TB3MS extension.

Prior to this correction S1603-A read the ``US`` column of
``Appendix16_RXRRULCOECD.xlsx`` (1981=0.15911, 2011=0.00300). That column is an
OECD-MEI-basis interbank/short rate carrying a positive credit/liquidity spread
over the T-Bill in every year (0.24-2.36pp) and is NOT the instrument the book
prints for the US line; it disagreed with the book's 14.03%/0.06% (RED anchor
F-P2.1-01). OECD (S1603-B) and EU (S1603-C) remain the RXRRULCOECD OECD/EU
columns (Shaikh-Ragab bespoke weighted averages), which are correct.

Phase 4 dual-variant emission (S1603_replicated / S1603_oecd_mei) and the
S1603-D FRED TB3MS extension remain deferred to Phase 6.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch16_helpers import (  # noqa: E402
    read_appendix16_rxrrulcoecd,
    read_appendix16_profit_rates,
)

SERIES_ID = "S1603"
BOOK_START = 1960
BOOK_END = 2012

# US 3-month T-Bill column in the ProfitRates appendix (book Fig 16.6/16.7).
US_TBILL_COL = "Interest Rate (3-mo. T-Bill)"

# OECD / EU keep the RXRRULCOECD columns (Shaikh-Ragab weighted averages).
OECD_EU_OUTPUTS = {
    "S1603-B": (DATA_RAW / "S1603_OECD.parquet", "OECD", "SHAIKH_APPENDIX_16_2"),
    "S1603-C": (DATA_RAW / "S1603_EU.parquet", "EU", "SHAIKH_APPENDIX_16_2"),
}
US_OUTPUT = (DATA_RAW / "S1603_US.parquet", US_TBILL_COL, "SHAIKH_APPENDIX_16_PROFITRATES_TBILL")


def _save(df: pd.DataFrame, col: str, out: Path, subseries_id: str,
          subsource_id: str) -> int:
    sub = df[["year", col]].rename(columns={col: "value"}).dropna(subset=["value"])
    sub = sub[(sub["year"] >= BOOK_START) & (sub["year"] <= BOOK_END)].copy()
    sub["units"] = "decimal_rate_annual_avg"
    sub["subseries_id"] = subseries_id
    sub["subsource_id"] = subsource_id
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(out, index=False)
    return int(len(sub))


def run() -> dict:
    panel = read_appendix16_rxrrulcoecd()
    profit = read_appendix16_profit_rates()
    rows: dict[str, int] = {}

    # US 3-month T-Bill (F-P2.1-01 corrected source)
    us_path, us_col, us_src = US_OUTPUT
    rows["S1603-A"] = _save(profit, us_col, us_path, "S1603-A", us_src)

    # OECD / EU weighted averages
    for sid, (path, col, src) in OECD_EU_OUTPUTS.items():
        rows[sid] = _save(panel, col, path, sid, src)

    return {
        "status": "OK",
        "rows_loaded": rows,
        "sources_fetched": ["SHAIKH_APPENDIX_16_PROFITRATES_TBILL", "SHAIKH_APPENDIX_16_2"],
        "us_source_correction": ("F-P2.1-01: S1603-A now reads ProfitRates "
                                 "'Interest Rate (3-mo. T-Bill)' (book Fig 16.6/16.7), "
                                 "not RXRRULCOECD 'US' (OECD-MEI interbank)."),
        "extension_status": "deferred_to_phase6",
        "extension_note": ("S1603_replicated (Fed H.10 x IMF IFS) and "
                           "S1603_oecd_mei (OECD MEI IRSTCI01) variants "
                           "deferred to Phase 6."),
        "outputs": [str(us_path)] + [str(p) for (p, _, _) in OECD_EU_OUTPUTS.values()],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
