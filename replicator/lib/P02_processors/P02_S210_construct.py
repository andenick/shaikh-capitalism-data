"""P02_S210_construct - emit US and UK WPI on 1930=100 base; extend US via FRED."""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_US = DATA_RAW / "S210_US_WPI_BOOK.parquet"
IN_UK = DATA_RAW / "S210_UK_WPI_BOOK.parquet"
IN_US_EXT = DATA_RAW / "S210_FRED_WPU00000000.parquet"
OUT = DATA_PROCESSED / "S210.parquet"
EXT_OVERLAP = 2010


def run() -> dict:
    if not IN_US.exists() or not IN_UK.exists():
        return {"status": "FAIL", "error": "raw missing"}
    us = pd.read_parquet(IN_US).rename(columns={"subsource_id": "source_id"})
    uk = pd.read_parquet(IN_UK).rename(columns={"subsource_id": "source_id"})
    us = us[["year", "value", "units", "subseries_id", "source_id"]]
    uk = uk[["year", "value", "units", "subseries_id", "source_id"]]
    diag = {"extension_status": "data_unavailable"}
    parts = [us, uk]
    if IN_US_EXT.exists():
        ext_raw = pd.read_parquet(IN_US_EXT).rename(columns={"subsource_id": "source_id"})
        in_book = us[us["year"] == EXT_OVERLAP]
        in_ext = ext_raw[ext_raw["year"] == EXT_OVERLAP]
        if not in_book.empty and not in_ext.empty:
            bv = float(in_book["value"].iloc[0]); ev = float(in_ext["value"].iloc[0])
            if ev:
                scale = bv / ev
                ext = ext_raw[ext_raw["year"] > EXT_OVERLAP].copy()
                ext["value"] = ext["value"] * scale
                ext["units"] = "index_1930=100"
                ext = ext[["year", "value", "units", "subseries_id", "source_id"]]
                parts.append(ext)
                diag = {"extension_status": "ok", "country": "US-only",
                        "overlap_year": EXT_OVERLAP, "scale_factor": scale,
                        "years_appended": int(len(ext)),
                        "note": "UK extension requires ONS PLLU which is not in our FRED pull; US-only continuation"}
    final = pd.concat(parts, ignore_index=True).sort_values(["subseries_id", "year"]).reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": diag, "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
