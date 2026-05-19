"""L01_S204_load - Ayres Business Cycles 1831-1866 (Fig 2.4A). Historical-only."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from L01_loaders._ayres_helper import save_window  # noqa: E402

YEARS = (1831, 1866)


def run() -> dict:
    n = save_window(YEARS[0], YEARS[1], "S204", "S204_AYRES_1831_1866.parquet")
    return {
        "status": "OK",
        "rows_loaded": {"AYRES": n},
        "sources_fetched": ["AYRES_1939_T9_APP_A"],
        "extension_status": "not_applicable_discontinued",
        "outputs": [f"Technical/data/raw/S204_AYRES_1831_1866.parquet"],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
