"""Chapter 2: Turbulent Trends and Hidden Structures — Loading Phase.

Series: S001 (Industrial Production), S002 (Real Investment), S003 (GDP),
        S004 (Ayres Business Cycle), S007 (Mfg Productivity), S008 (Mfg Compensation),
        S009 (Unemployment), S017 (GDP per Capita)

Source: Shaikh (2016) Appendix 2 data tables
Public URLs: FRED (INDPRO, GPDIC1, OPHMFG, UNRATE, COMPRMS), MeasuringWorth (GDP, CPI)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.result import LoadResult

CHAPTER = "ch02"

SOURCE_FILES = {
    "S001": "Appendix2_IndustrialProduction.csv",
    "S002": "Appendix2_RealInvestmentUS_1832-2010.csv",
    "S003": "Appendix2_MeasuringWorthGDP_1889-2010.csv",
    "S004": "Appendix2_Ayres.csv",
    "S007": "Appendix2_ManufacturingProductivityAndRealWages1889-2010.csv",
    "S008": "Appendix2_ManufacturingProductivity.csv",
    "S009": "Appendix2_Unemployment.csv",
    "S017": "Appendix2_GDPperCapita.csv",
}


def _load_series(series_id: str) -> LoadResult:
    filename = SOURCE_FILES.get(series_id)
    if not filename:
        return LoadResult(series_id, status="skip", message=f"No source file for {series_id}")

    try:
        df = read_source(CHAPTER, filename)
        return LoadResult(
            series_id=series_id,
            status="ok",
            source_file=f"{CHAPTER}/{filename}",
            obs_count=len(df),
            columns=list(df.columns),
        )
    except Exception as e:
        return LoadResult(series_id, status="fail", message=str(e))


def load_all(reg: dict) -> list[LoadResult]:
    return [_load_series(sid) for sid in SOURCE_FILES]
