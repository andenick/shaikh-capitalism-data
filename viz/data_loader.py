"""
RSCD viz data loader.

Reads (READ-ONLY) from Technical/ artifacts:
    series_registry.json   - 118 series, subseries, content_type, year_range
    SUBSOURCE_METADATA.json - 134 subsource records (agency/url/license)
    VALIDATION_REPORT.json  - per-series V03 status + MAE
    chopped/{SID}.csv       - tidy long-format observations
    docs/series/{SID}_DPR.md - Data Provenance Record
    docs/series/{SID}_EPR.md - Extension Provenance Record
    SalvagedInputs/figures_reference/FIGURE_MASTER_v4.json - 205 book figures

All accessors are cached with @lru_cache for fast Dash callbacks.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

import pandas as pd

# ---------------------------------------------------------------------------
# Paths (mirrors Technical/code/utils/paths.py — keeps viz self-contained)
# ---------------------------------------------------------------------------

VIZ_DIR = Path(__file__).resolve().parent
TECHNICAL = VIZ_DIR.parent
PROJECT_ROOT = TECHNICAL.parent

REGISTRY_PATH = TECHNICAL / "series_registry.json"
SUBSOURCE_PATH = TECHNICAL / "SUBSOURCE_METADATA.json"
VALIDATION_PATH = TECHNICAL / "VALIDATION_REPORT.json"
LEDGER_PATH = TECHNICAL / "ANU_LEDGER.json"
CHOPPED_DIR = TECHNICAL / "chopped"
DOCS_SERIES = TECHNICAL / "docs" / "series"
FIGURE_MASTER = PROJECT_ROOT / "SalvagedInputs" / "figures_reference" / "FIGURE_MASTER_v4.json"
BUILD_DIR = TECHNICAL / "Build"


# ---------------------------------------------------------------------------
# Raw JSON readers (cached singletons)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_registry() -> dict:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_subsources() -> dict:
    with open(SUBSOURCE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("subsources", {})


@lru_cache(maxsize=1)
def load_validation() -> dict:
    with open(VALIDATION_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("series", {})


@lru_cache(maxsize=1)
def load_figure_master() -> dict:
    """Return a {figure_id: figure_record} dict (normalized from list or dict)."""
    if not FIGURE_MASTER.exists():
        return {}
    with open(FIGURE_MASTER, "r", encoding="utf-8") as f:
        data = json.load(f)
    raw = data.get("figures", {})
    if isinstance(raw, list):
        # Normalize list of figure records to dict keyed by figure_id
        normalized: dict = {}
        for entry in raw:
            if isinstance(entry, dict):
                fid = entry.get("figure_id")
                if fid:
                    normalized[fid] = entry
        return normalized
    return raw if isinstance(raw, dict) else {}


# ---------------------------------------------------------------------------
# Series accessors
# ---------------------------------------------------------------------------

def series_dict() -> dict:
    """Return {sid: registry_entry} dict."""
    return load_registry().get("series", {})


def series_ids_sorted() -> list[str]:
    return sorted(series_dict().keys())


def get_series(sid: str) -> Optional[dict]:
    return series_dict().get(sid)


def get_validation(sid: str) -> Optional[dict]:
    return load_validation().get(sid)


def get_figure(fig_id: str) -> Optional[dict]:
    return load_figure_master().get(fig_id)


# ---------------------------------------------------------------------------
# Chapter grouping (sidebar)
# ---------------------------------------------------------------------------

def chapter_groups() -> dict[str, dict]:
    """
    Return ordered dict of {group_key: {label, series: [sid,...]}}.
    Groups:
        ch_2 .. ch_17  (skip 12 if absent)
        es             (ES papers, chapter is None)
    """
    reg = series_dict()
    ext_groups = load_registry().get("external_study_groups", {})

    by_chapter: dict[str | int, list[str]] = {}
    for sid, meta in reg.items():
        ch = meta.get("chapter")
        if ch is None:
            # ES paper
            grp = meta.get("external_study_group", "ES")
            key = f"es_{grp}"
        else:
            key = f"ch_{ch}"
        by_chapter.setdefault(key, []).append(sid)

    # Sort each list
    for k in by_chapter:
        by_chapter[k].sort()

    # Build ordered groups
    groups: dict[str, dict] = {}
    chap_keys = sorted(
        [k for k in by_chapter if k.startswith("ch_")],
        key=lambda x: int(x.split("_")[1]),
    )
    for k in chap_keys:
        ch = k.split("_")[1]
        groups[k] = {
            "label": f"Chapter {ch}",
            "series": by_chapter[k],
        }
    # ES groups
    es_keys = sorted(
        [k for k in by_chapter if k.startswith("es_")],
        key=lambda x: x.split("_", 1)[1],
    )
    for k in es_keys:
        grp_id = k.split("_", 1)[1]
        ext_label = ext_groups.get(str(grp_id), f"External Study {grp_id}")
        # Truncate the label
        short = ext_label.split(" - ", 1)[0] if " - " in ext_label else ext_label
        groups[k] = {
            "label": f"ES {grp_id} — {short[:50]}",
            "series": by_chapter[k],
        }
    return groups


# ---------------------------------------------------------------------------
# Chopped CSV loader
# ---------------------------------------------------------------------------

@lru_cache(maxsize=256)
def load_chopped(sid: str) -> Optional[pd.DataFrame]:
    """
    Load a chopped CSV (tidy long format: year, value, subseries_id, source_id, units).
    Returns None if the CSV does not exist.
    """
    path = CHOPPED_DIR / f"{sid}.csv"
    if not path.exists():
        return None
    try:
        df = pd.read_csv(path)
    except Exception:
        return None
    if df.empty:
        return df
    # Coerce numeric for known columns
    for col in ("year", "value"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def chopped_exists(sid: str) -> bool:
    return (CHOPPED_DIR / f"{sid}.csv").exists()


# ---------------------------------------------------------------------------
# DPR / EPR loaders (markdown)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=256)
def load_dpr(sid: str) -> Optional[str]:
    path = DOCS_SERIES / f"{sid}_DPR.md"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


@lru_cache(maxsize=256)
def load_epr(sid: str) -> Optional[str]:
    path = DOCS_SERIES / f"{sid}_EPR.md"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Source / subsource helpers
# ---------------------------------------------------------------------------

def get_subsource(subsource_id: str) -> Optional[dict]:
    return load_subsources().get(subsource_id)


def series_subsources(sid: str) -> list[dict]:
    """
    Return enriched subsource records for a series. Each item:
        {subseries_id, subseries_name, role, period, units,
         subsource_id, agency, full_title, url, url_status, license, native_units}
    """
    meta = get_series(sid)
    if not meta:
        return []
    out = []
    for sub_id, sub in (meta.get("subseries") or {}).items():
        ssid = sub.get("subsource_id")
        ss = get_subsource(ssid) if ssid else None
        rec = {
            "subseries_id": sub_id,
            "subseries_name": sub.get("name", sub_id),
            "role": sub.get("role", ""),
            "period": sub.get("period"),
            "units": sub.get("units", ""),
            "native_units": sub.get("native_units", ""),
            "subsource_id": ssid or "",
            "source_url_from_sub": sub.get("source_url"),
            "agency": ss.get("agency") if ss else "",
            "full_title": ss.get("full_title") if ss else "",
            "url": (ss.get("url") if ss else None) or sub.get("source_url"),
            "url_status": ss.get("url_status") if ss else "",
            "license": ss.get("license") if ss else "",
            "publication_year": ss.get("publication_year") if ss else "",
            "color": sub.get("color"),
        }
        out.append(rec)
    return out


# ---------------------------------------------------------------------------
# Sanity helpers used by validate_app_data
# ---------------------------------------------------------------------------

def all_series_ids() -> list[str]:
    return list(series_dict().keys())


def chopped_series_ids() -> list[str]:
    """Series with an existing chopped CSV."""
    return [sid for sid in all_series_ids() if chopped_exists(sid)]
