"""Chapter 17: Inequality -- Processing Phase.

Series: S102, S103, S104
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.extension import ExtensionEngine
from lib.result import SeriesResult


def _load_table(chapter: str, filename: str) -> pd.DataFrame | None:
    """Load a source table, returning None if not found."""
    try:
        return read_source(chapter, filename)
    except Exception:
        return None


def _extract_columns(df: pd.DataFrame, sid: str, subseries: dict) -> dict:
    """Extract subseries from a source table by matching column names."""
    data = {}
    for sub_id, sub_cfg in subseries.items():
        # Try exact column name match
        for col in df.columns:
            if col == sub_id or col == sub_cfg.get("shiny_column", ""):
                s = pd.to_numeric(df[col], errors="coerce").dropna()
                if len(s) > 0:
                    data[sub_id] = s
                    break

    # If no subseries matched, use first column
    if not data and len(df.columns) > 0:
        s = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
        if len(s) > 0:
            data[sid] = s

    return data


def process_s102(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S102: The Global Crisis of 2007 in Light of Past Long Waves."""
    r = SeriesResult("S102")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S102_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S102": primary}
            r.step("process", "ok", f"{len(primary)} obs")
            if len(primary) > 0:
                r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "No chopped output")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s103(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S103: Personal Income Distribution below $200,000, Cumulative Prob."""
    r = SeriesResult("S103")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S103_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S103": primary}
            r.step("process", "ok", f"{len(primary)} obs")
            if len(primary) > 0:
                r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "No chopped output")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s104(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S104: Personal Income Distribution above $200,000, Cumulative Prob."""
    r = SeriesResult("S104")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S104_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S104": primary}
            r.step("process", "ok", f"{len(primary)} obs")
            if len(primary) > 0:
                r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "No chopped output")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S102": process_s102,
    "S103": process_s103,
    "S104": process_s104,
}


def process_all(reg: dict, engine: ExtensionEngine) -> list[SeriesResult]:
    results = []
    for sid, fn in PROCESSORS.items():
        try:
            result = fn(reg, engine)
            results.append(result)
        except Exception as e:
            results.append(SeriesResult(sid, status="fail", message=str(e)))
    return results
