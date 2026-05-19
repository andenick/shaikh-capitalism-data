"""
ES2301 5-way Split Expansion — RSCD

Per approved decision 0006:
- Rescope ES2301 from composite parent to Fig-1 component only (US-China bilateral trade balance)
- Add ES2302 (China current account)
- Add ES2303 (China FX reserves)
- Add ES2304 (RMB misalignment extended PPP, literature compilation)
- Add ES2305 (RMB misalignment macro-balance, literature compilation)
- ES2306 (relative ULC) deferred to v1.1

Idempotent.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths

NEW_ES = [
    ("ES2302", "China Current Account Balance (level USD Bn and % GDP)",
     "IMF World Economic Outlook database", "https://www.imf.org/en/Publications/WEO",
     "billions_usd_and_percent_gdp", "annual", "time_series", "direct",
     "Fig 2 of Weber & Shaikh (2020). Two columns: BCA level (USD Bn) and BCA as % of GDP.",
     [1990, 2017]),
    ("ES2303", "China Official Foreign Exchange Reserves Excluding Gold",
     "World Bank WDI FI.RES.XGLD.CD", "https://data.worldbank.org/indicator/FI.RES.XGLD.CD",
     "current_usd", "annual", "time_series", "direct",
     "Fig 3 of Weber & Shaikh (2020). PBoC FX reserves ex-gold series.",
     [1990, 2017]),
    ("ES2304", "RMB Misalignment Estimates under Extended PPP Approach (literature compilation)",
     "Literature compilation", None,
     "percent", "annual", "time_series", "composite",
     "Fig 4 of Weber & Shaikh (2020). Compiled per paper note 17 from: Cline-Williamson 2007; Dunaway-Li 2005; Cheung-Chinn-Fujii 2010a; Cheung 2012.",
     [1995, 2012]),
    ("ES2305", "RMB Misalignment Estimates under Macroeconomic Balance Approach (literature compilation)",
     "Literature compilation", None,
     "percent", "annual", "time_series", "composite",
     "Fig 5 of Weber & Shaikh (2020). Same 4-paper literature compilation as ES2304.",
     [1995, 2012]),
]


def main():
    reg = json.loads(paths.REGISTRY.read_text(encoding="utf-8"))
    matrix = json.loads(paths.CORRESPONDENCE.read_text(encoding="utf-8"))
    initial = len(reg["series"])

    # 1. Rescope ES2301
    if "ES2301" in reg["series"]:
        es2301 = reg["series"]["ES2301"]
        es2301["name"] = "US-China Bilateral Merchandise Trade Balance"
        es2301["figures"] = ["Fig 1"]
        es2301["status"] = "candidate"
        es2301["construction"] = "direct"
        es2301["content_type"] = "time_series"
        es2301["primary_source"] = {
            "agency": "U.S. Census Bureau",
            "publication": "FT900 / USA Trade Online",
            "table_or_series_id": "Trade with China (FT900 Exhibit 14)",
            "url": "https://www.census.gov/foreign-trade/balance/c5700.html",
            "units": "billions_usd",
            "frequency": "annual",
            "license": "public-domain",
        }
        es2301["year_range"] = [1990, 2017]
        es2301["notes"] = (es2301.get("notes") or "") + " | Rescoped per decision 0006 to Fig 1 only; ES2302-ES2305 hold the other 4 figures."
        print("Rescoped ES2301")

    # 2. Add ES2302-ES2305
    added = 0
    for new_id, name, agency, url, units, freq, ctype, cons, note, year_range in NEW_ES:
        if new_id in reg["series"]:
            print(f"SKIP {new_id} (already exists)")
            continue
        reg["series"][new_id] = {
            "name": name,
            "chapter": None,
            "external_study_group": 23,
            "external_study_pdf": "Inputs/Capitalism Data/Technical/data/raw/01_SOURCE_MATERIALS/Web Folders/Shaikh Publications/[2020] Weber & Shaikh - The U.S.-China trade imbalance and the theory of free trade debunking the currency manipulation argument.pdf",
            "figures": [],
            "year_range": year_range,
            "content_type": ctype,
            "construction": cons,
            "status": "candidate",
            "units": units,
            "primary_source": {
                "agency": agency,
                "publication": agency,
                "table_or_series_id": None,
                "url": url,
                "units": units,
                "frequency": freq,
                "license": "public-domain" if url else "academic-compilation",
            },
            "subseries": {},
            "proxy": False,
            "predecessor_ids": {"cd_id": None, "cd2_id": None},
            "predecessor_artifacts": {"cd2_source_file": None},
            "notes": note + " | Added per decision 0006 5-way split.",
        }
        matrix["by_rscd_id"][new_id] = {
            "name": name,
            "chapter": None,
            "cd_id": None,
            "cd2_id": None,
            "status": "new",
            "external_study_group": 23,
        }
        added += 1
        print(f"Added {new_id}: {name[:60]}")

    # 3. Update registry meta
    reg["series_count"] = len(reg["series"])
    from collections import Counter
    by_ch = Counter()
    by_ct = Counter()
    for det in reg["series"].values():
        ch = det.get("chapter") or "ES"
        by_ch[str(ch)] += 1
        by_ct[str(det.get("content_type"))] += 1
    reg["by_chapter"] = dict(sorted(by_ch.items()))
    reg["by_content_type"] = dict(sorted(by_ct.items()))

    paths.REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
    paths.CORRESPONDENCE.write_text(json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8")

    print()
    print(f"Series count: {initial} -> {len(reg['series'])}")
    print(f"By chapter: {reg['by_chapter']}")


if __name__ == "__main__":
    main()
