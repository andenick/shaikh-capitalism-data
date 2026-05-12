"""Chapter 2: Turbulent Trends and Hidden Structures — Processing Phase.

8 series covering 18 figures, demonstrating long-run patterns in US capitalism.
Each function loads source data, applies construction steps, extends with API data.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.extension import ExtensionEngine
from lib.result import SeriesResult
from lib.transforms.reindex import reindex, reindex_to_match
from lib.transforms.splice import splice

CHAPTER = "ch02"


def process_s001(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S001: US Industrial Production Index (Fig 2.1).

    Source: BEA LTEG 1860-1970 (1913=100) + FRB 1919-2010 (2007=100).
    Construction: Reindex both to 1958=100, splice at 1919.
    Extension: FRED INDPRO (growth-rate splice at 2010).
    """
    r = SeriesResult("S001")
    df = read_source(CHAPTER, "Appendix2_IndustrialProduction.csv")

    s001_a = df.iloc[:, 0].dropna()  # BEA original
    s001_b = reindex(s001_a, base_year=1958)
    r.step("reindex_A", "ok", f"BEA reindexed to 1958=100, {len(s001_b)} obs")

    s001_c = df.iloc[:, 2].dropna() if df.shape[1] > 2 else pd.Series(dtype=float)
    s001_d = reindex_to_match(s001_c, s001_b, at_year=1919) if len(s001_c) > 0 else pd.Series(dtype=float)
    r.step("reindex_C", "ok", f"FRB reindexed to match BEA at 1919")

    composite = splice(s001_b, s001_d, at_year=1919) if len(s001_d) > 0 else s001_b
    r.step("splice", "ok", f"Spliced at 1919, {len(composite)} obs")

    extended, ext_data, desc = engine.extend("S001", composite)
    r.step("extend", "ok" if ext_data is not None else "skip", desc)

    r.data = {"S001-A": s001_a, "S001-B": s001_b, "S001": extended}
    if s001_c is not None and len(s001_c) > 0:
        r.data["S001-C"] = s001_c
        r.data["S001-D"] = s001_d
    if ext_data is not None:
        r.data["S001-EXT"] = ext_data
        r.data["S001-F"] = ext_data  # reindexed extension
    r.extension = ext_data
    r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
    return r


def process_s002(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S002: US Real Investment."""
    r = SeriesResult("S002")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S002_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S002" in df.columns:
                primary = pd.to_numeric(df["S002"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S002": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s003(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S003: US GDP (MeasuringWorth)."""
    r = SeriesResult("S003")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S003_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S003" in df.columns:
                primary = pd.to_numeric(df["S003"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S003": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s004(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S004: Ayres Business Cycle Index (Fig 2.4A-C).

    Source: Ayres (1939), 1831-1939. Historical, not extendable.
    """
    r = SeriesResult("S004")
    df = read_source(CHAPTER, "Appendix2_Ayres.csv")
    s004_a = df.iloc[:, 0].dropna()
    s004_a = s004_a[s004_a.index.notna()]
    r.step("process", "ok", f"{len(s004_a)} obs (1831-1939, historical)")
    r.data = {"S004-A": s004_a, "S004": s004_a}
    if len(s004_a) > 0:
        r.year_range = f"{int(s004_a.index.min())}–{int(s004_a.index.max())}"
    return r


def process_s007(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S007: Manufacturing Productivity and Real Wages (Fig 2.5).

    Source: BEA/BLS 1889-2010, spliced at 1950.
    Extension: FRED OPHMFG (growth-rate splice at 2009).
    """
    r = SeriesResult("S007")
    df = read_source(CHAPTER, "Appendix2_ManufacturingProductivityAndRealWages1889-2010.csv")

    s007_a = df.iloc[:, 0].dropna()
    s007_b = reindex(s007_a, base_year=1958)
    s007_c = df.iloc[:, 2].dropna() if df.shape[1] > 2 else pd.Series(dtype=float)
    s007_d = reindex_to_match(s007_c, s007_b, at_year=1950) if len(s007_c) > 0 else pd.Series(dtype=float)
    composite = splice(s007_b, s007_d, at_year=1950) if len(s007_d) > 0 else s007_b

    extended, ext_data, desc = engine.extend("S007", composite)
    r.step("process", "ok", f"{len(composite)} obs")
    r.step("extend", "ok" if ext_data is not None else "skip", desc)

    r.data = {"S007-A": s007_a, "S007-B": s007_b, "S007": extended}
    if ext_data is not None:
        r.data["S007-EXT"] = ext_data
    r.extension = ext_data
    r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
    return r


def process_s008(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S008: Manufacturing Real Compensation (Fig 2.6).

    Source: Multiple BEA/BLS sources 1790-2010.
    Extension: FRED COMPRMS (real manufacturing hourly compensation, growth-rate splice at 2010).
    """
    r = SeriesResult("S008")
    df = read_source(CHAPTER, "Appendix2_ManufacturingProductivity.csv")

    cols = df.columns.tolist()
    composite = df.iloc[:, 2].dropna() if df.shape[1] > 2 else df.iloc[:, 0].dropna()

    extended, ext_data, desc = engine.extend("S008", composite)
    r.step("process", "ok", f"{len(composite)} obs")
    r.step("extend", "ok" if ext_data is not None else "skip", desc)

    r.data = {"S008": extended}
    for i, col in enumerate(cols[:5]):
        r.data[f"S008-{chr(65+i)}"] = df.iloc[:, i].dropna()
    if ext_data is not None:
        r.data["S008-EXT"] = ext_data
    r.extension = ext_data
    r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
    return r


def process_s009(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S009: US Unemployment Rate (Fig 2.7).

    Source: BEA LTEG 1890-1970 + ERP 1948-2010, spliced at 1970.
    Extension: FRED UNRATE (direct levels, splice at 2010).
    """
    r = SeriesResult("S009")
    df = read_source(CHAPTER, "Appendix2_Unemployment.csv")

    s009_a = df.iloc[:, 0].dropna()
    s009_b = df.iloc[:, 1].dropna() if df.shape[1] > 1 else pd.Series(dtype=float)
    composite = splice(s009_a, s009_b, at_year=1970) if len(s009_b) > 0 else s009_a

    extended, ext_data, desc = engine.extend("S009", composite)
    r.step("process", "ok", f"{len(composite)} obs")
    r.step("extend", "ok" if ext_data is not None else "skip", desc)

    r.data = {"S009-A": s009_a, "S009": extended}
    if len(s009_b) > 0:
        r.data["S009-B"] = s009_b
    if ext_data is not None:
        r.data["S009-EXT"] = ext_data
    r.extension = ext_data
    r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
    return r


def process_s017(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S017: GDP per Capita, Maddison (Fig 2.15-17).

    Source: Maddison historical data, 1710-2000.
    Extension: Maddison Project Database 2023 (growth-rate splice at 2000).
    """
    r = SeriesResult("S017")
    df = read_source(CHAPTER, "Appendix2_GDPperCapita.csv")

    # Wide format — many countries. Use first column as primary.
    s017_a = df.iloc[:, 0].dropna()
    extended, ext_data, desc = engine.extend("S017", s017_a)
    r.step("process", "ok", f"{len(s017_a)} obs (wide table)")
    r.step("extend", "ok" if ext_data is not None else "skip", desc)

    r.data = {"S017-A": s017_a, "S017": extended}
    if ext_data is not None:
        r.data["S017-EXT"] = ext_data
    r.extension = ext_data
    r.year_range = f"{int(extended.index.min())}–{int(extended.index.max())}"
    return r


PROCESSORS = {
    "S001": process_s001,
    "S002": process_s002,
    "S003": process_s003,
    "S004": process_s004,
    "S007": process_s007,
    "S008": process_s008,
    "S009": process_s009,
    "S017": process_s017,
}


def process_all(reg: dict, engine: ExtensionEngine) -> list[SeriesResult]:
    results = []
    for sid, fn in PROCESSORS.items():
        try:
            result = fn(reg, engine)
            results.append(result)
        except Exception as e:
            r = SeriesResult(sid, status="fail", message=str(e))
            results.append(r)
    return results
