"""V03_S1003_validate — compare processed S1003 against USLR 'ib/p' column."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

PROCESSED = DATA_PROCESSED / "S1003.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix10_USLR.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1857, 2011)


def _load_truth() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df[["Year", "ib/p"]].rename(columns={"Year": "year", "ib/p": "expected"})


def _update_report(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S1003"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    actual = actual[actual["subseries_id"] == "S1003-A"][["year", "value"]]
    truth = _load_truth().dropna(subset=["expected"])
    truth = truth[(truth["year"] >= BOOK_OVERLAP[0]) & (truth["year"] <= BOOK_OVERLAP[1])]
    m = actual.merge(truth, on="year", how="inner")
    m["abs_err"] = (m["value"] - m["expected"]).abs()
    m["pct_err"] = (m["abs_err"] / m["expected"].abs().replace(0, float("nan"))) * 100.0
    n = int(len(m))
    mae = float(m["abs_err"].mean()) if n else float("nan")
    max_pct = float(m["pct_err"].max()) if n else float("nan")
    div = m[m["pct_err"] > VALIDATOR_TOL_PCT]["year"].astype(int).tolist()
    status = "PASS" if not div else "FAIL"
    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": list(BOOK_OVERLAP),
        "n_compared": n,
        "mae": round(mae, 6),
        "max_abs_err": round(float(m["abs_err"].max()) if n else 0, 6),
        "max_pct_err": round(max_pct, 6),
        "divergence_years": div[:50],
        "divergence_count": len(div),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
