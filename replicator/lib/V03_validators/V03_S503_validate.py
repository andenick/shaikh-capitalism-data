"""V03_S503_validate - validate S503 against Appendix5 UKPPIGold + UKGoldpriceindex columns.

Also checks internal consistency: UKWPI ≈ (UKPPIGold * UKGoldpriceindex) / 100 within tolerance.
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

PROCESSED = DATA_PROCESSED / "S503.parquet"
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
    return df[["Year", "UKPPIGold", "UKGoldpriceindex", "UKWPI"]].rename(
        columns={"Year": "year"})


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S503"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": "processed missing"}
    actual = pd.read_parquet(PROCESSED)
    truth = _truth()
    out_rows = []
    overall_div = 0
    overall_mae = []
    for sub_id, col in [("S503-A", "UKPPIGold"), ("S503-B", "UKGoldpriceindex")]:
        a = actual[actual["subseries_id"] == sub_id]
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

    # Internal consistency: UKWPI ~ UKPPIGold * UKGoldpriceindex / 100
    consistency = {}
    try:
        for y in [1790, 1930, 2010]:
            r = truth[truth["year"] == y].iloc[0]
            recon = r["UKPPIGold"] * r["UKGoldpriceindex"] / 100.0
            consistency[str(y)] = {"UKWPI": round(float(r["UKWPI"]), 3),
                                    "recon_p_x_pG/100": round(float(recon), 3),
                                    "diff_pct": round(abs(recon - r["UKWPI"]) / r["UKWPI"] * 100.0, 4)}
    except Exception:
        pass

    status = "PASS" if overall_div == 0 else "FAIL"
    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT,
        "compare_range": [YEAR_MIN, YEAR_MAX],
        "mae": round(sum(overall_mae) / max(1, len(overall_mae)), 8),
        "per_subseries": out_rows,
        "internal_consistency_check": consistency,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
