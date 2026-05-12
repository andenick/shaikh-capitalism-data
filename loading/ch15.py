"""Chapter 15: Money and Inflation -- Loading Phase.

Series: S076, S077, S078, S079, S080...
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.result import LoadResult

SOURCE_FILES = {
    "S076": ("ch15", "Appendix15_MeasuringWorthCPI.csv"),
    "S077": ("ch15", "Appendix15_USGDPRByIndustry.csv"),
    "S078": ("ch15", "Appendix15_USGDPRByIndustry.csv"),
    "S079": ("ch15", "Appendix15_USInflation.csv"),
    "S080": ("ch15", "Appendix15_USInflation.csv"),
    "S081": ("ch15", "Appendix15_USInflation.csv"),
    "S082": ("ch15", "Appendix15_USInflation.csv"),
    "S083": ("ch15", "Appendix15_USInflation.csv"),
    "S084": ("ch15", "Appendix15_USInflation.csv"),
    "S085": ("ch15", "Appendix15_USInflation.csv"),
    "S086": ("ch15", "Appendix15_USInflation.csv"),
    "S087": ("ch15", "Appendix15_USInflation.csv"),
    "S088": ("ch15", "Appendix15_WorldInflationDataByCountry.csv"),
    "S089": ("ch15", "Appendix15_WorldInflationDataLambda.csv"),
    "S090": ("ch15", "Appendix15_Argentina.csv"),
    "S091": ("ch15", "Appendix15_Argentina.csv"),
    "S092": ("ch15", "Appendix15_Argentina.csv"),
    "S225": ("ch15", "Appendix15_USGDPRByIndustry.csv"),
}


def _load_series(series_id: str) -> LoadResult:
    entry = SOURCE_FILES.get(series_id)
    if not entry:
        return LoadResult(series_id, status="skip", message="No source file")
    chapter_dir, filename = entry
    try:
        df = read_source(chapter_dir, filename)
        return LoadResult(series_id, status="ok", source_file=f"{chapter_dir}/{filename}",
                          obs_count=len(df), columns=list(df.columns))
    except Exception as e:
        return LoadResult(series_id, status="fail", message=str(e))


def load_all(reg: dict) -> list[LoadResult]:
    return [_load_series(sid) for sid in SOURCE_FILES]
