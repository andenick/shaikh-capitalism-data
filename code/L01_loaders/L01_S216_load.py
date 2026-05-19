"""L01_S216_load - Normalized Total Prices of Production Profit vs Total Unit Labor
Costs, US 1972 (71 industries) -- Fig 2.16, CROSS-SECTIONAL scatter (single year).

Source: Appendix9_1972fixed.xlsx columns:
  - 'tpm'  = total market prices per industry (Y axis: market prices)
  - 'tp(r)' = total prices of production per industry (computed at observed r)
  - 'tv'  = total vertically-integrated unit labor cost (X axis: integrated ULC)

Fig 2.16 plots (tv, tp(r)) and (tv, tpm), 71 industries, both axes normalized so
sums match. Per content_type='cross_sectional' (Phase 4 reclassification ratified),
no temporal extension applies.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

XLSX = book_data_path("Appendix9_1972fixed.xlsx")
OUT = DATA_RAW / "S216_IO_1972_71_INDUSTRIES.parquet"
YEAR = 1972


def run() -> dict:
    if not XLSX.exists():
        return {"status": "FAIL", "error": f"missing {XLSX}"}
    df = pd.read_excel(XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    # Need 'Index', 'tpm', 'tp(r)', 'tv'
    needed = ["Index", "tpm", "tp(r)", "tv"]
    for c in needed:
        if c not in df.columns:
            return {"status": "FAIL", "error": f"missing column {c}; have {list(df.columns)[:10]}"}
    df = df.dropna(subset=["Index"]).copy()
    df["Index"] = pd.to_numeric(df["Index"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["Index"])
    # Filter to industries 1..71
    df = df[(df["Index"] >= 1) & (df["Index"] <= 71)].copy()
    # Normalize axes so sums match (per fig description)
    tv_sum = df["tv"].sum()
    tpm_sum = df["tpm"].sum()
    tpr_sum = df["tp(r)"].sum()
    df["tv_norm"] = df["tv"] / tv_sum
    df["tpm_norm"] = df["tpm"] / tpm_sum
    df["tpr_norm"] = df["tp(r)"] / tpr_sum
    # Output long-form: one row per (industry, axis)
    rows = []
    for _, r in df.iterrows():
        ind = int(r["Index"])
        # X axis (vertically-integrated unit labor cost) -- always tv_norm
        # Two scatter series: one with y=tpm, one with y=tp(r)
        rows.append({"year": YEAR, "industry_index": ind, "x_tv_norm": r["tv_norm"],
                     "value": r["tpr_norm"], "units": "normalized_dollars",
                     "subseries_id": "S216-A", "subsource_id": "BEA_IO_1972_71IND_SHAIKH_APP9"})
        rows.append({"year": YEAR, "industry_index": ind, "x_tv_norm": r["tv_norm"],
                     "value": r["tpm_norm"], "units": "normalized_dollars",
                     "subseries_id": "S216-B", "subsource_id": "BEA_IO_1972_71IND_SHAIKH_APP9"})
    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": {"S216_1972": len(out)},
        "sources_fetched": ["BEA_IO_1972_71IND_SHAIKH_APP9"],
        "extension_status": "not_applicable_cross_sectional",
        "year": YEAR, "industries": int(df.shape[0]),
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
