"""Shared validator helpers for Chapter 14.

Provides a generic ``validate_against_appendix14`` helper used by V03_S1401
through V03_S1408. Each validator compares the processed parquet against a
specified set of Appendix-14.3 columns mapped to subseries_ids and emits a
PASS/FAIL row to VALIDATION_REPORT.json.
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

CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix14_InflationULdata.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"


def load_appendix14() -> pd.DataFrame:
    raw = pd.read_excel(CHOPPED_XLSX)
    df = raw.iloc[1:].reset_index(drop=True)
    df = df.rename(columns={"Unnamed: 0": "year"})
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year"]).reset_index(drop=True)
    df.columns = [str(c).strip() for c in df.columns]
    for col in df.columns:
        if col == "year":
            continue
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # Strict book-period clip (matches loader)
    df = df[df["year"] <= 2011].reset_index(drop=True)
    return df


def update_report(sid: str, row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[sid] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def validate_against_appendix14(
    sid: str,
    subseries_to_appendix_col: dict[str, str],
    overlap_range: tuple[int, int] = (1948, 2011),
    tol_pct: float = 1.0,
    abs_tol: float = 1e-6,
) -> dict:
    """Generic Appendix-14.3 comparator.

    Parameters
    ----------
    sid                       : series id (for reporting)
    subseries_to_appendix_col : {subseries_id: appendix_column_name}
    overlap_range             : (start_year, end_year) inclusive
    tol_pct                   : percent tolerance per cell (default 1%)
    abs_tol                   : absolute floor for very-small expected values
                                (avoids div-by-near-zero when expected is ~0;
                                cells with |expected| < abs_tol are scored on
                                |actual - expected| < abs_tol)
    """
    proc = DATA_PROCESSED / f"{sid}.parquet"
    if not proc.exists():
        row = {"status": "FAIL", "error": f"processed missing: {proc}"}
        update_report(sid, row)
        return row
    if not CHOPPED_XLSX.exists():
        row = {"status": "FAIL", "error": f"book truth missing: {CHOPPED_XLSX}"}
        update_report(sid, row)
        return row

    actual = pd.read_parquet(proc)
    truth = load_appendix14()

    all_div: list[dict] = []
    n_total = 0
    abs_errs: list[float] = []
    pct_errs: list[float] = []

    for subseries_id, appx_col in subseries_to_appendix_col.items():
        a = actual[actual["subseries_id"] == subseries_id][["year", "value"]].rename(
            columns={"value": "actual"})
        if appx_col not in truth.columns:
            continue
        t = truth[["year", appx_col]].rename(columns={appx_col: "expected"}).dropna(subset=["expected"])
        m = a.merge(t, on="year", how="inner")
        m = m[(m["year"] >= overlap_range[0]) & (m["year"] <= overlap_range[1])]
        if m.empty:
            continue
        m["actual"] = pd.to_numeric(m["actual"], errors="coerce")
        m["expected"] = pd.to_numeric(m["expected"], errors="coerce")
        m = m.dropna(subset=["actual", "expected"])
        m["abs_err"] = (m["actual"] - m["expected"]).abs()
        # For near-zero expected, score by abs_tol; otherwise by pct
        small = m["expected"].abs() < abs_tol
        m["pct_err"] = 0.0
        m.loc[~small, "pct_err"] = (
            m.loc[~small, "abs_err"] / m.loc[~small, "expected"].abs() * 100.0
        )
        # Divergence: pct > tol OR (small AND abs_err > abs_tol)
        div_mask = (m["pct_err"] > tol_pct) | (small & (m["abs_err"] > abs_tol))
        div = m[div_mask][["year", "actual", "expected", "abs_err", "pct_err"]]
        if not div.empty:
            for _, r in div.iterrows():
                all_div.append({
                    "subseries_id": subseries_id,
                    "year": int(r["year"]),
                    "actual": float(r["actual"]),
                    "expected": float(r["expected"]),
                    "abs_err": float(r["abs_err"]),
                    "pct_err": float(r["pct_err"]),
                })
        n_total += int(len(m))
        abs_errs.extend(m["abs_err"].tolist())
        pct_errs.extend(m["pct_err"].tolist())

    if n_total == 0:
        row = {"status": "FAIL", "error": "no overlap rows compared",
               "subseries_to_appendix_col": subseries_to_appendix_col}
        update_report(sid, row)
        return row

    mae = float(sum(abs_errs) / len(abs_errs))
    max_abs = float(max(abs_errs))
    max_pct = float(max(pct_errs))
    status = "PASS" if not all_div else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": tol_pct,
        "abs_tol_floor": abs_tol,
        "compare_range": list(overlap_range),
        "subseries_to_appendix_col": subseries_to_appendix_col,
        "n_compared": n_total,
        "mae": round(mae, 8),
        "max_abs_err": round(max_abs, 8),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": len(all_div),
        "divergence_years": sorted(list({d["year"] for d in all_div})),
        "divergences_sample": all_div[:10],
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    update_report(sid, row)
    return row
