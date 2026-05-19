"""
RSCD path abstractions.

Centralizes filesystem paths so scripts don't hardcode legacy locations.
Update this file when files move, not 100 scripts.
"""
from __future__ import annotations

from pathlib import Path

# Project root = parent of Technical/
PROJECT_ROOT = Path(__file__).resolve().parents[3]
assert PROJECT_ROOT.name == "RSCD", f"Unexpected project root: {PROJECT_ROOT}"

# Top-level
INPUTS = PROJECT_ROOT / "Inputs"
TECHNICAL = PROJECT_ROOT / "Technical"
OUTPUTS = PROJECT_ROOT / "Outputs"
SALVAGED = PROJECT_ROOT / "SalvagedInputs"   # NB: not under Inputs/ due to deny rule

# Frozen legacy (read-only — accessed only by Phase 3 research as needed)
CD_LEGACY = INPUTS / "Capitalism Data"
CD2_LEGACY = INPUTS / "CD2"

# Salvaged subdirectories
SALVAGED_BOOK_DATA = SALVAGED / "book_data"
SALVAGED_EXT_BENCH = SALVAGED / "extension_benchmarks"
SALVAGED_FIGURES = SALVAGED / "figures_reference"
SALVAGED_DECISIONS = SALVAGED / "methodology_decisions"

# Active pipeline directories
REGISTRY = TECHNICAL / "series_registry.json"
LEDGER = TECHNICAL / "ANU_LEDGER.json"
PIPELINE_STATE = TECHNICAL / "PIPELINE_STATE.json"
SUBSOURCE_METADATA = TECHNICAL / "SUBSOURCE_METADATA.json"
CORRESPONDENCE = TECHNICAL / "SERIES_CORRESPONDENCE_MATRIX.json"

BUILD_DIR = TECHNICAL / "Build"
CODE_DIR = TECHNICAL / "code"
RESEARCH_DIR = TECHNICAL / "research"
DOCS_DIR = TECHNICAL / "docs"
DOCS_CHAPTERS = DOCS_DIR / "chapters"
DOCS_SERIES = DOCS_DIR / "series"
DOCS_DECISIONS = DOCS_DIR / "decisions"
DOCS_METHODOLOGY = DOCS_DIR / "methodology"

CHOPPED_DIR = TECHNICAL / "chopped"
EXTENBOOK_DIR = TECHNICAL / "extenbooks"
VIZ_DIR = TECHNICAL / "viz"
HANDOFFS_DIR = TECHNICAL / "Handoffs"
MIGRATION_DIR = TECHNICAL / "MIGRATION"
DATA_RAW = TECHNICAL / "data" / "raw"
DATA_PROCESSED = TECHNICAL / "data" / "processed"
CONFIG_DIR = TECHNICAL / "config"

# Knowledge Base — the canonical figure/table/equation metadata. CD's HDARP
# v4.2 is the working KB (CD2's HDARP_Integration was started but largely empty).
KB_FIGURE_MASTER = SALVAGED_FIGURES / "FIGURE_MASTER_v4.json"
KB_LINKAGE = SALVAGED_FIGURES / "HDARP_SERIES_LINKAGE.json"
KB_CROSSREF = SALVAGED_FIGURES / "CD_CROSS_REFERENCE_INDEX.json"
KB_CHAPTER_INDEX = DOCS_CHAPTERS / "CHAPTER_FIGURE_TABLE_INDEX.json"

# Reference paths to CD/CD2 deep KB (lazy access — large)
CD_KB_HDARP_V4 = CD_LEGACY / "Outputs" / "ShinyApp" / "data" / "ShaikhAbsorbed" / "hdarp_v4"
CD_KB_HISTORICAL = CD_LEGACY / "Technical" / "Knowledge_Base"


def book_data_path(table_or_chapter: str) -> Path:
    """Resolve a Shaikh chopped table by name or chapter."""
    return SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / table_or_chapter


def cd2_per_series_csv(cd2_id: str) -> Path | None:
    """Return path to CD2's final per-series CSV if it exists."""
    cand = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / f"{cd2_id}.csv"
    return cand if cand.exists() else None


def assert_paths_exist():
    """Fail-fast sanity check at app/script startup."""
    required = [
        TECHNICAL, INPUTS, OUTPUTS, SALVAGED,
        REGISTRY, PIPELINE_STATE,
        BUILD_DIR, CODE_DIR, RESEARCH_DIR, DOCS_DIR,
        KB_FIGURE_MASTER, KB_LINKAGE, KB_CHAPTER_INDEX,
    ]
    missing = [p for p in required if not p.exists()]
    if missing:
        raise RuntimeError(f"Missing required paths: {missing}")


if __name__ == "__main__":
    assert_paths_exist()
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"All required paths present.")
