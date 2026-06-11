"""V03_S903_validate - validate wage-profit curves + R_t against PennWorldTables2 workbook.

Sanity gate: R_fixed values must match Table 9.18:
  [1.088, 0.9734, 0.8547, 0.7644, 0.7033, 0.7317]
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

PROCESSED = DATA_PROCESSED / "S903.parquet"
PWT2_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix9_PennWorldTables2.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = 0.5

EXPECTED_R_FIXED = [1.088, 0.9734, 0.8547, 0.7644, 0.7033, 0.7317]
EXPECTED_YEARS = [1947, 1958, 1963, 1967, 1972, 1998]

YEAR_LABELS = [
    ("47", 1947, "wshr47", "wr47"),
    ("58", 1958, "wshr58", "wr58"),
    ("63", 1963, "wshr63", "wr63"),
    ("67", 1967, "wshr67", "wr67"),
    ("72", 1972, "wshr72", "wr72"),
    ("98FIX", 1998, "wshr98", "wr98fix"),
    ("98CIRC", 1998, "wshrCirc", "wr98circ"),
]


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S903"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": "processed missing"}
    if not PWT2_XLSX.exists():
        return {"status": "FAIL", "error": f"PWT2 truth XLSX missing: {PWT2_XLSX}"}

    actual = pd.read_parquet(PROCESSED)
    truth = pd.read_excel(PWT2_XLSX, header=1)
    truth.columns = [str(c).strip() for c in truth.columns]

    per_curve = []
    total_div = 0
    overall_mae = []
    for label, year, wshcol, wrcol in YEAR_LABELS:
        for sid_prefix, col in [(f"S903-WSHARE-{label}", wshcol),
                                  (f"S903-WRCURVE-{label}", wrcol)]:
            if col not in truth.columns:
                continue
            a = actual[actual["subseries_id"] == sid_prefix]
            t_col = truth[[col]].copy().reset_index(drop=False).rename(
                columns={"index": "industry_index", col: "expected"})
            m = a.merge(t_col, on="industry_index", how="inner").dropna(subset=["expected"])
            m["abs_err"] = (m["value"] - m["expected"]).abs()
            m["pct_err"] = m["abs_err"] / m["expected"].abs() * 100.0
            div = m[m["pct_err"] > VALIDATOR_TOL_PCT]["industry_index"].astype(int).tolist()
            total_div += len(div)
            if len(m):
                overall_mae.append(float(m["abs_err"].mean()))
            per_curve.append({
                "subseries": sid_prefix, "n": int(len(m)),
                "mae": round(float(m["abs_err"].mean()) if len(m) else 0.0, 10),
                "max_pct_err": round(float(m["pct_err"].max()) if len(m) else 0.0, 10),
                "divergences_count": len(div),
            })

    # R_fixed sanity gate
    r_check = []
    r_actual = actual[actual["subseries_id"] == "S903-R-FIXED"]
    for y, exp in zip(EXPECTED_YEARS, EXPECTED_R_FIXED):
        match = r_actual[r_actual["year"] == y]
        if not match.empty:
            got = float(match["value"].iloc[0])
            diff_pct = abs(got - exp) / exp * 100.0
            r_check.append({"year": y, "expected": exp, "got": round(got, 6),
                             "diff_pct": round(diff_pct, 4), "ok": diff_pct < 0.5})

    status = "PASS" if (total_div == 0 and all(c["ok"] for c in r_check)) else "FAIL"
    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT,
        "per_curve": per_curve,
        "mae": round(sum(overall_mae) / max(1, len(overall_mae)), 10),
        "r_fixed_sanity_gate": r_check,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
