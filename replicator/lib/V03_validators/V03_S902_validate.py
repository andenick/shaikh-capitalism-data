"""V03_S902_validate - validate tp(r)_norm against workbook recomputation per benchmark."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402
from L01_loaders._ch9_helpers import (  # noqa: E402
    APPENDIX9_BENCHMARKS, read_benchmark, normalize_industry_frame,
)

PROCESSED = DATA_PROCESSED / "S902.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = 0.5

# Phase 4 + DPR sanity gate: observed profit rates must match Appendix9 (within 0.1%)
EXPECTED_ROBS = {1947: 0.236, 1958: 0.176, 1963: 0.21, 1967: 0.229, 1972: 0.188, 1998: 0.1258}


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S902"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": "processed missing"}
    actual = pd.read_parquet(PROCESSED)

    per_benchmark = []
    total_div = 0
    overall_mae = []
    for (year, label, filename, _, _) in APPENDIX9_BENCHMARKS:
        try:
            df = read_benchmark(filename)
        except Exception as exc:
            per_benchmark.append({"label": label, "error": str(exc)})
            continue
        norm = normalize_industry_frame(df)
        a = actual[actual["subseries_id"] == f"S902-P_{label}"]
        merged = a.merge(norm[["Index", "tpr_norm"]].rename(
            columns={"Index": "industry_index"}), on="industry_index", how="inner")
        merged["abs_err"] = (merged["value"] - merged["tpr_norm"]).abs()
        merged["pct_err"] = merged["abs_err"] / merged["tpr_norm"].abs() * 100.0
        div = merged[merged["pct_err"] > VALIDATOR_TOL_PCT]["industry_index"].astype(int).tolist()
        total_div += len(div)
        if len(merged):
            overall_mae.append(float(merged["abs_err"].mean()))

        # Distance measure delta_c = Σ|tp(r)_norm/tv_norm - 1|·tv_norm
        delta_c = float(((norm["tpr_norm"] / norm["tv_norm"] - 1.0).abs() *
                          norm["tv_norm"]).sum())

        per_benchmark.append({
            "label": label, "n_industries": int(merged["industry_index"].nunique()),
            "tpr_mae": round(float(merged["abs_err"].mean()) if len(merged) else 0.0, 10),
            "tpr_max_pct_err": round(float(merged["pct_err"].max()) if len(merged) else 0.0, 10),
            "divergences": div,
            "delta_c_standard_vs_labor": round(delta_c, 6),
        })

    # R_obs sanity check: actual S902-ROBS rows should match EXPECTED_ROBS
    robs_check = []
    robs_actual = actual[actual["subseries_id"] == "S902-ROBS"]
    for y, expected in EXPECTED_ROBS.items():
        match = robs_actual[robs_actual["year"] == y]
        if not match.empty:
            got = float(match["value"].iloc[0])
            diff_pct = abs(got - expected) / expected * 100.0
            robs_check.append({"year": y, "expected": expected, "got": round(got, 6),
                                "diff_pct": round(diff_pct, 4),
                                "ok": diff_pct < 0.5})

    status = "PASS" if (total_div == 0 and all(c["ok"] for c in robs_check)) else "FAIL"
    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT,
        "per_benchmark": per_benchmark,
        "mae": round(sum(overall_mae) / max(1, len(overall_mae)), 10),
        "observed_profit_rate_check": robs_check,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
