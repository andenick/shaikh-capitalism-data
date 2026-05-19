"""L01_S601_load — load Shaikh Appendix 6.8 columns for S601 (Corporate and Non-Corporate Profit Rates).

Reads the canonical Shaikh chopped Appendix 6.8 workbook(s) and emits one raw
parquet per subseries. Per Ch6 fanout playbook: the Appendix 6.8 workbooks are
the Phase-5 ground truth; extension recipes for re-fetching the underlying
NIPA / BEA FA / IRS / Census components are documented in S601_EPR.md.

Source map (subseries_id -> (Appendix table, variable, scale)):
  S601-A <- Appendix 6.8.I3 / variable 'rcorp'
  S601-B <- Appendix 6.8.I3 / variable 'rnoncorp'
  S601-C <- Appendix 6.8.I3 / variable 'rbus'
  S601-D <- Appendix 6.8.II7 / variable 'uK'
  S601-E <- Appendix 6.8.II7 / variable 'uFRB'

Units: decimal_rate
Book year range: [1947, 2011]
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch6_appendix_loader import load_variables  # noqa: E402

SERIES_ID = "S601"
OUT = DATA_RAW / f"{SERIES_ID}_raw.parquet"

SOURCE_MAP = {'S601-A': ['I3', 'rcorp', 1.0], 'S601-B': ['I3', 'rnoncorp', 1.0], 'S601-C': ['I3', 'rbus', 1.0], 'S601-D': ['II7', 'uK', 1.0], 'S601-E': ['II7', 'uFRB', 1.0]}


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
        df["units"] = "decimal_rate"
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
