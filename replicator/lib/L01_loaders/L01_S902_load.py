"""L01_S902_load - eigensystem standard prices + labor values + observed profit rates.

Per benchmark:
  - S902-P_{LABEL}: normalized standard price tp(r)_norm
  - S902-V_{LABEL}: normalized labor-time share tv_norm (labor value composition VR0)
Plus R_obs(year) scalars from Appendix9_ObservedProfitRates.xlsx (with parallel
sheet headers for 1998 circ vs fixed).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch9_helpers import (  # noqa: E402
    APPENDIX9_BENCHMARKS, read_benchmark, normalize_industry_frame,
)
from L01_loaders._ch2_helpers import book_path  # noqa: E402

SERIES_ID = "S902"
OUT_PRICES = DATA_RAW / f"{SERIES_ID}_STD_PRICES_AND_LABOR_VALUES.parquet"
OUT_ROBS = DATA_RAW / f"{SERIES_ID}_OBSERVED_PROFIT_RATES.parquet"


def _load_observed_profit_rates() -> pd.DataFrame:
    path = book_path("Appendix9_ObservedProfitRates.xlsx")
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    df = pd.read_excel(path, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    # First row is header text, second row first valid data:
    # cols: ['IO Table', 'robs']  — values are 1947, 1958, 1963, 1967, 1972, 1998
    df = df.rename(columns={"IO Table": "io_table", "robs": "r_obs"})
    df = df.dropna(subset=["io_table"])
    df["io_table"] = pd.to_numeric(df["io_table"], errors="coerce")
    df = df.dropna(subset=["io_table"])
    df["io_table"] = df["io_table"].astype(int)
    df["r_obs"] = pd.to_numeric(df["r_obs"], errors="coerce")
    return df[["io_table", "r_obs"]]


def run() -> dict:
    rows = []
    n_loaded = {}
    missing = []
    for (year, label, filename, exp_n, model) in APPENDIX9_BENCHMARKS:
        try:
            df = read_benchmark(filename)
        except (FileNotFoundError, RuntimeError) as exc:
            missing.append(f"{label}: {exc}")
            continue
        norm = normalize_industry_frame(df)
        subsource = f"SHAIKH_APPENDIX_9_{label}"
        for _, r in norm.iterrows():
            ind = int(r["Index"])
            rows.append({
                "year": int(year), "industry_index": ind,
                "x_tv_norm": float(r["tv_norm"]),
                "value": float(r["tpr_norm"]),
                "units": "normalized_share",
                "subseries_id": f"S902-P_{label}",
                "subsource_id": subsource,
                "model": model,
            })
            rows.append({
                "year": int(year), "industry_index": ind,
                "x_tv_norm": float(r["tv_norm"]),
                "value": float(r["tv_norm"]),
                "units": "normalized_share",
                "subseries_id": f"S902-V_{label}",
                "subsource_id": subsource,
                "model": model,
            })
        n_loaded[label] = int(len(df))

    if not rows:
        return {"status": "FAIL", "error": "no benchmark workbooks loaded", "missing": missing}

    out_prices = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out_prices.to_parquet(OUT_PRICES, index=False)

    # Observed profit rates
    robs_status = "ok"
    robs_rows = 0
    try:
        robs = _load_observed_profit_rates()
        # Reshape into long-form parquet:
        # year, industry_index=0 (sentinel), value=r_obs, subseries_id=S902-ROBS, subsource
        robs_out = pd.DataFrame({
            "year": robs["io_table"].astype(int),
            "industry_index": 0,
            "x_tv_norm": 0.0,
            "value": robs["r_obs"].astype(float),
            "units": "decimal_profit_rate",
            "subseries_id": "S902-ROBS",
            "subsource_id": "SHAIKH_APPENDIX_9_OBSERVED_PROFIT_RATES",
            "model": "observed",
        })
        robs_out.to_parquet(OUT_ROBS, index=False)
        robs_rows = int(len(robs_out))
    except FileNotFoundError as exc:
        robs_status = f"missing: {exc}"

    return {
        "status": "OK" if (not missing and robs_status == "ok") else "OK_WITH_WARNINGS",
        "rows_loaded": {"prices_total": len(out_prices),
                        "robs": robs_rows, **n_loaded},
        "robs_status": robs_status,
        "sources_fetched": sorted({r["subsource_id"] for r in rows} |
                                   {"SHAIKH_APPENDIX_9_OBSERVED_PROFIT_RATES"}),
        "missing": missing,
        "extension_status": "not_applicable_cross_sectional",
        "outputs": [str(OUT_PRICES), str(OUT_ROBS)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
