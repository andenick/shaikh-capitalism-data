"""Chapter 11: International Trade -- Processing Phase.

Series: S060, S061, S062, S063, S200...
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


def process_s060(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S060: Trade Balances in Major Countries (Fig11.2)."""
    r = SeriesResult("S060")
    try:
        # Derived from S201
        df = read_source("ch11", "Appendix11_XMData.csv")
        # Extract subseries columns
        subseries = reg.get("series", reg).get("S060", {}).get("subseries", {})
        extracted = _extract_columns(df, "S060", subseries)
        primary = extracted.get("S060", extracted.get(list(extracted.keys())[0]) if extracted else pd.Series(dtype=float))

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S060", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S060": extended}
            if ext_data is not None:
                r.data["S060-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s061(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S061: Real Effective Exchange Rates (PPI), US and Japan (Fig11.3)."""
    r = SeriesResult("S061")
    try:
        # Derived from S200
        df = read_source("ch11", "Appendix11_USJPNdata.csv")
        # Extract subseries columns
        subseries = reg.get("series", reg).get("S061", {}).get("subseries", {})
        extracted = _extract_columns(df, "S061", subseries)
        primary = extracted.get("S061", extracted.get(list(extracted.keys())[0]) if extracted else pd.Series(dtype=float))

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S061", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S061": extended}
            if ext_data is not None:
                r.data["S061-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s062(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S062: Law of One Price at Aggregate Level, US and Japan (Fig11.6)."""
    r = SeriesResult("S062")
    try:
        # Derived from S200
        df = read_source("ch11", "Appendix11_USJPNdata.csv")
        # Extract subseries columns
        subseries = reg.get("series", reg).get("S062", {}).get("subseries", {})
        extracted = _extract_columns(df, "S062", subseries)
        primary = extracted.get("S062", extracted.get(list(extracted.keys())[0]) if extracted else pd.Series(dtype=float))

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S062", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S062": extended}
            if ext_data is not None:
                r.data["S062-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s063(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S063: US Balance of Trade, Real Exchange Rate, Relative GDP (Fig11.7)."""
    r = SeriesResult("S063")
    try:
        # Derived from S200
        df = read_source("ch11", "Appendix11_USJPNdata.csv")
        # Extract subseries columns
        subseries = reg.get("series", reg).get("S063", {}).get("subseries", {})
        extracted = _extract_columns(df, "S063", subseries)
        primary = extracted.get("S063", extracted.get(list(extracted.keys())[0]) if extracted else pd.Series(dtype=float))

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S063", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S063": extended}
            if ext_data is not None:
                r.data["S063-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s200(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S200: US-Japan Trade and Exchange Rate Data (Source Table) (N/A)."""
    r = SeriesResult("S200")
    try:
        df = read_source("ch11", "Appendix11_USJPNdata.csv")
        if "S200B" in df.columns:
            primary = pd.to_numeric(df["S200B"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S200", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S200": extended}
            if ext_data is not None:
                r.data["S200-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s201(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S201: Export-Import Trade Balance Data (Source Table) (N/A)."""
    r = SeriesResult("S201")
    try:
        df = read_source("ch11", "Appendix11_XMData.csv")
        if "S201B" in df.columns:
            primary = pd.to_numeric(df["S201B"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S201", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S201": extended}
            if ext_data is not None:
                r.data["S201-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S060": process_s060,
    "S061": process_s061,
    "S062": process_s062,
    "S063": process_s063,
    "S200": process_s200,
    "S201": process_s201,
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
