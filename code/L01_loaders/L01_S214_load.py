"""L01_S214_load - Average Rates of Profit in US Manufacturing, 1960-1989 (Fig 2.14).

DATA STATUS: The 1960-1989 book period data was constructed by Shaikh from
OECD ISDB (1994 vintage) + anwarshaikhecon.org Appendix 7.2 (companion site).
Neither is hosted in SalvagedInputs at the time of Phase 5 ingestion. Per the
anu-framework no-fabrication rule, we DO NOT synthesize the book series. The
loader emits a STATUS marker indicating the gap and writes the 1987-2005
industry-level data from Appendix7_ropdataUSind.xlsx as a related extension
series (USMANAVG-style mean across manufacturing industries), explicitly
labeled as 'post-book period only' so no visualization splices it across the
book gap.

Remediation note: when anwarshaikhecon.org Appendix 7.2 or the original
OECD ISDB 1994 vintage is recovered to SalvagedInputs, regenerate this loader
to emit the 1960-1989 segment.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED = book_data_path("Appendix7_ropdataUSind.xlsx")
OUT = DATA_RAW / "S214_APP7_INDUSTRY_AVG.parquet"
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
    out["subseries_id"] = "S214-EXT"   # explicitly NOT S214-A (book period); marks post-book extension
    out["subsource_id"] = "SHAIKH_APP7_ROP_USIND_1987_2005"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {
        "status": "PARTIAL",
        "rows_loaded": {"APP7_MFG_AVG": len(out)},
        "sources_fetched": ["SHAIKH_APP7_ROP_USIND_1987_2005"],
        "book_period_status": "data_unavailable",
        "book_period_reason": "1960-1989 source (anwarshaikhecon.org App 7.2 / OECD ISDB 1994) not in SalvagedInputs",
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
