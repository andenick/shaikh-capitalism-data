"""P02_S1605_construct - assemble S1605 household debt-to-income ratio.

Book-period (1975-2012): pass-through composite of HHDebt, HHDispPersInc, and
HHDebtIncRatio columns from Appendix 16.2.  Both Appendix numerator and
denominator are already in billions USD, so no unit conversion is needed for
the book-period ratio (which is also stored ready-made in the Appendix).

Extension period (2013-2024) - DEFERRED TO PHASE 6.  When implemented, the
extension MUST apply the following dimensional-analysis-corrected formula,
which is the SAME failure mode the anu-framework Unit Documentation rule
warns about and which CD2's CMDEBT/PI implementation got wrong by 1000x:

    # ------------------------------------------------------------------
    # DIMENSIONAL ANALYSIS  (S1605 extension only; book period uses
    # Appendix 16.2 HHDebtIncRatio column directly so no conversion needed)
    #
    #   HCCSDODNS  units = millions USD          (FRED, Z.1 D.3 line 2)
    #   DPI        units = billions USD SAAR     (FRED, NIPA T2.1 line 27)
    #
    #   raw       ratio = HCCSDODNS / DPI
    #                   = millions / billions
    #                   = (10^6 USD) / (10^9 USD)
    #                   = 10^-3   (factor-1000 too SMALL)
    #
    #   corrected ratio = HCCSDODNS / (DPI * 1000)
    #                   = millions / (billions * 1000)
    #                   = millions / millions
    #                   = dimensionless ratio matching Fig 16.9 axis (0.6-1.4)
    #
    # The CD2 implementation used `CMDEBT / DPI` -> off by 1000x.  Phase 4
    # ratified the substitution to HCCSDODNS/DPI AND the explicit unit
    # conversion to prevent regression.
    # ------------------------------------------------------------------
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

INPUTS = {
    "S1605-A": DATA_RAW / "S1605_HHDebt.parquet",
    "S1605-B": DATA_RAW / "S1605_DPI.parquet",
    "S1605-C": DATA_RAW / "S1605_Ratio.parquet",
}
OUT = DATA_PROCESSED / "S1605.parquet"


def run() -> dict:
    missing = [str(p) for p in INPUTS.values() if not p.exists()]
    if missing:
        return {"status": "FAIL", "error": "raw parquet missing", "missing": missing}
    frames = [pd.read_parquet(p) for p in INPUTS.values()]
    df = pd.concat(frames, ignore_index=True).rename(columns={"subsource_id": "source_id"})
    df = df.sort_values(["subseries_id", "year"]).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "output": str(OUT),
        "unit_conversion_note": ("Book period: no conversion (HHDebt and "
                                  "HHDispPersInc both billions USD; HHDebtIncRatio "
                                  "is the ready-made decimal).  Extension Phase 6 "
                                  "applies HCCSDODNS_millions/(DPI_billions*1000) "
                                  "with dimensional-analysis comment in this "
                                  "module's docstring."),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
