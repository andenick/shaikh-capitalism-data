"""L01_S201_load — fetch raw inputs for S201 (US Industrial Production).

Fetches three inputs:
  - BEA LTEG A173 from the salvaged chopped table (column IndProdHS_BEA)
    written to Technical/data/raw/S201_BEA_LTEG_A173.parquet
  - FRB G.17 book-period values from the same chopped table (column IndProd_FRB)
    written to Technical/data/raw/S201_FRB_G17_BOOK.parquet
  - FRED INDPRO (2010-2025) via API, annual avg
    written to Technical/data/raw/S201_FRED_INDPRO.parquet

If FRED_API_KEY is missing or FRED is unavailable, that input is skipped and
the loader returns status=degraded with `fred_skipped: true`. The processor
will then publish S201 over the book period only.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# Ensure code/ is importable when invoked directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from S00_setup import S00_apis, S00_config  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix2_IndustrialProduction.xlsx")
OUT_BEA = DATA_RAW / "S201_BEA_LTEG_A173.parquet"
OUT_FRB = DATA_RAW / "S201_FRB_G17_BOOK.parquet"
OUT_FRED = DATA_RAW / "S201_FRED_INDPRO.parquet"
FRED_SERIES_ID = "INDPRO"


def _load_chopped() -> pd.DataFrame:
    """Parse the salvaged chopped table; row 0 is the long descriptive header,
    row 1 holds the short column names. Returns a clean DataFrame indexed by year."""
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def _save_bea(chopped: pd.DataFrame) -> int:
    bea = chopped[["Year", "IndProdHS_BEA"]].rename(
        columns={"IndProdHS_BEA": "value"}
    ).dropna(subset=["value"])
    bea = bea.rename(columns={"Year": "year"})
    bea["units"] = "index_1913=100"
    bea["subseries_id"] = "S201-A"
    bea["subsource_id"] = "BEA_LTEG_1966"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    bea.to_parquet(OUT_BEA, index=False)
    return len(bea)


def _save_frb_book(chopped: pd.DataFrame) -> int:
    frb = chopped[["Year", "IndProd_FRB"]].rename(
        columns={"IndProd_FRB": "value"}
    ).dropna(subset=["value"])
    frb = frb.rename(columns={"Year": "year"})
    frb["units"] = "index_2007=100"   # native unit when Shaikh retrieved (~2011)
    frb["subseries_id"] = "S201-B"
    frb["subsource_id"] = "FRB_G17_INDPRO"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    frb.to_parquet(OUT_FRB, index=False)
    return len(frb)


def _save_fred() -> tuple[int, bool, str | None]:
    """Returns (rows, fetched, error_message)."""
    if not S00_config.have_key("FRED_API_KEY"):
        return 0, False, "FRED_API_KEY not set"
    try:
        # Pull from 2005 onward — provides overlap candidates back to 2005 if 2010 NaN
        df = S00_apis.fred_observations(
            series_id=FRED_SERIES_ID,
            frequency="a",
            aggregation_method="avg",
            observation_start="2005-01-01",
            observation_end="2025-12-31",
        )
    except S00_apis.ApiUnavailable as exc:
        return 0, False, str(exc)
    # Normalize to (year, value, units, subseries_id)
    df = df.copy()
    df["year"] = df["date"].dt.year.astype(int)
    df = df[["year", "value"]]
    df["units"] = "index_2017=100"  # current FRED base; processor reindexes
    df["subseries_id"] = "S201-C"
    df["subsource_id"] = "FRED_INDPRO"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT_FRED, index=False)
    return len(df), True, None


def run() -> dict:
    """Phase entry point invoked by run.py."""
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}

    chopped = _load_chopped()

    n_bea = _save_bea(chopped)
    n_frb = _save_frb_book(chopped)
    n_fred, fred_ok, fred_err = _save_fred()

    sources = ["BEA_LTEG_1966", "FRB_G17_INDPRO"]
    if fred_ok:
        sources.append("FRED_INDPRO")

    result = {
        "status": "OK",
        "rows_loaded": {"BEA": n_bea, "FRB_book": n_frb, "FRED": n_fred},
        "sources_fetched": sources,
        "fred_status": "ok" if fred_ok else "skipped",
        "fred_error": fred_err,
        "outputs": [str(OUT_BEA), str(OUT_FRB)] + ([str(OUT_FRED)] if fred_ok else []),
    }
    return result


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
