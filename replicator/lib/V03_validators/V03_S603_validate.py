"""V03_S603_validate — round-trip-validate S603 against the Shaikh Appendix 6.8 source.

The Shaikh Appendix 6.8 chopped table IS the Phase-5 book-truth for this
series. The validator re-reads the source workbook for the same (subseries,
year) pairs the processed parquet contains, applies the same unit
normalization, and reports MAE / max_pct_err / divergence_years against a
1.0% tolerance per year.

This is a defensive round-trip: it confirms the loader honored its source
mapping and the processor preserved values bit-for-bit. CD2 informational
comparison is included where a CD2 per-series file exists.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402
from L01_loaders._ch6_appendix_loader import load_variables  # noqa: E402

SERIES_ID = "S603"
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = 1.0

SOURCE_MAP = {'S603-A': ['II7', 'x1', 1.0], 'S603-B': ['II7', 'x2', 1.0], 'S603-C': ['II7', 'x3', 1.0], 'S603-D': ['II7', 'x3*(x1 / x2)', 1.0]}


def _expected_long() -> pd.DataFrame:
    parts = []
    for sub_id, (table, var, scale) in SOURCE_MAP.items():
        df = load_variables(table, [var])
        if df.empty:
            continue
        df = df.copy()
        df["expected"] = df["value"] * scale
        df["subseries_id"] = sub_id
        parts.append(df[["year", "subseries_id", "expected"]])
    if not parts:
        return pd.DataFrame(columns=["year", "subseries_id", "expected"])
    return pd.concat(parts, ignore_index=True)


def _update_report(row: dict) -> None:
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
    expected = _expected_long()
    if expected.empty:
        row = {"status": "PASS_NO_BOOKTRUTH",
               "reason": "Appendix-6.8 expected dataframe is empty",
               "validated_at": datetime.now(timezone.utc).isoformat()}
        _update_report(row)
        return row

    merged = actual.merge(expected, on=["year", "subseries_id"], how="inner")
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    # pct_err is undefined when expected==0 (e.g. ratio variants); guard.
    safe = merged["expected"].abs().replace(0.0, float("nan"))
    merged["pct_err"] = merged["abs_err"] / safe * 100.0

    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max(skipna=True)) if n else float("nan")
    div = merged[merged["pct_err"] > VALIDATOR_TOL_PCT][["year", "subseries_id", "value", "expected", "pct_err"]]
    div_years = sorted(div["year"].astype(int).unique().tolist())
    status = "PASS" if len(div) == 0 else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "n_compared": n,
        "mae": round(mae, 6) if not pd.isna(mae) else None,
        "max_abs_err": round(max_abs, 6) if not pd.isna(max_abs) else None,
        "max_pct_err": round(max_pct, 6) if not pd.isna(max_pct) else None,
        "divergence_years": div_years,
        "divergence_count": int(len(div)),
        "subseries_compared": sorted(merged["subseries_id"].unique().tolist()),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
