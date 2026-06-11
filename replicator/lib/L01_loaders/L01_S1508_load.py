"""L01_S1508_load - load Harberger (1988) 29-country cross-section.

Reads Appendix15_WorldInflationDataLambda.xlsx sheet HarbergerTable12.
Also documents modern IMF SDMX equivalents via _imf_ifs_resolver for audit.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from loaders._imf_ifs_resolver import describe_ifs_line, resolve_ifs_line  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix15_WorldInflationDataLambda.xlsx")
OUT = DATA_RAW / "S1508_HARBERGER_29_COUNTRIES.parquet"


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="HarbergerTable12", header=1)
    raw.columns = [str(c).strip() for c in raw.columns]
    # Two columns: lambda = gDC, Inflation. No country names in this xlsx.
    # Use the row index (0-28) as the index identifier.
    raw = raw.dropna(how="all").reset_index(drop=True)
    rows = []
    for i, r in raw.iterrows():
        lam = float(r.iloc[0])
        pi = float(r.iloc[1])
        # Use synthetic country-index "C01..C29" as observation key
        country_key = f"H{i+1:02d}"
        rows.append({"year": 1988, "value": lam, "subseries_id": "S1508-lambda",
                     "source_id": "HARBERGER_1988_TABLE_12_11", "units": "rate_percent",
                     "country_key": country_key})
        rows.append({"year": 1988, "value": pi, "subseries_id": "S1508-pi",
                     "source_id": "HARBERGER_1988_TABLE_12_11", "units": "rate_percent",
                     "country_key": country_key})
    df = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)

    # Audit: document modern IFS equivalents
    line_32 = describe_ifs_line(32)
    line_64 = describe_ifs_line(64)
    audit = {
        "shaikh_legacy_line_32": {"modern_code": resolve_ifs_line(32),
                                  "modern_concept": line_32["modern_concept"],
                                  "api_dataflow": line_32["api_dataflow"]},
        "shaikh_legacy_line_64": {"modern_code": resolve_ifs_line(64),
                                  "modern_concept": line_64["modern_concept"],
                                  "api_dataflow": line_64["api_dataflow"]},
    }

    return {
        "status": "OK",
        "rows_loaded": int(len(df)),
        "country_keys": sorted(df["country_key"].unique().tolist()),
        "n_countries": int(df["country_key"].nunique()),
        "sources_fetched": ["HARBERGER_1988_TABLE_12_11"],
        "imf_resolver_audit": audit,
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
