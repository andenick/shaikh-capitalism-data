"""Chapter 16: Long Waves and Crises -- Processing Phase.

Series: S093, S094, S095, S096, S097
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.extension import ExtensionEngine
from lib.result import SeriesResult

def process_s093(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S093: US and UK Golden Waves, 1786-2010."""
    r = SeriesResult("S093")
    try:
        df = read_source("ch05", "Appendix5_DATALRprices.csv")
        if "S010AK" in df.columns:
            primary = pd.to_numeric(df["S010AK"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S093", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S093": extended}
            if ext_data is not None:
                r.data["S093-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s094(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S094: Impact on Profitability of Suppression of Real Wage Growth."""
    r = SeriesResult("S094")
    try:
        df = read_source("ch16", "Appendix16_WageProdData.csv")
        if "S091G" in df.columns:
            primary = pd.to_numeric(df["S091G"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S094", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S094": extended}
            if ext_data is not None:
                r.data["S094-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s095(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S095: Hourly Real Wages and Productivity, US Business Sector."""
    r = SeriesResult("S095")
    try:
        df = read_source("ch16", "Appendix16_WageProdData.csv")
        if "S091E" in df.columns:
            primary = pd.to_numeric(df["S091E"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S095", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S095": extended}
            if ext_data is not None:
                r.data["S095-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s096(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S096: Theoretical Figure (Ch16)."""
    r = SeriesResult("S096")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S096_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S096": primary}
            r.step("process", "ok", f"{len(primary)} obs")
            if len(primary) > 0:
                r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "No chopped output")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s097(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S097: The Extraordinary Postwar Path of the Interest Rate."""
    r = SeriesResult("S097")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S097_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S097" in df.columns:
                primary = pd.to_numeric(df["S097"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S097": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s098(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S098: US and OECD Short-Term Interest Rates."""
    r = SeriesResult("S098")
    try:
        df = read_source("ch16", "Appendix16_RXRRULCOECD.csv")
        if "S094A" in df.columns:
            primary = pd.to_numeric(df["S094A"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S098", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S098": extended}
            if ext_data is not None:
                r.data["S098-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s099(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S099: Net Average and Real Incremental Rates of Profit."""
    r = SeriesResult("S099")
    try:
        df = read_source("ch06", "Appendix6_Table68II7.csv")
        if "S013J" in df.columns:
            primary = pd.to_numeric(df["S013J"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S099", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S099": extended}
            if ext_data is not None:
                r.data["S099-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s100(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S100: Household Debt-to-Income Ratio."""
    r = SeriesResult("S100")
    try:
        df = read_source("ch16", "Appendix16_DebtIncRatio.csv")
        if "S092A" in df.columns:
            primary = pd.to_numeric(df["S092A"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S100", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S100": extended}
            if ext_data is not None:
                r.data["S100-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s101(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S101: Household Debt-Service Ratio."""
    r = SeriesResult("S101")
    try:
        df = read_source("ch16", "Appendix16_HouseholdDebtService.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S101", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S101": extended}
            if ext_data is not None:
                r.data["S101-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s220(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S220: Wage and Productivity Data (Source Table, Ch16)."""
    r = SeriesResult("S220")
    try:
        df = read_source("ch16", "Appendix16_WageProdData.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S220", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S220": extended}
            if ext_data is not None:
                r.data["S220-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s221(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S221: Profit Rate Data (Source Table, Ch16)."""
    r = SeriesResult("S221")
    try:
        df = read_source("ch16", "Appendix16_ProfitRates.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S221", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S221": extended}
            if ext_data is not None:
                r.data["S221-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s222(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S222: Household Debt-to-Income Ratio Data (Source Table, Ch16)."""
    r = SeriesResult("S222")
    try:
        df = read_source("ch16", "Appendix16_DebtIncRatio.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S222", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S222": extended}
            if ext_data is not None:
                r.data["S222-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s223(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S223: Household Debt-Service Ratio Data (Source Table, Ch16)."""
    r = SeriesResult("S223")
    try:
        df = read_source("ch16", "Appendix16_HouseholdDebtService.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S223", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S223": extended}
            if ext_data is not None:
                r.data["S223-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s224(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S224: RXRRULC/OECD Interest Rate Data (Source Table, Ch16)."""
    r = SeriesResult("S224")
    try:
        df = read_source("ch16", "Appendix16_RXRRULCOECD.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S224", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S224": extended}
            if ext_data is not None:
                r.data["S224-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S093": process_s093,
    "S094": process_s094,
    "S095": process_s095,
    "S096": process_s096,
    "S097": process_s097,
    "S098": process_s098,
    "S099": process_s099,
    "S100": process_s100,
    "S101": process_s101,
    "S220": process_s220,
    "S221": process_s221,
    "S222": process_s222,
    "S223": process_s223,
    "S224": process_s224,
}


def process_all(reg: dict, engine: ExtensionEngine) -> list[SeriesResult]:
    results = []
    for sid, fn in PROCESSORS.items():
        try:
            results.append(fn(reg, engine))
        except Exception as e:
            results.append(SeriesResult(sid, status="fail", message=str(e)))
    return results
