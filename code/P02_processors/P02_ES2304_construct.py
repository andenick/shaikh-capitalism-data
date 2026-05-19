"""P02_ES2304_construct — pass-through for ES2304 literature compilation."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "ES2304"
IN = DATA_RAW / f"{SERIES_ID}_LIT_COMPILATION.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df.rename(columns={"subsource_id": "source_id"})
    # Need (year, subseries_id) uniqueness for chopped writer; if duplicate years
    # exist (multiple estimates same year), use study as country_key analog
    cols = ["year", "value", "subseries_id", "source_id", "units"]
    if df.duplicated(["year", "subseries_id"]).any():
        # Disambiguate via country_key (chopped writer recognizes country_key)
        df["country_key"] = df["study"] + "_" + df["year"].astype(str)
        cols.append("country_key")
    out = df[cols].copy()
    out = out.sort_values(["subseries_id", "year"]).reset_index(drop=True)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_processed": int(len(out)),
        "year_range": [int(out["year"].min()), int(out["year"].max())],
        "subseries_present": sorted(out["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_literature_compilation",
                      "reason": "4 cited reviews are 2005-2012 snapshots; debate moved to IMF EBA post-2014 (methodologically distinct)"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
