"""L01_S209_load - US Unemployment Rate (Fig 2.9).

Composite: BEA LTEG B1-B2 1890-1970 + Economic Report of the President Table B-40
(1948-2010). The chopped table already has all three columns including the spliced
'TotUnempl'. We emit the per-source columns and the pre-spliced book series.

Extension: FRED UNRATE (Civilian Unemployment Rate, annual avg of monthly).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch2_helpers import read_chopped, slice_column, fred_annual  # noqa: E402

CHOPPED = "Appendix2_Unemployment.xlsx"
OUT_A = DATA_RAW / "S209_BEA_LTEG_B1_B2.parquet"
OUT_B = DATA_RAW / "S209_ERP_T_B40.parquet"
OUT_C = DATA_RAW / "S209_FRED_UNRATE.parquet"


def run() -> dict:
    chopped = read_chopped(CHOPPED)
    a = slice_column(chopped, "TotUnempl1",
                     subseries_id="S209-A", subsource_id="BEA_LTEG_B1_B2",
                     units="percent")
    b = slice_column(chopped, "TotUnempl2",
                     subseries_id="S209-B", subsource_id="ERP_T_B40",
                     units="percent")
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    a.to_parquet(OUT_A, index=False)
    b.to_parquet(OUT_B, index=False)
    fred_df, ok, err = fred_annual("UNRATE", start="2005-01-01")
    sources = ["BEA_LTEG_B1_B2", "ERP_T_B40"]
    if ok and not fred_df.empty:
        fred_df["units"] = "percent"
        fred_df["subseries_id"] = "S209-C"
        fred_df["subsource_id"] = "FRED_UNRATE"
        fred_df.to_parquet(OUT_C, index=False)
        sources.append("FRED_UNRATE")
    return {
        "status": "OK",
        "rows_loaded": {"BEA_LTEG": len(a), "ERP": len(b),
                        "FRED_UNRATE": int(len(fred_df)) if ok else 0},
        "sources_fetched": sources,
        "fred_status": "ok" if ok else "skipped", "fred_error": err,
        "outputs": [str(OUT_A), str(OUT_B)] + ([str(OUT_C)] if ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
