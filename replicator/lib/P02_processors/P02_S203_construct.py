"""P02_S203_construct - emit MeasuringWorth book-period values directly; optionally
append FRED-based real GDP per capita extension reindexed at 2010 overlap.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_MW = DATA_RAW / "S203_MEASURINGWORTH_USGDP.parquet"
IN_FRED = DATA_RAW / "S203_FRED_RGDPPC.parquet"
OUT = DATA_PROCESSED / "S203.parquet"
OVERLAP = 2010


def run() -> dict:
    if not IN_MW.exists():
        return {"status": "FAIL", "error": "MW raw missing"}
    mw = pd.read_parquet(IN_MW).rename(columns={"subsource_id": "source_id"})
    mw = mw[["year", "value", "units", "subseries_id", "source_id"]]
    diag: dict = {"extension_status": "data_unavailable", "reason": "FRED not loaded"}
    if IN_FRED.exists():
        fred = pd.read_parquet(IN_FRED)
        in_mw = mw[mw["year"] == OVERLAP]
        in_fred = fred[fred["year"] == OVERLAP]
        if not in_mw.empty and not in_fred.empty:
            mw_val = float(in_mw["value"].iloc[0])
            fred_val = float(in_fred["value"].iloc[0])
            scale = mw_val / fred_val
            ext = fred[fred["year"] > OVERLAP].copy()
            ext["value"] = ext["value"] * scale
            ext["units"] = "real_dollars_2005"
            ext = ext.rename(columns={"subsource_id": "source_id"})
            ext = ext[["year", "value", "units", "subseries_id", "source_id"]]
            mw = pd.concat([mw, ext], ignore_index=True).sort_values("year").reset_index(drop=True)
            diag = {"extension_status": "ok", "overlap_year": OVERLAP, "scale_factor": scale,
                    "years_appended": int(len(ext)), "last_year": int(mw["year"].max())}
        else:
            diag = {"extension_status": "no_overlap", "overlap_attempted": OVERLAP}
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    mw.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(mw)),
        "year_range": [int(mw["year"].min()), int(mw["year"].max())],
        "subseries_present": sorted(mw["subseries_id"].unique().tolist()),
        "extension": diag, "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
