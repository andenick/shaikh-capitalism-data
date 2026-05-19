"""
Phase 2 Registry Seeder — RSCD

Reads docs/chapters/SERIES_CANDIDATE_LIST.json and emits:
  Technical/series_registry.json (v0.1, candidates only)
  Technical/SERIES_CORRESPONDENCE_MATRIX.json

This is one-shot scaffolding (prefix _). After Phase 3 research closes,
the registry is hand-edited (or regenerated via a different tool) to add
subseries, units, construction formulas, and source URLs.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TECH = ROOT / "Technical"
CANDIDATES_PATH = TECH / "docs" / "chapters" / "SERIES_CANDIDATE_LIST.json"
REGISTRY_PATH = TECH / "series_registry.json"
MATRIX_PATH = TECH / "SERIES_CORRESPONDENCE_MATRIX.json"


def main():
    cands = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))

    registry = {
        "version": "0.1.0",
        "schema_version": "anu-ingestion-v4.0",
        "project": "rscd-shaikh-2016-replication",
        "project_name": "RSCD - Shaikh (2016) Capitalism Replication",
        "project_title": "Replication and Extension of Shaikh (2016) Capitalism: Competition, Conflict, Crises",
        "author": "Nicholas Anderson",
        "original_work": "Shaikh, Anwar (2016). Capitalism: Competition, Conflict, Crises. Oxford University Press.",
        "book": "Shaikh (2016) Capitalism: Competition, Conflict, Crises",
        "core_period": [1860, 2010],
        "extension_period": [2011, 2025],
        "drive_config": {
            "drive_version": "0.1",
            "original_work": {
                "title": "Capitalism: Competition, Conflict, Crises",
                "author": "Anwar Shaikh",
                "year": "2016",
                "publisher": "Oxford University Press",
                "isbn": "978-0-19-539066-4",
            },
            "author": {"first_name": "Nicholas", "last_name": "Anderson"},
            "institution": "The New School for Social Research",
            "email": "ibeforeena@gmail.com",
            "license": "CC-BY-4.0 (data); MIT (code, see project LICENSE)",
        },
        "prefix_scheme": {
            "primary": {"prefix": "S", "pattern": "S{chapter}{seq}", "example": "S201"},
            "external": {"prefix": "ES", "pattern": "ES{group}{seq}", "example": "ES1701"},
            "analytical": {"prefix": "AS", "pattern": "AS###", "example": "AS001"},
        },
        "external_study_groups": {
            "_note": "Frozen for v1.0 after docs/decisions/0001_external_study_scope.md is authored",
            "13": "Shaikh (2020) - Empirical regularities of Sraffa prices",
            "14": "Shaikh, Coronado, Nassif-Pires (2020)",
            "15": "Shaikh & Jacobo (2020)",
            "16": "Weber & Shaikh (2020)",
        },
        "stage": "candidates",
        "stage_notes": (
            "Candidates derived from CD FIGURE_MASTER_v4 + HDARP_SERIES_LINKAGE + CD2 registry "
            "by _phase2_taxonomy_builder.py. Subseries decomposition, units, construction formulas, "
            "and source URLs are added during Phase 3 (research) and Phase 5 (ingestion). "
            "Some candidates may merge or split during Phase 3."
        ),
        "series_count": cands["total_candidates"],
        "by_chapter": cands["by_chapter"],
        "by_content_type": cands["by_content_type"],
        "series": {},
    }

    for c in cands["candidates"]:
        sid = c["new_id"]
        registry["series"][sid] = {
            "name": c["name"],
            "chapter": c["chapter"],
            "figures": c["figures"],
            "year_range": c["year_range"],
            "content_type": c["content_type"],
            "construction": c["construction"],
            "status": "candidate",
            "units": None,                # populated in Phase 5
            "primary_source": None,       # populated in Phase 3
            "subseries": {},              # populated in Phase 5
            "proxy": False,
            "predecessor_ids": {
                "cd_id": c.get("cd_id"),
                "cd2_id": c.get("cd2_id"),
            },
            "predecessor_artifacts": {
                "appendix_reference": c.get("primary_appendix"),
                "hdarp_sources": c.get("hdarp_sources", []),
                "cd2_source_file": c.get("cd2_source_file"),
            },
            "notes": c.get("note", ""),
        }

    REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {REGISTRY_PATH}: {len(registry['series'])} series")

    # Correspondence matrix: per RSCD ID, list of predecessor IDs
    matrix = {
        "schema_version": "rscd-correspondence-v1.0",
        "generated_at": "2026-05-18T12:30:00+00:00",
        "description": "For each new RSCD series ID, the corresponding predecessor IDs in CD and CD2.",
        "by_rscd_id": {},
        "by_cd_id": {},
        "by_cd2_id": {},
    }
    for sid, det in registry["series"].items():
        matrix["by_rscd_id"][sid] = {
            "name": det["name"],
            "chapter": det["chapter"],
            "cd_id": det["predecessor_ids"]["cd_id"],
            "cd2_id": det["predecessor_ids"]["cd2_id"],
            "status": "mapped" if det["predecessor_ids"]["cd_id"] else "new",
        }
        if det["predecessor_ids"]["cd_id"]:
            matrix["by_cd_id"][det["predecessor_ids"]["cd_id"]] = sid
        if det["predecessor_ids"]["cd2_id"]:
            matrix["by_cd2_id"][det["predecessor_ids"]["cd2_id"]] = sid

    MATRIX_PATH.write_text(json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {MATRIX_PATH}: {len(matrix['by_rscd_id'])} mappings")


if __name__ == "__main__":
    main()
