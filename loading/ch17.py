"""Chapter 17: Inequality -- Loading Phase.

Series: S102, S103, S104
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.result import LoadResult

SOURCE_FILES = {
    "S102": ("ch17", "Appendix17_USIRS2011.csv"),
    "S103": ("ch17", "Appendix17_USIRS2011.csv"),
    "S104": ("ch17", "Appendix17_USIRS2011.csv"),
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
