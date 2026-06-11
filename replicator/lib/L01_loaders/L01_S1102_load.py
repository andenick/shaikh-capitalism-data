"""L01_S1102_load - load Shaikh's REER (PPI-basis) for US and Japan.

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix11_USJPNdata.xlsx
(100-row long panel: Country, Year, rxr1, rulcadjratio1, rulcadjratio1rescaled,
rxrrulcratio1, intratediff1, realintratediff1). Emits S1102-A (Japan) and
S1102-B (US) for the book period 1960-2009.

Extension classification: BLS International Labor Comparisons program
discontinued 2013. Per Phase 4 Adequacy (CH11), the canonical post-2013
substitute is the BIS PPI-based EER broad index. The BIS series requires
SDMX or workbook download from bis.org/statistics/eer.htm; that fetch is not
included in this loader since it requires a credentialled session. The loader
records `bis_extension_status: not_attempted_v1` so the processor degrades
cleanly. EPR documents the Concept Match Justification.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

SERIES_ID = "S1102"
CHOPPED_XLSX = book_data_path("Appendix11_USJPNdata.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_BLS_REER_PPI.parquet"

SUBSERIES_COUNTRIES = {
    "S1102-A": "Japan",
    "S1102-B": "United States",
}


def _load_chopped() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}

    df = _load_chopped()

    rows = []
    for sub_id, country in SUBSERIES_COUNTRIES.items():
        sub = df[df["Country"] == country][["Year", "rxr1"]].copy()
        for _, r in sub.iterrows():
            v = r["rxr1"]
            if pd.isna(v):
                continue
            rows.append({
                "year": int(r["Year"]),
                "value": float(v),
                "subseries_id": sub_id,
                "subsource_id": "BLS_ILC_REER_PPI_APPENDIX_11_1",
                "units": "index_2002=100",
                "country": country,
            })

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"rxr1": len(out)},
        "countries_loaded": sorted(out["country"].unique().tolist()),
        "sources_fetched": ["BLS_ILC_REER_PPI_APPENDIX_11_1"],
        "outputs": [str(OUT)],
        "bis_extension_status": "not_attempted_v1",
        "bis_extension_note": ("BIS PPI EER broad-index extension is the "
                               "canonical post-2013 substitute (CH11 Adequacy). "
                               "Implementation deferred to a follow-up loader."),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
