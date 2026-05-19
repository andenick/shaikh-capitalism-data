"""V03_S801_validate — data_unavailable; returns PASS_DATA_UNAVAILABLE."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from V03_validators._ch8_validator_lib import pass_data_unavailable  # noqa: E402

SERIES_ID = "S801"
VALIDATOR_TOL_PCT = None  # data_unavailable; tolerance not applicable


def run() -> dict:
    return pass_data_unavailable(
        sid=SERIES_ID,
        reason=(
            "Eichner (1973) Fig 8.1 is chart-only with no underlying table in the "
            "publication; Shaikh did not transcribe values; no Appendix8_* chopped "
            "table exists for this figure; PDF not in RSCD workspace. Phase 5 "
            "blocker B6 resolved as data_unavailable. Per playbook recipe."
        ),
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
