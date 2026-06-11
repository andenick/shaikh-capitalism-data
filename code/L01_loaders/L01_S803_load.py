"""L01_S803_load — load Bain 1951 + Demsetz 1973b for Figs 8.3 and 8.4.

Three sources:
  - Appendix8_Bain42IndustryProfit.xlsx       (42-industry scatter for Fig 8.3)
  - Appendix8_Bain42IndustryAggregates.xlsx   (10-decile Bain ORIGINAL for Fig 8.4)
  - Appendix8_CorrectedBainData.xlsx          (10-decile Demsetz-CORRECTED for Fig 8.4)

Writes three parquets:
  Technical/data/raw/S803_BAIN_FIG83.parquet
  Technical/data/raw/S803_BAIN_FIG84_BAIN.parquet
  Technical/data/raw/S803_BAIN_FIG84_DEMSETZ.parquet
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

XLSX_FIG83 = book_data_path("Appendix8_Bain42IndustryProfit.xlsx")
XLSX_FIG84_BAIN = book_data_path("Appendix8_Bain42IndustryAggregates.xlsx")
XLSX_FIG84_DEMSETZ = book_data_path("Appendix8_CorrectedBainData.xlsx")

OUT_FIG83 = DATA_RAW / "S803_BAIN_FIG83.parquet"
OUT_FIG84_BAIN = DATA_RAW / "S803_BAIN_FIG84_BAIN.parquet"
OUT_FIG84_DEMSETZ = DATA_RAW / "S803_BAIN_FIG84_DEMSETZ.parquet"

YEAR_LABEL = 1938  # midpoint of 1936-40 averaging window


def _load_fig83() -> int:
    raw = pd.read_excel(XLSX_FIG83, sheet_name="Sheet1", header=None)
    # Layout (per dossier inspection):
    #   row 0: figure title
    #   row 1: industry names (42 cols, starting col 1)
    #   row 2: census numbers
    #   row 3: CR8 values
    #   row 4: 1936-40 ROE values
    industries = [str(c).strip() for c in raw.iloc[1, 1:].tolist()]
    census_nums = raw.iloc[2, 1:].tolist()
    cr8_vals = raw.iloc[3, 1:].tolist()
    roe_vals = raw.iloc[4, 1:].tolist()
    rows = []
    for ind, census, cr, roe in zip(industries, census_nums, cr8_vals, roe_vals):
        if pd.isna(cr) or pd.isna(roe):
            continue
        rows.extend([
            {"year": YEAR_LABEL, "value": float(cr), "subseries_id": "S803-FIG83",
             "source_id": "BAIN_1951_TABLE_I", "units": "percent",
             "industry": str(ind).strip(), "census_number": str(census),
             "axis": "CR8"},
            {"year": YEAR_LABEL, "value": float(roe), "subseries_id": "S803-FIG83",
             "source_id": "BAIN_1951_TABLE_I", "units": "percent",
             "industry": str(ind).strip(), "census_number": str(census),
             "axis": "ROE"},
        ])
    df = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT_FIG83, index=False)
    return len(df)


def _load_fig84_bain() -> int:
    raw = pd.read_excel(XLSX_FIG84_BAIN, sheet_name="Sheet1", header=None)
    # Layout: row 0 title, row 1 header, rows 2-11 data
    data = raw.iloc[2:12, :5].reset_index(drop=True)
    data.columns = ["decile_index", "cr_lower", "cr_upper", "n_industries", "mean_roe"]
    rows = []
    for _, r in data.iterrows():
        if pd.isna(r["mean_roe"]):
            continue
        idx = int(float(r["decile_index"]))
        rows.append({
            "year": YEAR_LABEL,
            "value": float(r["mean_roe"]),
            "subseries_id": "S803-FIG84-BAIN",
            "source_id": "BAIN_1951_TABLE_II",
            "units": "percent",
            "decile_index": idx,
            "cr_lower": float(r["cr_lower"]),
            "cr_upper": float(r["cr_upper"]),
            "n_industries": int(float(r["n_industries"])),
        })
    df = pd.DataFrame(rows)
    df.to_parquet(OUT_FIG84_BAIN, index=False)
    return len(df)


def _load_fig84_demsetz() -> int:
    raw = pd.read_excel(XLSX_FIG84_DEMSETZ, sheet_name="Sheet1", header=None)
    # Layout: row 0 title, row 1 header, rows 2-end alternating midpoints
    # Keep rows where col 1 (Profit Rate on Equity) is not NaN
    data = raw.iloc[2:, :2].reset_index(drop=True)
    data.columns = ["cr8_midpoint", "mean_roe"]
    data = data.dropna(subset=["mean_roe"]).reset_index(drop=True)
    rows = []
    for _, r in data.iterrows():
        rows.append({
            "year": YEAR_LABEL,
            "value": float(r["mean_roe"]),
            "subseries_id": "S803-FIG84-DEMSETZ",
            "source_id": "BAIN_DEMSETZ_CORRECTED_GROUPED",
            "units": "percent",
            "cr8_midpoint": int(float(r["cr8_midpoint"])),
        })
    df = pd.DataFrame(rows)
    df.to_parquet(OUT_FIG84_DEMSETZ, index=False)
    return len(df)


def run() -> dict:
    for p in (XLSX_FIG83, XLSX_FIG84_BAIN, XLSX_FIG84_DEMSETZ):
        if not p.exists():
            return {"status": "FAIL", "error": f"chopped table missing: {p}"}
    n83 = _load_fig83()
    n84b = _load_fig84_bain()
    n84d = _load_fig84_demsetz()
    return {
        "status": "OK",
        "rows_loaded": {"FIG83": n83, "FIG84_BAIN": n84b, "FIG84_DEMSETZ": n84d},
        "sources_fetched": ["BAIN_1951_TABLE_I", "BAIN_1951_TABLE_II",
                            "BAIN_DEMSETZ_CORRECTED_GROUPED"],
        "outputs": [str(OUT_FIG83), str(OUT_FIG84_BAIN), str(OUT_FIG84_DEMSETZ)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
