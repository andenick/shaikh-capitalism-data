"""L01_S903_load - actual wage-profit curves per benchmark year (Fig 9.19).

Reads pre-computed columns from Appendix9_PennWorldTables2.xlsx:
  r{YR}        — profit-rate grid for year YR
  wshr{YR}     — wage share at that r
  wr{YR}       — real-wage curve (= wage share * productivity index ratio)
  R_fixed      — Table 9.18 maximum profit rates per year
  RealGDPperworkerindex — PWT 7.1 productivity index (with 1947 anchor)

YEARS used: 47, 58, 63, 67, 72, 98fix, 98circ.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch2_helpers import book_path  # noqa: E402

SERIES_ID = "S903"
PWT2_XLSX = book_path("Appendix9_PennWorldTables2.xlsx")
OUT_CURVES = DATA_RAW / f"{SERIES_ID}_WAGE_PROFIT_CURVES.parquet"
OUT_SCALARS = DATA_RAW / f"{SERIES_ID}_SCALARS_R_AND_PWT.parquet"

# short label, year, r column, wshr column, wr column
# Note: 1998 fixed uses r98/wshr98/wr98fix (no 'fix' suffix on r/wsh); 1998 circ
# uses r98circ/wshrCirc/wr98circ.
YEAR_LABELS = [
    ("47", 1947, "r47", "wshr47", "wr47"),
    ("58", 1958, "r58", "wshr58", "wr58"),
    ("63", 1963, "r63", "wshr63", "wr63"),
    ("67", 1967, "r67", "wshr67", "wr67"),
    ("72", 1972, "r72", "wshr72", "wr72"),
    ("98fix", 1998, "r98", "wshr98", "wr98fix"),
    ("98circ", 1998, "r98circ", "wshrCirc", "wr98circ"),
]


def run() -> dict:
    if not PWT2_XLSX.exists():
        return {"status": "FAIL", "error": f"missing {PWT2_XLSX}"}
    df = pd.read_excel(PWT2_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]

    rows = []
    for short, year, rcol, wshcol, wrcol in YEAR_LABELS:
        for col in [rcol, wshcol, wrcol]:
            if col not in df.columns:
                return {"status": "FAIL", "error": f"missing column {col}"}
        sub = df[[rcol, wshcol, wrcol]].dropna(how="all").copy()
        sub = sub.dropna(subset=[rcol])
        # Each row is one r-grid point
        for i, r in sub.iterrows():
            rval = r[rcol]
            wshval = r[wshcol]
            wrval = r[wrcol]
            # Emit two subseries: wage share and real-wage curve
            if pd.notna(wshval):
                rows.append({
                    "year": int(year), "r_value": float(rval),
                    "industry_index": int(i),  # use row index as pointer
                    "x_tv_norm": float(rval),  # x-axis is r (or r/R)
                    "value": float(wshval),
                    "units": "wage_share_dimensionless",
                    "subseries_id": f"S903-WSHARE-{short.upper()}",
                    "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2",
                    "model": "circulating" if short == "98circ" else "fixed",
                })
            if pd.notna(wrval):
                rows.append({
                    "year": int(year), "r_value": float(rval),
                    "industry_index": int(i),
                    "x_tv_norm": float(rval),
                    "value": float(wrval),
                    "units": "real_wage_productivity_index_dimensionless",
                    "subseries_id": f"S903-WRCURVE-{short.upper()}",
                    "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2",
                    "model": "circulating" if short == "98circ" else "fixed",
                })

    curves = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    curves.to_parquet(OUT_CURVES, index=False)

    # Scalars: R_fixed per year + RealGDPperworkerindex anchors
    scalars = []
    r_fixed = df["R_fixed"].dropna()
    # R_fixed is given on the first six valid rows corresponding to the six benchmark years
    # We map them positionally: 1947, 1958, 1963, 1967, 1972, 1998
    benchmark_years = [1947, 1958, 1963, 1967, 1972, 1998]
    for y, rv in zip(benchmark_years, r_fixed.tolist()):
        scalars.append({"year": int(y), "industry_index": 0, "x_tv_norm": 0.0,
                         "value": float(rv), "units": "decimal_max_profit_rate",
                         "subseries_id": "S903-R-FIXED",
                         "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2_TABLE_9_18",
                         "model": "fixed"})
    r_circ = df["R_circ"].dropna()
    if len(r_circ):
        scalars.append({"year": 1998, "industry_index": 0, "x_tv_norm": 0.0,
                         "value": float(r_circ.iloc[0]),
                         "units": "decimal_max_profit_rate",
                         "subseries_id": "S903-R-CIRC",
                         "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2_TABLE_9_18",
                         "model": "circulating"})
    pwt = df[["Year", "RealGDPperworkerindex"]].dropna(subset=["RealGDPperworkerindex"])
    for _, r in pwt.iterrows():
        y = r["Year"]
        if pd.isna(y):
            continue
        scalars.append({"year": int(y), "industry_index": 0, "x_tv_norm": 0.0,
                         "value": float(r["RealGDPperworkerindex"]),
                         "units": "PWT71_RGDPperworker_index_1947base",
                         "subseries_id": "S903-PWT-RGDPPERWORKER",
                         "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2",
                         "model": "anchor"})
    scalar_df = pd.DataFrame(scalars)
    scalar_df.to_parquet(OUT_SCALARS, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"curves": int(len(curves)), "scalars": int(len(scalar_df))},
        "sources_fetched": ["SHAIKH_APPENDIX_9_PWT_BOOK2",
                             "SHAIKH_APPENDIX_9_PWT_BOOK2_TABLE_9_18"],
        "year_labels": [yl[0] for yl in YEAR_LABELS],
        "extension_status": "not_applicable_cross_sectional",
        "outputs": [str(OUT_CURVES), str(OUT_SCALARS)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
