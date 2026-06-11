"""L01_S1003_load — Relative Price of Finance, 1857-2011 (+ extension).

S1003 is a derived ratio; the loader's job is to ensure the source ratio
column (`ib/p`) is available for validation, and to ensure the S1002 raw
component inputs (iblong, USWPI, FRED AAA, FRED PPIACO) are loaded so the
P02 processor can recompute the ratio from extended components per the
No-Lazy-Splices-on-Derived-Quantities rule.

Per Anu rule: NEVER splice the published `ib/p` ratio; always recompute from
extended components. This loader delegates component fetching to L01_S1002
(reuses the same raw parquet files when they already exist).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix10_USLR.xlsx")
OUT_TRUTH = DATA_RAW / "S1003_USLR_ibp.parquet"            # book published ratio for validation
S1002_AAA = DATA_RAW / "S1002_FRED_AAA.parquet"
S1002_PPIACO = DATA_RAW / "S1002_FRED_PPIACO.parquet"
S1002_iblong = DATA_RAW / "S1002_USLR_iblong.parquet"
S1002_USWPI = DATA_RAW / "S1002_USLR_USWPI.parquet"


def _ensure_s1002_components() -> dict:
    """Ensure S1002 raw parquets exist; if not, fetch them now."""
    diag = {}
    if not (S1002_iblong.exists() and S1002_USWPI.exists()):
        from L01_loaders import L01_S1002_load as l01
        r = l01.run()
        diag["S1002_loader"] = r
    else:
        diag["S1002_loader"] = "already_present"

    # FRED components (optional — extension if available)
    if not S1002_AAA.exists():
        try:
            raw = S00_apis.fred_csv_observations("AAA")
            raw["year"] = raw["date"].dt.year.astype(int)
            ann = raw.groupby("year", as_index=False)["value"].mean()
            ann["units"] = "percent"; ann["subseries_id"] = "S1002-C"; ann["subsource_id"] = "FRED_AAA"
            ann.to_parquet(S1002_AAA, index=False)
            diag["AAA_status"] = "fetched_fresh"
        except S00_apis.ApiUnavailable as exc:
            diag["AAA_status"] = f"unavailable: {exc}"
    if not S1002_PPIACO.exists():
        try:
            raw = S00_apis.fred_csv_observations("PPIACO")
            raw["year"] = raw["date"].dt.year.astype(int)
            ann = raw.groupby("year", as_index=False)["value"].mean()
            ann["units"] = "index_native"; ann["subseries_id"] = "S1002-D"; ann["subsource_id"] = "FRED_PPIACO"
            ann.to_parquet(S1002_PPIACO, index=False)
            diag["PPIACO_status"] = "fetched_fresh"
        except S00_apis.ApiUnavailable as exc:
            diag["PPIACO_status"] = f"unavailable: {exc}"
    return diag


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"USLR missing: {CHOPPED_XLSX}"}
    # Save the book-published `ib/p` truth column for V03
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    sub = df[["Year", "ib/p"]].rename(columns={"Year": "year", "ib/p": "value"}).dropna(subset=["value"])
    sub["units"] = "ratio_1947=1"
    sub["subseries_id"] = "S1003-TRUTH"
    sub["subsource_id"] = "USLR_ibp"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(OUT_TRUTH, index=False)

    diag = _ensure_s1002_components()
    return {
        "status": "OK",
        "rows_loaded": {"USLR_ibp_truth": int(len(sub))},
        "sources_fetched": ["USLR_ibp", "S1002_components"],
        "component_status": diag,
        "outputs": [str(OUT_TRUTH)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
