"""V03_S1504_validate - validate S1504 against the book chopped table.

Compares S1504-GDP, S1504-CR, S1504-CA, S1504-gGDP, S1504-pp values against
the corresponding columns of Appendix15_USInflation.xlsx on 1948-2010.

If modern IMF CR rows are present, also runs the resolver's
validate_against_shaikh cross-check on the 2001-2010 overlap with +/- 2%.
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
from loaders._imf_ifs_resolver import validate_against_shaikh  # noqa: E402

PROCESSED = DATA_PROCESSED / "S1504.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix15_USInflation.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 1.0
BOOK_OVERLAP = (1948, 2010)
SERIES_ID = "S1504"

# Subseries -> chopped column
SUB_TO_COL = {
    "S1504-GDP": "GDP",
    "S1504-pGDP": "pgdp",
    "S1504-CR": "CR",
    "S1504-CA": "CA",
    "S1504-gGDP": "gGDP",
    "S1504-gCR": "gCR",
    "S1504-pp": "pp",
}


def _load_book_truth() -> pd.DataFrame:
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=[0, 1])
    raw.columns = [str(c[1]).strip() for c in raw.columns]
    raw = raw.dropna(subset=["Year"])
    raw["Year"] = pd.to_numeric(raw["Year"], errors="coerce")
    raw = raw.dropna(subset=["Year"]).astype({"Year": int})
    raw = raw.rename(columns={"Year": "year"})
    rows = []
    for sub_id, col in SUB_TO_COL.items():
        if col not in raw.columns:
            continue
        sl = raw[["year", col]].rename(columns={col: "expected"}).dropna(subset=["expected"])
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
    truth = _load_book_truth()
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

    # IMF cross-check (informational)
    imf_check = {}
    cr_modern = actual[actual["subseries_id"] == "S1504-CR-modern"]
    cr_shaikh = actual[actual["subseries_id"] == "S1504-CR"]
    if not cr_modern.empty and not cr_shaikh.empty:
        modern_dict = {int(r.year): float(r.value) for r in cr_modern.itertuples()}
        shaikh_dict = {int(r.year): float(r.value) for r in cr_shaikh.itertuples()}
        imf_check = validate_against_shaikh(modern_dict, shaikh_dict, tolerance_pct=2.0)

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
        "imf_cross_check": imf_check,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
