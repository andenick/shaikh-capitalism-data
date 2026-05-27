"""L01_S707 — Greek manufacturing average-profit-rate DEVIATION panel, 1962-1991.

Digitized from Tsoulfidis & Tsaliki (2011/2013), MPRA 51334, Figure 4 (= Shaikh 2016
Fig 7.19), via offline PDF vector extraction (RSCD 2026-05-26). The source publishes the
series as a chart only (no underlying table); values are recovered at digitization fidelity.
Provenance and method: Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402
from L01_loaders._ch7_xlsx_panels import read_panel, deviations_long  # noqa: E402

SERIES_ID = "S707"
SRC_XLSX = SALVAGED_BOOK_DATA / "Reconstructed" / "Tsoulfidis_Tsaliki_2011_Fig4_S707.xlsx"
OUT = DATA_RAW / f"{SERIES_ID}_TT2011_FIG4_DEV.parquet"


def run() -> dict:
    if not SRC_XLSX.exists():
        return {"status": "FAIL", "error": f"digitized source missing: {SRC_XLSX}"}

    panel = read_panel(SRC_XLSX)
    long_df = deviations_long(
        panel,
        subseries_id=f"{SERIES_ID}-A",
        subsource_id="TSOULFIDIS_TSALIKI_2011_FIG4",
        units="rate_deviation_decimal",
        include_aggregate=False,
    )

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    long_df.to_parquet(OUT, index=False)

    industries = sorted(long_df["industry"].unique().tolist())
    return {
        "status": "OK",
        "rows_loaded": {"tt2011_fig4_dev": int(len(long_df))},
        "year_range": [int(long_df["year"].min()), int(long_df["year"].max())],
        "industries": industries,
        "industry_count": len(industries),
        "sources_fetched": ["TSOULFIDIS_TSALIKI_2011_FIG4"],
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
