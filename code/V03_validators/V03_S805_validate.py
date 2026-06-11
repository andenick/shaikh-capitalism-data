"""V03_S805_validate — validate S805 against Demsetz 1973b Table 4 chopped xlsx."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402
from V03_validators._ch8_validator_lib import validate_long_form  # noqa: E402

SERIES_ID = "S805"
VALIDATOR_TOL_PCT = 0.5  # cross_sectional per playbook

PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix8_DemsetzRatesOfReturn.xlsx"


def _truth() -> pd.DataFrame:
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=None)
    data = raw.iloc[2:8, :3].reset_index(drop=True)
    data.columns = ["cr4_bin", "y1963", "y1969"]
    rows = []
    for _, r in data.iterrows():
        bin_label = str(r["cr4_bin"]).strip()
        rows.append({"year": 1963, "subseries_id": "S805-1963",
                     "cr4_bin": bin_label, "expected": float(r["y1963"])})
        rows.append({"year": 1969, "subseries_id": "S805-1969",
                     "cr4_bin": bin_label, "expected": float(r["y1969"])})
    return pd.DataFrame(rows)


def run() -> dict:
    return validate_long_form(
        sid=SERIES_ID,
        processed_parquet=PROCESSED,
        truth_long=_truth(),
        tolerance_pct=VALIDATOR_TOL_PCT,
        join_keys=["year", "subseries_id", "cr4_bin"],
        content_type="cross_sectional",
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
