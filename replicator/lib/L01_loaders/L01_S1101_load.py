"""L01_S1101_load - load IMF IFS trade balance ratios (X/M) for 15 countries.

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix11_XMData.xlsx
(800-row long panel: Country, Year, X, M, X+M, X/M). Emits one parquet row per
(country, year) with X/M as the primary value. S1101-A..S1101-D are the four
focal countries highlighted by Shaikh in Fig 11.2 (US, UK, Germany, Japan).
S1101-E is China kept as a Phase 4 cd2_addition comparator (sourced from CD2's
S060-E; not present in Appendix11_XMData.xlsx so emitted only if a salvaged
CD2 file is available).

This loader does NOT call any API; the book-period panel is fully covered by
the salvaged workbook 1960-2009.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

SERIES_ID = "S1101"
CHOPPED_XLSX = book_data_path("Appendix11_XMData.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_IMF_IFS_XM.parquet"

# Mapping: subseries -> country label as it appears in the workbook
SUBSERIES_COUNTRIES = {
    "S1101-A": "United States",
    "S1101-B": "United Kingdom",
    "S1101-C": "Germany",
    "S1101-D": "Japan",
}
# Full 15-country basket per book Appendix 11.1
ALL_15 = [
    "Australia", "Belgium", "Canada", "Denmark", "Finland", "France",
    "Germany", "Italy", "Japan", "Korea, Republic of", "Netherlands",
    "Norway", "Spain", "Sweden", "United Kingdom", "United States",
]


def _load_chopped() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    # The workbook contains a stray 'Japan+A548' row; drop it.
    df = df[df["Country"].isin(ALL_15)].copy()
    return df


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}

    df = _load_chopped()

    rows = []
    # Emit the four focal-country subseries (Fig 11.2 highlights)
    for sub_id, country in SUBSERIES_COUNTRIES.items():
        sub = df[df["Country"] == country][["Year", "X/M (Trade Balance)"]].copy()
        for _, r in sub.iterrows():
            v = r["X/M (Trade Balance)"]
            if pd.isna(v):
                continue
            rows.append({
                "year": int(r["Year"]),
                "value": float(v),
                "subseries_id": sub_id,
                "subsource_id": "IMF_IFS_XM_APPENDIX_11_1",
                "units": "ratio_exports_over_imports",
                "country": country,
            })
    # Also emit the rest of the 15-country basket as labeled supplementary rows
    # so the chopped CSV preserves Shaikh's full panel. We assign subseries IDs
    # S1101-COUNTRY (uppercased ISO-ish slug) to each remaining country.
    other = [c for c in ALL_15 if c not in SUBSERIES_COUNTRIES.values()]
    for country in other:
        slug = country.replace(",", "").replace(" ", "_").upper()[:16]
        sub_id = f"S1101-{slug}"
        sub = df[df["Country"] == country][["Year", "X/M (Trade Balance)"]].copy()
        for _, r in sub.iterrows():
            v = r["X/M (Trade Balance)"]
            if pd.isna(v):
                continue
            rows.append({
                "year": int(r["Year"]),
                "value": float(v),
                "subseries_id": sub_id,
                "subsource_id": "IMF_IFS_XM_APPENDIX_11_1",
                "units": "ratio_exports_over_imports",
                "country": country,
            })

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"appendix11_xmdata": len(out)},
        "countries_loaded": sorted(out["country"].unique().tolist()),
        "sources_fetched": ["IMF_IFS_XM_APPENDIX_11_1"],
        "outputs": [str(OUT)],
        "notes": "S1101-E (China cd2_addition) not in salvaged workbook; deferred "
                 "to Phase 9 enrichment if/when CD2 S060-E is re-salvaged.",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
