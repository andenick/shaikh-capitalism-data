"""V03_S705_validate — validate processed S705 against the book chopped table."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, book_data_path  # noqa: E402
from V03_validators._ch7_validator_lib import validate_against_panel  # noqa: E402

SERIES_ID = "S705"
VALIDATOR_TOL_PCT = 1.0
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
CHOPPED_XLSX = book_data_path("Appendix7_ropdataUSind.xlsx")


def run() -> dict:
    return validate_against_panel(
        sid=SERIES_ID,
        processed_parquet=PROCESSED,
        chopped_xlsx=CHOPPED_XLSX,
        tolerance_pct=VALIDATOR_TOL_PCT,
        is_deviation=False,
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
