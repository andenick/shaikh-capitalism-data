"""L01_S205_load - Ayres Business Cycles 1867-1902 (Fig 2.4B). Historical-only."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from L01_loaders._ayres_helper import save_window  # noqa: E402

YEARS = (1867, 1902)


def run() -> dict:
    n = save_window(YEARS[0], YEARS[1], "S205", "S205_AYRES_1867_1902.parquet")
    return {
        "status": "OK",
        "rows_loaded": {"AYRES": n},
        "sources_fetched": ["AYRES_1939_T9_APP_A"],
        "extension_status": "not_applicable_discontinued",
        "outputs": ["Technical/data/raw/S205_AYRES_1867_1902.parquet"],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
