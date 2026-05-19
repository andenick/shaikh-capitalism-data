"""L01_S1504_load - load S1504 (Growth of Nominal GDP and Relative New Purchasing Power).

Composite source:
  - Book period (1948-2010): Appendix15_USInflation.xlsx columns GDP, pGDP, CR, CA, gGDP, gCR, pp
  - Extension (2011+): attempts IMF MFS_DC DCORP_N_DC USA via _imf_ifs_resolver
    + BEA NIPA API (if BEA_API_KEY present) for GDP and CA

Writes to Technical/data/raw/:
  - S1504_USINFLATION_CHOPPED.parquet   (book-period authoritative values, long form)
  - S1504_IMF_IFS_DCORP_N_DC.parquet    (extension CR via IMF SDMX, when available)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from loaders._imf_ifs_resolver import (  # noqa: E402
    describe_ifs_line, fetch_ifs_series, resolve_ifs_line,
)

CHOPPED_XLSX = book_data_path("Appendix15_USInflation.xlsx")
OUT_CHOPPED = DATA_RAW / "S1504_USINFLATION_CHOPPED.parquet"
OUT_IMF = DATA_RAW / "S1504_IMF_IFS_DCORP_N_DC.parquet"

SHAIKH_LEGACY_LINE_CR = 32   # Total Domestic Claims aggregate
COUNTRY = "USA"
EXT_START = 2001  # IMF MFS_DC USA coverage begins here
EXT_END = 2025


def _load_chopped() -> pd.DataFrame:
    """Read the multi-header Appendix15_USInflation table and return long-form raw."""
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=[0, 1])
    # Drop the first header level (descriptive) - keep short codes
    raw.columns = [str(c[1]).strip() for c in raw.columns]
    raw = raw.dropna(subset=["Year"])
    raw["Year"] = pd.to_numeric(raw["Year"], errors="coerce")
    raw = raw.dropna(subset=["Year"]).astype({"Year": int})
    raw = raw.rename(columns={"Year": "year"})
    return raw


def _save_chopped() -> tuple[int, list[str]]:
    raw = _load_chopped()
    # Select the columns we publish as S1504 subseries
    cols_to_emit = {
        "GDP": ("S1504-GDP", "usd_billions"),
        "pgdp": ("S1504-pGDP", "index_2005=100"),
        "CR": ("S1504-CR", "usd_billions"),
        "CA": ("S1504-CA", "usd_billions"),
        "gGDP": ("S1504-gGDP", "rate_decimal"),
        "gCR": ("S1504-gCR", "rate_decimal"),
        "pp": ("S1504-pp", "rate_decimal"),
    }
    long_rows = []
    cols_seen = []
    for col, (sub_id, unit) in cols_to_emit.items():
        if col not in raw.columns:
            continue
        cols_seen.append(col)
        slice_df = raw[["year", col]].rename(columns={col: "value"}).dropna(subset=["value"])
        slice_df["subseries_id"] = sub_id
        slice_df["source_id"] = "SHAIKH_2016_APPENDIX_15_1"
        slice_df["units"] = unit
        long_rows.append(slice_df[["year", "value", "subseries_id", "source_id", "units"]])
    long_df = pd.concat(long_rows, ignore_index=True)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    long_df.to_parquet(OUT_CHOPPED, index=False)
    return len(long_df), cols_seen


def _fetch_imf_modern_cr() -> tuple[int, bool, str | None, dict]:
    """Fetch modern DCS Domestic Claims (Net) for USA via IMF SDMX 3.0."""
    try:
        modern_code = resolve_ifs_line(SHAIKH_LEGACY_LINE_CR)
        meta = describe_ifs_line(SHAIKH_LEGACY_LINE_CR)
    except KeyError as exc:
        return 0, False, f"resolver KeyError: {exc}", {}
    fr = fetch_ifs_series(
        indicator=modern_code,
        country=COUNTRY,
        start=EXT_START,
        end=EXT_END,
        dataflow=meta.get("api_dataflow", "MFS_DC"),
        frequency="A",
        unit="USD",
    )
    diag = {
        "indicator": modern_code,
        "country": COUNTRY,
        "year_window": [EXT_START, EXT_END],
        "http_status": fr.http_status,
        "source_url": fr.source_url,
        "shaikh_legacy_line": SHAIKH_LEGACY_LINE_CR,
        "modern_concept": meta.get("modern_concept"),
        "error": fr.error,
    }
    if not fr.success:
        return 0, False, fr.error, diag
    rows = [
        {"year": int(y), "value": float(v), "subseries_id": "S1504-CR-modern",
         "source_id": "IMF_MFS_DC_DCORP_N_DC", "units": "usd"}
        for y, v in sorted(fr.values.items())
    ]
    df = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT_IMF, index=False)
    diag["n_obs"] = len(rows)
    diag["years"] = [r["year"] for r in rows]
    return len(rows), True, None, diag


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}
    n_chopped, cols_seen = _save_chopped()
    n_imf, imf_ok, imf_err, imf_diag = _fetch_imf_modern_cr()
    sources = ["SHAIKH_2016_APPENDIX_15_1"]
    if imf_ok:
        sources.append("IMF_MFS_DC_DCORP_N_DC")
    return {
        "status": "OK",
        "rows_loaded": {"chopped_book": n_chopped, "imf_modern_cr": n_imf},
        "sources_fetched": sources,
        "imf_status": "ok" if imf_ok else "unavailable",
        "imf_error": imf_err,
        "imf_diagnostics": imf_diag,
        "chopped_columns_seen": cols_seen,
        "outputs": [str(OUT_CHOPPED)] + ([str(OUT_IMF)] if imf_ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
