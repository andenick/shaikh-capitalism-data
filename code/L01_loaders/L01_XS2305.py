"""L01_ES2305 — macro-balance RMB misalignment literature compilation."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "XS2305"
SOURCE_ID = "WEBER_SHAIKH_2020_FIG5_LIT_COMPILATION"
def _resolve_csv() -> Path:
    """Resolve the reconstructed CSV, tolerating the ES/XS filename split
    (prefer XS, fall back to the legacy ES name in read-only SalvagedInputs)."""
    recon = SALVAGED_BOOK_DATA / "Reconstructed"
    xs = recon / f"{SERIES_ID}_literature_compilation.csv"
    es = recon / f"ES{SERIES_ID[2:]}_literature_compilation.csv"
    if xs.exists():
        return xs
    if es.exists():
        return es
    return xs


CSV_PATH = _resolve_csv()
OUT = DATA_RAW / f"{SERIES_ID}_LIT_COMPILATION.parquet"


def run() -> dict:
    if not CSV_PATH.exists():
        return {"status": "FAIL", "error": f"missing CSV: {CSV_PATH}"}
    df = pd.read_csv(CSV_PATH)
    out = pd.DataFrame({
        "year": df["estimate_year"].astype(int),
        "value": df["misalignment_pct"].astype(float),
        "subseries_id": f"{SERIES_ID}-A",
        "subsource_id": SOURCE_ID,
        "units": "percent",
        "study": df["study"].astype(str),
        "source_paper": df["source_paper"].astype(str),
        "methodology": df["methodology"].astype(str),
    })
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {"status": "OK", "rows_loaded": int(len(out)),
            "sources_fetched": [SOURCE_ID], "output": str(OUT)}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
