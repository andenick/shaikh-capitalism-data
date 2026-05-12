"""Chapter 6: The Rate of Profit -- Loading Phase.

Series: S013, S026, S027, S028, S105...
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.chopped_io import read_source
from lib.result import LoadResult

SOURCE_FILES = {
    "S013": ("ch06", "Appendix6_Table68II7.csv"),
    "S206": ("ch06", "Appendix6_Table68I1.csv"),
    "S207": ("ch06", "Appendix6_Table68I2.csv"),
    "S208": ("ch06", "Appendix6_Table68I3.csv"),
    "S209": ("ch06", "Appendix6_Table68II1.csv"),
    "S210": ("ch06", "Appendix6_Table68II2.csv"),
    "S211": ("ch06", "Appendix6_Table68II3.csv"),
    "S212": ("ch06", "Appendix6_Table68II4.csv"),
    "S213": ("ch06", "Appendix6_Table68II5.csv"),
    "S214": ("ch06", "Appendix6_Table68II6.csv"),
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
