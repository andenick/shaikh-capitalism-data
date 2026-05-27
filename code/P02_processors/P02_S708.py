"""P02_S708 — process the digitized Greek IROP-deviation panel to canonical schema."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402
from P02_processors._ch7_industry_panel_processor import process_panel  # noqa: E402

SERIES_ID = "S708"
IN = DATA_RAW / "S708_TT2011_FIG5_DEV.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"


def run() -> dict:
    return process_panel(IN, OUT)


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
