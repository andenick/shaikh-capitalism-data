"""L01_S1509_load - load Ramamurthy (2014) 38-country (46-episode) panel."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from loaders._imf_ifs_resolver import describe_ifs_line, resolve_ifs_line  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix15_WorldInflationDataByCountry.xlsx")
OUT = DATA_RAW / "S1509_RAMAMURTHY_PANEL.parquet"


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Ramamurthy2013", header=1)
    raw.columns = [str(c).strip() for c in raw.columns]
    # Expected: Index, lambda, pi, inflation period, credit period, episode, country
    # Pick by position to avoid Unicode column-name issues
    df = pd.DataFrame({
        "row_index": pd.to_numeric(raw.iloc[:, 0], errors="coerce"),
        "lambda_gDC": pd.to_numeric(raw.iloc[:, 1], errors="coerce"),
        "pi_inflation": pd.to_numeric(raw.iloc[:, 2], errors="coerce"),
        "inflation_period": raw.iloc[:, 3].astype(str),
        "credit_period": raw.iloc[:, 4].astype(str),
        "episode": raw.iloc[:, 5].astype(str),
        "country": raw.iloc[:, 6].astype(str),
    }).dropna(subset=["row_index"])
    df = df.astype({"row_index": int})

    rows = []
    for _, r in df.iterrows():
        country_key = f"R{int(r['row_index']):02d}_{r['country'].strip()}"
        for col, sub_id, unit, vtype in [
            ("lambda_gDC", "S1509-lambda", "rate_percent", "num"),
            ("pi_inflation", "S1509-pi", "rate_percent", "num"),
        ]:
            v = r[col]
            if pd.isna(v):
                continue
            rows.append({
                "year": 2011, "value": float(v), "subseries_id": sub_id,
                "source_id": "RAMAMURTHY_2014_CH3", "units": unit,
                "country_key": country_key,
                "episode": r["episode"].strip(),
                "country": r["country"].strip(),
                "inflation_period": r["inflation_period"].strip(),
                "credit_period": r["credit_period"].strip(),
            })
    out_df = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out_df.to_parquet(OUT, index=False)

    line_32 = describe_ifs_line(32)
    line_64 = describe_ifs_line(64)
    audit = {
        "shaikh_legacy_line_32": {"modern_code": resolve_ifs_line(32),
                                  "modern_concept": line_32["modern_concept"]},
        "shaikh_legacy_line_64": {"modern_code": resolve_ifs_line(64),
                                  "modern_concept": line_64["modern_concept"]},
    }

    n_unique_countries = out_df["country"].nunique() if "country" in out_df.columns else 0
    return {
        "status": "OK",
        "rows_loaded": int(len(out_df)),
        "n_country_episodes": int(out_df["country_key"].nunique()),
        "n_unique_countries": int(n_unique_countries),
        "romania_dedup_note": "Romania appears twice (Acute 1991-94 + Chronic 1998-02); preserved as two distinct episode rows. Country-level unique count = 38; episode rows = 46.",
        "sources_fetched": ["RAMAMURTHY_2014_CH3"],
        "imf_resolver_audit": audit,
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
