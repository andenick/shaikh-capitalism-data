"""Chapter 14: Classical Phillips Curve -- Loading Phase.

Series: S068, S069, S070, S071, S072...
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.result import LoadResult

SOURCE_FILES = {
    "S068": ("ch14", "Appendix14_InflationULdata.csv"),
    "S069": ("ch14", "Appendix14_InflationULdata.csv"),
    "S070": ("ch14", "Appendix14_InflationULdata.csv"),
    "S071": ("ch14", "Appendix14_InflationULdata.csv"),
    "S072": ("ch14", "Appendix14_InflationULdata.csv"),
    "S073": ("ch14", "Appendix14_InflationULdata.csv"),
    "S074": ("ch14", "Appendix14_InflationULdata.csv"),
    "S075": ("ch14", "Appendix14_InflationULdata.csv"),
    "S202": ("ch14", "Appendix14_InflationULdata.csv"),
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
