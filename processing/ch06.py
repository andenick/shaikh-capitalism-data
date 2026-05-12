"""Chapter 6: The Rate of Profit -- Processing Phase.

Series: S013, S026, S027, S028, S105
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.extension import ExtensionEngine
from lib.result import SeriesResult

def process_s013(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S013: Final Profit Rate Measures."""
    r = SeriesResult("S013")
    try:
        df = read_source("ch06", "Appendix6_Table68II7.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S013", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S013": extended}
            if ext_data is not None:
                r.data["S013-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s026(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S026: Corporate and Non-Corporate Profit Rates."""
    r = SeriesResult("S026")
    try:
        df = read_source("ch06", "Appendix6_Table68I3.csv")
        if "S208AW_EXT" in df.columns:
            primary = pd.to_numeric(df["S208AW_EXT"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S026", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S026": extended}
            if ext_data is not None:
                r.data["S026-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s027(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S027: Corrected vs Conventional Corporate Profitability."""
    r = SeriesResult("S027")
    try:
        df = read_source("ch06", "Appendix6_Table68II7.csv")
        if "S013J_EXT" in df.columns:
            primary = pd.to_numeric(df["S013J_EXT"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S027", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S027": extended}
            if ext_data is not None:
                r.data["S027-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s028(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S028: Component Ratios x1, x2, x3."""
    r = SeriesResult("S028")
    try:
        df = read_source("ch06", "Appendix6_Table68II7.csv")
        if "S013P" in df.columns:
            primary = pd.to_numeric(df["S013P"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S028", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S028": extended}
            if ext_data is not None:
                r.data["S028-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s105(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S105: Corporate Incremental Rate of Profit (IROP)."""
    r = SeriesResult("S105")
    try:
        df = read_source("ch06", "Appendix6_Table68II7.csv")
        if "S013AO_COMBINED" in df.columns:
            primary = pd.to_numeric(df["S013AO_COMBINED"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S105", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S105": extended}
            if ext_data is not None:
                r.data["S105-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s206(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S206: GDP/GDI Decomposition and Business NOS."""
    r = SeriesResult("S206")
    try:
        df = read_source("ch06", "Appendix6_Table68I1.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S206", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S206": extended}
            if ext_data is not None:
                r.data["S206-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s207(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S207: Wage Equivalent and Corporate/Noncorporate Split."""
    r = SeriesResult("S207")
    try:
        df = read_source("ch06", "Appendix6_Table68I2.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S207", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S207": extended}
            if ext_data is not None:
                r.data["S207-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s208(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S208: Imputed Interest Adjustment and Sectoral Profit Rates."""
    r = SeriesResult("S208")
    try:
        df = read_source("ch06", "Appendix6_Table68I3.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S208", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S208": extended}
            if ext_data is not None:
                r.data["S208-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s209(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S209: GPIM Corporate Capital Stock."""
    r = SeriesResult("S209")
    try:
        df = read_source("ch06", "Appendix6_Table68II1.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S209", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S209": extended}
            if ext_data is not None:
                r.data["S209-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s210(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S210: GPIM Variant - BEA 2011 Initial Value."""
    r = SeriesResult("S210")
    try:
        df = read_source("ch06", "Appendix6_Table68II2.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S210", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S210": extended}
            if ext_data is not None:
                r.data["S210-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s211(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S211: GPIM Variant - BEA 1993 vs 2011."""
    r = SeriesResult("S211")
    try:
        df = read_source("ch06", "Appendix6_Table68II3.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S211", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S211": extended}
            if ext_data is not None:
                r.data["S211-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s212(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S212: GPIM Variant - IRS Adjusted."""
    r = SeriesResult("S212")
    try:
        df = read_source("ch06", "Appendix6_Table68II4.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S212", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S212": extended}
            if ext_data is not None:
                r.data["S212-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s213(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S213: GPIM Variant - Interwar Adjusted."""
    r = SeriesResult("S213")
    try:
        df = read_source("ch06", "Appendix6_Table68II5.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S213", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S213": extended}
            if ext_data is not None:
                r.data["S213-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s214(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S214: IRS Corporate Inventories and Total Capital Stock."""
    r = SeriesResult("S214")
    try:
        df = read_source("ch06", "Appendix6_Table68II6.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S214", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S214": extended}
            if ext_data is not None:
                r.data["S214-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S013": process_s013,
    "S026": process_s026,
    "S027": process_s027,
    "S028": process_s028,
    "S105": process_s105,
    "S206": process_s206,
    "S207": process_s207,
    "S208": process_s208,
    "S209": process_s209,
    "S210": process_s210,
    "S211": process_s211,
    "S212": process_s212,
    "S213": process_s213,
    "S214": process_s214,
}


def process_all(reg: dict, engine: ExtensionEngine) -> list[SeriesResult]:
    results = []
    for sid, fn in PROCESSORS.items():
        try:
            results.append(fn(reg, engine))
        except Exception as e:
            results.append(SeriesResult(sid, status="fail", message=str(e)))
    return results
