"""P02_S1703_construct - pass-through processor for Fig 17.3 top-3% income.

Also recomputes the Pareto exponent (OLS) and records it in the run summary
for downstream consumption.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1703"
IN = DATA_RAW / f"{SERIES_ID}_IRS_2011_TOP3.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN)
    df = df.rename(columns={"subsource_id": "source_id"})
    out = df[["year", "value", "subseries_id", "source_id", "units",
              "country", "country_key", "agi_midpoint_usd", "agi_label"]].copy()
    out = out.sort_values(["year", "subseries_id", "agi_midpoint_usd"]).reset_index(drop=True)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    # Pareto fit
    ln_x = np.log(out["agi_midpoint_usd"].astype(float).values)
    ln_y = np.log(out["value"].astype(float).values)
    slope, intercept = np.polyfit(ln_x, ln_y, 1)
    alpha = float(-slope)
    y_hat = intercept + slope * ln_x
    ss_res = float(((ln_y - y_hat) ** 2).sum())
    ss_tot = float(((ln_y - ln_y.mean()) ** 2).sum())
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else None

    return {
        "status": "OK",
        "rows_processed": int(len(out)),
        "subseries_present": sorted(out["subseries_id"].unique().tolist()),
        "pareto_alpha": round(alpha, 4),
        "pareto_r_squared": round(r2, 4) if r2 else None,
        "n_top_tail_bins": int(len(out)),
        "extension": {"extension_status": "not_applicable_cross_sectional"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
