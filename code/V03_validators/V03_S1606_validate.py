"""V03_S1606_validate - compare S1606 (annual + quarterly) to Appendix 16."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402
from L01_loaders._ch16_helpers import read_appendix16_debt_service  # noqa: E402

PROCESSED_ANNUAL = DATA_PROCESSED / "S1606.parquet"
PROCESSED_QUARTERLY = DATA_PROCESSED / "_sidecars" / "S1606_quarterly.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1980, 2012)

SUBS = [
    ("S1606-A", "Financial obligations ratio, seasonally adjusted"),
    ("S1606-B", "Debt service ratio, seasonally adjusted"),
]


def _update_report(row: dict) -> None:
    rpt = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else \
        {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S1606"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED_QUARTERLY.exists():
        return {"status": "FAIL", "error": f"quarterly sidecar missing: {PROCESSED_QUARTERLY}"}
    actual_q = pd.read_parquet(PROCESSED_QUARTERLY)
    truth_q = read_appendix16_debt_service()
    truth_q = truth_q[(truth_q["year"] >= BOOK_OVERLAP[0]) & (truth_q["year"] <= BOOK_OVERLAP[1])]

    per_sub: dict[str, dict] = {}
    div_total: list[str] = []
    mae_list, max_pct_list = [], []
    n_total = 0
    for sub_id, col in SUBS:
        a = actual_q[actual_q["subseries_id"] == sub_id][["qdate", "value"]]
        t = truth_q[["qdate", col]].rename(columns={col: "expected"})
        m = a.merge(t, on="qdate", how="inner").dropna(subset=["expected", "value"])
        m["abs_err"] = (m["value"] - m["expected"]).abs()
        m["pct_err"] = (m["abs_err"] / m["expected"].abs().replace(0, float("nan"))) * 100.0
        mae = float(m["abs_err"].mean()) if len(m) else float("nan")
        max_pct = float(m["pct_err"].max()) if len(m) else float("nan")
        div = m[m["pct_err"] > VALIDATOR_TOL_PCT]["qdate"].dt.strftime("%Y-%m-%d").tolist()
        per_sub[sub_id] = {"n": int(len(m)), "mae": round(mae, 6),
                            "max_pct_err": round(max_pct, 6),
                            "div_quarters": div}
        div_total += div
        if len(m):
            mae_list.append(mae); max_pct_list.append(max_pct); n_total += len(m)

    # Annual validation: compare annual parquet to mean of truth quarters
    annual_status = "PASS"
    annual_per_sub: dict[str, dict] = {}
    if PROCESSED_ANNUAL.exists():
        actual_a = pd.read_parquet(PROCESSED_ANNUAL)
        for sub_id, col in SUBS:
            t_annual = (truth_q.groupby("year", as_index=False)[col]
                        .mean().rename(columns={col: "expected"}))
            a_annual = actual_a[actual_a["subseries_id"] == sub_id][["year", "value"]]
            m = a_annual.merge(t_annual, on="year", how="inner").dropna(
                subset=["expected", "value"])
            m["abs_err"] = (m["value"] - m["expected"]).abs()
            m["pct_err"] = (m["abs_err"] / m["expected"].abs().replace(0, float("nan"))) * 100.0
            mae_a = float(m["abs_err"].mean()) if len(m) else float("nan")
            max_pct_a = float(m["pct_err"].max()) if len(m) else float("nan")
            div_a = m[m["pct_err"] > VALIDATOR_TOL_PCT]["year"].astype(int).tolist()
            annual_per_sub[sub_id] = {"n": int(len(m)), "mae": round(mae_a, 6),
                                       "max_pct_err": round(max_pct_a, 6),
                                       "div_years": div_a}
            if div_a:
                annual_status = "FAIL"

    overall_mae = sum(mae_list)/len(mae_list) if mae_list else float("nan")
    overall_max = max(max_pct_list) if max_pct_list else float("nan")
    status = "PASS" if (not div_total and annual_status == "PASS") else "FAIL"
    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": list(BOOK_OVERLAP), "n_compared": n_total,
        "mae": round(overall_mae, 6), "max_pct_err": round(overall_max, 6),
        "max_abs_err": round(max((per_sub[k].get("mae") or 0) for k in per_sub), 6),
        "divergence_quarters": sorted(set(div_total)),
        "divergence_count": len(set(div_total)),
        "per_subseries_quarterly": per_sub,
        "per_subseries_annual": annual_per_sub,
        "annual_status": annual_status,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
