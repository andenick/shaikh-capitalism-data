"""L01_S215_load - Incremental Rates of Profit in US Manufacturing, 1960-1989 (Fig 2.15).

Same data-status situation as S214: book period 1960-1989 source not in
SalvagedInputs. We emit the post-book Appendix7 industry-level IROP averages
labeled as S215-EXT only.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED = book_data_path("Appendix7_iropdataUSind.xlsx")
OUT = DATA_RAW / "S215_APP7_INDUSTRY_IROP_AVG.parquet"
MFG_INDUSTRIES = ["Chemicals", "Electr.Equ.", "Fab.Metal.", "Food", "Machinery",
                  "Mtr.Veh.", "Paper", "Petr.&Coal", "Plastic.", "Prim.Met.",
                  "Print.&Pub.", "Textile.", "Wood"]


def run() -> dict:
    if not CHOPPED.exists():
        return {"status": "FAIL", "error": f"chopped missing: {CHOPPED}"}
    df = pd.read_excel(CHOPPED, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    have = [c for c in MFG_INDUSTRIES if c in df.columns]
    if not have:
        return {"status": "FAIL", "error": "no mfg industry columns found"}
    df["mfg_avg"] = df[have].mean(axis=1)
    out = df[["Year", "mfg_avg"]].rename(columns={"Year": "year", "mfg_avg": "value"}).copy()
    out["units"] = "rate_decimal"
    out["subseries_id"] = "S215-EXT"
    out["subsource_id"] = "SHAIKH_APP7_IROP_USIND_1988_2005"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {
        "status": "PARTIAL",
        "rows_loaded": {"APP7_MFG_IROP_AVG": len(out)},
        "sources_fetched": ["SHAIKH_APP7_IROP_USIND_1988_2005"],
        "book_period_status": "data_unavailable",
        "book_period_reason": "1960-1989 source (anwarshaikhecon.org App 7.2) not in SalvagedInputs",
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
