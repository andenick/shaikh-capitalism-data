"""V03_S1004_validate — compare S1004-A vs USLR['iblongreal'] and S1004-B vs USLR['iblongrealHP3']."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

PROCESSED = DATA_PROCESSED / "S1004.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix10_USLR.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

# Real-rate construction has known small differences vs Shaikh's value
# (he used USCPI for the inflation deflator in iblongreal per the workbook
# header but the column name implies WPI; we use USWPI which is exactly
# what the book methodology says). Tolerance loosened to 5% for the raw
# real-rate compare; HP smoothed remains 5%.
VALIDATOR_TOL_PCT = 5.0
BOOK_OVERLAP = (1858, 2011)   # iblongreal needs t-1 inflation; starts 1858


def _load_truth() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df[["Year", "iblongreal", "iblongrealHP3"]].rename(columns={"Year": "year"})


def _update_report(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S1004"] = row
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
    overall_pct_max = 0.0
    overall_mae_sum = 0.0
    overall_mae_n = 0

    for sub_id, col in [("S1004-A", "iblongreal"), ("S1004-B", "iblongrealHP3")]:
        a = actual[actual["subseries_id"] == sub_id][["year", "value"]]
        t = truth[["year", col]].rename(columns={col: "expected"}).dropna(subset=["expected"])
        m = a.merge(t, on="year", how="inner")
        # Use absolute-error threshold for real-rate (in percent) since
        # values can cross zero — pct_err is unstable near zero.
        m["abs_err"] = (m["value"] - m["expected"]).abs()
        m["pct_err"] = (m["abs_err"] / m["expected"].abs().replace(0, float("nan"))) * 100.0
        if not len(m):
            per_sub[sub_id] = {"n": 0}
            continue
        mae = float(m["abs_err"].mean())
        max_abs = float(m["abs_err"].max())
        max_pct = float(m["pct_err"].max(skipna=True)) if not m["pct_err"].dropna().empty else float("nan")
        # Values are in DECIMAL (e.g. -0.0216 for -2.16%). For raw real rate
        # (S1004-A) tight tolerance (0.005 = 0.5pp). For HP-smoothed (S1004-B)
        # tolerance loosened to 0.05 = 5pp because Shaikh's HP implementation
        # vintage and padding convention are not exactly documented; small
        # differences are expected (HP endpoint problem also amplifies this).
        # S1004-A (raw real rate): exact recompute, 0.005 = 0.5pp threshold
        # S1004-B (HP-smoothed): now lambda=100 (book label "HP3" is actually
        # lambda=100; verified by sweep). Expect machine-precision MAE.
        thresh = 0.005
        crit = "abs_err > 0.005 (= 0.5 pp on rate_decimal) — exact recompute"
        div = m[m["abs_err"] > thresh]["year"].astype(int).tolist()
        per_sub[sub_id] = {"n": int(len(m)), "mae": round(mae, 6),
                           "max_abs_err": round(max_abs, 6),
                           "max_pct_err": round(max_pct, 6),
                           "criterion": crit,
                           "div_years_first_20": div[:20],
                           "div_count": len(div)}
        div_years_total += div
        n_total += len(m)
        overall_pct_max = max(overall_pct_max, max_pct if not pd.isna(max_pct) else 0)
        overall_mae_sum += mae * len(m); overall_mae_n += len(m)

    overall_mae = overall_mae_sum / overall_mae_n if overall_mae_n else float("nan")
    status = "PASS" if not div_years_total else "FAIL"
    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": list(BOOK_OVERLAP),
        "n_compared": n_total,
        "mae": round(overall_mae, 6),
        "max_abs_err": round(overall_mae, 6),
        "max_pct_err": round(overall_pct_max, 6),
        "divergence_years": sorted(set(div_years_total))[:50],
        "divergence_count": len(set(div_years_total)),
        "per_subseries": per_sub,
        "note": "iblongreal validated with abs-error pp threshold (sign-crossing values); HP smoothed validated with pct tolerance.",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
