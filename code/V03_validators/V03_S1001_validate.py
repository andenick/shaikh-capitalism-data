"""V03_S1001_validate — compare processed S1001 against App. 7.2 panel columns.

Compares S1001-A vs Appendix7_iropdataUSind 'Banks' column, and S1001-B vs
'All Private' column, on 1988-2005. Expected MAE ~ 0 (pass-through).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

PROCESSED = DATA_PROCESSED / "S1001.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix7_iropdataUSind.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1988, 2005)


def _load_truth() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df[["Year", "Banks", "All Private"]].rename(columns={"Year": "year"})


def _update_report(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S1001"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = _load_truth()
    truth = truth[(truth["year"] >= BOOK_OVERLAP[0]) & (truth["year"] <= BOOK_OVERLAP[1])]

    per_sub: dict[str, dict] = {}
    div_years_total: list[int] = []
    mae_total = []
    max_pct_total = []
    n_total = 0
    for sub_id, col in [("S1001-A", "Banks"), ("S1001-B", "All Private")]:
        a = actual[actual["subseries_id"] == sub_id][["year", "value"]]
        m = a.merge(truth[["year", col]].rename(columns={col: "expected"}), on="year", how="inner")
        m["abs_err"] = (m["value"] - m["expected"]).abs()
        m["pct_err"] = (m["abs_err"] / m["expected"].abs().replace(0, float("nan"))) * 100.0
        mae = float(m["abs_err"].mean()) if len(m) else float("nan")
        max_pct = float(m["pct_err"].max()) if len(m) else float("nan")
        div = m[m["pct_err"] > VALIDATOR_TOL_PCT]["year"].astype(int).tolist()
        per_sub[sub_id] = {"n": int(len(m)), "mae": round(mae, 6),
                           "max_pct_err": round(max_pct, 6), "div_years": div}
        div_years_total += div
        if len(m):
            mae_total.append(mae); max_pct_total.append(max_pct); n_total += len(m)

    overall_mae = float(sum(mae_total)/len(mae_total)) if mae_total else float("nan")
    overall_max = max(max_pct_total) if max_pct_total else float("nan")
    status = "PASS" if not div_years_total else "FAIL"
    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": list(BOOK_OVERLAP),
        "n_compared": n_total,
        "mae": round(overall_mae, 6),
        "max_pct_err": round(overall_max, 6),
        "max_abs_err": round(float(max((per_sub[k].get("mae") or 0) for k in per_sub)), 6),
        "divergence_years": sorted(set(div_years_total)),
        "divergence_count": len(set(div_years_total)),
        "per_subseries": per_sub,
        "cd2_comparison": {"note": "CD2 S050 spot values do not match Appendix 7.2; informational only."},
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
