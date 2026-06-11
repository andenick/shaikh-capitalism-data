"""P02_S1509_construct - emit processed S1509 (Ramamurthy cross-section)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, DATA_RAW  # noqa: E402

IN = DATA_RAW / "S1509_RAMAMURTHY_PANEL.parquet"
OUT = DATA_PROCESSED / "S1509.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    keep = ["year", "value", "subseries_id", "source_id", "units"]
    extras = [c for c in ["country_key", "country", "episode",
                          "inflation_period", "credit_period"] if c in df.columns]
    df = df[keep + extras]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "n_country_episodes": int(df["country_key"].nunique()) if "country_key" in df.columns else 0,
        "n_unique_countries": int(df["country"].nunique()) if "country" in df.columns else 0,
        "content_type": "cross_sectional",
        "extension": {"extension_status": "not_applicable_cross_sectional"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
