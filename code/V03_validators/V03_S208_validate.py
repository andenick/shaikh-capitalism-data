"""V03_S208_validate - compare processed S208 to book RULC column."""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

PROCESSED = DATA_PROCESSED / "S208.parquet"
XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix2_ManufacturingProductivity.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
TOL_PCT = 1.0
BOOK_OVERLAP = (1889, 2010)


def _truth() -> pd.DataFrame:
    df = pd.read_excel(XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df["year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    return df[["year", "Mfgrealunitlaborcost"]].rename(
        columns={"Mfgrealunitlaborcost": "expected"}).dropna(subset=["expected"])


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S208"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    actual = actual[actual["subseries_id"] == "S208-A"]
    truth = _truth()
    m = actual.merge(truth, on="year", how="inner")
    m = m[(m["year"] >= BOOK_OVERLAP[0]) & (m["year"] <= BOOK_OVERLAP[1])]
    m["abs_err"] = (m["value"] - m["expected"]).abs()
    m["pct_err"] = m["abs_err"] / m["expected"].abs() * 100.0
    n = int(len(m))
    div = m[m["pct_err"] > TOL_PCT]["year"].astype(int).tolist()
    row = {
        "status": "PASS" if not div else "FAIL", "tolerance_pct": TOL_PCT,
        "compare_range": list(BOOK_OVERLAP), "n_compared": n,
        "mae": round(float(m["abs_err"].mean()) if n else float("nan"), 6),
        "max_pct_err": round(float(m["pct_err"].max()) if n else float("nan"), 6),
        "divergence_years": div, "divergence_count": len(div),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
