"""V03_S802_validate — validate S802 against Semmler 1984 Table 3.3 chopped xlsx."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402
from V03_validators._ch8_validator_lib import validate_long_form  # noqa: E402

SERIES_ID = "S802"
VALIDATOR_TOL_PCT = 0.5  # cross_sectional per playbook

PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix8_Semmler19843.3.xlsx"


def _truth() -> pd.DataFrame:
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=None)
    data = raw.iloc[2:5, :].reset_index(drop=True)
    data.columns = ["cr4_midpoint", "C1957", "C1960", "C1969"]
    rows = []
    for _, r in data.iterrows():
        cr = int(float(r["cr4_midpoint"]))
        for yr, col in ((1957, "C1957"), (1960, "C1960"), (1969, "C1969")):
            rows.append({
                "year": int(yr),
                "subseries_id": f"S802-C{yr}",
                "cr4_midpoint": cr,
                "expected": float(r[col]),
            })
    return pd.DataFrame(rows)


def run() -> dict:
    return validate_long_form(
        sid=SERIES_ID,
        processed_parquet=PROCESSED,
        truth_long=_truth(),
        tolerance_pct=VALIDATOR_TOL_PCT,
        join_keys=["year", "subseries_id", "cr4_midpoint"],
        content_type="cross_sectional",
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
