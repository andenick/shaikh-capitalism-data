"""V03_S1402_validate - validate S1402 (unemployment measures) against Appendix 14.3."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from V03_validators._ch14_validator_lib import validate_against_appendix14  # noqa: E402

SERIES_ID = "S1402"
VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1948, 2011)


def run() -> dict:
    return validate_against_appendix14(
        SERIES_ID,
        {
            f"{SERIES_ID}-A": "UNEMPLRATE",
            f"{SERIES_ID}-B": "UNEMPDURATION",
            f"{SERIES_ID}-C": "ulintensity",
        },
        overlap_range=BOOK_OVERLAP,
        tol_pct=VALIDATOR_TOL_PCT,
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
