"""L01_S1505_load - load S1505 (Phillips-curve composite variables) book period.

Reads Appendix15_USInflation.xlsx for pi/sigma/sigma'/uL/uLintensity book values.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix15_USInflation.xlsx")
OUT = DATA_RAW / "S1505_USINFLATION_CHOPPED.parquet"

# Map: (chopped col short code) -> (S1505 subseries id, units)
SUB_DEFS = [
    # Note: book column "π" (pi) appears twice with different content (rate vs first vs explicit pi col 26)
    # We use col index 3 (first occurrence) which is the published inflation rate.
    ("pi_col_3", "S1505-pi", "rate_decimal"),
    ("sigma", "S1505-sigma", "rate_decimal"),
    ("sigma_prime", "S1505-sigma-prime", "rate_decimal"),
    ("uL", "S1505-uL", "rate_decimal"),
    ("uLintensity", "S1505-uLintensity", "rate_decimal"),
]


def _load_long() -> pd.DataFrame:
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Sheet1", header=[0, 1])
    # Header row 1 has short codes; sometimes duplicates (pi appears twice).
    # Use positional indexing to disambiguate.
    headers = [str(c[1]).strip() for c in raw.columns]
    # Find columns positionally
    # Per inspection: [0]=Year, [1]=GDP, [2]=pgdp, [3]=π (inflation rate),
    # [8]=σ (sigma), [14]=uL, [15]=uLintensity, [22]=σ' (sigma_prime), [23]=π'
    col_pi = raw.columns[3]
    col_sigma = raw.columns[8]
    col_sigma_prime = raw.columns[22]
    col_uL = raw.columns[14]
    col_uLint = raw.columns[15]
    col_year = raw.columns[0]
    df = pd.DataFrame({
        "year": pd.to_numeric(raw[col_year], errors="coerce"),
        "pi": pd.to_numeric(raw[col_pi], errors="coerce"),
        "sigma": pd.to_numeric(raw[col_sigma], errors="coerce"),
        "sigma_prime": pd.to_numeric(raw[col_sigma_prime], errors="coerce"),
        "uL": pd.to_numeric(raw[col_uL], errors="coerce"),
        "uLintensity": pd.to_numeric(raw[col_uLint], errors="coerce"),
    }).dropna(subset=["year"]).astype({"year": int})

    # Apply column name "pi_col_3" alias
    df = df.rename(columns={"pi": "pi_col_3"})

    rows = []
    for col, sub_id, unit in SUB_DEFS:
        sub = df[["year", col]].rename(columns={col: "value"}).dropna(subset=["value"])
        sub["subseries_id"] = sub_id
        sub["source_id"] = "SHAIKH_2016_APPENDIX_15_1"
        sub["units"] = unit
        rows.append(sub[["year", "value", "subseries_id", "source_id", "units"]])
    return pd.concat(rows, ignore_index=True)


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}
    long_df = _load_long()
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    long_df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": int(len(long_df)),
        "subseries": sorted(long_df["subseries_id"].unique().tolist()),
        "year_range": [int(long_df["year"].min()), int(long_df["year"].max())],
        "sources_fetched": ["SHAIKH_2016_APPENDIX_15_1"],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
