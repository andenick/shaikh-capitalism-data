"""V03_S207_validate - compare S207-A vs productivity, S207-B vs real comp index.

We validate each subseries separately against its book column. PASS requires
both to be within tolerance.
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

PROCESSED = DATA_PROCESSED / "S207.parquet"
PROD_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix2_ManufacturingProductivityAndRealWages1889-2010.xlsx"
COMP_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix2_ManufacturingProductivity.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
TOL_PCT = 1.0
BOOK_OVERLAP = (1889, 2010)


def _truth_prod() -> pd.DataFrame:
    df = pd.read_excel(PROD_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    return df[["year", "Mfgprdvty_spliced_Reindexed1889"]].rename(
        columns={"Mfgprdvty_spliced_Reindexed1889": "expected"}).dropna(subset=["expected"])


def _truth_comp() -> pd.DataFrame:
    df = pd.read_excel(COMP_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    return df[["year", "mfgprdwkrecrealindex"]].rename(
        columns={"mfgprdwkrecrealindex": "expected"}).dropna(subset=["expected"])


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S207"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def _check(actual: pd.DataFrame, truth: pd.DataFrame, label: str) -> dict:
    m = actual.merge(truth, on="year", how="inner")
    m = m[(m["year"] >= BOOK_OVERLAP[0]) & (m["year"] <= BOOK_OVERLAP[1])]
    m["abs_err"] = (m["value"] - m["expected"]).abs()
    m["pct_err"] = m["abs_err"] / m["expected"].abs() * 100.0
    div = m[m["pct_err"] > TOL_PCT]["year"].astype(int).tolist()
    n = int(len(m))
    return {
        "label": label, "n": n,
        "mae": round(float(m["abs_err"].mean()) if n else float("nan"), 6),
        "max_pct_err": round(float(m["pct_err"].max()) if n else float("nan"), 6),
        "divergence_years": div, "divergence_count": len(div),
    }


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    a_check = _check(actual[actual["subseries_id"] == "S207-A"], _truth_prod(), "productivity")
    b_check = _check(actual[actual["subseries_id"] == "S207-B"], _truth_comp(), "compensation")
    all_div = a_check["divergence_count"] + b_check["divergence_count"]
    status = "PASS" if all_div == 0 else "FAIL"
    row = {
        "status": status, "tolerance_pct": TOL_PCT, "compare_range": list(BOOK_OVERLAP),
        "n_compared": a_check["n"] + b_check["n"],
        "mae": round((a_check["mae"] + b_check["mae"]) / 2.0, 6) if (a_check["n"] and b_check["n"]) else (a_check["mae"] or b_check["mae"]),
        "max_pct_err": max(a_check["max_pct_err"], b_check["max_pct_err"]),
        "divergence_years": sorted(set(a_check["divergence_years"] + b_check["divergence_years"])),
        "divergence_count": all_div,
        "per_subseries": [a_check, b_check],
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
