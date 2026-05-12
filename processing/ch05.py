"""Chapter 5: The General Price Level -- Processing Phase.

Series: S010, S020, S021, S022, S023...
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


def process_s010(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S010: Gold Prices and Wholesale Price Indexes (Source Table) (N/A)."""
    r = SeriesResult("S010")
    try:
        df = read_source("ch05", "Appendix5_DATALRprices.csv")
        if "S010A" in df.columns:
            primary = pd.to_numeric(df["S010A"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S010", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S010": extended}
            if ext_data is not None:
                r.data["S010-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s020(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S020: US and UK Gold Prices (Fig5.1)."""
    r = SeriesResult("S020")
    try:
        df = read_source("ch05", "Appendix5_DATALRprices.csv")
        if "S010AA" in df.columns:
            primary = pd.to_numeric(df["S010AA"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S020", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S020": extended}
            if ext_data is not None:
                r.data["S020-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s021(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S021: UK Wholesale Price Indexes in Pound Sterling, US Dollars, and Ounces of Gold (Fig5.2)."""
    r = SeriesResult("S021")
    try:
        df = read_source("ch05", "Appendix5_DATALRprices.csv")
        if "S010R" in df.columns:
            primary = pd.to_numeric(df["S010R"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S021", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S021": extended}
            if ext_data is not None:
                r.data["S021-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s022(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S022: US and UK Wholesale Price Indexes, 1790-1940 (Fig5.3)."""
    r = SeriesResult("S022")
    try:
        df = read_source("ch05", "Appendix5_DATALRprices.csv")
        if "S010F" in df.columns:
            primary = pd.to_numeric(df["S010F"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S022", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S022": extended}
            if ext_data is not None:
                r.data["S022-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s023(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S023: US and UK Wholesale Price Indexes, 1790-2010 (Fig5.4)."""
    r = SeriesResult("S023")
    try:
        df = read_source("ch05", "Appendix5_DATALRprices.csv")
        if "S010F" in df.columns:
            primary = pd.to_numeric(df["S010F"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S023", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S023": extended}
            if ext_data is not None:
                r.data["S023-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s024(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S024: UK WPI in Gold and UK Gold Price (Fig5.5)."""
    r = SeriesResult("S024")
    try:
        df = read_source("ch05", "Appendix5_DATALRprices.csv")
        if "S010S" in df.columns:
            primary = pd.to_numeric(df["S010S"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S024", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S024": extended}
            if ext_data is not None:
                r.data["S024-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s025(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S025: US WPI in Gold and US Gold Price (Fig5.6)."""
    r = SeriesResult("S025")
    try:
        df = read_source("ch05", "Appendix5_DATALRprices.csv")
        if "S010H" in df.columns:
            primary = pd.to_numeric(df["S010H"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S025", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S025": extended}
            if ext_data is not None:
                r.data["S025-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S010": process_s010,
    "S020": process_s020,
    "S021": process_s021,
    "S022": process_s022,
    "S023": process_s023,
    "S024": process_s024,
    "S025": process_s025,
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
