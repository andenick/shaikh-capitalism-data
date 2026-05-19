"""
Phase 3b Registry Expansion — RSCD

Implements decisions 0001 (ES scope), 0002 (Ch6 GPIM as AS series),
0003 (crosswalk cleanup), 0004 (add S709-S711).

One-shot scaffolding (prefix _). Idempotent re-runs safe.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths

# CD2 ID → (new RSCD AS ID, name, components) — from decision 0002
AS_FROM_CH6_GPIM = [
    ("AS001", "S206", "GDP/GDI Decomposition and Business NOS",
     ["BEA NIPA T1.7.5", "BEA NIPA T1.10", "BEA NIPA T1.13"]),
    ("AS002", "S207", "Wage Equivalent and Corporate/Noncorporate Split",
     ["BEA NIPA T6.2", "BEA NIPA T1.14", "BEA NIPA T1.15"]),
    ("AS003", "S208", "Imputed Interest Adjustment and Sectoral Profit Rates",
     ["BEA NIPA T7.11", "BEA NIPA T1.14", "Fed Z.1 D.3"]),
    ("AS004", "S209", "GPIM Corporate Capital Stock",
     ["BEA Fixed Asset T6.1", "BEA Fixed Asset T6.4", "IRS SOI"]),
    ("AS005", "S210", "GPIM Variant — BEA 2011 Initial Value",
     ["BEA Fixed Asset T6.1 (2011 vintage)"]),
    ("AS006", "S211", "GPIM Variant — BEA 1993 vs 2011",
     ["BEA Fixed Asset T6.1 (1993)", "BEA Fixed Asset T6.1 (2011)"]),
    ("AS007", "S212", "GPIM Variant — IRS Adjusted",
     ["BEA Fixed Asset T6.1", "IRS SOI"]),
    ("AS008", "S213", "GPIM Variant — Interwar Adjusted",
     ["BEA Fixed Asset T6.1", "Historical Statistics interwar series"]),
    ("AS009", "S214", "IRS Corporate Inventories and Total Capital Stock",
     ["IRS SOI inventories", "BEA Fixed Asset T6.1"]),
]

# Per decision 0004
NEW_S_CH7 = [
    ("S709", "S035", "US ROP Deviations from Average", ["Fig7.16"]),
    ("S710", "S037", "US IROP Deviations from Average", ["Fig7.18"]),
    ("S711", "S038", "OECD IROP Deviations from Average", ["Fig7.21"]),
]

# Per decision 0001 (ES codes 20-23)
ES_PLACEHOLDERS = [
    ("ES2001", 20, "Shaikh (2020) - An Empirically Sufficient Form for Sraffa Prices",
     "[2020] Shaikh - An Empirically Sufficient Form for Sraffa Prices.pdf"),
    ("ES2101", 21, "Shaikh, Coronado, Nassif-Pires (2020) - On the empirical regularities of Sraffa prices",
     "[2020] Shaikh Coronado & Nassif-Pires - On the empirical regularities of Sraffa prices.pdf"),
    ("ES2201", 22, "Shaikh & Jacobo (2020) - Economic Arbitrage and the Econophysics of Income Inequality",
     "[2020] Shaikh & Jacobo - Economic Arbitrage and the Econophysics of Income Inequality.pdf"),
    ("ES2301", 23, "Weber & Shaikh (2020) - The US-China trade imbalance and the theory of free trade",
     "[2020] Weber & Shaikh - The U.S.-China trade imbalance and the theory of free trade debunking the currency manipulation argument.pdf"),
]

# Per decision 0003
CROSSWALK_FIXES = {
    "S707": {"cd_id_new": None, "cd2_id_new": None, "note": "Phase 3 finding: CD2 S038 link was stale; S707 belongs to Ch7 Fig 7.19; CD2 ancestor disputed"},
    "S801": {"cd_id_new": None, "cd2_id_new": None, "note": "Phase 3 finding: CD2 S042 mismap (S042 is Ch10 interest rates); S801 is Ch8 Eichner price paths; no CD2 ancestor"},
    "S803": {"cd_id_new": None, "cd2_id_new": None, "note": "Phase 3 finding: CD2 S041 mismap (S041 is Ch10 interest rates); S803 is Ch8 Bain ROE/CR8; no CD2 ancestor"},
}


def main():
    reg = json.loads(paths.REGISTRY.read_text(encoding="utf-8"))
    matrix = json.loads(paths.CORRESPONDENCE.read_text(encoding="utf-8"))

    initial_count = len(reg["series"])

    # 1. Update external_study_groups block
    reg["external_study_groups"] = {
        "_note": "ES codes 10-17 reserved (would visually collide with chapter codes); ES papers use codes 20+",
        "20": "Shaikh (2020) - An Empirically Sufficient Form for Sraffa Prices",
        "21": "Shaikh, Coronado, Nassif-Pires (2020) - On the empirical regularities of Sraffa prices",
        "22": "Shaikh & Jacobo (2020) - Economic Arbitrage and the Econophysics of Income Inequality",
        "23": "Weber & Shaikh (2020) - The US-China trade imbalance and the theory of free trade",
    }

    # 2. Add Ch6 AS series
    added_as = 0
    for new_id, cd2_id, name, components in AS_FROM_CH6_GPIM:
        if new_id in reg["series"]:
            continue
        reg["series"][new_id] = {
            "name": name,
            "chapter": 6,
            "figures": [],
            "year_range": [1947, 2025],
            "content_type": "derived",
            "construction": "composite",
            "status": "candidate",
            "units": None,
            "primary_source": None,
            "subseries": {},
            "proxy": False,
            "components": components,
            "predecessor_ids": {"cd_id": None, "cd2_id": cd2_id},
            "predecessor_artifacts": {
                "appendix_reference": "Appendix 6 (multiple sub-sections)",
                "hdarp_sources": [],
                "cd2_source_file": None,
            },
            "notes": f"Decision 0002: GPIM construction internal promoted from CD2 {cd2_id} unmapped status to AS series.",
        }
        matrix["by_rscd_id"][new_id] = {
            "name": name,
            "chapter": 6,
            "cd_id": None,
            "cd2_id": cd2_id,
            "status": "mapped",
        }
        matrix["by_cd2_id"][cd2_id] = new_id
        added_as += 1
    print(f"Added {added_as} AS series (decision 0002)")

    # 3. Add Ch7 series S709-S711
    added_s7 = 0
    for new_id, cd2_id, name, figures in NEW_S_CH7:
        if new_id in reg["series"]:
            continue
        reg["series"][new_id] = {
            "name": name,
            "chapter": 7,
            "figures": figures,
            "year_range": [1947, 2010],
            "content_type": "time_series",
            "construction": "direct",
            "status": "candidate",
            "units": None,
            "primary_source": None,
            "subseries": {},
            "proxy": False,
            "predecessor_ids": {"cd_id": cd2_id, "cd2_id": cd2_id},
            "predecessor_artifacts": {
                "appendix_reference": "Appendix 7",
                "hdarp_sources": [],
                "cd2_source_file": None,
            },
            "notes": f"Decision 0004: Ch7 figure not covered by Phase 2 candidate list; ported from CD2 {cd2_id}.",
        }
        matrix["by_rscd_id"][new_id] = {
            "name": name,
            "chapter": 7,
            "cd_id": cd2_id,
            "cd2_id": cd2_id,
            "status": "mapped",
        }
        matrix["by_cd2_id"][cd2_id] = new_id
        matrix["by_cd_id"][cd2_id] = new_id
        added_s7 += 1
    print(f"Added {added_s7} Ch7 S series (decision 0004)")

    # 4. Add ES placeholder series (decision 0001)
    added_es = 0
    for new_id, group_code, name, pdf in ES_PLACEHOLDERS:
        if new_id in reg["series"]:
            continue
        reg["series"][new_id] = {
            "name": name,
            "chapter": None,
            "external_study_group": group_code,
            "external_study_pdf": f"Inputs/Capitalism Data/Technical/data/raw/01_SOURCE_MATERIALS/Web Folders/Shaikh Publications/{pdf}",
            "figures": [],
            "year_range": [None, None],
            "content_type": "time_series",
            "construction": "direct",
            "status": "needs_decomposition",
            "units": None,
            "primary_source": None,
            "subseries": {},
            "proxy": False,
            "predecessor_ids": {"cd_id": None, "cd2_id": None},
            "predecessor_artifacts": {"cd2_source_file": None},
            "notes": (
                "Decision 0001: ES placeholder. Phase 3 subagent must read the paper PDF, "
                "identify empirical figures, and either populate this placeholder as a "
                "single series OR expand to N series ES{group}01..ES{group}NN."
            ),
        }
        matrix["by_rscd_id"][new_id] = {
            "name": name,
            "chapter": None,
            "cd_id": None,
            "cd2_id": None,
            "status": "new",
            "external_study_group": group_code,
        }
        added_es += 1
    print(f"Added {added_es} ES placeholder series (decision 0001)")

    # 5. Apply crosswalk fixes (decision 0003)
    fixed = 0
    for sid, fix in CROSSWALK_FIXES.items():
        if sid not in reg["series"]:
            continue
        old_cd2 = reg["series"][sid].get("predecessor_ids", {}).get("cd2_id")
        reg["series"][sid]["predecessor_ids"]["cd_id"] = fix["cd_id_new"]
        reg["series"][sid]["predecessor_ids"]["cd2_id"] = fix["cd2_id_new"]
        existing_notes = reg["series"][sid].get("notes") or ""
        reg["series"][sid]["notes"] = (existing_notes + " | " + fix["note"]).strip(" |")
        # Update matrix
        if sid in matrix["by_rscd_id"]:
            matrix["by_rscd_id"][sid]["cd_id"] = fix["cd_id_new"]
            matrix["by_rscd_id"][sid]["cd2_id"] = fix["cd2_id_new"]
            matrix["by_rscd_id"][sid]["status"] = "new"
        # Remove stale entries in by_cd2_id (only if they currently point to this sid)
        if old_cd2 and matrix["by_cd2_id"].get(old_cd2) == sid:
            del matrix["by_cd2_id"][old_cd2]
        fixed += 1
    print(f"Fixed {fixed} crosswalk mismaps (decision 0003)")

    # 6. Update registry meta
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
    print(f"Series count: {initial_count} -> {len(reg['series'])}")
    print(f"By chapter: {reg['by_chapter']}")

    # 7. Rewrite crosswalk CSV with notes column for fixes
    cw_path = paths.MIGRATION_DIR / "CD2_to_RSCD_crosswalk.csv"
    rows = list(csv.reader(cw_path.open(encoding="utf-8")))
    header = rows[0]
    body = rows[1:]
    # Find rows that should be updated to reflect crosswalk fixes
    # (already-unmapped rows now get a new RSCD ID if they were promoted to AS)
    for r in body:
        cd2_id = r[0]
        # If CD2 ID now maps to an AS series, update
        new_rscd = matrix["by_cd2_id"].get(cd2_id)
        if new_rscd and not r[3]:
            r[3] = new_rscd
            r[4] = matrix["by_rscd_id"][new_rscd]["name"]
            r[5] = "mapped (decision 0002)"
            r[6] = "promoted to AS series per decision 0002"
    csv.writer(cw_path.open("w", encoding="utf-8", newline="")).writerows([header] + body)
    # Append new mappings not in original (S709-711 from S035/S037/S038 — these had no CD2 row originally)
    print(f"Crosswalk CSV updated: {cw_path}")


if __name__ == "__main__":
    main()
