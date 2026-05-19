"""L01_AS002_load — load Shaikh Appendix 6.8 columns for AS002 (Wage Equivalent and Corp/Noncorp Split).

Reads the canonical Shaikh chopped Appendix 6.8 workbook(s) and emits one raw
parquet per subseries. Per Ch6 fanout playbook: the Appendix 6.8 workbooks are
the Phase-5 ground truth; extension recipes for re-fetching the underlying
NIPA / BEA FA / IRS / Census components are documented in AS002_EPR.md.

Source map (subseries_id -> (Appendix table, variable, scale)):
  AS002-A <- Appendix 6.8.I2 / variable 'PropInc'
  AS002-B <- Appendix 6.8.I2 / variable 'ECprop'
  AS002-C <- Appendix 6.8.I2 / variable 'WEQ2'
  AS002-D <- Appendix 6.8.I2 / variable 'WEQ1'
  AS002-E <- Appendix 6.8.I2 / variable 'Pnoncorp'
  AS002-F <- Appendix 6.8.I2 / variable 'Pcorpnipa'
  AS002-G <- Appendix 6.8.I2 / variable 's'

Units: billions_current_usd
Book year range: [1947, 2011]
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch6_appendix_loader import load_variables  # noqa: E402

SERIES_ID = "AS002"
OUT = DATA_RAW / f"{SERIES_ID}_raw.parquet"

SOURCE_MAP = {'AS002-A': ['I2', 'PropInc', 1.0], 'AS002-B': ['I2', 'ECprop', 1.0], 'AS002-C': ['I2', 'WEQ2', 1.0], 'AS002-D': ['I2', 'WEQ1', 1.0], 'AS002-E': ['I2', 'Pnoncorp', 1.0], 'AS002-F': ['I2', 'Pcorpnipa', 1.0], 'AS002-G': ['I2', 's', 1.0]}


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
        df["units"] = "billions_current_usd"
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
