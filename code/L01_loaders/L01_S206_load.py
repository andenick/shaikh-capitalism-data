"""L01_S206_load - Ayres Business Cycles 1903-1939 (Fig 2.4C). Historical-only."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from L01_loaders._ayres_helper import save_window  # noqa: E402

YEARS = (1903, 1939)


def run() -> dict:
    n = save_window(YEARS[0], YEARS[1], "S206", "S206_AYRES_1903_1939.parquet")
    return {
        "status": "OK",
        "rows_loaded": {"AYRES": n},
        "sources_fetched": ["AYRES_1939_T9_APP_A"],
        "extension_status": "not_applicable_discontinued",
        "outputs": ["Technical/data/raw/S206_AYRES_1903_1939.parquet"],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
