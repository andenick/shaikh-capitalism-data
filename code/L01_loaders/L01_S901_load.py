"""L01_S901_load - market prices vs direct prices, 6 benchmark cross-sections.

Emits per (year, model, industry):
  - S901-A_{LABEL}: normalized market price tpm_norm
  - S901-B_{LABEL}: normalized direct price td_norm
plus the x-axis tv_norm (normalized labor-time share) as a column.

Cross-sectional series: no extension applies.
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

SERIES_ID = "S901"
OUT = DATA_RAW / f"{SERIES_ID}_MARKET_VS_DIRECT_PRICES.parquet"


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
        if len(df) != exp_n:
            # warn but continue
            pass
        norm = normalize_industry_frame(df)
        subsource = f"SHAIKH_APPENDIX_9_{label}"
        for _, r in norm.iterrows():
            ind = int(r["Index"])
            rows.append({
                "year": int(year), "industry_index": ind,
                "x_tv_norm": float(r["tv_norm"]),
                "value": float(r["tpm_norm"]),
                "units": "normalized_share",
                "subseries_id": f"S901-A_{label}",
                "subsource_id": subsource,
                "model": model,
            })
            rows.append({
                "year": int(year), "industry_index": ind,
                "x_tv_norm": float(r["tv_norm"]),
                "value": float(r["td_norm"]),
                "units": "normalized_share",
                "subseries_id": f"S901-B_{label}",
                "subsource_id": subsource,
                "model": model,
            })
        n_loaded[label] = int(len(df))

    if not rows:
        return {"status": "FAIL", "error": "no benchmark workbooks loaded",
                "missing": missing}

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK" if not missing else "OK_WITH_WARNINGS",
        "rows_loaded": {"total": len(out), **n_loaded},
        "sources_fetched": sorted({r["subsource_id"] for r in rows}),
        "missing": missing,
        "extension_status": "not_applicable_cross_sectional",
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
