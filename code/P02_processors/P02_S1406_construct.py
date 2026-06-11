"""P02_S1406_construct - Inflation and Productivity Growth (Ch14 Fig 14.15).

Book period: pass-through of Appendix 14.3 inflrate and GPRODVTY.

Extension (2012+): re-derive
  - inflation = GDPDEF.pct_change() (annual)
  - productivity yr = (GDP*100/GDPDEF) / (FEE/1000)
  - productivity growth = yr.pct_change()

PRODUCTIVITY CONCEPT-POLICING: formula implemented LITERALLY per Appendix 14.2
p. 892 -- no algebraic simplification. The *100 (deflator scale) and /1000 (FEE
unit conversion) multipliers are unit-correcting; removing them silently scales
productivity by 100,000x.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1406"
IN_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
IN_GDP  = DATA_RAW / f"{SERIES_ID}_FRED_GDP.parquet"
IN_DEF  = DATA_RAW / f"{SERIES_ID}_FRED_GDPDEF.parquet"
IN_FEE  = DATA_RAW / f"{SERIES_ID}_FRED_B4701C0A222NBEA.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"
BOOK_END = 2011


def _book_long(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={"subsource_id": "source_id"})[
        ["year", "value", "subseries_id", "source_id", "units"]
    ]


def _derive_extension(gdp: pd.DataFrame, defl: pd.DataFrame, fee: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    m = gdp[["year", "value"]].rename(columns={"value": "GDP"}).merge(
        defl[["year", "value"]].rename(columns={"value": "p"}), on="year", how="inner"
    ).merge(fee[["year", "value"]].rename(columns={"value": "FEE"}), on="year", how="inner")
    m = m.sort_values("year").reset_index(drop=True)
    # LITERAL Shaikh formula. DO NOT simplify.
    m["yr"] = (m["GDP"] * 100.0 / m["p"]) / (m["FEE"] / 1000.0)
    m["inflrate"] = m["p"].pct_change()
    m["GPRODVTY"] = m["yr"].pct_change()

    ext = m[m["year"] > BOOK_END].copy()
    rows = []
    for _, r in ext.iterrows():
        y = int(r["year"])
        if pd.notna(r["inflrate"]):
            rows.append({"year": y, "value": float(r["inflrate"]),
                         "subseries_id": f"{SERIES_ID}-A",
                         "source_id": "FRED_DERIVED_INFLRATE",
                         "units": "decimal_annual_inflation_rate"})
        if pd.notna(r["GPRODVTY"]):
            rows.append({"year": y, "value": float(r["GPRODVTY"]),
                         "subseries_id": f"{SERIES_ID}-B",
                         "source_id": "FRED_DERIVED_GPRODVTY",
                         "units": "decimal_annual_productivity_growth_per_FTE"})
    diag = {
        "extension_status": "ok",
        "productivity_formula_applied": "(GDP*100/p)/(FEE/1000)",
        "years_appended": int(ext["year"].nunique()) if not ext.empty else 0,
        "concept_policing_assertion": "productivity_per_FTE_not_per_hour",
    }
    return pd.DataFrame(rows), diag


def run() -> dict:
    if not IN_BOOK.exists():
        return {"status": "FAIL", "error": f"missing book parquet {IN_BOOK}"}
    book = _book_long(pd.read_parquet(IN_BOOK))
    ext_rows = pd.DataFrame()
    ext_diag = {"extension_status": "data_unavailable", "reason": "one or more FRED inputs missing"}
    if IN_GDP.exists() and IN_DEF.exists() and IN_FEE.exists():
        ext_rows, ext_diag = _derive_extension(
            pd.read_parquet(IN_GDP), pd.read_parquet(IN_DEF), pd.read_parquet(IN_FEE)
        )
    final = pd.concat([book, ext_rows], ignore_index=True).sort_values(
        ["subseries_id", "year"]).reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": ext_diag,
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
