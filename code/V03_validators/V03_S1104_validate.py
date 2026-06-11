"""V03_S1104_validate - validate S1104-A (X-M)/(X+M) and S1104-B REER.

S1104-A: compare against derived (X-M)/(X+M) computed from Appendix11_XMData.xlsx
        US block. Reference CD2 sample values (1960=-0.606, 2008=-0.533) come
        from intratediff1 column NOT trade balance; the V03 reconstructs the
        Phase-4-canonical trade-balance values directly.
S1104-B: compare against rxr1 (US) from Appendix11_USJPNdata.xlsx.
S1104-C: not loaded (deferred); validator records data_unavailable.
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

SERIES_ID = "S1104"
VALIDATOR_TOL_PCT = 0.5
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
TRUTH_XM = book_data_path("Appendix11_XMData.xlsx")
TRUTH_USJPN = book_data_path("Appendix11_USJPNdata.xlsx")
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"


def _update_report(row: dict) -> None:
    rpt = (json.loads(REPORT.read_text(encoding="utf-8"))
           if REPORT.exists() else
           {"schema_version": "anu-validation-v1.0", "series": {}})
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[SERIES_ID] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def _build_truth_a() -> pd.DataFrame:
    xm = pd.read_excel(TRUTH_XM, header=1).dropna(subset=["Year"])
    xm["Year"] = pd.to_numeric(xm["Year"], errors="coerce").astype("Int64")
    xm = xm.dropna(subset=["Year"])
    xm["Year"] = xm["Year"].astype(int)
    us = xm[xm["Country"] == "United States"].copy()
    us["X"] = pd.to_numeric(us["X (in $M)"], errors="coerce")
    us["M"] = pd.to_numeric(us["M (in $M)"], errors="coerce")
    us["expected"] = (us["X"] - us["M"]) / (us["X"] + us["M"])
    return us[["Year", "expected"]].rename(columns={"Year": "year"}).dropna()


def _build_truth_b() -> pd.DataFrame:
    rr = pd.read_excel(TRUTH_USJPN, header=1).dropna(subset=["Year"])
    rr["Year"] = pd.to_numeric(rr["Year"], errors="coerce").astype("Int64")
    rr = rr.dropna(subset=["Year"])
    rr["Year"] = rr["Year"].astype(int)
    us = rr[rr["Country"] == "United States"].copy()
    return us[["Year", "rxr1"]].rename(columns={"Year": "year", "rxr1": "expected"}).dropna()


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}

    actual = pd.read_parquet(PROCESSED)
    truth_a = _build_truth_a()
    truth_b = _build_truth_b()

    def _check(sub_id: str, truth: pd.DataFrame) -> dict:
        a = actual[actual["subseries_id"] == sub_id]
        merged = a.merge(truth, on="year", how="inner")
        merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
        merged["pct_err"] = merged["abs_err"] / merged["expected"].abs() * 100.0
        return {
            "n": int(len(merged)),
            "mae": float(merged["abs_err"].mean()) if len(merged) else 0.0,
            "max_pct_err": float(merged["pct_err"].max()) if len(merged) else 0.0,
            "div_years": merged[merged["pct_err"] > VALIDATOR_TOL_PCT][
                "year"].astype(int).tolist(),
        }

    r_a = _check("S1104-A", truth_a)
    r_b = _check("S1104-B", truth_b)

    n_total = r_a["n"] + r_b["n"]
    mae = (r_a["mae"] * r_a["n"] + r_b["mae"] * r_b["n"]) / max(n_total, 1)
    max_pct = max(r_a["max_pct_err"], r_b["max_pct_err"])
    all_div = r_a["div_years"] + r_b["div_years"]
    status = "PASS" if not all_div else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "time_series",
        "comparison_basis": "S1104-A: (X-M)/(X+M) from Appendix11_XMData US block; S1104-B: rxr1 from Appendix11_USJPNdata US block",
        "n_compared": n_total,
        "mae": round(mae, 6),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(all_div),
        "divergence_years": all_div,
        "per_subseries": {"S1104-A": r_a, "S1104-B": r_b,
                          "S1104-C": {"n": 0, "status": "data_unavailable_eu12_relgdp_not_in_salvage"}},
        "cd2_comparison": {"note": "CD2 S063 trade-balance samples align with (X-M)/(X+M), not X/M."},
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
