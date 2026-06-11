"""L01_S1104_load - US trade balance, REER and relative GDP for Fig 11.7.

Three-line overlay for the United States, 1960-2009:
  S1104-A US trade balance = (X-M)/(X+M) net-trade ratio (per Phase 4 unit
          correction); inputs from Appendix11_XMData.xlsx US block.
  S1104-B US REER PPI = rxr1 column for the US row of Appendix11_USJPNdata.xlsx
          (same data as S1102-B; emitted here for self-contained chopped CSV).
  S1104-C US/EU12 relative real GDP = constructed from World Bank WDI
          NY.GDP.MKTP.KD (constant 2015 USD) for the 12 pre-1995 EU members
          plus the US. NOTE: this requires a per-country API/file fetch that
          is not present in the salvaged workbook. The loader emits S1104-C
          rows only if a salvaged relative_gdp_us_eu12.csv is found; otherwise
          marks the subseries `data_unavailable_eu12_relgdp_not_in_salvage`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

SERIES_ID = "S1104"
CHOPPED_XM = book_data_path("Appendix11_XMData.xlsx")
CHOPPED_USJPN = book_data_path("Appendix11_USJPNdata.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_US_BOP_REER_RELGDP.parquet"


def run() -> dict:
    for fp in (CHOPPED_XM, CHOPPED_USJPN):
        if not fp.exists():
            return {"status": "FAIL", "error": f"chopped table missing: {fp}"}

    # Load trade data
    xm = pd.read_excel(CHOPPED_XM, header=1)
    xm = xm.dropna(subset=["Year"])
    xm["Year"] = pd.to_numeric(xm["Year"], errors="coerce").astype("Int64")
    xm = xm.dropna(subset=["Year"])
    us_xm = xm[xm["Country"] == "United States"].copy()

    # Load REER data
    rr = pd.read_excel(CHOPPED_USJPN, header=1)
    rr = rr.dropna(subset=["Year"])
    rr["Year"] = pd.to_numeric(rr["Year"], errors="coerce").astype("Int64")
    rr = rr.dropna(subset=["Year"])
    us_rr = rr[rr["Country"] == "United States"].copy()

    rows = []
    # S1104-A: (X-M)/(X+M) net-trade ratio (Phase 4 unit correction)
    for _, r in us_xm.iterrows():
        x = pd.to_numeric(r["X (in $M)"], errors="coerce")
        m = pd.to_numeric(r["M (in $M)"], errors="coerce")
        if pd.isna(x) or pd.isna(m) or (x + m) == 0:
            continue
        nt = float((x - m) / (x + m))
        rows.append({
            "year": int(r["Year"]),
            "value": nt,
            "subseries_id": "S1104-A",
            "subsource_id": "IMF_IFS_XM_APPENDIX_11_1",
            "units": "net_trade_ratio_dimensionless",
            "country": "United States",
        })

    # S1104-B: US REER PPI (rxr1)
    for _, r in us_rr.iterrows():
        v = r["rxr1"]
        if pd.isna(v):
            continue
        rows.append({
            "year": int(r["Year"]),
            "value": float(v),
            "subseries_id": "S1104-B",
            "subsource_id": "BLS_ILC_REER_PPI_APPENDIX_11_1",
            "units": "index_2002=100",
            "country": "United States",
        })

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"S1104-A": int((out["subseries_id"] == "S1104-A").sum()),
                         "S1104-B": int((out["subseries_id"] == "S1104-B").sum()),
                         "S1104-C": 0},
        "sources_fetched": ["IMF_IFS_XM_APPENDIX_11_1",
                            "BLS_ILC_REER_PPI_APPENDIX_11_1"],
        "outputs": [str(OUT)],
        "s1104c_status": "data_unavailable_eu12_relgdp_not_in_salvage",
        "notes": ("S1104-C US/EU12 relative real GDP requires a 12-country WDI "
                  "NY.GDP.MKTP.KD fetch + per-country sum; not in salvage. "
                  "Per Phase 4 Adequacy Q5, the canonical recipe holds Shaikh's "
                  "pre-1995 EU12 basket fixed via per-country backfill. "
                  "Deferred to Phase 9 enrichment."),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
