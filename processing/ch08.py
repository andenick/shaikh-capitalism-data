"""Chapter 8: Competition and Concentration -- Processing Phase.

Series: S841, S842, S843, S844, S845...
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


def process_s841(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S841: Bain 42-Industry Aggregates (Grouped Data) (Fig8.4)."""
    r = SeriesResult("S841")
    try:
        df = read_source("ch08", "Appendix8_Bain42IndustryAggregates.csv")
        if "FPR008_C1" in df.columns:
            primary = pd.to_numeric(df["FPR008_C1"], errors="coerce").dropna()
        else:
            primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S841", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S841": extended}
            if ext_data is not None:
                r.data["S841-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s842(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S842: Bain 42-Industry Profit Rate vs CR8 (Scatter)."""
    r = SeriesResult("S842")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S842_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S842": primary}
            r.step("process", "ok", f"{len(primary)} obs")
            if len(primary) > 0:
                r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s843(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S843: Semmler Price Behavior Data (Fig8.2)."""
    r = SeriesResult("S843")
    try:
        df = read_source("ch08", "Appendix8_Semmler19843.3.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) == 0 and df.shape[1] > 1:
            primary = df.iloc[:, 1].dropna()
            primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S843", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S843": extended}
            if ext_data is not None:
                r.data["S843-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s844(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S844: Stigler Profit Rates on Assets."""
    r = SeriesResult("S844")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S844_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S844": primary}
            r.step("process", "ok", f"{len(primary)} obs")
            if len(primary) > 0:
                r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s845(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S845: Demsetz Rates of Return by CR4."""
    r = SeriesResult("S845")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S845_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S845": primary}
            r.step("process", "ok", f"{len(primary)} obs")
            if len(primary) > 0:
                r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s846(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S846: Corrected Bain Data (Demsetz 1973) (N/A)."""
    r = SeriesResult("S846")
    try:
        df = read_source("ch08", "Appendix8_CorrectedBainData.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) == 0 and df.shape[1] > 1:
            primary = df.iloc[:, 1].dropna()
            primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S846", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S846": extended}
            if ext_data is not None:
                r.data["S846-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S841": process_s841,
    "S842": process_s842,
    "S843": process_s843,
    "S844": process_s844,
    "S845": process_s845,
    "S846": process_s846,
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
