"""L01_S207_load - US Manufacturing Productivity & Production Worker Real Compensation.

Two co-plotted series (Fig 2.7), both indexed to 1889 = 100:
  - S207-A: Productivity (spliced BEA LTEG A173 1860-1970 + BLS FLS Table 1 1950-2009)
            from Appendix2_ManufacturingProductivityAndRealWages1889-2010.xlsx
            column 'Mfgprdvty_spliced_Reindexed1889'.
  - S207-B: Production-worker real compensation per hour (nominal/CPI)
            from Appendix2_ManufacturingProductivity.xlsx column 'mfgprdwkrecrealindex'.

Phase 4 substitutions applied:
  - MeasuringWorth /datasets/uscompensation/ -> /datasets/uswage/ (URL rename only);
    the salvaged chopped table already contains Shaikh's pulled values, so no
    re-fetch needed for the book period.
  - BLS FLS sunset 2013 -> FRED OPHMFG (US-only continuation; document concept
    narrowing in EPR). Compensation extension via FRED COMPRMS (Mfg Real
    Compensation per Hour) which continues the BLS production-worker concept
    in US-only form.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch2_helpers import read_chopped, slice_column, fred_annual  # noqa: E402

CHOPPED_PROD = "Appendix2_ManufacturingProductivityAndRealWages1889-2010.xlsx"
CHOPPED_COMP = "Appendix2_ManufacturingProductivity.xlsx"
OUT_PROD = DATA_RAW / "S207_PROD_BOOK.parquet"
OUT_COMP = DATA_RAW / "S207_COMP_BOOK.parquet"
OUT_FRED_PROD = DATA_RAW / "S207_FRED_OPHMFG.parquet"
OUT_FRED_COMP = DATA_RAW / "S207_FRED_COMPRMS.parquet"


def run() -> dict:
    prod_chop = read_chopped(CHOPPED_PROD)
    comp_chop = read_chopped(CHOPPED_COMP)
    prod = slice_column(
        prod_chop, "Mfgprdvty_spliced_Reindexed1889",
        subseries_id="S207-A", subsource_id="BEA_LTEG_BLS_FLS_SPLICE",
        units="index_1889=100",
    )
    comp = slice_column(
        comp_chop, "mfgprdwkrecrealindex",
        subseries_id="S207-B", subsource_id="MEASURINGWORTH_USWAGE_CPI",
        units="index_1889=100",
    )
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    prod.to_parquet(OUT_PROD, index=False)
    comp.to_parquet(OUT_COMP, index=False)
    # Extensions via FRED
    sources = ["BEA_LTEG_BLS_FLS_SPLICE", "MEASURINGWORTH_USWAGE_CPI"]
    fred_prod_df, ok_p, err_p = fred_annual("OPHMFG", start="2005-01-01")
    if ok_p and not fred_prod_df.empty:
        fred_prod_df["units"] = "index_2017=100"
        fred_prod_df["subseries_id"] = "S207-C"
        fred_prod_df["subsource_id"] = "FRED_OPHMFG"
        fred_prod_df.to_parquet(OUT_FRED_PROD, index=False)
        sources.append("FRED_OPHMFG")
    fred_comp_df, ok_c, err_c = fred_annual("COMPRMS", start="2005-01-01")
    if ok_c and not fred_comp_df.empty:
        fred_comp_df["units"] = "index_2017=100"
        fred_comp_df["subseries_id"] = "S207-D"
        fred_comp_df["subsource_id"] = "FRED_COMPRMS"
        fred_comp_df.to_parquet(OUT_FRED_COMP, index=False)
        sources.append("FRED_COMPRMS")
    return {
        "status": "OK",
        "rows_loaded": {
            "PROD_BOOK": len(prod), "COMP_BOOK": len(comp),
            "FRED_OPHMFG": int(len(fred_prod_df)) if ok_p else 0,
            "FRED_COMPRMS": int(len(fred_comp_df)) if ok_c else 0,
        },
        "sources_fetched": sources,
        "fred_status": {"OPHMFG": "ok" if ok_p else "skipped",
                        "COMPRMS": "ok" if ok_c else "skipped"},
        "fred_error": {"OPHMFG": err_p, "COMPRMS": err_c},
        "outputs": [str(OUT_PROD), str(OUT_COMP)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
