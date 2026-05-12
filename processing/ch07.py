"""Chapter 7: Real Competition -- Processing Phase.

Series: S034, S035, S036, S037, S038...
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


def process_s034(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S034: US Industry Average Rates of Profit."""
    r = SeriesResult("S034")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S034_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S034" in df.columns:
                primary = pd.to_numeric(df["S034"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S034": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s035(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S035: US Industry Profit Rate Deviations from Average."""
    r = SeriesResult("S035")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S035_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S035" in df.columns:
                primary = pd.to_numeric(df["S035"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S035": primary}
            r.step("process", "ok", f"{len(primary)} obs")
            if len(primary) > 0:
                r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "No chopped output")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s036(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S036: US Industry Incremental Rates of Profit."""
    r = SeriesResult("S036")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S036_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S036" in df.columns:
                primary = pd.to_numeric(df["S036"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S036": primary}
            r.step("process", "ok", f"{len(primary)} obs (from validated chopped)")
            r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "Chopped output not found")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s037(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S037: US Industry IROP Deviations from Average."""
    r = SeriesResult("S037")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S037_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S037" in df.columns:
                primary = pd.to_numeric(df["S037"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S037": primary}
            r.step("process", "ok", f"{len(primary)} obs")
            if len(primary) > 0:
                r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "No chopped output")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s038(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S038: OECD Industry IROP Deviations (PPP-adjusted)."""
    r = SeriesResult("S038")
    try:
        chopped = Path(__file__).resolve().parent.parent / "data" / "output" / "chopped" / "S038_chopped.csv"
        if chopped.exists():
            with open(chopped, "r") as f:
                for i, line in enumerate(f):
                    if line.startswith("year,") or line.startswith("Year,"):
                        break
            df = pd.read_csv(chopped, skiprows=i, index_col=0)
            if "S038" in df.columns:
                primary = pd.to_numeric(df["S038"], errors="coerce").dropna()
            else:
                primary = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
            primary = primary[primary.index.notna()]
            r.data = {"S038": primary}
            r.step("process", "ok", f"{len(primary)} obs")
            if len(primary) > 0:
                r.year_range = f"{int(primary.index.min())}–{int(primary.index.max())}"
        else:
            r.step("process", "skip", "No chopped output")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s050(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S050: Bank vs Private Industry IROP (Fig10.1)."""
    r = SeriesResult("S050")
    try:
        # Derived from S215
        df = read_source("ch07", "Appendix7_iropdataUSind.csv")
        # Extract subseries columns
        subseries = reg.get("series", reg).get("S050", {}).get("subseries", {})
        extracted = _extract_columns(df, "S050", subseries)
        primary = extracted.get("S050", extracted.get(list(extracted.keys())[0]) if extracted else pd.Series(dtype=float))

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S050", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S050": extended}
            if ext_data is not None:
                r.data["S050-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s215(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S215: US Industry Incremental Rates of Profit (IROP) (N/A)."""
    r = SeriesResult("S215")
    try:
        df = read_source("ch07", "Appendix7_iropdataUSind.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) == 0 and df.shape[1] > 1:
            primary = df.iloc[:, 1].dropna()
            primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S215", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S215": extended}
            if ext_data is not None:
                r.data["S215-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s216(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S216: OECD Industry IROP (PPP-adjusted) (N/A)."""
    r = SeriesResult("S216")
    try:
        df = read_source("ch07", "Appendix7_iropOECDPPP.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) == 0 and df.shape[1] > 1:
            primary = df.iloc[:, 1].dropna()
            primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S216", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S216": extended}
            if ext_data is not None:
                r.data["S216-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


def process_s217(reg: dict, engine: ExtensionEngine) -> SeriesResult:
    """S217: US Industry Average Rates of Profit (ROP) (N/A)."""
    r = SeriesResult("S217")
    try:
        df = read_source("ch07", "Appendix7_ropdataUSind.csv")
        primary = df.iloc[:, 0].dropna()
        primary = primary[primary.index.notna()]
        if len(primary) == 0 and df.shape[1] > 1:
            primary = df.iloc[:, 1].dropna()
            primary = primary[primary.index.notna()]

        if len(primary) > 0:
            extended, ext_data, desc = engine.extend("S217", primary)
            r.step("process", "ok", f"{len(primary)} obs")
            r.step("extend", "ok" if ext_data is not None else "skip", desc)
            r.data = {"S217": extended}
            if ext_data is not None:
                r.data["S217-EXT"] = ext_data
            r.extension = ext_data
            r.year_range = f"{int(extended.index.min())}\u2013{int(extended.index.max())}"
        else:
            r.step("process", "skip", "No data available")
    except Exception as e:
        r.status = "fail"
        r.message = str(e)
    return r


PROCESSORS = {
    "S034": process_s034,
    "S035": process_s035,
    "S036": process_s036,
    "S037": process_s037,
    "S038": process_s038,
    "S050": process_s050,
    "S215": process_s215,
    "S216": process_s216,
    "S217": process_s217,
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
