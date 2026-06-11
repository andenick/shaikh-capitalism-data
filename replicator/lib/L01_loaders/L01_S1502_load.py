"""L01_S1502_load - load BEA GDP-by-Industry Panel A (goods & trade) for S1502.

Reads the salvaged chopped table and writes one parquet per panel-A industry
to Technical/data/raw/S1502_*.parquet (long form: year, value, subseries_id, ...).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from L01_loaders._bea_industry_loader import (  # noqa: E402
    PANEL_A_INDUSTRIES, load_chopped_levels_and_growth, panel_to_long,
)

CHOPPED_XLSX = book_data_path("Appendix15_USGDPRByIndustry.xlsx")
OUT = DATA_RAW / "S1502_BEA_INDUSTRY_PANEL_A.parquet"
SUBSOURCE_ID = "BEA_GDP_BY_INDUSTRY"


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}
    levels, growth = load_chopped_levels_and_growth(CHOPPED_XLSX)
    panel = panel_to_long(levels, growth, PANEL_A_INDUSTRIES, "S1502", SUBSOURCE_ID,
                          include_all_ref=True)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": int(len(panel)),
        "industries": sorted(panel["subseries_id"].unique().tolist()),
        "year_range": [int(panel["year"].min()), int(panel["year"].max())],
        "sources_fetched": [SUBSOURCE_ID],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
