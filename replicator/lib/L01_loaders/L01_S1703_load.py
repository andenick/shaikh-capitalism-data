"""L01_S1703_load - load IRS SOI 2011 personal income distribution, top 3%.

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix17_USIRS2011.xlsx.
Per Phase 4 CH17 adequacy, the Fig 17.3 y-axis is 'Cumulative Frequency from
Above' (FPR017_C5). Filter to bins with midpoint >= $200,000 (top ~3%).

The top open-ended '$10,000,000 or more' bin has NO midpoint in the
spreadsheet (cum_above = 0.0 with NaN midpoint) and per Phase 4 is DROPPED
from the plot (anti-synthetic: no midpoint to impute).

Also computes the Pareto exponent alpha by OLS:
  ln(cum_above) = a - alpha * ln(midpoint)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

SERIES_ID = "S1703"
CHOPPED_XLSX = book_data_path("Appendix17_USIRS2011.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_IRS_2011_TOP3.parquet"
TAX_YEAR = 2011
THRESHOLD_USD = 200_000


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}

    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df = df.rename(columns={
        "Size of\nadjusted gross income": "agi_label",
        "Number\nof\nreturns": "n_returns",
        "Bin": "midpoint",
        "Frequency": "frequency",
        "Cumulative Frequency from Below": "cum_below",
        "Cumulative Frequency from Above": "cum_above",
    })
    df = df[df["agi_label"].astype(str).str.strip() != "Total"].copy()
    # Drop rows with NaN midpoint (i.e., the $10M+ open-ended bin) — anti-synthetic
    df = df.dropna(subset=["midpoint"]).copy()
    df["midpoint"] = pd.to_numeric(df["midpoint"], errors="coerce")
    df = df.dropna(subset=["midpoint"]).copy()

    sub = df[df["midpoint"] >= THRESHOLD_USD].copy()
    # Defensive: also drop cum_above==0 (would be -inf in log-space)
    sub = sub[sub["cum_above"] > 0].copy()

    rows = []
    for _, r in sub.iterrows():
        rows.append({
            "year": TAX_YEAR,
            "value": float(r["cum_above"]),
            "subseries_id": "S1703-A",
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

    # Pareto exponent recovery via OLS in log-log space
    ln_x = np.log(out["agi_midpoint_usd"].astype(float).values)
    ln_y = np.log(out["value"].astype(float).values)
    n = len(ln_x)
    pareto_alpha = None
    r_squared = None
    if n >= 2:
        slope, intercept = np.polyfit(ln_x, ln_y, 1)
        pareto_alpha = float(-slope)
        y_hat = intercept + slope * ln_x
        ss_res = float(((ln_y - y_hat) ** 2).sum())
        ss_tot = float(((ln_y - ln_y.mean()) ** 2).sum())
        r_squared = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else None

    return {
        "status": "OK",
        "rows_loaded": {"top_3pct_bins": len(out)},
        "midpoint_range_usd": [float(out["agi_midpoint_usd"].min()),
                               float(out["agi_midpoint_usd"].max())],
        "pareto_alpha_estimate": round(pareto_alpha, 4) if pareto_alpha else None,
        "r_squared": round(r_squared, 4) if r_squared else None,
        "sources_fetched": ["IRS_SOI_2011_PUB1304_TABLE_1_4"],
        "outputs": [str(OUT)],
        "extension": "not_applicable_cross_sectional",
        "dropped_bins": ["$10,000,000 or more (no midpoint, anti-synthetic)"],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
