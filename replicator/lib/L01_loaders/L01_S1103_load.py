"""L01_S1103_load - load Shaikh's LOP-aggregate ratio (REER PPI / RULC_adj).

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix11_USJPNdata.xlsx
columns rxr1 and rxrrulcratio1 for Japan and the US (1960-2009). The S1103
construction is `formula` per Phase 4 ratification: S1103 = rxr1 /
rulcadjratio1rescaled. This loader records the book-truth `rxrrulcratio1`
column directly (no re-derivation) and also the rxr1 numerator and
rulcadjratio1rescaled denominator for the V03 cell-by-cell check.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

SERIES_ID = "S1103"
CHOPPED_XLSX = book_data_path("Appendix11_USJPNdata.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_LOP_RATIO.parquet"

SUBSERIES_COUNTRIES = {
    "S1103-A": "Japan",
    "S1103-B": "United States",
}


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}

    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})

    rows = []
    for sub_id, country in SUBSERIES_COUNTRIES.items():
        sub = df[df["Country"] == country][
            ["Year", "rxr1", "rulcadjratio1rescaled", "rxrrulcratio1"]
        ].copy()
        for _, r in sub.iterrows():
            v = r["rxrrulcratio1"]
            if pd.isna(v):
                continue
            rows.append({
                "year": int(r["Year"]),
                "value": float(v),
                "subseries_id": sub_id,
                "subsource_id": "BLS_ILC_LOP_RATIO_APPENDIX_11_1",
                "units": "ratio_dimensionless",
                "country": country,
                "rxr1": float(r["rxr1"]) if not pd.isna(r["rxr1"]) else None,
                "rulcadjratio1rescaled": (float(r["rulcadjratio1rescaled"])
                                          if not pd.isna(r["rulcadjratio1rescaled"]) else None),
            })

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_loaded": {"rxrrulcratio1": len(out)},
        "countries_loaded": sorted(out["country"].unique().tolist()),
        "sources_fetched": ["BLS_ILC_LOP_RATIO_APPENDIX_11_1"],
        "outputs": [str(OUT)],
        "extension_note": ("S1103 = rxr1 / rulcadjratio1rescaled is a formula "
                           "construction; per No-Lazy-Splices rule extension "
                           "requires re-computing both numerator (BIS PPI EER) "
                           "and denominator (OECD/Conference Board ULC). "
                           "Deferred to Phase 9 enrichment."),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
