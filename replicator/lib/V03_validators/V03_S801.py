"""V03_S801 — validate processed Eichner Fig 8.1 panel against the digitized source.

Round-trips the processed parquet against the level columns (Oligopolistic, Competitive) of the
digitized panel xlsx. Certifies loader/processor fidelity; underlying values are digitization-grade
(provenance: digitized, overlay-validated vs the book figure — see EXTRACTION_REPORT.md).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402
from V03_validators._ch7_validator_lib import validate_against_panel  # noqa: E402

SERIES_ID = "S801"
VALIDATOR_TOL_PCT = 1.0
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
SRC_XLSX = SALVAGED_BOOK_DATA / "Reconstructed" / "Eichner_1973_Fig8_1_S801.xlsx"


def run() -> dict:
    return validate_against_panel(
        sid=SERIES_ID,
        processed_parquet=PROCESSED,
        chopped_xlsx=SRC_XLSX,
        tolerance_pct=VALIDATOR_TOL_PCT,
        is_deviation=False,
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
