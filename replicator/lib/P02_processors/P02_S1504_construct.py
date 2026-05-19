"""P02_S1504_construct - emit processed S1504 with book-period values
plus optional modern IMF cross-check rows.

Final schema: year, value, subseries_id, source_id, units.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, DATA_RAW  # noqa: E402

IN_CHOPPED = DATA_RAW / "S1504_USINFLATION_CHOPPED.parquet"
IN_IMF = DATA_RAW / "S1504_IMF_IFS_DCORP_N_DC.parquet"
OUT = DATA_PROCESSED / "S1504.parquet"


def run() -> dict:
    if not IN_CHOPPED.exists():
        return {"status": "FAIL", "error": f"chopped raw missing: {IN_CHOPPED}"}
    book = pd.read_parquet(IN_CHOPPED)

    parts = [book]
    diag = {"extension_status": "book_period_only",
            "reason": "S1504 extension requires BEA NIPA API + IMF SDMX; "
                      "modern IMF CR fetched only when available"}
    if IN_IMF.exists():
        modern = pd.read_parquet(IN_IMF)
        parts.append(modern)
        diag = {"extension_status": "imf_cr_modern_attached",
                "imf_years_attached": int(len(modern)),
                "note": "Modern DCORP_N_DC USA values attached as S1504-CR-modern subseries; "
                        "validator cross-checks against Shaikh CR over 2001-2010 overlap."}

    final = pd.concat(parts, ignore_index=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    final = final.sort_values(["year", "subseries_id"]).reset_index(drop=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": diag,
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
