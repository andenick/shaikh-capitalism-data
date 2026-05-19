"""V03_S210_validate - compare processed S210 (US, UK) to CD2 S023 values.

CD2 S023 IS our book truth here (no Appendix 2 chopped table for WPI).
"""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_EXT_BENCH  # noqa: E402

PROCESSED = DATA_PROCESSED / "S210.parquet"
S023_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S023_us_and_uk_wholesale_price_indexes_1790_2010.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
TOL_PCT = 1.0
BOOK_OVERLAP = (1790, 2010)


def _truth() -> pd.DataFrame:
    df = pd.read_excel(S023_XLSX, sheet_name="Data").rename(columns={"Year": "year"})
    df = df.dropna(subset=["year"]).astype({"year": int})
    return df[["year", "S023-A", "S023-B"]].rename(columns={"S023-A": "us_exp", "S023-B": "uk_exp"})


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S210"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def _check(actual: pd.DataFrame, expected: pd.Series, label: str, year_min: int, year_max: int) -> dict:
    m = actual.merge(expected.reset_index().rename(columns={expected.name: "expected"}), on="year", how="inner")
    m = m[(m["year"] >= year_min) & (m["year"] <= year_max)].dropna(subset=["expected"])
    m["abs_err"] = (m["value"] - m["expected"]).abs()
    m["pct_err"] = m["abs_err"] / m["expected"].abs() * 100.0
    div = m[m["pct_err"] > TOL_PCT]["year"].astype(int).tolist()
    n = int(len(m))
    return {"label": label, "n": n,
            "mae": round(float(m["abs_err"].mean()) if n else float("nan"), 6),
            "max_pct_err": round(float(m["pct_err"].max()) if n else float("nan"), 6),
            "divergence_years": div, "divergence_count": len(div)}


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = _truth().set_index("year")
    a_check = _check(actual[actual["subseries_id"] == "S210-A"], truth["us_exp"], "US WPI", *BOOK_OVERLAP)
    b_check = _check(actual[actual["subseries_id"] == "S210-B"], truth["uk_exp"], "UK WPI", *BOOK_OVERLAP)
    total_div = a_check["divergence_count"] + b_check["divergence_count"]
    status = "PASS" if total_div == 0 else "FAIL"
    row = {
        "status": status, "tolerance_pct": TOL_PCT, "compare_range": list(BOOK_OVERLAP),
        "n_compared": a_check["n"] + b_check["n"],
        "mae": round((a_check["mae"] + b_check["mae"]) / 2.0, 6),
        "max_pct_err": max(a_check["max_pct_err"], b_check["max_pct_err"]),
        "divergence_count": total_div,
        "per_subseries": [a_check, b_check],
        "note": "Book truth = CD2 S023 (no Appendix 2 chopped table); BLS WPU substituted for frozen WPS post-1974.",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
