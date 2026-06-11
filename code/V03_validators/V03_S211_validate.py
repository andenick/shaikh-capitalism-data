"""V03_S211_validate - compare S211 to CD2 S022 (the 1790-1940 window)."""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_EXT_BENCH  # noqa: E402

PROCESSED = DATA_PROCESSED / "S211.parquet"
S022_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S022_us_and_uk_wholesale_price_indexes_1790_1940.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
TOL_PCT = 1.0
BOOK_OVERLAP = (1790, 1940)


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S211"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = pd.read_excel(S022_XLSX, sheet_name="Data").rename(columns={"Year": "year"})
    truth = truth.dropna(subset=["year"]).astype({"year": int})
    div_per = {}
    total_n = 0; total_div = 0; mae_sum = 0.0; max_pct = 0.0
    for sid, col, label in [("S211-A", "S022-A", "US WPI"), ("S211-B", "S022-B", "UK WPI")]:
        a = actual[actual["subseries_id"] == sid][["year", "value"]]
        t = truth[["year", col]].rename(columns={col: "expected"}).dropna(subset=["expected"])
        m = a.merge(t, on="year", how="inner")
        m = m[(m["year"] >= BOOK_OVERLAP[0]) & (m["year"] <= BOOK_OVERLAP[1])]
        m["abs_err"] = (m["value"] - m["expected"]).abs()
        m["pct_err"] = m["abs_err"] / m["expected"].abs() * 100.0
        div = m[m["pct_err"] > TOL_PCT]["year"].astype(int).tolist()
        n = int(len(m))
        div_per[sid] = {"label": label, "n": n, "divergence_years": div,
                        "mae": round(float(m["abs_err"].mean()) if n else float("nan"), 6),
                        "max_pct_err": round(float(m["pct_err"].max()) if n else float("nan"), 6)}
        total_n += n; total_div += len(div); mae_sum += div_per[sid]["mae"] or 0
        max_pct = max(max_pct, div_per[sid]["max_pct_err"] or 0)
    status = "PASS" if total_div == 0 else "FAIL"
    row = {
        "status": status, "tolerance_pct": TOL_PCT, "compare_range": list(BOOK_OVERLAP),
        "n_compared": total_n, "mae": round(mae_sum / 2.0, 6), "max_pct_err": max_pct,
        "divergence_count": total_div, "per_subseries": list(div_per.values()),
        "note": "Book truth = CD2 S022 (Jastram 1977 + NBER). No extension by design.",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
