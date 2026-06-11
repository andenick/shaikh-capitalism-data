"""L01_S706_load — US industry IROP panel, 1988-2005 (Shaikh Appendix 7.2 iropdataUSind)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from L01_loaders._ch7_xlsx_panels import read_panel, levels_long  # noqa: E402

SERIES_ID = "S706"
CHOPPED_XLSX = book_data_path("Appendix7_iropdataUSind.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_SHAIKH_APX7_IROP.parquet"


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}

    panel = read_panel(CHOPPED_XLSX)
    long_df = levels_long(
        panel,
        subseries_id=f"{SERIES_ID}-A",
        subsource_id="SHAIKH_2008_APPENDIX_7_2_IROP",
        units="rate_decimal",
        include_aggregate=True,
    )

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    long_df.to_parquet(OUT, index=False)

    industries = sorted(long_df["industry"].unique().tolist())
    return {
        "status": "OK",
        "rows_loaded": {"shaikh_apx7_irop": int(len(long_df))},
        "year_range": [int(long_df["year"].min()), int(long_df["year"].max())],
        "industries": industries,
        "industry_count": len(industries),
        "sources_fetched": ["SHAIKH_2008_APPENDIX_7_2_IROP"],
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
