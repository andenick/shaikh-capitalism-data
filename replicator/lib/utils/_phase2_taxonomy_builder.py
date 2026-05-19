"""
Phase 2 Taxonomy Builder — RSCD

Reads CD's FIGURE_MASTER_v4.json, HDARP_SERIES_LINKAGE.json, and CD2's
series_registry.json (all in Inputs/, read-only) and emits:

  Technical/docs/chapters/CHAPTER_FIGURE_TABLE_INDEX.json
  Technical/docs/chapters/SERIES_CANDIDATE_LIST.json
  Technical/MIGRATION/CD2_to_RSCD_crosswalk.csv
  Technical/MIGRATION/CD_to_RSCD_crosswalk.csv

This script is one-shot scaffolding (prefix _). It is NOT part of the live
pipeline and may be deleted after Phase 2 is locked.

Conventions:
- New IDs assigned per Technical/MIGRATION/PREFIX_SCHEME.md
- Series candidate grouping: figures with the same linked_series in
  HDARP_SERIES_LINKAGE.json are merged into one candidate.
- Figures with no linked_series become individual candidates.
- Content type classification: empirical figures with year ranges → time_series;
  figures with figure_type != "empirical" → theoretical;
  cross-sectional snapshots inferred from caption keywords.
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

# ---- Paths -----------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[3]          # Projects/RSCD/
INPUTS = ROOT / "Inputs"
TECH = ROOT / "Technical"
DOCS_CH = TECH / "docs" / "chapters"
MIGR = TECH / "MIGRATION"

CD_FIGURE_MASTER = INPUTS / "Capitalism Data" / "Outputs" / "ShinyApp" / "data" / "ShaikhAbsorbed" / "FIGURE_MASTER_v4.json"
CD_LINKAGE = INPUTS / "Capitalism Data" / "Outputs" / "ShinyApp" / "data" / "ShaikhAbsorbed" / "catalogs" / "HDARP_SERIES_LINKAGE.json"
CD2_REGISTRY = INPUTS / "CD2" / "series_registry.json"

CROSS_SECTIONAL_KEYWORDS = re.compile(
    r"\b(scatter|cross-?section|distribution|by industry|by country|by sector|hist[oa]gram|density|share of)\b",
    re.IGNORECASE,
)
THEORETICAL_KEYWORDS = re.compile(
    r"\b(stylized|hypothetical|schematic|conceptual|illustrative|theoretical)\b",
    re.IGNORECASE,
)

# ---- Loaders ---------------------------------------------------------------


def load_figure_master() -> dict:
    with CD_FIGURE_MASTER.open(encoding="utf-8") as f:
        return json.load(f)


def load_linkage() -> dict:
    with CD_LINKAGE.open(encoding="utf-8") as f:
        return json.load(f)


def load_cd2_registry() -> dict:
    with CD2_REGISTRY.open(encoding="utf-8") as f:
        return json.load(f)


# ---- Classification --------------------------------------------------------


def classify_content_type(fig: dict) -> str:
    """Classify a figure's content type.

    figure_type != "empirical" → theoretical (conceptual/illustrative)
    empirical + theoretical keyword → theoretical
    empirical + cross-sectional keyword → cross_sectional
    empirical + has_axis → time_series (default for time-axis figures)
    empirical + no axis metadata → cross_sectional (most no-axis empirical
        figures in Shaikh 2016 are industry-level scatter plots or year
        snapshots; Phase 3 research reclassifies if wrong)
    """
    ftype = (fig.get("figure_type") or "").lower()
    caption = fig.get("full_caption") or ""
    if ftype != "empirical":
        return "theoretical"
    if THEORETICAL_KEYWORDS.search(caption):
        return "theoretical"
    if CROSS_SECTIONAL_KEYWORDS.search(caption):
        return "cross_sectional"
    if fig.get("has_axis"):
        return "time_series"
    return "cross_sectional"


# ---- Chapter index ---------------------------------------------------------


def build_chapter_index(fm: dict, linkage: dict) -> dict:
    """Per-chapter inventory of empirical figures and their CD/CD2 series links."""
    chapters: dict[int, dict] = {}
    for fig in fm.get("figures", []):
        ch = fig.get("chapter")
        if ch is None:
            continue
        chapters.setdefault(
            ch,
            {
                "chapter": ch,
                "figures": [],
                "counts": {
                    "total": 0,
                    "empirical": 0,
                    "time_series": 0,
                    "cross_sectional": 0,
                    "theoretical": 0,
                },
            },
        )

        ctype = classify_content_type(fig)
        chapters[ch]["counts"]["total"] += 1
        chapters[ch]["counts"][ctype if ctype != "theoretical" else "theoretical"] += 1
        if (fig.get("figure_type") or "").lower() == "empirical":
            chapters[ch]["counts"]["empirical"] += 1

        link = linkage.get("figures", {}).get(fig["figure_id"], {})
        chapters[ch]["figures"].append(
            {
                "figure_id": fig["figure_id"],
                "caption": fig.get("full_caption"),
                "page": fig.get("page_number"),
                "section": fig.get("section"),
                "type": fig.get("figure_type"),
                "content_type": ctype,
                "has_axis": fig.get("has_axis"),
                "appendix_reference": fig.get("appendix_reference"),
                "cd_linked_series": link.get("linked_series", []),
                "year_range": link.get("year_range"),
                "hdarp_table_sources": link.get("hdarp_table_sources", []),
            }
        )

    return {
        "schema_version": "rscd-chapter-index-v1.0",
        "generated_by": "_phase2_taxonomy_builder.py",
        "source_files": {
            "FIGURE_MASTER_v4": str(CD_FIGURE_MASTER.relative_to(ROOT)),
            "HDARP_SERIES_LINKAGE": str(CD_LINKAGE.relative_to(ROOT)),
        },
        "total_chapters": len(chapters),
        "total_figures": sum(c["counts"]["total"] for c in chapters.values()),
        "chapters": [chapters[k] for k in sorted(chapters)],
    }


# ---- Candidate series ------------------------------------------------------


def build_series_candidates(chapter_index: dict, cd2_registry: dict) -> dict:
    """Group figures into candidate series, assign new S{ch}{seq} IDs."""
    # Group: (chapter, cd_linked_series_id) → list of figure ids
    groups: dict[tuple[int, str], list[dict]] = defaultdict(list)
    orphans: list[dict] = []  # figures with no linked_series

    cd_series_to_chapter: dict[str, int] = {}

    for ch_block in chapter_index["chapters"]:
        ch = ch_block["chapter"]
        for fig in ch_block["figures"]:
            if fig["content_type"] == "theoretical":
                continue  # skip — no series
            links = fig.get("cd_linked_series", [])
            if not links:
                orphans.append({"chapter": ch, **fig})
                continue
            for cd_sid in links:
                groups[(ch, cd_sid)].append(fig)
                cd_series_to_chapter.setdefault(cd_sid, ch)

    # Assign new RSCD IDs: S{chapter}{seq}, seq starts at 01 per chapter
    seq_counter: dict[int, int] = defaultdict(int)
    candidates = []
    cd_to_rscd: dict[str, str] = {}

    # Sort groups by (chapter, first figure page, cd_sid) for deterministic IDs
    ordered_groups = sorted(
        groups.items(),
        key=lambda kv: (
            kv[0][0],
            min((f.get("page") or 9999) for f in kv[1]),
            kv[0][1],
        ),
    )

    for (ch, cd_sid), figs in ordered_groups:
        seq_counter[ch] += 1
        new_id = f"S{ch}{seq_counter[ch]:02d}"
        cd_to_rscd[cd_sid] = new_id

        # Aggregate year range, sources
        year_ranges = [f.get("year_range") for f in figs if f.get("year_range")]
        if year_ranges:
            yr_starts = [y.get("start") for y in year_ranges if isinstance(y, dict) and y.get("start")]
            yr_ends = [y.get("end") for y in year_ranges if isinstance(y, dict) and y.get("end")]
            year_range = [
                min(yr_starts) if yr_starts else None,
                max(yr_ends) if yr_ends else None,
            ]
        else:
            year_range = [None, None]

        content_types = {f["content_type"] for f in figs}
        if content_types == {"time_series"}:
            ctype = "time_series"
        elif "time_series" in content_types:
            ctype = "time_series"  # majority rule
        elif content_types == {"cross_sectional"}:
            ctype = "cross_sectional"
        else:
            ctype = list(content_types)[0]

        # Pull CD2 series detail if present (same CD ID label)
        cd2_detail = cd2_registry.get("series", {}).get(cd_sid, {})

        candidates.append(
            {
                "new_id": new_id,
                "chapter": ch,
                "cd_id": cd_sid,
                "cd2_id": cd_sid if cd_sid in cd2_registry.get("series", {}) else None,
                "name": cd2_detail.get("name") or _name_from_figures(figs),
                "content_type": ctype,
                "construction": _infer_construction(cd2_detail),
                "year_range": year_range,
                "figures": [f["figure_id"] for f in figs],
                "primary_appendix": _most_common(
                    [f.get("appendix_reference") for f in figs if f.get("appendix_reference")]
                ),
                "hdarp_sources": _dedup_hdarp_sources(figs),
                "cd2_source_file": cd2_detail.get("source_file"),
            }
        )

    # Orphan figures: each becomes its own candidate
    for o in orphans:
        ch = o["chapter"]
        seq_counter[ch] += 1
        new_id = f"S{ch}{seq_counter[ch]:02d}"
        candidates.append(
            {
                "new_id": new_id,
                "chapter": ch,
                "cd_id": None,
                "cd2_id": None,
                "name": o.get("caption") or f"Untitled {o['figure_id']}",
                "content_type": o["content_type"],
                "construction": "direct",
                "year_range": [
                    (o.get("year_range") or {}).get("start"),
                    (o.get("year_range") or {}).get("end"),
                ],
                "figures": [o["figure_id"]],
                "primary_appendix": o.get("appendix_reference"),
                "hdarp_sources": o.get("hdarp_table_sources") or [],
                "cd2_source_file": None,
                "note": "ORPHAN — no CD linkage; needs Phase 3 research to confirm series identity",
            }
        )

    return {
        "schema_version": "rscd-series-candidates-v1.0",
        "generated_by": "_phase2_taxonomy_builder.py",
        "total_candidates": len(candidates),
        "by_chapter": _count_by(candidates, "chapter"),
        "by_content_type": _count_by(candidates, "content_type"),
        "by_construction": _count_by(candidates, "construction"),
        "candidates": candidates,
    }, cd_to_rscd


def _name_from_figures(figs: list[dict]) -> str:
    caps = [f.get("caption") for f in figs if f.get("caption")]
    if not caps:
        return "Untitled"
    # Use the shortest caption as the canonical name
    return min(caps, key=len)


def _infer_construction(cd2_detail: dict) -> str:
    """direct | formula | composite — best-guess from CD2 metadata."""
    subs = cd2_detail.get("subseries", {})
    if not subs:
        return "direct"
    if len(subs) >= 3:
        return "composite"
    return "direct"


def _most_common(items):
    if not items:
        return None
    c = defaultdict(int)
    for i in items:
        c[i] += 1
    return max(c, key=c.get)


def _dedup_hdarp_sources(figs: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for f in figs:
        for src in f.get("hdarp_table_sources") or []:
            key = src.get("source"), tuple(src.get("tables", []))
            if key in seen:
                continue
            seen.add(key)
            out.append(src)
    return out


def _count_by(items, field) -> dict:
    c = defaultdict(int)
    for it in items:
        c[str(it.get(field))] += 1
    return dict(sorted(c.items()))


# ---- Crosswalks ------------------------------------------------------------


def write_cd2_crosswalk(cd_to_rscd: dict[str, str], cd2_registry: dict, candidates: list[dict]):
    """For every CD2 series ID, find the matching new RSCD ID (or 'unmapped')."""
    path = MIGR / "CD2_to_RSCD_crosswalk.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    rscd_to_cand = {c["new_id"]: c for c in candidates}
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cd2_id", "cd2_name", "cd2_chapter", "rscd_id", "rscd_name", "status", "notes"])
        for cd2_sid, detail in cd2_registry.get("series", {}).items():
            new_id = cd_to_rscd.get(cd2_sid)
            if new_id:
                cand = rscd_to_cand.get(new_id, {})
                status = "mapped"
                notes = ""
            else:
                cand = {}
                status = "unmapped"
                notes = "no figure linkage found in CD HDARP_SERIES_LINKAGE.json"
            w.writerow(
                [
                    cd2_sid,
                    detail.get("name", ""),
                    detail.get("chapter", ""),
                    new_id or "",
                    cand.get("name", ""),
                    status,
                    notes,
                ]
            )
    return path


def write_cd_crosswalk(cd_to_rscd: dict[str, str], linkage: dict):
    """For every CD series ID seen in linkage, the matching new RSCD ID."""
    path = MIGR / "CD_to_RSCD_crosswalk.csv"
    path.parent.mkdir(parents=True, exist_ok=True)

    # Build CD ID → (name, figures) from linkage
    cd_series: dict[str, dict] = defaultdict(lambda: {"name": "", "figures": []})
    for fig_id, fig in linkage.get("figures", {}).items():
        for cd_sid in fig.get("linked_series", []):
            cd_series[cd_sid]["figures"].append(fig_id)
            for sd in fig.get("series_details", []):
                if sd.get("series_id") == cd_sid and not cd_series[cd_sid]["name"]:
                    cd_series[cd_sid]["name"] = sd.get("name", "")

    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cd_id", "cd_name", "figure_count", "rscd_id", "status"])
        for cd_sid, info in sorted(cd_series.items()):
            new_id = cd_to_rscd.get(cd_sid)
            w.writerow(
                [
                    cd_sid,
                    info["name"],
                    len(info["figures"]),
                    new_id or "",
                    "mapped" if new_id else "unmapped",
                ]
            )
    return path


# ---- Driver ----------------------------------------------------------------


def main():
    print("Loading CD FIGURE_MASTER_v4.json ...")
    fm = load_figure_master()
    print(f"  -> {len(fm.get('figures', []))} figures")

    print("Loading CD HDARP_SERIES_LINKAGE.json ...")
    linkage = load_linkage()
    print(f"  -> {len(linkage.get('figures', {}))} linked figures")

    print("Loading CD2 series_registry.json ...")
    cd2_reg = load_cd2_registry()
    print(f"  -> {len(cd2_reg.get('series', {}))} CD2 series")

    DOCS_CH.mkdir(parents=True, exist_ok=True)
    MIGR.mkdir(parents=True, exist_ok=True)

    print("Building CHAPTER_FIGURE_TABLE_INDEX.json ...")
    ch_index = build_chapter_index(fm, linkage)
    (DOCS_CH / "CHAPTER_FIGURE_TABLE_INDEX.json").write_text(
        json.dumps(ch_index, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  -> {ch_index['total_chapters']} chapters, {ch_index['total_figures']} figures")

    print("Building SERIES_CANDIDATE_LIST.json ...")
    cands, cd_to_rscd = build_series_candidates(ch_index, cd2_reg)
    (DOCS_CH / "SERIES_CANDIDATE_LIST.json").write_text(
        json.dumps(cands, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  -> {cands['total_candidates']} candidates")
    print(f"     by chapter: {cands['by_chapter']}")
    print(f"     by content_type: {cands['by_content_type']}")

    print("Writing CD2_to_RSCD_crosswalk.csv ...")
    p = write_cd2_crosswalk(cd_to_rscd, cd2_reg, cands["candidates"])
    print(f"  -> {p}")

    print("Writing CD_to_RSCD_crosswalk.csv ...")
    p = write_cd_crosswalk(cd_to_rscd, linkage)
    print(f"  -> {p}")

    print("DONE.")


if __name__ == "__main__":
    main()
