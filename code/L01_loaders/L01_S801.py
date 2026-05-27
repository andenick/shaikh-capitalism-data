"""L01_S801 — Oligopolistic vs Competitive wholesale price indices (1957-59=100), 1965-1973.

Digitized from Shaikh (2016) Fig 8.1 (= Eichner 1973, EJ 83(332) p.1187) via offline vector
extraction of the book PDF (Oxford print p413), overlay-validated against the figure
(RSCD 2026-05-26). Chart-only source; values at digitization fidelity. Provenance:
Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md (+ fig8_1_extracted.json).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402
from L01_loaders._ch7_xlsx_panels import read_panel, levels_long  # noqa: E402

SERIES_ID = "S801"
SRC_XLSX = SALVAGED_BOOK_DATA / "Reconstructed" / "Eichner_1973_Fig8_1_S801.xlsx"
OUT = DATA_RAW / f"{SERIES_ID}_EICHNER_FIG8_1.parquet"


def run() -> dict:
    if not SRC_XLSX.exists():
        return {"status": "FAIL", "error": f"digitized source missing: {SRC_XLSX}"}
    panel = read_panel(SRC_XLSX)
    long_df = levels_long(
        panel,
        subseries_id=f"{SERIES_ID}-A",
        subsource_id="EICHNER_1973_EJ",
        units="index_1957-59=100",
        include_aggregate=True,
    )
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    long_df.to_parquet(OUT, index=False)
    industries = sorted(long_df["industry"].unique().tolist())
    return {
        "status": "OK",
        "rows_loaded": {"eichner_fig8_1": int(len(long_df))},
        "year_range": [int(long_df["year"].min()), int(long_df["year"].max())],
        "industries": industries,
        "industry_count": len(industries),
        "sources_fetched": ["EICHNER_1973_EJ"],
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
