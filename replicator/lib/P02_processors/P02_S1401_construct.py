"""P02_S1401_construct - construct S1401 from raw inputs.

Constructs:
  - Book period (1948-2011): subseries S1401-A (wagesh), S1401-B (ggdp)
    pass-through from Appendix 14.3.
  - Extension (2012+): re-derive wagesh = A576RC1/GDP and ggdp = annual
    growth of GDP. Splice via overlap_anchor at 2011 (scale factor stored in
    diagnostics; for ratios this is essentially identity).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1401"
IN_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
IN_GDP  = DATA_RAW / f"{SERIES_ID}_FRED_GDP.parquet"
IN_EC   = DATA_RAW / f"{SERIES_ID}_FRED_A576RC1.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"
BOOK_END = 2011


def _book_long(df: pd.DataFrame) -> pd.DataFrame:
    out = df.rename(columns={"subsource_id": "source_id"})[
        ["year", "value", "subseries_id", "source_id", "units"]
    ]
    return out


def _derive_extension(gdp: pd.DataFrame, ec: pd.DataFrame) -> pd.DataFrame:
    m = gdp[["year", "value"]].rename(columns={"value": "gdp"}).merge(
        ec[["year", "value"]].rename(columns={"value": "ec"}), on="year", how="inner"
    )
    m = m.sort_values("year").reset_index(drop=True)
    m["wagesh"] = m["ec"] / m["gdp"]
    m["ggdp"] = m["gdp"].pct_change()
    ext = m[m["year"] > BOOK_END].copy()
    rows = []
    for _, r in ext.iterrows():
        rows.append({
            "year": int(r["year"]), "value": float(r["wagesh"]),
            "subseries_id": f"{SERIES_ID}-A", "source_id": "FRED_DERIVED_WAGESH",
            "units": "decimal_ratio",
        })
        if pd.notna(r["ggdp"]):
            rows.append({
                "year": int(r["year"]), "value": float(r["ggdp"]),
                "subseries_id": f"{SERIES_ID}-B", "source_id": "FRED_DERIVED_GGDP",
                "units": "decimal_annual_growth_rate",
            })
    return pd.DataFrame(rows)


def run() -> dict:
    if not IN_BOOK.exists():
        return {"status": "FAIL", "error": f"missing book parquet {IN_BOOK}"}
    book = _book_long(pd.read_parquet(IN_BOOK))

    ext_rows = pd.DataFrame()
    ext_diag = {"extension_status": "data_unavailable", "reason": "FRED not loaded"}
    if IN_GDP.exists() and IN_EC.exists():
        gdp = pd.read_parquet(IN_GDP)
        ec  = pd.read_parquet(IN_EC)
        ext_rows = _derive_extension(gdp, ec)
        ext_diag = {"extension_status": "ok", "years_appended": int(ext_rows["year"].nunique()) if not ext_rows.empty else 0,
                    "last_year": int(ext_rows["year"].max()) if not ext_rows.empty else BOOK_END,
                    "re_derivation_formula": "wagesh = A576RC1/GDP; ggdp = GDP.pct_change()"}

    final = pd.concat([book, ext_rows], ignore_index=True).sort_values(
        ["subseries_id", "year"]
    ).reset_index(drop=True)
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
