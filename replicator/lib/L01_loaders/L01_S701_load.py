"""L01_S701_load — load Salter (1969) Table 28 (US 1923-50) cross-section.

Reads SalvagedInputs/book_data/ShaikhChoppedTables/Appendix7_SalterULCPriceTable28.xlsx
and writes one parquet per industry-axis pair: long form (industry, axis, value).

Per Phase 4 adequacy: file is verified present; underlying Salter data is fair-use academic.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

SERIES_ID = "S701"
CHOPPED_XLSX = book_data_path("Appendix7_SalterULCPriceTable28.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_SALTER_T28_US.parquet"


def _load_chopped() -> pd.DataFrame:
    """Parse Salter Table 28 (US 1923-50). Row 0 is descriptive title, row 1 is column names."""
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    # Drop trailing summary rows (Median / Upper quartile / Lower quartile)
    if "Industry" in df.columns:
        mask = df["Industry"].astype(str).str.match(r"^\s*\d+", na=False)
        df = df[mask].reset_index(drop=True)
    return df


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}

    df = _load_chopped()
    # Required cols: Industry, Unit labour cost (1923=100, 1950 value), Whole sale price (1923=100, 1950 value)
    rows = []
    for _, r in df.iterrows():
        ind = str(r["Industry"]).strip()
        ulc = pd.to_numeric(r.get("Unit labour cost"), errors="coerce")
        price = pd.to_numeric(r.get("Whole sale price"), errors="coerce")
        # Each industry is one observation; encode as two pseudo-rows so that
        # downstream tooling (chopped writer, validator) sees the data.
        # We use the field 'year' = base period code (1923 vs 1950 ratio = 1950)
        # and 'axis' embedded in subseries_id.
        if pd.notna(ulc):
            rows.append({
                "year": 1950,
                "value": float(ulc),
                "subseries_id": f"{SERIES_ID}-A-{ind}-ULC",
                "subsource_id": "SALTER_1969_TABLE28_US",
                "units": "ratio_1950_over_1923_x100",
                "industry": ind,
                "axis": "unit_labour_cost",
            })
        if pd.notna(price):
            rows.append({
                "year": 1950,
                "value": float(price),
                "subseries_id": f"{SERIES_ID}-A-{ind}-PRICE",
                "subsource_id": "SALTER_1969_TABLE28_US",
                "units": "ratio_1950_over_1923_x100",
                "industry": ind,
                "axis": "selling_price",
            })

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": {"salter_T28": len(out)},
        "industries": int(out["industry"].nunique()) if len(out) else 0,
        "sources_fetched": ["SALTER_1969_TABLE28_US"],
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
