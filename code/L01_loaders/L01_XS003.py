"""L01_AS003 — load Shaikh Appendix 6.8 columns for XS003 (Imputed Interest Adjustment and Sectoral Profit Rates).

Reads the canonical Shaikh chopped Appendix 6.8 workbook(s) and emits one raw
parquet per subseries. Per Ch6 automated-agent playbook: the Appendix 6.8 workbooks are
the Phase-5 ground truth; extension recipes for re-fetching the underlying
NIPA / BEA FA / IRS / Census components are documented in XS003_EPR.md.

Source map (subseries_id -> (Appendix table, variable, scale)):
  XS003-A <- Appendix 6.8.I3 / variable 'BankMonIntPaid'
  XS003-B <- Appendix 6.8.I3 / variable 'NFNetImpIntPaid'
  XS003-C <- Appendix 6.8.I3 / variable 'BusImpIntAdj'
  XS003-D <- Appendix 6.8.I3 / variable 'rbus'
  XS003-E <- Appendix 6.8.I3 / variable 'rcorp'
  XS003-F <- Appendix 6.8.I3 / variable 'rnoncorp'
  XS003-G <- Appendix 6.8.I3 / variable 'rnoncorp1'

Units: per-subseries (A/B/C billions_current_usd; D/E/F/G decimal_rate). The
former single label "mixed_billions_usd_and_decimal_rates" was a banned mixed
string that mislabeled every column; corrected 2026-07-02 (T3.3) to honest
per-subseries units via UNITS_MAP.
Book year range: [1947, 2011]
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch6_appendix_loader import load_variables  # noqa: E402

SERIES_ID = "XS003"
OUT = DATA_RAW / f"{SERIES_ID}_raw.parquet"

SOURCE_MAP = {'XS003-A': ['I3', 'BankMonIntPaid', 1.0], 'XS003-B': ['I3', 'NFNetImpIntPaid', 1.0], 'XS003-C': ['I3', 'BusImpIntAdj', 1.0], 'XS003-D': ['I3', 'rbus', 1.0], 'XS003-E': ['I3', 'rcorp', 1.0], 'XS003-F': ['I3', 'rnoncorp', 1.0], 'XS003-G': ['I3', 'rnoncorp1', 1.0]}

# Honest per-subseries units (T3.3). A/B/C are dollar levels; D-G are profit rates.
UNITS_MAP = {
    'XS003-A': 'billions_current_usd', 'XS003-B': 'billions_current_usd',
    'XS003-C': 'billions_current_usd', 'XS003-D': 'decimal_rate',
    'XS003-E': 'decimal_rate', 'XS003-F': 'decimal_rate', 'XS003-G': 'decimal_rate',
}


def run() -> dict:
    rows = []
    sources_used: set[str] = set()
    rows_per_sub: dict[str, int] = {}
    for sub_id, (table, var, scale) in SOURCE_MAP.items():
        try:
            df = load_variables(table, [var])
        except FileNotFoundError as exc:
            return {"status": "FAIL", "error": str(exc), "subseries": sub_id}
        if df.empty:
            rows_per_sub[sub_id] = 0
            continue
        df = df.copy()
        df["value"] = df["value"] * scale
        df["subseries_id"] = sub_id
        df["units"] = UNITS_MAP[sub_id]
        rows_per_sub[sub_id] = int(len(df))
        sources_used.add(df["source_id"].iloc[0])
        rows.append(df[["year", "value", "subseries_id", "source_id", "units"]])

    if not rows:
        return {"status": "FAIL", "error": "no rows loaded for any subseries", "sub_rows": rows_per_sub}

    out = pd.concat(rows, ignore_index=True)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_loaded": int(len(out)),
        "rows_per_sub": rows_per_sub,
        "sources_fetched": sorted(sources_used),
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
