"""V03_S804_validate — validate S804 against Stigler 1963 Table 17 chopped xlsx."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402
from V03_validators._ch8_validator_lib import validate_long_form  # noqa: E402

SERIES_ID = "S804"
VALIDATOR_TOL_PCT = 1.0  # time_series per playbook

PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix8_StiglerRatesOfProfit.xlsx"


def _truth() -> pd.DataFrame:
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=None)
    data = raw.iloc[2:8, :3].reset_index(drop=True)
    data.columns = ["bin_label", "unconc", "conc"]
    rows = []
    for _, r in data.iterrows():
        rows.append({"bin_label": str(r["bin_label"]).strip(),
                     "subseries_id": "S804-UNCONC", "expected": float(r["unconc"])})
        rows.append({"bin_label": str(r["bin_label"]).strip(),
                     "subseries_id": "S804-CONC", "expected": float(r["conc"])})
    return pd.DataFrame(rows)


def run() -> dict:
    return validate_long_form(
        sid=SERIES_ID,
        processed_parquet=PROCESSED,
        truth_long=_truth(),
        tolerance_pct=VALIDATOR_TOL_PCT,
        join_keys=["bin_label", "subseries_id"],
        content_type="time_series",
    )


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
