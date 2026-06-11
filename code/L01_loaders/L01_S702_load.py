"""L01_S702_load — load Salter (1969) Table 33 / Reddaway Addendum (UK 1954-63) cross-section.

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix7_SalterULCPriceTable33.xlsx.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

SERIES_ID = "S702"
CHOPPED_XLSX = book_data_path("Appendix7_SalterULCPriceTable33.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_SALTER_T33_UK.parquet"


def _load_chopped() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    # The first column in this sheet is named "Industry (1958 S.I.C.) ranked according to increases in output"
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "Industry"})
    mask = df["Industry"].astype(str).str.match(r"^\s*\d+", na=False)
    df = df[mask].reset_index(drop=True)
    return df


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}

    df = _load_chopped()
    # UK table column names per inspection: 'Unit labour cost' and 'Net price' (or 'Gross price')
    # Per book caption (selling price ratio): use 'Net price' (selling price net of indirect tax) as the
    # primary y-axis; record both to allow downstream choice.
    rows = []
    for _, r in df.iterrows():
        ind = str(r["Industry"]).strip()
        ulc = pd.to_numeric(r.get("Unit labour cost"), errors="coerce")
        price_net = pd.to_numeric(r.get("Net price"), errors="coerce")
        if pd.notna(ulc):
            rows.append({
                "year": 1963,
                "value": float(ulc),
                "subseries_id": f"{SERIES_ID}-A-{ind}-ULC",
                "subsource_id": "SALTER_1969_TABLE33_UK",
                "units": "ratio_1963_over_1954_x100",
                "industry": ind,
                "axis": "unit_labour_cost",
            })
        if pd.notna(price_net):
            rows.append({
                "year": 1963,
                "value": float(price_net),
                "subseries_id": f"{SERIES_ID}-A-{ind}-PRICE",
                "subsource_id": "SALTER_1969_TABLE33_UK",
                "units": "ratio_1963_over_1954_x100",
                "industry": ind,
                "axis": "selling_price",
            })

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": {"salter_T33": len(out)},
        "industries": int(out["industry"].nunique()) if len(out) else 0,
        "sources_fetched": ["SALTER_1969_TABLE33_UK"],
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
