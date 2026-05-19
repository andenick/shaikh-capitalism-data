"""L01_S218_load - GDP per Capita Richest Four and Poorest Four Countries (Maddison).

Fig 2.16 in the book uses precomputed 'RICHEST 4' and 'POOREST 4' rows directly
from the Appendix2_GDPperCapita.xlsx table (Shaikh has already applied the
Kuwait/Qatar/Venezuela exclusion rule).

Per Phase 4 substitution: MPD 2023 extension would require re-applying the
exclusion rule to the modern panel (and possibly adding Macao, Luxembourg
exclusions). We do NOT attempt that automatically here — the EPR documents
the rule and flags it for a focused Phase 9 effort. The book period values
1600-2000 are emitted directly from the salvaged table.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

XLSX = book_data_path("Appendix2_GDPperCapita.xlsx")
OUT = DATA_RAW / "S218_MADDISON_RICHEST_POOREST_4.parquet"

LABELS = {
    "RICHEST 4": "S218-A",
    "POOREST 4": "S218-B",
    "RATIO OF RICHEST 4 TO POOREST 4": "S218-C",
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
        label = row["Year"]
        if not isinstance(label, str):
            continue
        label = label.strip()
        if label in LABELS and label not in seen:
            seen.add(label)
            sid = LABELS[label]
            units = "ratio" if "RATIO" in label else "geary_khamis_1990_per_capita"
            for yc in year_cols:
                v = row[yc]
                if pd.notna(v):
                    rows.append({"year": int(yc), "value": float(v), "units": units,
                                 "subseries_id": sid,
                                 "subsource_id": "MADDISON_2003_SHAIKH_EXCLUSION_RULE",
                                 "label": label})
    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": {"MADDISON_RICH_POOR": len(out)},
        "sources_fetched": ["MADDISON_2003_SHAIKH_EXCLUSION_RULE"],
        "labels_loaded": sorted(seen),
        "year_range": [int(out["year"].min()), int(out["year"].max())],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
