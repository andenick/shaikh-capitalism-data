"""V03_S1006_validate — compare S1006 book subseries vs Appendix10_Ibbotson.xlsx."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

PROCESSED = DATA_PROCESSED / "S1006.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix10_Ibbotson.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

# Total-return percent values cross zero and span wide ranges; use abs-pp
# tolerance for the validation criterion.
VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1926, 2010)


def _load_truth() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    cols = ["Large Company Stocks", "Long-Term Corporate Bonds", "Long-Term Government Bonds"]
    return df[["Year"] + cols].rename(columns={"Year": "year"})


def _update_report(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S1006"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = _load_truth()
    truth = truth[(truth["year"] >= BOOK_OVERLAP[0]) & (truth["year"] <= BOOK_OVERLAP[1])]

    per_sub: dict[str, dict] = {}
    div_years_total: list[int] = []
    n_total = 0
    overall_mae_sum = 0.0
    overall_mae_n = 0
    overall_pct_max = 0.0
    for sub_id, col in [("S1006-A", "Large Company Stocks"),
                        ("S1006-B", "Long-Term Corporate Bonds"),
                        ("S1006-C", "Long-Term Government Bonds")]:
        a = actual[actual["subseries_id"] == sub_id][["year", "value"]]
        t = truth[["year", col]].rename(columns={col: "expected"}).dropna(subset=["expected"])
        m = a.merge(t, on="year", how="inner")
        if not len(m):
            per_sub[sub_id] = {"n": 0}
            continue
        m["abs_err"] = (m["value"] - m["expected"]).abs()
        mae = float(m["abs_err"].mean())
        max_abs = float(m["abs_err"].max())
        # Use abs-pp tolerance: 1.0 percentage-point for return series
        div = m[m["abs_err"] > 1.0]["year"].astype(int).tolist()
        per_sub[sub_id] = {"n": int(len(m)), "mae": round(mae, 6),
                           "max_abs_err": round(max_abs, 6),
                           "div_years_first_20": div[:20],
                           "div_count": len(div)}
        div_years_total += div
        n_total += len(m)
        overall_pct_max = max(overall_pct_max, max_abs)
        overall_mae_sum += mae * len(m); overall_mae_n += len(m)

    overall_mae = overall_mae_sum / overall_mae_n if overall_mae_n else float("nan")
    status = "PASS" if not div_years_total else "FAIL"
    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "criterion": "abs_err > 1.0 percentage point (return series)",
        "compare_range": list(BOOK_OVERLAP),
        "n_compared": n_total,
        "mae": round(overall_mae, 6),
        "max_abs_err": round(overall_pct_max, 6),
        "max_pct_err": round(overall_pct_max, 6),
        "divergence_years": sorted(set(div_years_total))[:50],
        "divergence_count": len(set(div_years_total)),
        "per_subseries": per_sub,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
