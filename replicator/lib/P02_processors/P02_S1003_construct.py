"""P02_S1003_construct — Relative Price of Finance.

Formula series: S1003[t] = (iblong[t]/iblong[1947]) / (USWPI[t]/USWPI[1947]).
Extension recomputed from extended S1002 components (No-Lazy-Splices rule).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_IBLONG = DATA_RAW / "S1002_USLR_iblong.parquet"
IN_USWPI = DATA_RAW / "S1002_USLR_USWPI.parquet"
IN_AAA = DATA_RAW / "S1002_FRED_AAA.parquet"
IN_PPIACO = DATA_RAW / "S1002_FRED_PPIACO.parquet"
OUT = DATA_PROCESSED / "S1003.parquet"

BASE_YEAR = 1947
ANCHOR_YEAR = 2011


def run() -> dict:
    if not (IN_IBLONG.exists() and IN_USWPI.exists()):
        return {"status": "FAIL", "error": "S1002 book components missing",
                "missing": [str(p) for p in (IN_IBLONG, IN_USWPI) if not p.exists()]}
    iblong = pd.read_parquet(IN_IBLONG)[["year", "value"]].rename(columns={"value": "i"})
    uswpi = pd.read_parquet(IN_USWPI)[["year", "value"]].rename(columns={"value": "p"})
    book = iblong.merge(uswpi, on="year", how="outer").sort_values("year")
    i_1947 = float(book.loc[book["year"] == BASE_YEAR, "i"].iloc[0])
    p_1947 = float(book.loc[book["year"] == BASE_YEAR, "p"].iloc[0])
    book["value"] = (book["i"] / i_1947) / (book["p"] / p_1947)
    book = book.dropna(subset=["value"])
    book_part = book[["year", "value"]].copy()
    book_part["subseries_id"] = "S1003-A"
    book_part["source_id"] = "S1002_components_book"
    book_part["units"] = "ratio_1947=1"

    parts = [book_part]
    diag: dict = {"extension_status": "book_only", "base_year": BASE_YEAR,
                  "i_1947": i_1947, "p_1947": p_1947}

    if IN_AAA.exists() and IN_PPIACO.exists():
        aaa = pd.read_parquet(IN_AAA)[["year", "value"]].rename(columns={"value": "i"})
        ppiaco = pd.read_parquet(IN_PPIACO)[["year", "value"]].rename(columns={"value": "p_raw"})
        try:
            uswpi_2011 = float(uswpi.loc[uswpi["year"] == ANCHOR_YEAR, "p"].iloc[0])
            ppiaco_2011 = float(ppiaco.loc[ppiaco["year"] == ANCHOR_YEAR, "p_raw"].iloc[0])
            scale = uswpi_2011 / ppiaco_2011
            ext = aaa.merge(ppiaco, on="year", how="inner").sort_values("year")
            ext["p"] = ext["p_raw"] * scale
            ext = ext[ext["year"] > ANCHOR_YEAR].copy()
            ext["value"] = (ext["i"] / i_1947) / (ext["p"] / p_1947)
            ext = ext.dropna(subset=["value"])
            ext_part = ext[["year", "value"]].copy()
            ext_part["subseries_id"] = "S1003-B"
            ext_part["source_id"] = "S1002_components_extended"
            ext_part["units"] = "ratio_1947=1"
            parts.append(ext_part)
            diag["extension_status"] = "ok"
            diag["ext_years"] = int(len(ext_part))
            diag["ppiaco_scale_factor"] = scale
        except Exception as exc:
            diag["extension_error"] = str(exc)

    df = pd.concat(parts, ignore_index=True).sort_values(["year", "subseries_id"]).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": diag,
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
