"""V03_S502_validate - compare processed S502 against Appendix5 columns (book period).

Also reports the 58x (UK 2010/1939) and 14x (US 2010/1940) book-cited ratios as
informational diagnostics.
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

PROCESSED = DATA_PROCESSED / "S502.parquet"
XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix5_DATALRprices.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = 1.0
YEAR_MIN, YEAR_MAX = 1790, 2010


def _truth() -> pd.DataFrame:
    df = pd.read_excel(XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    df = df[(df["Year"] >= YEAR_MIN) & (df["Year"] <= YEAR_MAX)]
    return df[["Year", "USWPI", "UKWPI"]].rename(columns={"Year": "year"})


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S502"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": "processed missing"}
    actual = pd.read_parquet(PROCESSED)
    truth = _truth()
    out_rows = []
    overall_div = 0
    overall_mae = []
    for sub_id, col in [("S502-A", "USWPI"), ("S502-B", "UKWPI")]:
        a = actual[(actual["subseries_id"] == sub_id) &
                   (actual["year"] >= YEAR_MIN) & (actual["year"] <= YEAR_MAX)]
        m = a.merge(truth[["year", col]], on="year", how="inner").dropna(subset=[col])
        m["abs_err"] = (m["value"] - m[col]).abs()
        m["pct_err"] = m["abs_err"] / m[col].abs() * 100.0
        div = m[m["pct_err"] > VALIDATOR_TOL_PCT]["year"].astype(int).tolist()
        overall_div += len(div)
        if len(m) > 0:
            overall_mae.append(float(m["abs_err"].mean()))
        out_rows.append({
            "subseries": sub_id, "col": col, "n": int(len(m)),
            "mae": round(float(m["abs_err"].mean()) if len(m) else 0.0, 8),
            "max_pct_err": round(float(m["pct_err"].max()) if len(m) else 0.0, 8),
            "divergence_years": div,
        })

    # Informational diagnostics
    diag = {}
    try:
        us_2010 = float(truth[truth["year"] == 2010]["USWPI"].iloc[0])
        us_1940 = float(truth[truth["year"] == 1940]["USWPI"].iloc[0])
        uk_2010 = float(truth[truth["year"] == 2010]["UKWPI"].iloc[0])
        uk_1939 = float(truth[truth["year"] == 1939]["UKWPI"].iloc[0])
        diag = {
            "US_2010_over_1940": round(us_2010 / us_1940, 3),
            "UK_2010_over_1939": round(uk_2010 / uk_1939, 3),
            "book_claim_US": 14.0, "book_claim_UK": 58.0,
        }
    except Exception:
        pass

    status = "PASS" if overall_div == 0 else "FAIL"
    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": [YEAR_MIN, YEAR_MAX],
        "mae": round(sum(overall_mae) / max(1, len(overall_mae)), 8),
        "per_subseries": out_rows,
        "inflation_diagnostics": diag,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
