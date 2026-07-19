"""P02_ES2302 — pass-through with dual-subseries split for XS2302.

Decision 0009 (project-wide forecast policy: FLAG, don't truncate). The IMF WEO
vintage the loader pulls carries realized values through 2024 and forward-looking
PROJECTIONS from 2025 onward (the prior hyper-review established realized-through-2024,
2025–2031 = WEO projections). The IMF Datamapper JSON API does not expose the WEO
"estimates start after" flag per observation, so the realized/projection boundary is
recorded here as a single documented constant (``FORECAST_START_YEAR``) rather than
truncated. Rows are RETAINED; an ``is_forecast`` boolean is emitted (True for
projection years >= FORECAST_START_YEAR) and carried through the long-form chopped
writer (O06). No forecast value is ever registered as a reference_value.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "XS2302"
IN = DATA_RAW / f"{SERIES_ID}_IMF_WEO_CHN.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"

# WEO vintage boundary: realized values run through 2024; 2025+ are IMF WEO
# PROJECTIONS (Decision 0009 — flag, don't truncate). See DPR §5.
FORECAST_START_YEAR = 2025


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df.rename(columns={"subsource_id": "source_id"})
    df = df[["year", "value", "subseries_id", "source_id", "units"]].copy()
    df["is_forecast"] = df["year"] >= FORECAST_START_YEAR
    df = df.sort_values(["subseries_id", "year"]).reset_index(drop=True)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)

    n_forecast = int(df["is_forecast"].sum())
    realized = df[~df["is_forecast"]]
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "realized_year_range": [int(realized["year"].min()), int(realized["year"].max())],
        "forecast_start_year": FORECAST_START_YEAR,
        "n_forecast_rows": n_forecast,
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "ok",
                      "last_year": int(df["year"].max())},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
