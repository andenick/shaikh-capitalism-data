"""V03_S1408_validate - validate S1408 (HP100 nominal-wage Phillips) against Appendix 14.3."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from V03_validators._ch14_validator_lib import validate_against_appendix14  # noqa: E402

SERIES_ID = "S1408"
VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1949, 2011)


def run() -> dict:
    return validate_against_appendix14(
        SERIES_ID,
        {
            f"{SERIES_ID}-A": "GMWAGEHP100",
            f"{SERIES_ID}-B": "ulintensityhp100",
        },
        overlap_range=BOOK_OVERLAP,
        tol_pct=VALIDATOR_TOL_PCT,
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
