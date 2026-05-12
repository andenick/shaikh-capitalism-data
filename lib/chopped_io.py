"""Read/write Anu Chopped CSV format."""
from __future__ import annotations

import pandas as pd
from pathlib import Path


def read_chopped(filepath: Path) -> pd.DataFrame:
    """Load an Anu Chopped CSV.

    Format: Row 0 = source metadata, Row 1 = column IDs (Year + subseries), Row 2+ = data.
    Auto-detects whether Row 0 is metadata or a plain header.
    """
    probe = pd.read_csv(filepath, nrows=0, encoding="utf-8-sig")
    first_col = probe.columns[0] if len(probe.columns) > 0 else ""

    if first_col == "" or first_col.startswith("Unnamed"):
        df = pd.read_csv(filepath, skiprows=[0], encoding="utf-8-sig")
    else:
        df = pd.read_csv(filepath, encoding="utf-8-sig")

    col0 = df.columns[0]
    if col0 != "Year":
        df = df.rename(columns={col0: "Year"})

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    df = df.set_index("Year")
    df = df.apply(pd.to_numeric, errors="coerce")
    return df


def read_source(chapter: str, filename: str) -> pd.DataFrame:
    """Load a Shaikh source CSV from data/inputs/{chapter}/{filename}.

    Parses the Anu Chopped format (Row 0 = metadata, Row 1 = column IDs).
    Returns DataFrame with first column as index (usually Year) and numeric values.
    Does NOT assume year indexing — some CSVs are cross-sectional or sub-annual.
    """
    from .registry import ROOT
    path = ROOT / "data" / "inputs" / chapter / filename

    with open(path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    # Find the column ID row (starts with comma or has S### patterns)
    header_row = 1  # default: row 1 has column IDs
    for i, line in enumerate(lines[:5]):
        stripped = line.strip()
        if stripped.startswith(",S") or stripped.startswith(",FPR"):
            header_row = i
            break

    df = pd.read_csv(path, skiprows=range(0, header_row), encoding="utf-8-sig")

    # Rename first column to Year if it looks numeric
    col0 = df.columns[0]
    if col0 == "" or col0.startswith("Unnamed"):
        df = df.rename(columns={col0: "Year"})

    # Try to set Year as index, but don't fail if non-numeric
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        valid = df["Year"].notna()
        if valid.sum() > 0:
            df = df[valid]
            df["Year"] = df["Year"].astype(int)
            df = df.set_index("Year")

    df = df.apply(pd.to_numeric, errors="coerce")
    return df
