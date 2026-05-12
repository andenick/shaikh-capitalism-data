"""Chapter 10: Finance and Interest -- Processing Phase.

Series: S040, S041, S042, S050, S051
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.extension import ExtensionEngine
from lib.result import SeriesResult

def process_s040(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S040: Ibbotson Returns on Stocks and Bonds."""
    r = SeriesResult("S040")
    try:
        df = read_source("ch10", "Appendix10_Ibbotson.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S040", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S040": extended}
            if ext_data is not None:
                r.data["S040-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s041(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S041: Interest Rates, Prices, and Equity Data."""
    r = SeriesResult("S041")
    try:
        df = read_source("ch10", "Appendix10_IntroPPrice.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S041", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S041": extended}
            if ext_data is not None:
                r.data["S041-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s042(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S042: US Long-Run Interest Rates and Prices."""
    r = SeriesResult("S042")
    try:
        df = read_source("ch10", "Appendix10_USLR.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S042", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S042": extended}
            if ext_data is not None:
                r.data["S042-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s050(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S050: Bank vs Private Industry IROP."""
    r = SeriesResult("S050")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S050_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S050" in df.columns:
                primary = pd.to_numeric(df["S050"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S050": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s051(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S051: Business Profit Rate and Prime Rate."""
    r = SeriesResult("S051")
    try:
        df = read_source("ch10", "Appendix10_IntroPPrice.csv")
        if "S041O" in df.columns:
            primary = pd.to_numeric(df["S041O"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S051", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S051": extended}
            if ext_data is not None:
                r.data["S051-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s052(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S052: Interest Rate and Price Level."""
    r = SeriesResult("S052")
    try:
        df = read_source("ch10", "Appendix10_USLR.csv")
        if "S042D" in df.columns:
            primary = pd.to_numeric(df["S042D"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S052", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S052": extended}
            if ext_data is not None:
                r.data["S052-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s053(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S053: Relative Price of Finance."""
    r = SeriesResult("S053")
    try:
        df = read_source("ch10", "Appendix10_USLR.csv")
        if "S042" in df.columns:
            primary = pd.to_numeric(df["S042"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S053", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S053": extended}
            if ext_data is not None:
                r.data["S053-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s054(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S054: Real Interest Rate HP-filtered."""
    r = SeriesResult("S054")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S054_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S054" in df.columns:
                primary = pd.to_numeric(df["S054"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S054": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s055(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S055: Dividend Yield vs Bond Yield."""
    r = SeriesResult("S055")
    try:
        df = read_source("ch10", "Appendix10_USLR.csv")
        if "S042G" in df.columns:
            primary = pd.to_numeric(df["S042G"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S055", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S055": extended}
            if ext_data is not None:
                r.data["S055-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s056(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S056: Bond and Equity Returns."""
    r = SeriesResult("S056")
    try:
        df = read_source("ch10", "Appendix10_Ibbotson.csv")
        if "S040A" in df.columns:
            primary = pd.to_numeric(df["S040A"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S056", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S056": extended}
            if ext_data is not None:
                r.data["S056-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s057(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S057: Equity Rate vs Corporate IROP."""
    r = SeriesResult("S057")
    try:
        df = read_source("ch10", "Appendix10_IntroPPrice.csv")
        if "S041AB" in df.columns:
            primary = pd.to_numeric(df["S041AB"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S057", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S057": extended}
            if ext_data is not None:
                r.data["S057-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s058(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S058: Equity Rate vs Corporate ROP."""
    r = SeriesResult("S058")
    try:
        df = read_source("ch10", "Appendix10_IntroPPrice.csv")
        if "S041AB" in df.columns:
            primary = pd.to_numeric(df["S041AB"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S058", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S058": extended}
            if ext_data is not None:
                r.data["S058-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s059(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S059: Actual vs Warranted Stock Price."""
    r = SeriesResult("S059")
    try:
        df = read_source("ch10", "Appendix10_IntroPPrice.csv")
        if "S041Y" in df.columns:
            primary = pd.to_numeric(df["S041Y"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S059", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S059": extended}
            if ext_data is not None:
                r.data["S059-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S040": process_s040,
    "S041": process_s041,
    "S042": process_s042,
    "S050": process_s050,
    "S051": process_s051,
    "S052": process_s052,
    "S053": process_s053,
    "S054": process_s054,
    "S055": process_s055,
    "S056": process_s056,
    "S057": process_s057,
    "S058": process_s058,
    "S059": process_s059,
}


def process_all(reg: dict, engine: ExtensionEngine) -> list[SeriesResult]:
    results = []
    for sid, fn in PROCESSORS.items():
        try:
            results.append(fn(reg, engine))
        except Exception as e:
            results.append(SeriesResult(sid, status="fail", message=str(e)))
    return results
