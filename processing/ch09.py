"""Chapter 9: Prices of Production -- Processing Phase.

Series: S047, S048, S049
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


def process_s047(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S047: Market Prices vs Direct Prices, 71 Industries (Fig9.1, Fig9.2)."""
    r = SeriesResult("S047")
    try:
        primary = pd.Series(dtype=float)

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S047", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S047": extended}
            if ext_data is not None:
                r.data["S047-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s048(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S048: Integrated Output-Capital Ratios and Standard Prices (Fig9.4, Fig9.5, Fig9.6)."""
    r = SeriesResult("S048")
    try:
        primary = pd.Series(dtype=float)

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S048", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S048": extended}
            if ext_data is not None:
                r.data["S048-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s049(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S049: Actual Wage-Profit Curves (Fig9.6, Fig9.7, Fig9.8)."""
    r = SeriesResult("S049")
    try:
        primary = pd.Series(dtype=float)

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S049", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S049": extended}
            if ext_data is not None:
                r.data["S049-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S047": process_s047,
    "S048": process_s048,
    "S049": process_s049,
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
