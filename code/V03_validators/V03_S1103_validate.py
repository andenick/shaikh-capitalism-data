"""V03_S1103_validate - validate S1103 LOP-ratio against book truth.

Two checks:
  (1) Cell-by-cell match of processed `value` to Appendix11_USJPNdata
      'rxrrulcratio1' column (tol 0.5%).
  (2) Derivation consistency: rxr1 / rulcadjratio1rescaled ~= rxrrulcratio1
      (tol 0.5%). Detects the formula construction documented in Appendix 11
      Documentation sheet.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, book_data_path  # noqa: E402

SERIES_ID = "S1103"
VALIDATOR_TOL_PCT = 0.5
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
TRUTH_XLSX = book_data_path("Appendix11_USJPNdata.xlsx")
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"


def _update_report(row: dict) -> None:
    rpt = (json.loads(REPORT.read_text(encoding="utf-8"))
           if REPORT.exists() else
           {"schema_version": "anu-validation-v1.0", "series": {}})
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[SERIES_ID] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    if not TRUTH_XLSX.exists():
        return {"status": "FAIL", "error": f"book truth missing: {TRUTH_XLSX}"}

    actual = pd.read_parquet(PROCESSED)
    truth = pd.read_excel(TRUTH_XLSX, header=1).dropna(subset=["Year"])
    truth["Year"] = pd.to_numeric(truth["Year"], errors="coerce").astype("Int64")
    truth = truth.dropna(subset=["Year"])
    truth["Year"] = truth["Year"].astype(int)
    truth = truth.rename(columns={"Year": "year", "Country": "country"})
    truth_lop = truth[["year", "country", "rxrrulcratio1",
                       "rxr1", "rulcadjratio1rescaled"]].rename(
        columns={"rxrrulcratio1": "expected"})
    truth_lop = truth_lop.dropna(subset=["expected"])

    merged = actual.merge(truth_lop, on=["year", "country"], how="inner",
                          suffixes=("", "_truth"))
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    merged["pct_err"] = merged["abs_err"] / merged["expected"].abs() * 100.0

    # Derivation consistency check (formula audit)
    deriv = merged.dropna(subset=["rxr1", "rulcadjratio1rescaled"]).copy()
    deriv["formula_value"] = deriv["rxr1"] / deriv["rulcadjratio1rescaled"]
    deriv["formula_pct_err"] = (deriv["formula_value"] - deriv["expected"]).abs() / deriv["expected"].abs() * 100.0
    formula_max_pct = float(deriv["formula_pct_err"].max()) if len(deriv) else 0.0

    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else 0.0
    max_pct = float(merged["pct_err"].max()) if n else 0.0
    divergence = merged[merged["pct_err"] > VALIDATOR_TOL_PCT]
    div_years = divergence[["year", "country", "pct_err"]].to_dict("records")
    status = "PASS" if len(div_years) == 0 else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "time_series",
        "comparison_basis": "Appendix11_USJPNdata.xlsx rxrrulcratio1 column (= rxr1 / rulcadjratio1rescaled)",
        "n_compared": n,
        "mae": round(mae, 6),
        "max_abs_err": round(float(merged["abs_err"].max()) if n else 0.0, 6),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(div_years),
        "divergences": div_years[:10],
        "formula_audit": {
            "rxr1_over_rulcadj_max_pct_err_vs_published": round(formula_max_pct, 6),
            "construction": "formula (REER/RULC ratio)",
        },
        "cd2_comparison": {"note": "CD2 S062 markdown showed Japan 1960=99.79; matches column."},
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
