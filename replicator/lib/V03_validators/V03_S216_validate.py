"""V03_S216_validate - compare normalized prices to book's Appendix9 1972 values.

Tolerance 0.5% per industry (cross-sectional per playbook).
"""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

PROCESSED = DATA_PROCESSED / "S216.parquet"
XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix9_1972fixed.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = 0.5


def _truth() -> pd.DataFrame:
    df = pd.read_excel(XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Index"]).copy()
    df["Index"] = pd.to_numeric(df["Index"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["Index"])
    df = df[(df["Index"] >= 1) & (df["Index"] <= 71)].copy()
    df["tpm_norm"] = df["tpm"] / df["tpm"].sum()
    df["tpr_norm"] = df["tp(r)"] / df["tp(r)"].sum()
    return df[["Index", "tpm_norm", "tpr_norm"]].rename(columns={"Index": "industry_index"})


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S216"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": "processed missing"}
    actual = pd.read_parquet(PROCESSED)
    truth = _truth()
    # Compare A (tp(r) normalized) and B (tpm normalized)
    a = actual[actual["subseries_id"] == "S216-A"].merge(truth, on="industry_index", how="inner")
    b = actual[actual["subseries_id"] == "S216-B"].merge(truth, on="industry_index", how="inner")
    a["abs_err"] = (a["value"] - a["tpr_norm"]).abs()
    b["abs_err"] = (b["value"] - b["tpm_norm"]).abs()
    a["pct_err"] = a["abs_err"] / a["tpr_norm"].abs() * 100.0
    b["pct_err"] = b["abs_err"] / b["tpm_norm"].abs() * 100.0
    a_div = a[a["pct_err"] > VALIDATOR_TOL_PCT]["industry_index"].astype(int).tolist()
    b_div = b[b["pct_err"] > VALIDATOR_TOL_PCT]["industry_index"].astype(int).tolist()
    total_div = len(a_div) + len(b_div)
    status = "PASS" if total_div == 0 else "FAIL"
    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT, "year": 1972,
        "n_industries": int(a["industry_index"].nunique()),
        "per_subseries": [
            {"label": "tp(r) normalized", "n": int(len(a)),
             "mae": round(float(a["abs_err"].mean()), 8),
             "max_pct_err": round(float(a["pct_err"].max()), 6),
             "divergence_industries": a_div},
            {"label": "tpm normalized", "n": int(len(b)),
             "mae": round(float(b["abs_err"].mean()), 8),
             "max_pct_err": round(float(b["pct_err"].max()), 6),
             "divergence_industries": b_div},
        ],
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
