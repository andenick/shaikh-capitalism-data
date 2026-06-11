"""L01_S1006_load — Bond and Equity Returns, 1926-2010 + Damodaran extension.

Book period from Appendix10_Ibbotson.xlsx (Ibbotson SBBI 2004 + Stubbs 2004-2010
update). Modern extension from Damodaran NYU histretSP (substitutes the now-
commercial Morningstar SBBI per Phase 4 decision 0005). LT Corporate Bond
extension uses FRED AAA yield as a PROXY (Damodaran does not publish this
series); flagged proxy:true in registry with Concept Match Justification in EPR.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix10_Ibbotson.xlsx")
OUT_BOOK = DATA_RAW / "S1006_IBBOTSON_book.parquet"
OUT_DAM = DATA_RAW / "S1006_DAMODARAN_ext.parquet"
OUT_AAA = DATA_RAW / "S1006_FRED_AAA_ext.parquet"


def _load_ibbotson() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"Ibbotson missing: {CHOPPED_XLSX}"}
    ib = _load_ibbotson()
    # Three book subseries: Large Company Stocks, LT Corp, LT Gov
    rows = []
    for col, sub_id, ss_id in [
        ("Large Company Stocks", "S1006-A", "IBBOTSON_SBBI_rslarge"),
        ("Long-Term Corporate Bonds", "S1006-B", "IBBOTSON_SBBI_rbcorplt"),
        ("Long-Term Government Bonds", "S1006-C", "IBBOTSON_SBBI_rbgovlt"),
    ]:
        if col not in ib.columns:
            continue
        part = ib[["Year", col]].rename(columns={"Year": "year", col: "value"}).dropna(subset=["value"])
        part["units"] = "percent_total_return"
        part["subseries_id"] = sub_id
        part["subsource_id"] = ss_id
        rows.append(part)
    book = pd.concat(rows, ignore_index=True)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    book.to_parquet(OUT_BOOK, index=False)

    # Damodaran extension
    dam_ok = False
    dam_err = None
    n_dam = 0
    try:
        dam = S00_apis.damodaran_histret()
        # Keep years > 2010 and the three relevant columns
        ext_rows = []
        for src_col, sub_id, ss_id in [
            ("rslarge", "S1006-A-ext", "DAMODARAN_rslarge"),
            ("rbgovlt", "S1006-C-ext", "DAMODARAN_rbgovlt"),
            ("rbcorplt", "S1006-B-ext-damodaran", "DAMODARAN_rbcorplt_Baa"),
        ]:
            if src_col not in dam.columns:
                continue
            p = dam[["year", src_col]].rename(columns={src_col: "value"}).dropna(subset=["value"])
            p = p[p["year"] > 2010].copy()
            p["units"] = "percent_total_return"
            p["subseries_id"] = sub_id
            p["subsource_id"] = ss_id
            ext_rows.append(p)
        if ext_rows:
            ext = pd.concat(ext_rows, ignore_index=True)
            ext.to_parquet(OUT_DAM, index=False)
            n_dam = int(len(ext))
            dam_ok = True
    except S00_apis.ApiUnavailable as exc:
        dam_err = str(exc)

    # LT Corp extension: FRED AAA yield (PROXY)
    aaa_ok = False
    aaa_err = None
    n_aaa = 0
    try:
        raw = S00_apis.fred_csv_observations("AAA")
        raw["year"] = raw["date"].dt.year.astype(int)
        ann = raw.groupby("year", as_index=False)["value"].mean()
        ext = ann[ann["year"] > 2010].copy()
        ext["units"] = "percent_yield_proxy_for_total_return"
        ext["subseries_id"] = "S1006-B-ext"
        ext["subsource_id"] = "FRED_AAA_proxy_LTcorp"
        ext.to_parquet(OUT_AAA, index=False)
        n_aaa = int(len(ext))
        aaa_ok = True
    except S00_apis.ApiUnavailable as exc:
        aaa_err = str(exc)

    sources = ["IBBOTSON_book"]
    if dam_ok: sources.append("DAMODARAN")
    if aaa_ok: sources.append("FRED_AAA")

    return {
        "status": "OK",
        "rows_loaded": {"ibbotson_book": int(len(book)), "damodaran_ext": n_dam,
                        "fred_aaa_proxy": n_aaa},
        "sources_fetched": sources,
        "damodaran_status": "ok" if dam_ok else f"unavailable: {dam_err}",
        "fred_aaa_status": "ok" if aaa_ok else f"unavailable: {aaa_err}",
        "proxy_disclosure": {
            "S1006-B-ext": {
                "proxy": True,
                "justification": "Damodaran does not publish LT Corp total return; FRED AAA yield approximates running yield of duration-stable LT corp index. Omits capital-gain component from yield changes. See S1006_EPR.md.",
            }
        },
        "outputs": [str(OUT_BOOK)] +
                   ([str(OUT_DAM)] if dam_ok else []) +
                   ([str(OUT_AAA)] if aaa_ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
