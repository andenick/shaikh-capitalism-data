"""V03_S218_validate - compare processed S218 against the RICHEST/POOREST 4
and ratio rows of Appendix2_GDPperCapita.xlsx.
"""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402

PROCESSED = DATA_PROCESSED / "S218.parquet"
XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix2_GDPperCapita.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
TOL_PCT = 1.0
BOOK_OVERLAP = (1600, 2000)
LABELS = ["RICHEST 4", "POOREST 4", "RATIO OF RICHEST 4 TO POOREST 4"]


def _truth() -> pd.DataFrame:
    df = pd.read_excel(XLSX, header=1)
    df.columns = [c if isinstance(c, int) else str(c).strip() for c in df.columns]
    year_cols = [c for c in df.columns if isinstance(c, int)]
    rows = []
    seen = set()
    for _, row in df.iterrows():
        label = row["Year"]
        if not isinstance(label, str):
            continue
        label = label.strip()
        if label in LABELS and label not in seen:
            seen.add(label)
            for yc in year_cols:
                v = row[yc]
                if pd.notna(v):
                    rows.append({"label": label, "year": int(yc), "expected": float(v)})
    return pd.DataFrame(rows)


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S218"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": "processed missing"}
    actual = pd.read_parquet(PROCESSED)
    truth = _truth()
    m = actual.merge(truth, on=["label", "year"], how="inner")
    m["abs_err"] = (m["value"] - m["expected"]).abs()
    m["pct_err"] = m["abs_err"] / m["expected"].abs() * 100.0
    div = m[m["pct_err"] > TOL_PCT][["label", "year", "value", "expected", "pct_err"]]
    n = int(len(m))
    row = {
        "status": "PASS" if len(div) == 0 else "FAIL",
        "tolerance_pct": TOL_PCT, "compare_range": list(BOOK_OVERLAP),
        "n_compared": n,
        "mae": round(float(m["abs_err"].mean()) if n else float("nan"), 6),
        "max_pct_err": round(float(m["pct_err"].max()) if n else float("nan"), 6),
        "divergence_count": int(len(div)),
        "labels_compared": sorted(m["label"].unique().tolist()),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
