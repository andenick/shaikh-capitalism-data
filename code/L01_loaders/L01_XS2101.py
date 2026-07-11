"""L01_XS2101 — Shaikh-Coronado-Nassif-Pires (2020) headline summary stats.

Filename note (AS/ES->XS migration, 2026-06-10): the ground-truth SalvagedInputs
copy retains the LEGACY ES-prefixed name (ES2101_summary_statistics.csv) BY DESIGN —
SalvagedInputs is read-only and is never renamed. The replicator's XS-named
inputs_bundled copy (XS2101_summary_statistics.csv) is preferred where present;
this loader resolves the XS name first and falls back to the legacy ES name.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402

SERIES_ID = "XS2101"
SOURCE_ID = "SHAIKH_CORONADO_NASSIF_2020_S5_SUMMARY"
_RECON_DIR = SALVAGED_BOOK_DATA / "Reconstructed"


def _resolve_csv() -> Path:
    """Resolve the reconstructed CSV, tolerating the ES/XS filename split.

    Prefer the migrated XS name (present in the replicator's XS-named
    inputs_bundled copy); fall back to the legacy ES name retained in the
    read-only SalvagedInputs tree. Returns the XS candidate if neither
    exists so error messages name the canonical spelling.
    """
    xs = _RECON_DIR / "XS2101_summary_statistics.csv"
    es = _RECON_DIR / "ES2101_summary_statistics.csv"
    if xs.exists():
        return xs
    if es.exists():
        return es
    return xs


CSV_PATH = _resolve_csv()
OUT = DATA_RAW / f"{SERIES_ID}_SUMMARY_STATS.parquet"


def run() -> dict:
    if not CSV_PATH.exists():
        return {"status": "FAIL", "error": f"missing CSV: {CSV_PATH}"}
    df = pd.read_csv(CSV_PATH)
    rows = []
    for _, r in df.iterrows():
        stat = str(r["statistic"])
        rows.append({
            "year": int(r["year"]),
            "value": float(r["value"]),
            "subseries_id": f"{SERIES_ID}-{stat}",
            "subsource_id": SOURCE_ID,
            "units": str(r["units"]),
            "statistic": stat,
        })
    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {"status": "OK", "rows_loaded": int(len(out)),
            "sources_fetched": [SOURCE_ID], "output": str(OUT)}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
