"""L01_S1002_load — Interest Rate (iblong) + Price Level (USWPI), 1857-2011.

Book inputs:
  USLR['iblong']  -> S1002-A (composite long bond yield, percent)
  USLR['USWPI']   -> S1002-B (composite PPI, index 1947=100)

Extension via FRED fredgraph.csv (no API key required):
  AAA      -> S1002-C (2012+ corp yield)
  PPIACO   -> S1002-D (2012+ PPI, reindexed to USWPI[2011] anchor)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix10_USLR.xlsx")
OUT_A = DATA_RAW / "S1002_USLR_iblong.parquet"
OUT_B = DATA_RAW / "S1002_USLR_USWPI.parquet"
OUT_C = DATA_RAW / "S1002_FRED_AAA.parquet"
OUT_D = DATA_RAW / "S1002_FRED_PPIACO.parquet"


def _load_uslr() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def _save_book(df: pd.DataFrame, col: str, out: Path, subseries_id: str,
               subsource_id: str, units: str) -> int:
    sub = df[["Year", col]].rename(columns={"Year": "year", col: "value"}).dropna(subset=["value"])
    sub["units"] = units
    sub["subseries_id"] = subseries_id
    sub["subsource_id"] = subsource_id
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(out, index=False)
    return int(len(sub))


def _save_fred_annual(series_id: str, out: Path, subseries_id: str,
                      subsource_id: str, units: str) -> tuple[int, bool, str | None]:
    try:
        raw = S00_apis.fred_csv_observations(series_id)
    except S00_apis.ApiUnavailable as exc:
        return 0, False, str(exc)
    raw = raw.copy()
    raw["year"] = raw["date"].dt.year.astype(int)
    annual = raw.groupby("year", as_index=False)["value"].mean()
    annual["units"] = units
    annual["subseries_id"] = subseries_id
    annual["subsource_id"] = subsource_id
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    annual.to_parquet(out, index=False)
    return int(len(annual)), True, None


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"USLR missing: {CHOPPED_XLSX}"}
    uslr = _load_uslr()
    n_a = _save_book(uslr, "iblong", OUT_A, "S1002-A", "USLR_iblong", "percent")
    n_b = _save_book(uslr, "USWPI", OUT_B, "S1002-B", "USLR_USWPI", "index_1947=100")

    n_c, ok_c, err_c = _save_fred_annual("AAA", OUT_C, "S1002-C", "FRED_AAA", "percent")
    n_d, ok_d, err_d = _save_fred_annual("PPIACO", OUT_D, "S1002-D", "FRED_PPIACO", "index_native")

    sources = ["USLR_iblong", "USLR_USWPI"]
    if ok_c:
        sources.append("FRED_AAA")
    if ok_d:
        sources.append("FRED_PPIACO")

    return {
        "status": "OK",
        "rows_loaded": {"iblong": n_a, "USWPI": n_b, "AAA": n_c, "PPIACO": n_d},
        "sources_fetched": sources,
        "fred_status": "ok" if (ok_c and ok_d) else "partial" if (ok_c or ok_d) else "skipped",
        "fred_errors": {"AAA": err_c, "PPIACO": err_d},
        "outputs": [str(p) for p, ok in [(OUT_A, True), (OUT_B, True), (OUT_C, ok_c), (OUT_D, ok_d)] if ok],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
