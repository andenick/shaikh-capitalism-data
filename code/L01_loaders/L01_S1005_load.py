"""L01_S1005_load — Dividend Yield vs Bond Yield, 1871-2011 (+ extension).

Book: USLR columns `ys` (dividend yield), `ib10yr Gov` (10yr govt), plus
inherits the corporate composite from S1002-A.

Extension: Shiller ie_data.xls (annual avg of monthly D/P) + FRED GS10 + FRED
AAA (corporate yield via S1002).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix10_USLR.xlsx")
OUT_DIV_BOOK = DATA_RAW / "S1005_USLR_ys.parquet"
OUT_GOV_BOOK = DATA_RAW / "S1005_USLR_ib10yr.parquet"
OUT_DIV_EXT = DATA_RAW / "S1005_SHILLER_div_ext.parquet"
OUT_GOV_EXT = DATA_RAW / "S1005_FRED_GS10.parquet"


def _load_uslr() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def _save_book(df: pd.DataFrame, col: str, out: Path, subseries_id: str,
               subsource_id: str) -> int:
    sub = df[["Year", col]].rename(columns={"Year": "year", col: "value"}).dropna(subset=["value"])
    sub["units"] = "percent"
    sub["subseries_id"] = subseries_id
    sub["subsource_id"] = subsource_id
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(out, index=False)
    return int(len(sub))


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"USLR missing: {CHOPPED_XLSX}"}
    uslr = _load_uslr()
    n_div = _save_book(uslr, "ys", OUT_DIV_BOOK, "S1005-A", "USLR_ys")
    n_gov = _save_book(uslr, "ib10yr Gov", OUT_GOV_BOOK, "S1005-B", "USLR_ib10yr")

    # Extension via Shiller
    shiller_ok = False
    shiller_err = None
    n_shi = 0
    try:
        ann = S00_apis.shiller_annual()
        # dividend yield = D/P * 100
        if "P" in ann.columns and "D" in ann.columns:
            div = ann[["year", "P", "D"]].dropna(subset=["P", "D"]).copy()
            div["value"] = 100.0 * div["D"] / div["P"]
            ext = div[div["year"] > 2011][["year", "value"]].copy()
            ext["units"] = "percent"
            ext["subseries_id"] = "S1005-A-ext"
            ext["subsource_id"] = "SHILLER_ie_data"
            ext.to_parquet(OUT_DIV_EXT, index=False)
            n_shi = int(len(ext))
            shiller_ok = True
    except S00_apis.ApiUnavailable as exc:
        shiller_err = str(exc)

    # FRED GS10 extension
    gs10_ok = False
    gs10_err = None
    n_gs10 = 0
    try:
        raw = S00_apis.fred_csv_observations("GS10")
        raw["year"] = raw["date"].dt.year.astype(int)
        ann = raw.groupby("year", as_index=False)["value"].mean()
        ext = ann[ann["year"] > 2011].copy()
        ext["units"] = "percent"
        ext["subseries_id"] = "S1005-B-ext"
        ext["subsource_id"] = "FRED_GS10"
        ext.to_parquet(OUT_GOV_EXT, index=False)
        n_gs10 = int(len(ext))
        gs10_ok = True
    except S00_apis.ApiUnavailable as exc:
        gs10_err = str(exc)

    sources = ["USLR_ys", "USLR_ib10yr"]
    if shiller_ok: sources.append("SHILLER_ie_data")
    if gs10_ok:    sources.append("FRED_GS10")

    return {
        "status": "OK",
        "rows_loaded": {"div_book": n_div, "gov_book": n_gov,
                        "shiller_ext": n_shi, "gs10_ext": n_gs10},
        "sources_fetched": sources,
        "shiller_status": "ok" if shiller_ok else f"unavailable: {shiller_err}",
        "fred_status": "ok" if gs10_ok else f"unavailable: {gs10_err}",
        "outputs": [str(OUT_DIV_BOOK), str(OUT_GOV_BOOK)] +
                   ([str(OUT_DIV_EXT)] if shiller_ok else []) +
                   ([str(OUT_GOV_EXT)] if gs10_ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
