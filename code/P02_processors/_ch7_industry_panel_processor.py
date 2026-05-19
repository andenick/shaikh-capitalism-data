"""Shared processor for Ch7 industry-panel series.

For each series that loads a single raw parquet from L01, the processor simply
ensures the required schema (year, value, subseries_id, source_id, units) is
present and writes data/processed/{SID}.parquet. The 'industry' column is
preserved as an extra column for Phase 9 visualization.

For series that store the source_id in 'subsource_id' (loaders for S701/S702),
this helper renames it to 'source_id' to match the canonical schema.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def process_panel(raw_parquet: Path, out_parquet: Path) -> dict:
    if not raw_parquet.exists():
        return {"status": "FAIL", "error": f"raw missing: {raw_parquet}"}

    df = pd.read_parquet(raw_parquet)
    if "subsource_id" in df.columns and "source_id" not in df.columns:
        df = df.rename(columns={"subsource_id": "source_id"})

    required = ["year", "value", "subseries_id", "source_id", "units"]
    for col in required:
        if col not in df.columns:
            return {"status": "FAIL", "error": f"missing column: {col}"}

    # Sort year + subseries + (industry if present) for deterministic output
    sort_cols = ["year", "subseries_id"]
    if "industry" in df.columns:
        sort_cols.append("industry")
    if "axis" in df.columns:
        sort_cols.append("axis")
    df = df.sort_values(sort_cols).reset_index(drop=True)

    out_parquet.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_parquet, index=False)

    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "industries": int(df["industry"].nunique()) if "industry" in df.columns else None,
        "output": str(out_parquet),
    }
