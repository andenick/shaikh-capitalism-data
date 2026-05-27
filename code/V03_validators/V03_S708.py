"""V03_S708 — validate processed Greek IROP-deviation panel against the digitized source.

Round-trips the processed parquet against the *_Deviation columns of the digitized panel
xlsx (is_deviation=True). Certifies loader/processor fidelity; underlying values are
digitization-grade (provenance: digitized — see EXTRACTION_REPORT.md).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402
from V03_validators._ch7_validator_lib import validate_against_panel  # noqa: E402

SERIES_ID = "S708"
VALIDATOR_TOL_PCT = 1.0
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
SRC_XLSX = SALVAGED_BOOK_DATA / "Reconstructed" / "Tsoulfidis_Tsaliki_2011_Fig5_S708.xlsx"


def run() -> dict:
    return validate_against_panel(
        sid=SERIES_ID,
        processed_parquet=PROCESSED,
        chopped_xlsx=SRC_XLSX,
        tolerance_pct=VALIDATOR_TOL_PCT,
        is_deviation=True,
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
