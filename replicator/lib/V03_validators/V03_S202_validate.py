"""V03_S202_validate - check processed S202 against SplicedRealInvest_Reindexed1958.

Tolerance 1% per year on overlap 1832-2010.
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

PROCESSED = DATA_PROCESSED / "S202.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix2_RealInvestmentUS_1832-2010.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1832, 2010)


def _book_truth() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    truth = df[["Year", "SplicedRealInvest_Reindexed1958"]].rename(
        columns={"Year": "year", "SplicedRealInvest_Reindexed1958": "expected"})
    return truth.dropna(subset=["expected"])


def _update_report(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S202"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = _book_truth()
    m = actual.merge(truth, on="year", how="inner")
    m = m[(m["year"] >= BOOK_OVERLAP[0]) & (m["year"] <= BOOK_OVERLAP[1])]
    m["abs_err"] = (m["value"] - m["expected"]).abs()
    m["pct_err"] = m["abs_err"] / m["expected"].abs() * 100.0
    n = int(len(m))
    mae = float(m["abs_err"].mean()) if n else float("nan")
    max_pct = float(m["pct_err"].max()) if n else float("nan")
    max_abs = float(m["abs_err"].max()) if n else float("nan")
    div = m[m["pct_err"] > VALIDATOR_TOL_PCT][["year", "value", "expected", "pct_err"]]
    div_years = div["year"].astype(int).tolist()
    status = "PASS" if not div_years else "FAIL"
    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": list(BOOK_OVERLAP), "n_compared": n,
        "mae": round(mae, 6), "max_abs_err": round(max_abs, 6),
        "max_pct_err": round(max_pct, 6),
        "divergence_years": div_years, "divergence_count": len(div_years),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
