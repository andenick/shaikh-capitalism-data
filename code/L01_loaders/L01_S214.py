"""L01_S214 - Average Rates of Profit in US Manufacturing, 1960-1989 (Fig 2.14).

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

# Explicit normalization: intended manufacturing industry -> actual Appendix-7 XLSX
# header. The prior hard-coded literal list silently matched only 6 of the intended
# industries because 6 real manufacturing columns are spelled differently in the
# workbook (e.g. "Machinery" vs "Mach.", "Petr.&Coal" vs "Petroleum"), shipping a
# 6-of-12 subset as the "manufacturing average" (F-4C-02 CRITICAL, fixed 2026-07-10).
# Motor Vehicles ("Mtr.Veh.") is GENUINELY ABSENT from this panel (VERIFY_4C), so the
# recoverable manufacturing set is 12, not the 13 the old list named.
MFG_INDUSTRY_MAP = {
    "Chemicals": "Chemicals",
    "Electrical Equipment": "Electr.Equ.",
    "Fabricated Metals": "Fab.Metal.",
    "Food": "Food",
    "Machinery": "Mach.",
    "Paper": "Paper",
    "Petroleum & Coal": "Petroleum",
    "Plastics": "Plastic",
    "Primary Metals": "Prim.Metal.",
    "Printing & Publishing": "Printing",
    "Textiles": "Text.Mills",
    "Wood": "Wood",
}
N_EXPECTED_MFG = 12


def run() -> dict:
    if not CHOPPED.exists():
        return {"status": "FAIL", "error": f"chopped missing: {CHOPPED}"}
    df = pd.read_excel(CHOPPED, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    # Resolve every intended industry to an actual header. ANY unmatched column is a
    # hard failure (header drift) — never silently drop it (invert of the old dead
    # `if not have:` guard, which fired only when ALL matched).
    matched = [hdr for hdr in MFG_INDUSTRY_MAP.values() if hdr in df.columns]
    missing = {name: hdr for name, hdr in MFG_INDUSTRY_MAP.items() if hdr not in df.columns}
    assert len(matched) == N_EXPECTED_MFG, (
        f"expected {N_EXPECTED_MFG} manufacturing industries, matched {len(matched)}: "
        f"{matched}; MISSING header(s) -> {missing} (column-name drift in "
        f"{CHOPPED.name}; refusing to ship a partial average)")
    df["mfg_avg"] = df[matched].mean(axis=1)
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
