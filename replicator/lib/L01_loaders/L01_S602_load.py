"""L01_S602_load — load Shaikh Appendix 6.8 columns for S602 (Corrected vs Conventional Corporate Profitability).

Reads the canonical Shaikh chopped Appendix 6.8 workbook(s) and emits one raw
parquet per subseries. Per Ch6 fanout playbook: the Appendix 6.8 workbooks are
the Phase-5 ground truth; extension recipes for re-fetching the underlying
NIPA / BEA FA / IRS / Census components are documented in S602_EPR.md.

Source map (subseries_id -> (Appendix table, variable, scale)):
  S602-A <- Appendix 6.8.II7 / variable 'Rcorp'
  S602-B <- Appendix 6.8.II7 / variable 'Rcorpnipa'
  S602-C <- Appendix 6.8.II7 / variable 'rcorp'
  S602-D <- Appendix 6.8.II7 / variable 'rcorpnipa'
  S602-E <- Appendix 6.8.II7 / variable 'Profshcorp'
  S602-F <- Appendix 6.8.II7 / variable 'Profshcorpnipa'

Units: decimal_rate_and_share
Book year range: [1947, 2011]
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch6_appendix_loader import load_variables  # noqa: E402

SERIES_ID = "S602"
OUT = DATA_RAW / f"{SERIES_ID}_raw.parquet"

SOURCE_MAP = {'S602-A': ['II7', 'Rcorp', 1.0], 'S602-B': ['II7', 'Rcorpnipa', 1.0], 'S602-C': ['II7', 'rcorp', 1.0], 'S602-D': ['II7', 'rcorpnipa', 1.0], 'S602-E': ['II7', 'Profshcorp', 1.0], 'S602-F': ['II7', 'Profshcorpnipa', 1.0]}


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
        df["units"] = "decimal_rate_and_share"
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
