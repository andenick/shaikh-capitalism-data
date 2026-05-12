"""Chapter 14: Classical Phillips Curve -- Processing Phase.

Series: S068, S069, S070, S071, S072...
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


def process_s068(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S068: Nominal GDP Growth and Level of Wage Share (Fig14.10)."""
    r = SeriesResult("S068")
    try:
        df = read_source("ch14", "Appendix14_InflationULdata.csv")
        if "S202E" in df.columns:
            primary = pd.to_numeric(df["S202E"], errors="coerce").dropna()
        else:
            primary = pd.to_numeric(df["S202E"], errors="coerce").dropna() if "S202E" in df.columns else df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S068", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S068": extended}
            if ext_data is not None:
                r.data["S068-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s069(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S069: Unemployment Measures US 1948-2011 (Fig14.11)."""
    r = SeriesResult("S069")
    try:
        df = read_source("ch14", "Appendix14_InflationULdata.csv")
        if "S202M" in df.columns:
            primary = pd.to_numeric(df["S202M"], errors="coerce").dropna()
        else:
            primary = pd.to_numeric(df["S073N"], errors="coerce").dropna() if "S073N" in df.columns else df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S069", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S069": extended}
            if ext_data is not None:
                r.data["S069-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s070(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S070: Wage Share vs Unemployment Intensity (Fig14.12)."""
    r = SeriesResult("S070")
    try:
        df = read_source("ch14", "Appendix14_InflationULdata.csv")
        if "S202J" in df.columns:
            primary = pd.to_numeric(df["S202J"], errors="coerce").dropna()
        else:
            primary = pd.to_numeric(df["S202J"], errors="coerce").dropna() if "S202J" in df.columns else df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S070", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S070": extended}
            if ext_data is not None:
                r.data["S070-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s071(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S071: Rate of Change of Wage Share vs Unemployment Intensity (Fig14.13)."""
    r = SeriesResult("S071")
    try:
        df = read_source("ch14", "Appendix14_InflationULdata.csv")
        if "S202K" in df.columns:
            primary = pd.to_numeric(df["S202K"], errors="coerce").dropna()
        else:
            primary = pd.to_numeric(df["S202K"], errors="coerce").dropna() if "S202K" in df.columns else df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S071", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S071": extended}
            if ext_data is not None:
                r.data["S071-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s072(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S072: HP-Filtered Wage Share Growth vs Unemployment Intensity (Fig14.14)."""
    r = SeriesResult("S072")
    try:
        df = read_source("ch14", "Appendix14_InflationULdata.csv")
        if "S202L" in df.columns:
            primary = pd.to_numeric(df["S202L"], errors="coerce").dropna()
        else:
            primary = pd.to_numeric(df["S202L"], errors="coerce").dropna() if "S202L" in df.columns else df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S072", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S072": extended}
            if ext_data is not None:
                r.data["S072-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s073(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S073: Inflation and Productivity Growth (Fig14.15)."""
    r = SeriesResult("S073")
    try:
        df = read_source("ch14", "Appendix14_InflationULdata.csv")
        if "S202A" in df.columns:
            primary = pd.to_numeric(df["S202A"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S073", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S073": extended}
            if ext_data is not None:
                r.data["S073-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s074(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S074: HP-Filtered Real Wage Growth vs Unemployment Intensity (Fig14.16)."""
    r = SeriesResult("S074")
    try:
        df = read_source("ch14", "Appendix14_InflationULdata.csv")
        if "S202Z" in df.columns:
            primary = pd.to_numeric(df["S202Z"], errors="coerce").dropna()
        else:
            primary = pd.to_numeric(df["S202Z"], errors="coerce").dropna() if "S202Z" in df.columns else df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S074", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S074": extended}
            if ext_data is not None:
                r.data["S074-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s075(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S075: HP-Filtered Nominal Wage Growth vs Unemployment Intensity (Fig14.17)."""
    r = SeriesResult("S075")
    try:
        df = read_source("ch14", "Appendix14_InflationULdata.csv")
        if "S202Y" in df.columns:
            primary = pd.to_numeric(df["S202Y"], errors="coerce").dropna()
        else:
            primary = pd.to_numeric(df["S202Y"], errors="coerce").dropna() if "S202Y" in df.columns else df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S075", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S075": extended}
            if ext_data is not None:
                r.data["S075-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s202(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S202: Inflation, Unemployment, and Wage Share Data (Source Table) (N/A)."""
    r = SeriesResult("S202")
    try:
        df = read_source("ch14", "Appendix14_InflationULdata.csv")
        if "S202A" in df.columns:
            primary = pd.to_numeric(df["S202A"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S202", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S202": extended}
            if ext_data is not None:
                r.data["S202-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S068": process_s068,
    "S069": process_s069,
    "S070": process_s070,
    "S071": process_s071,
    "S072": process_s072,
    "S073": process_s073,
    "S074": process_s074,
    "S075": process_s075,
    "S202": process_s202,
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
