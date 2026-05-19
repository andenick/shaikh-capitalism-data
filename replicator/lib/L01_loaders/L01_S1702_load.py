"""L01_S1702_load - load IRS SOI 2011 personal income distribution, bottom 97%.

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix17_USIRS2011.xlsx.
Per Phase 4 CH17 adequacy, the Fig 17.2 y-axis is the
'Cumulative Frequency from Above' column (FPR017_C5), NOT the 'Frequency'
column (FPR017_C3) as the CD2 markdown suggested. Filter to bins with
midpoint < $200,000 (bottom 97% of returns).

Top open-ended bin '$10M or more' has no midpoint in the spreadsheet and is
dropped (handled by S1703 logic; not relevant for S1702 bottom-97% set).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

SERIES_ID = "S1702"
CHOPPED_XLSX = book_data_path("Appendix17_USIRS2011.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_IRS_2011_BOTTOM97.parquet"
TAX_YEAR = 2011
THRESHOLD_USD = 200_000


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}

    df = pd.read_excel(CHOPPED_XLSX, header=1)
    # Column names per inspection:
    #   'Size of\nadjusted gross income', 'Number\nof\nreturns', 'Bin',
    #   'Frequency', 'Cumulative Frequency from Below',
    #   'Cumulative Frequency from Above'
    df = df.rename(columns={
        "Size of\nadjusted gross income": "agi_label",
        "Number\nof\nreturns": "n_returns",
        "Bin": "midpoint",
        "Frequency": "frequency",
        "Cumulative Frequency from Below": "cum_below",
        "Cumulative Frequency from Above": "cum_above",
    })
    # Drop the 'Total' summary row and the open-ended '$10,000,000 or more' bin
    # (no midpoint, no plotted point per Phase 4 instruction).
    df = df[df["agi_label"].astype(str).str.strip() != "Total"].copy()
    df = df.dropna(subset=["midpoint"]).copy()
    df["midpoint"] = pd.to_numeric(df["midpoint"], errors="coerce")
    df = df.dropna(subset=["midpoint"]).copy()

    # Filter to bottom 97% (midpoint < $200,000)
    sub = df[df["midpoint"] < THRESHOLD_USD].copy()

    rows = []
    for _, r in sub.iterrows():
        rows.append({
            "year": TAX_YEAR,
            "value": float(r["cum_above"]),
            "subseries_id": "S1702-A",
            "subsource_id": "IRS_SOI_2011_PUB1304_TABLE_1_4",
            "units": "cumulative_probability_from_above_dimensionless",
            "country": "United States",
            "country_key": f"USD_{int(r['midpoint'])}",
            "agi_midpoint_usd": float(r["midpoint"]),
            "agi_label": str(r["agi_label"]).strip(),
            "n_returns": float(r["n_returns"]) if not pd.isna(r["n_returns"]) else None,
        })

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"bottom_97pct_bins": len(out)},
        "midpoint_range_usd": [float(out["agi_midpoint_usd"].min()),
                               float(out["agi_midpoint_usd"].max())],
        "sources_fetched": ["IRS_SOI_2011_PUB1304_TABLE_1_4"],
        "outputs": [str(OUT)],
        "extension": "not_applicable_cross_sectional",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
