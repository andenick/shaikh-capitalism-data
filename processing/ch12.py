"""Chapter 12: Phillips Curves -- Processing Phase.

Series: S064, S065, S066, S067, S203
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.extension import ExtensionEngine
from lib.result import SeriesResult

def process_s064(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S064: Phillips Curve, US, 1955-1970."""
    r = SeriesResult("S064")
    try:
        df = read_source("ch12", "Appendix12_CreditInflUnempl.csv")
        if "S065B" in df.columns:
            primary = pd.to_numeric(df["S065B"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S064", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S064": extended}
            if ext_data is not None:
                r.data["S064-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s065(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S065: US Inflation and Unemployment Rates, 1955-1986."""
    r = SeriesResult("S065")
    try:
        df = read_source("ch12", "Appendix12_CreditInflUnempl.csv")
        if "S065B" in df.columns:
            primary = pd.to_numeric(df["S065B"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S065", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S065": extended}
            if ext_data is not None:
                r.data["S065-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s066(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S066: Phillips Curve, US, 1971-1981."""
    r = SeriesResult("S066")
    try:
        df = read_source("ch12", "Appendix12_CreditInflUnempl.csv")
        if "S065B" in df.columns:
            primary = pd.to_numeric(df["S065B"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S066", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S066": extended}
            if ext_data is not None:
                r.data["S066-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s067(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S067: Phillips Curve, US, 1955-2010."""
    r = SeriesResult("S067")
    try:
        df = read_source("ch12", "Appendix12_CreditInflUnempl.csv")
        if "S065A" in df.columns:
            primary = pd.to_numeric(df["S065A"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S067", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S067": extended}
            if ext_data is not None:
                r.data["S067-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s203(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S203: Credit, Inflation, and Unemployment Data (Source Table)."""
    r = SeriesResult("S203")
    try:
        df = read_source("ch12", "Appendix12_CreditInflUnempl.csv")
        if "S065A" in df.columns:
            primary = pd.to_numeric(df["S065A"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S203", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S203": extended}
            if ext_data is not None:
                r.data["S203-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S064": process_s064,
    "S065": process_s065,
    "S066": process_s066,
    "S067": process_s067,
    "S203": process_s203,
}


def process_all(reg: dict, engine: ExtensionEngine) -> list[SeriesResult]:
    results = []
    for sid, fn in PROCESSORS.items():
        try:
            results.append(fn(reg, engine))
        except Exception as e:
            results.append(SeriesResult(sid, status="fail", message=str(e)))
    return results
