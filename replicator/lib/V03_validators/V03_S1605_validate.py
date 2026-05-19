"""V03_S1605_validate - compare S1605 to Appendix 16 DebtIncRatio."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402
from L01_loaders._ch16_helpers import read_appendix16_debt_inc_ratio  # noqa: E402

PROCESSED = DATA_PROCESSED / "S1605.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1975, 2012)

SUBS = [
    ("S1605-A", "HHDebt"),
    ("S1605-B", "HHDispPersInc"),
    ("S1605-C", "HHDebtIncRatio"),
]


def _update_report(row: dict) -> None:
    rpt = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else \
        {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S1605"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = read_appendix16_debt_inc_ratio()
    truth = truth[(truth["year"] >= BOOK_OVERLAP[0]) & (truth["year"] <= BOOK_OVERLAP[1])]
    per_sub: dict[str, dict] = {}
    div_total: list[int] = []
    mae_list, max_pct_list = [], []
    n_total = 0
    for sub_id, col in SUBS:
        a = actual[actual["subseries_id"] == sub_id][["year", "value"]]
        m = a.merge(truth[["year", col]].rename(columns={col: "expected"}),
                    on="year", how="inner").dropna(subset=["expected", "value"])
        m["abs_err"] = (m["value"] - m["expected"]).abs()
        m["pct_err"] = (m["abs_err"] / m["expected"].abs().replace(0, float("nan"))) * 100.0
        mae = float(m["abs_err"].mean()) if len(m) else float("nan")
        max_pct = float(m["pct_err"].max()) if len(m) else float("nan")
        div = m[m["pct_err"] > VALIDATOR_TOL_PCT]["year"].astype(int).tolist()
        per_sub[sub_id] = {"n": int(len(m)), "mae": round(mae, 6),
                            "max_pct_err": round(max_pct, 6), "div_years": div}
        div_total += div
        if len(m):
            mae_list.append(mae); max_pct_list.append(max_pct); n_total += len(m)
    overall_mae = sum(mae_list)/len(mae_list) if mae_list else float("nan")
    overall_max = max(max_pct_list) if max_pct_list else float("nan")
    status = "PASS" if not div_total else "FAIL"
    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": list(BOOK_OVERLAP), "n_compared": n_total,
        "mae": round(overall_mae, 6), "max_pct_err": round(overall_max, 6),
        "max_abs_err": round(max((per_sub[k].get("mae") or 0) for k in per_sub), 6),
        "divergence_years": sorted(set(div_total)),
        "divergence_count": len(set(div_total)),
        "per_subseries": per_sub,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
