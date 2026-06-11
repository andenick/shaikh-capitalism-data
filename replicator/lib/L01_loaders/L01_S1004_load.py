"""L01_S1004_load — Real Interest Rate HP-filtered, 1857-2011 (+ extension).

Derived from S1002 components (iblong, USWPI). Loader ensures component
parquets exist (delegates to L01_S1002) and also saves the book-published
USLR columns 'iblongreal' and 'iblongrealHP3' for validation purposes.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix10_USLR.xlsx")
OUT_TRUTH = DATA_RAW / "S1004_USLR_truth.parquet"
S1002_iblong = DATA_RAW / "S1002_USLR_iblong.parquet"
S1002_USWPI = DATA_RAW / "S1002_USLR_USWPI.parquet"


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"USLR missing: {CHOPPED_XLSX}"}
    # Ensure S1002 components are present
    if not (S1002_iblong.exists() and S1002_USWPI.exists()):
        from L01_loaders import L01_S1002_load as l01
        l01.run()

    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    sub = df[["Year", "iblongreal", "iblongrealHP3"]].rename(columns={"Year": "year"})
    sub = sub.dropna(subset=["iblongreal"], how="all")
    sub["units"] = "percent"
    sub["subseries_id"] = "S1004-TRUTH"
    sub["subsource_id"] = "USLR_iblongreal"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(OUT_TRUTH, index=False)
    return {
        "status": "OK",
        "rows_loaded": {"USLR_truth": int(len(sub))},
        "sources_fetched": ["USLR_iblongreal", "S1002_components"],
        "outputs": [str(OUT_TRUTH)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
