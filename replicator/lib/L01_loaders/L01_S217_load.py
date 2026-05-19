"""L01_S217_load - GDP per Capita of World Regions (Maddison), Fig 2.17.

Reads the salvaged Maddison region table (Appendix2_GDPperCapita.xlsx):
World, Western Europe, Western Offshoots, Latin America, Asia, Africa, 1600-2000.

The table is wide (rows=region, cols=decade). We unpivot to long form.

Phase 4 substitution: Extension via Maddison Project Database 2023 (Bolt &
van Zanden 2024) — but their 2011 PPP base differs from the book's 1990 GK
base. We do NOT attempt automated splice within this loader; the EPR
documents the discontinuity. Extension via MPD 2023 is left for a focused
Phase 9 effort because regional aggregations changed.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

XLSX = book_data_path("Appendix2_GDPperCapita.xlsx")
OUT = DATA_RAW / "S217_MADDISON_REGIONS.parquet"

REGIONS = {
    "World": "S217-A",
    "Western Europe": "S217-B",
    "Western Offshoots": "S217-C",
    "Latin America": "S217-D",
    "Asia": "S217-E",
    "Africa": "S217-F",
}


def run() -> dict:
    if not XLSX.exists():
        return {"status": "FAIL", "error": f"missing {XLSX}"}
    df = pd.read_excel(XLSX, header=1)
    df.columns = [c if isinstance(c, int) else str(c).strip() for c in df.columns]
    year_cols = [c for c in df.columns if isinstance(c, int)]
    rows = []
    seen = set()
    for _, row in df.iterrows():
        region_label = row["Year"]
        if not isinstance(region_label, str):
            continue
        region_label = region_label.strip()
        if region_label in REGIONS and region_label not in seen:
            seen.add(region_label)
            sid = REGIONS[region_label]
            for yc in year_cols:
                v = row[yc]
                if pd.notna(v):
                    rows.append({"year": int(yc), "value": float(v),
                                 "units": "geary_khamis_1990_per_capita",
                                 "subseries_id": sid,
                                 "subsource_id": "MADDISON_2003_APP_TABLE_2A",
                                 "region": region_label})
    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": {"MADDISON_REGIONS": len(out)},
        "sources_fetched": ["MADDISON_2003_APP_TABLE_2A"],
        "regions_loaded": sorted(seen),
        "year_range": [int(out["year"].min()), int(out["year"].max())],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
