"""V03_S215 — full-series recompute check for the Appendix-7 12-industry IROP average.

F-P2.4-01 CLOSURE (swap-blindness). The prior validator returned a static
``PASS_DATA_UNAVAILABLE`` and compared NO values, so the mutation harness's
``swap_2_mid`` (swap two mid-region years' values) was BLIND. This validator now
RE-DERIVES the shipped extension from the RAW Appendix-7 incremental-ROP workbook —
using its OWN hard-coded canonical industry map (NOT imported from L01_S215) —
computes the 12-industry mean for every year, and asserts the processed/chopped value
equals it at EVERY year. Any per-year divergence (swap/scale/shift) => FAIL.

Loader-independence: a from-scratch second derivation of the same canonical mapping;
a mapping bug would have to hit BOTH loader and validator identically to pass —
mitigated by the hard 12-industry assert. Book period 1960-1989 remains
``data_unavailable``; this validator certifies only the shipped post-book extension.
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

PROCESSED = DATA_PROCESSED / "S215.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
RAW_WORKBOOK = "Appendix7_iropdataUSind.xlsx"

# Independent copy of the canonical intended-industry -> Appendix-7 header map
# (see V03_S214). Motor Vehicles is genuinely absent -> recoverable set is 12.
MFG_HEADERS = [
    "Chemicals", "Electr.Equ.", "Fab.Metal.", "Food", "Mach.", "Paper",
    "Petroleum", "Plastic", "Prim.Metal.", "Printing", "Text.Mills", "Wood",
]
N_EXPECTED_MFG = 12
ABS_TOL = 1e-6


def _recompute_mfg_avg() -> dict:
    xl = book_data_path(RAW_WORKBOOK)
    df = pd.read_excel(xl, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    matched = [h for h in MFG_HEADERS if h in df.columns]
    missing = [h for h in MFG_HEADERS if h not in df.columns]
    assert len(matched) == N_EXPECTED_MFG, (
        f"expected {N_EXPECTED_MFG} manufacturing headers, matched {len(matched)}; "
        f"MISSING {missing} (header drift in {xl.name}) — refusing to certify a partial average")
    df["mfg_avg"] = df[matched].mean(axis=1)
    return {int(y): float(v) for y, v in zip(df["Year"], df["mfg_avg"])}


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S215"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": "processed missing"}
    df = pd.read_parquet(PROCESSED)
    df = df[["year", "value"]].dropna().copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype(int)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    recompute = _recompute_mfg_avg()
    mismatches = []
    max_abs_err = 0.0
    for _, r in df.iterrows():
        y = int(r["year"])
        exp = recompute.get(y)
        if exp is None:
            mismatches.append({"year": y, "reason": "year absent from raw workbook recompute",
                               "chopped": float(r["value"])})
            continue
        err = abs(float(r["value"]) - exp)
        max_abs_err = max(max_abs_err, err)
        if err > ABS_TOL:
            mismatches.append({"year": y, "chopped": float(r["value"]),
                               "recompute": exp, "abs_err": err})

    status = "FAIL" if mismatches else "PASS_EXTENSION_ONLY"
    row = {
        "status": status,
        "validation_class": "extension_only",
        "check": "full_series_recompute_vs_raw_Appendix7 (F-P2.4-01)",
        "n_years_checked": int(len(df)),
        "max_abs_err": max_abs_err,
        "tolerance_abs": ABS_TOL,
        "n_mismatches": len(mismatches),
        "mismatches": mismatches[:20],
        "extension_range": [int(df["year"].min()), int(df["year"].max())] if len(df) else None,
        "book_period": [1960, 1989],
        "book_period_status": "data_unavailable",
        "reason": ("Post-book 12-industry incremental-ROP average (1988-2005) recompute-verified against "
                   "raw Appendix7_iropdataUSind.xlsx at every year. Book period 1960-1989 remains "
                   "data_unavailable (anwarshaikhecon.org App 7.2 not in SalvagedInputs); no values fabricated."),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
