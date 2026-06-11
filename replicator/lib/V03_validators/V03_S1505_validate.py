"""V03_S1505_validate - validate S1505 against the book chopped table."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

PROCESSED = DATA_PROCESSED / "S1505.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix15_USInflation.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1948, 2010)
SERIES_ID = "S1505"


def _truth() -> pd.DataFrame:
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=[0, 1])
    col_year = raw.columns[0]
    col_pi = raw.columns[3]
    col_sigma = raw.columns[8]
    col_sigma_prime = raw.columns[22]
    col_uL = raw.columns[14]
    col_uLint = raw.columns[15]
    df = pd.DataFrame({
        "year": pd.to_numeric(raw[col_year], errors="coerce"),
        "S1505-pi": pd.to_numeric(raw[col_pi], errors="coerce"),
        "S1505-sigma": pd.to_numeric(raw[col_sigma], errors="coerce"),
        "S1505-sigma-prime": pd.to_numeric(raw[col_sigma_prime], errors="coerce"),
        "S1505-uL": pd.to_numeric(raw[col_uL], errors="coerce"),
        "S1505-uLintensity": pd.to_numeric(raw[col_uLint], errors="coerce"),
    }).dropna(subset=["year"]).astype({"year": int})
    rows = []
    for sub_id in ["S1505-pi", "S1505-sigma", "S1505-sigma-prime", "S1505-uL", "S1505-uLintensity"]:
        sl = df[["year", sub_id]].rename(columns={sub_id: "expected"}).dropna(subset=["expected"])
        sl["subseries_id"] = sub_id
        rows.append(sl)
    return pd.concat(rows, ignore_index=True)


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[SERIES_ID] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = _truth()
    merged = actual.merge(truth, on=["year", "subseries_id"], how="inner")
    merged = merged[(merged["year"] >= BOOK_OVERLAP[0]) & (merged["year"] <= BOOK_OVERLAP[1])]
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    merged["pct_err"] = merged["abs_err"] / merged["expected"].abs().clip(lower=1e-9) * 100.0
    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max()) if n else float("nan")
    bad = merged[(merged["abs_err"] > 0.005) & (merged["pct_err"] > VALIDATOR_TOL_PCT)]
    div = bad[["year", "subseries_id", "value", "expected", "abs_err", "pct_err"]].to_dict("records")
    status = "PASS" if not div else "FAIL"
    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "tolerance_abs": 0.005,
        "compare_range": list(BOOK_OVERLAP),
        "n_compared": n,
        "mae": round(mae, 8),
        "max_abs_err": round(max_abs, 8),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(div),
        "divergence_sample": div[:5],
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
