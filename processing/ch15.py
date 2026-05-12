"""Chapter 15: Money and Inflation -- Processing Phase.

Series: S076, S077, S078, S079, S080
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.extension import ExtensionEngine
from lib.result import SeriesResult

def process_s076(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S076: Consumer Price Level, US, 1774-2011."""
    r = SeriesResult("S076")
    try:
        df = read_source("ch15", "Appendix15_MeasuringWorthCPI.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S076", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S076": extended}
            if ext_data is not None:
                r.data["S076-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s077(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S077: Growth Rates of Real Output, US Major Industries (Part 1)."""
    r = SeriesResult("S077")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S077_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S077" in df.columns:
                primary = pd.to_numeric(df["S077"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S077": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s078(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S078: Growth Rates of Real Output, US Major Industries (Part 2)."""
    r = SeriesResult("S078")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S078_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S078" in df.columns:
                primary = pd.to_numeric(df["S078"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S078": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s079(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S079: Growth of Nominal GDP and Relative New Purchasing Power."""
    r = SeriesResult("S079")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S079_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S079" in df.columns:
                primary = pd.to_numeric(df["S079"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S079": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s080(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S080: Growth of Nominal GDP vs Relative New Purchasing Power."""
    r = SeriesResult("S080")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S080_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S080" in df.columns:
                primary = pd.to_numeric(df["S080"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S080": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s081(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S081: Real Output Growth vs Real Net Rate of Return on New Capital."""
    r = SeriesResult("S081")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S081_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S081" in df.columns:
                primary = pd.to_numeric(df["S081"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S081": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s082(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S082: Change in Real Output vs Change in Real Gross Profits."""
    r = SeriesResult("S082")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S082_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S082" in df.columns:
                primary = pd.to_numeric(df["S082"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S082": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s083(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S083: Classical and Conventional Phillips-Type Curves, 1948-2010."""
    r = SeriesResult("S083")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S083_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S083" in df.columns:
                primary = pd.to_numeric(df["S083"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S083": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s084(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S084: Classical and Conventional Phillips-Type Curves, 1948-1981."""
    r = SeriesResult("S084")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S084_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S084" in df.columns:
                primary = pd.to_numeric(df["S084"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S084": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s085(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S085: Classical and Conventional Phillips-Type Curves, 1982-2010."""
    r = SeriesResult("S085")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S085_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S085" in df.columns:
                primary = pd.to_numeric(df["S085"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S085": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s086(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S086: Normalized Inflation and Growth Utilization Rates."""
    r = SeriesResult("S086")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S086_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S086" in df.columns:
                primary = pd.to_numeric(df["S086"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S086": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s087(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S087: HP(100) Trend of Net Incremental Rate of Profit."""
    r = SeriesResult("S087")
    try:
        df = read_source("ch06", "Appendix6_Table68II7.csv")
        if "S013AY" in df.columns:
            primary = pd.to_numeric(df["S013AY"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S087", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S087": extended}
            if ext_data is not None:
                r.data["S087-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s088(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S088: World Inflation vs Growth of Private and Public Credit, 1970."""
    r = SeriesResult("S088")
    try:
        df = read_source("ch15", "Appendix15_WorldInflationDataByCountry.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S088", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S088": extended}
            if ext_data is not None:
                r.data["S088-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s089(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S089: World Inflation vs Growth of Total Credit, 1988-2011."""
    r = SeriesResult("S089")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S089_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S089" in df.columns:
                primary = pd.to_numeric(df["S089"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S089": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s090(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S090: Argentina Total Credit Growth and Nominal GDP Growth."""
    r = SeriesResult("S090")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S090_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S090-A" in df.columns:
                primary = pd.to_numeric(df["S090-A"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S090": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s091(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S091: Total Credit Growth and Inflation (Argentina)."""
    r = SeriesResult("S091")
    try:
        df = read_source("ch15", "Appendix15_Argentina.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S091", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S091": extended}
            if ext_data is not None:
                r.data["S091-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r

def process_s092(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S092: Inflation and Currency Depreciation (Argentina)."""
    r = SeriesResult("S092")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S092_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S092" in df.columns:
                primary = pd.to_numeric(df["S092"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S092": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s225(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S225: US Real GDP by Industry (Source Table, Ch15)."""
    r = SeriesResult("S225")
    try:
        df = read_source("ch15", "Appendix15_USGDPRByIndustry.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S225", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S225": extended}
            if ext_data is not None:
                r.data["S225-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S076": process_s076,
    "S077": process_s077,
    "S078": process_s078,
    "S079": process_s079,
    "S080": process_s080,
    "S081": process_s081,
    "S082": process_s082,
    "S083": process_s083,
    "S084": process_s084,
    "S085": process_s085,
    "S086": process_s086,
    "S087": process_s087,
    "S088": process_s088,
    "S089": process_s089,
    "S090": process_s090,
    "S091": process_s091,
    "S092": process_s092,
    "S225": process_s225,
}


def process_all(reg: dict, engine: ExtensionEngine) -> list[SeriesResult]:
    results = []
    for sid, fn in PROCESSORS.items():
        try:
            results.append(fn(reg, engine))
        except Exception as e:
            results.append(SeriesResult(sid, status="fail", message=str(e)))
    return results
