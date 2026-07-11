"""ALFRED vintage-manifest helper (SI-1, Block G1).

Optional read-only accessor over ``config/VINTAGE_MANIFEST.json``. Loaders MAY
consult this to discover the pinned ALFRED realtime vintage for a series x FRED-id
(the follow-up ALFRED fetch migration will use it); nothing in this pass forces a
loader to change its data.

    from utils.vintage_manifest import realtime_pin, fred_ids_for, live_fred_series

    realtime_pin("S1401", "GDP")   # -> "2026-07-02"
    fred_ids_for("S1002")          # -> ["AAA", "PPIACO"]
"""
from __future__ import annotations

import json
import warnings
from functools import lru_cache
from pathlib import Path

_MANIFEST = (
    Path(__file__).resolve().parents[2] / "config" / "VINTAGE_MANIFEST.json"
)


@lru_cache(maxsize=1)
def load() -> dict:
    """Parse and cache VINTAGE_MANIFEST.json."""
    if not _MANIFEST.exists():
        raise FileNotFoundError(f"VINTAGE_MANIFEST.json not found at {_MANIFEST}")
    with _MANIFEST.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def series_entry(series_id: str) -> dict | None:
    """Return the manifest block for a series, or None if absent."""
    return load().get("series", {}).get(series_id)


def fred_ids_for(series_id: str) -> list[str]:
    """Return the FRED ids registered for a series ([] if none / not present)."""
    entry = series_entry(series_id)
    if not entry:
        return []
    return [f["id"] for f in entry.get("fred_ids", [])]


def _fred_record(series_id: str, fred_id: str) -> dict | None:
    entry = series_entry(series_id)
    if not entry:
        return None
    for f in entry.get("fred_ids", []):
        if f["id"] == fred_id:
            return f
    return None


def realtime_pin(series_id: str, fred_id: str) -> str | None:
    """Return the ALFRED realtime pin date for a series x FRED-id, or None."""
    rec = _fred_record(series_id, fred_id)
    return rec.get("alfred_realtime_pin") if rec else None


def retrieval_date(series_id: str, fred_id: str) -> str | None:
    """Return the retrieval date of the currently-shipped data for series x FRED-id."""
    rec = _fred_record(series_id, fred_id)
    return rec.get("retrieval_date") if rec else None


def realtime_window(series_id: str, fred_id: str) -> tuple[str | None, str | None]:
    """Resolve the ALFRED realtime window ``(start, end)`` for a series x FRED-id.

    This is the ONE shared pin-resolution point used by every live-FRED L01
    loader (SI-1 follow-up). When a manifest pin exists it returns
    ``(pin, pin)`` so ``S00_apis.fred_observations`` fetches the vintage as-of
    that date (reproducing the shipped figures). When NO pin exists it emits an
    explicit ``RuntimeWarning`` and returns ``(None, None)`` — the caller then
    falls back to the LATEST vintage, which is NOT reproducible. A new live-FRED
    extension that forgets to register a pin will therefore warn loudly rather
    than silently ship unpinned.
    """
    pin = realtime_pin(series_id, fred_id)
    if pin is None:
        warnings.warn(
            f"[VINTAGE_MANIFEST] No ALFRED pin for ({series_id!r}, {fred_id!r}); "
            f"fetching LATEST vintage from FRED — this fetch is NOT reproducible. "
            f"Register the pair in config/VINTAGE_MANIFEST.json to pin a vintage.",
            RuntimeWarning,
            stacklevel=2,
        )
        return (None, None)
    return (pin, pin)


def vintage_policy(series_id: str) -> str | None:
    """Return the vintage_policy for a series, or None."""
    entry = series_entry(series_id)
    return entry.get("vintage_policy") if entry else None


def live_fred_series() -> set[str]:
    """Series that make a live FRED fetch (excludes salvaged_baked_no_live_fetch)."""
    out = set()
    for sid, entry in load().get("series", {}).items():
        if entry.get("vintage_policy") == "salvaged_baked_no_live_fetch":
            continue
        if entry.get("fred_ids"):
            out.add(sid)
    return out


def all_pairs() -> set[tuple[str, str]]:
    """All (series_id, fred_id) pairs recorded in the manifest."""
    out = set()
    for sid, entry in load().get("series", {}).items():
        for f in entry.get("fred_ids", []):
            out.add((sid, f["id"]))
    return out
