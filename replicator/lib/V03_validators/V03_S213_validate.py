"""V03_S213_validate - compare processed S213 to CD2 S026-A column."""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_EXT_BENCH  # noqa: E402

PROCESSED = DATA_PROCESSED / "S213.parquet"
S026_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S026_corporate_and_non_corporate_profit_rates.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
TOL_PCT = 1.0
BOOK_OVERLAP = (1947, 2011)


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S213"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = pd.read_excel(S026_XLSX, sheet_name="Data").rename(columns={"Year": "year"})
    truth = truth.dropna(subset=["year"]).astype({"year": int})[["year", "S026-A"]].rename(columns={"S026-A": "expected"}).dropna(subset=["expected"])
    m = actual.merge(truth, on="year", how="inner")
    m = m[(m["year"] >= BOOK_OVERLAP[0]) & (m["year"] <= BOOK_OVERLAP[1])]
    m["abs_err"] = (m["value"] - m["expected"]).abs()
    # Profit rates are 0.10-0.20 typically; small abs threshold for div
    is_div = m["abs_err"] > 0.005   # 0.5pp absolute
    n = int(len(m))
    div = m[is_div]["year"].astype(int).tolist()
    row = {
        "status": "PASS" if not div else "FAIL", "tolerance_pct": TOL_PCT,
        "compare_range": list(BOOK_OVERLAP), "n_compared": n,
        "mae": round(float(m["abs_err"].mean()) if n else float("nan"), 6),
        "max_abs_err": round(float(m["abs_err"].max()) if n else float("nan"), 6),
        "divergence_years": div, "divergence_count": len(div),
        "note": "Tolerance: 0.005 absolute (profit rates ~0.10-0.20).",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
