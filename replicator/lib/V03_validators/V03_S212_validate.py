"""V03_S212_validate - compare S212 to CD2 S024/S025 WPI-in-gold columns."""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_EXT_BENCH  # noqa: E402

PROCESSED = DATA_PROCESSED / "S212.parquet"
S024_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S024_uk_wpi_in_gold_and_uk_gold_price.xlsx"
S025_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S025_us_wpi_in_gold_and_us_gold_price.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
TOL_PCT = 1.0
BOOK_OVERLAP = (1790, 2010)


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S212"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    us_truth = pd.read_excel(S025_XLSX, sheet_name="Data").rename(columns={"Year": "year"})
    uk_truth = pd.read_excel(S024_XLSX, sheet_name="Data").rename(columns={"Year": "year"})
    us_truth = us_truth.dropna(subset=["year"]).astype({"year": int})[["year", "S025-A"]].rename(columns={"S025-A": "expected"}).dropna(subset=["expected"])
    uk_truth = uk_truth.dropna(subset=["year"]).astype({"year": int})[["year", "S024-A"]].rename(columns={"S024-A": "expected"}).dropna(subset=["expected"])
    per = []
    total_n = 0; total_div = 0; mae_sum = 0.0; max_pct = 0.0
    for sid, truth, label in [("S212-A", us_truth, "US WPI in gold"), ("S212-B", uk_truth, "UK WPI in gold")]:
        a = actual[actual["subseries_id"] == sid][["year", "value"]]
        m = a.merge(truth, on="year", how="inner")
        m = m[(m["year"] >= BOOK_OVERLAP[0]) & (m["year"] <= BOOK_OVERLAP[1])]
        m["abs_err"] = (m["value"] - m["expected"]).abs()
        m["pct_err"] = m["abs_err"] / m["expected"].abs() * 100.0
        div = m[m["pct_err"] > TOL_PCT]["year"].astype(int).tolist()
        n = int(len(m))
        per.append({"label": label, "n": n, "divergence_years": div,
                    "mae": round(float(m["abs_err"].mean()) if n else float("nan"), 6),
                    "max_pct_err": round(float(m["pct_err"].max()) if n else float("nan"), 6)})
        total_n += n; total_div += len(div); mae_sum += per[-1]["mae"] or 0
        max_pct = max(max_pct, per[-1]["max_pct_err"] or 0)
    status = "PASS" if total_div == 0 else "FAIL"
    row = {
        "status": status, "tolerance_pct": TOL_PCT, "compare_range": list(BOOK_OVERLAP),
        "n_compared": total_n, "mae": round(mae_sum / 2.0, 6), "max_pct_err": max_pct,
        "divergence_count": total_div, "per_subseries": per,
        "note": "Book truth = CD2 S024/S025 (Jastram 1977 + MeasuringWorth gold).",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
