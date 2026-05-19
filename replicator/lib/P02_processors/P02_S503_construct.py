"""P02_S503_construct - concatenate UK p' and UK pG into S503 (book period only, v1)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_PPRIME = DATA_RAW / "S503_UK_WPI_in_GOLD.parquet"
IN_PG = DATA_RAW / "S503_UK_GOLD_PRICE_IDX.parquet"
OUT = DATA_PROCESSED / "S503.parquet"


def run() -> dict:
    for p in (IN_PPRIME, IN_PG):
        if not p.exists():
            return {"status": "FAIL", "error": f"missing {p}"}
    pprime = pd.read_parquet(IN_PPRIME).rename(columns={"subsource_id": "source_id"})
    pg = pd.read_parquet(IN_PG).rename(columns={"subsource_id": "source_id"})
    final = pd.concat([pprime, pg], ignore_index=True).sort_values(
        ["year", "subseries_id"]).reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_attempted_v1",
                      "reason": "missing_uk_wpi_2011plus_AND_missing_lbma_helper"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
