"""Load and query the series registry (single source of truth)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "config" / "registry.json"


def load() -> dict:
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


def series(reg: dict) -> dict:
    return reg.get("series", reg)


def get(reg: dict, series_id: str) -> dict:
    return series(reg).get(series_id, {})


def chapters(reg: dict) -> dict[int, list[str]]:
    ch: dict[int, list[str]] = {}
    for sid, entry in series(reg).items():
        c = entry.get("chapter", 0)
        ch.setdefault(c, []).append(sid)
    for v in ch.values():
        v.sort()
    return ch


def extension_config(reg: dict, series_id: str) -> dict | None:
    ext = get(reg, series_id).get("extension")
    return ext if isinstance(ext, dict) else None


def validation_config(reg: dict, series_id: str) -> dict:
    return get(reg, series_id).get("validation", {})


def subseries(reg: dict, series_id: str) -> dict:
    return get(reg, series_id).get("subseries", {})


def research(series_id: str) -> dict | None:
    path = ROOT / "data" / "inputs" / "research" / f"{series_id}_research.json"
    if not path.exists():
        path = ROOT.parent / "research" / f"{series_id}_research.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None
