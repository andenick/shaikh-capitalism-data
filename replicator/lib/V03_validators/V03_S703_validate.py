"""V03_S703_validate — data_unavailable; returns PASS_DATA_UNAVAILABLE."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from V03_validators._ch7_validator_lib import pass_data_unavailable  # noqa: E402

SERIES_ID = "S703"
VALIDATOR_TOL_PCT = None  # data_unavailable; tolerance not applicable


def run() -> dict:
    return pass_data_unavailable(
        sid=SERIES_ID,
        reason="Christodoulopoulos (1995) world ISDB panel not in SalvagedInputs; OECD ISDB 1994 discontinued. PDF figure remains; no chopped CSV.",
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
