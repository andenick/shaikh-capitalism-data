"""V03_S704_validate — data_unavailable; returns PASS_DATA_UNAVAILABLE."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from V03_validators._ch7_validator_lib import pass_data_unavailable  # noqa: E402

SERIES_ID = "S704"
VALIDATOR_TOL_PCT = None  # data_unavailable; tolerance not applicable


def run() -> dict:
    return pass_data_unavailable(
        sid=SERIES_ID,
        reason="Christodoulopoulos (1995) US ISDB sub-industry panel not in SalvagedInputs; OECD ISDB 1994 discontinued.",
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
