"""P02_S1007_construct — Equity Rate vs Corporate IROP.

Pass-through of three derived columns from Appendix10 IntroPPrice.
Extension deferred to Phase 6 per adequacy report.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_A = DATA_RAW / "S1007_rreq.parquet"
IN_B = DATA_RAW / "S1007_iropcorp.parquet"
IN_C = DATA_RAW / "S1007_iropcorpnipa.parquet"
OUT = DATA_PROCESSED / "S1007.parquet"


def run() -> dict:
    missing = [str(p) for p in (IN_A, IN_B, IN_C) if not p.exists()]
    if missing:
        return {"status": "FAIL", "error": "raw parquet missing", "missing": missing}
    parts = [pd.read_parquet(p) for p in (IN_A, IN_B, IN_C)]
    df = pd.concat(parts, ignore_index=True).rename(columns={"subsource_id": "source_id"})
    df = df.sort_values(["year", "subseries_id"]).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "deferred_to_phase6"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
