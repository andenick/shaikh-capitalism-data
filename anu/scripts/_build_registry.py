"""Generate anu/series_registry.json from the repo's canonical registries.

Single source of truth: the repository-root ``series_registry.json`` and
``SUBSOURCE_METADATA.json``. This script derives the public anu-package
registry (template schema 1.0) from them; it never edits the canonical files.

Run from anywhere inside the repo:
    python anu/scripts/_build_registry.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common  # noqa: E402


def classify_subsource(meta: dict, subsource_id: str) -> str:
    """Map a subsource to a fetcher family (key of _common.FAMILIES)."""
    url = (meta.get("url") or "").lower()
    rm = (meta.get("retrieval_method") or "").lower()
    agency = (meta.get("agency") or "").lower()
    blob = " ".join([url, rm, agency, subsource_id.lower()])

    if ("fred.stlouisfed.org" in url or subsource_id.startswith("FRED_")
            or "via fred" in blob or "fredgraph" in blob
            or re.search(r"\bfred\b", rm)):
        return "fred"
    if ("apps.bea.gov" in url or "bea.gov" in url
            or (subsource_id.startswith("BEA_")
                and any(k in rm for k in ("api", "itable", "live")))):
        return "bea_api"
    if "worldbank" in blob.replace(" ", "") or subsource_id.startswith("WB_"):
        return "worldbank"
    if (re.search(r"\bimf\b", blob) or "imf.org" in url
            or "international monetary fund" in agency
            or subsource_id.startswith("IMF_")):
        return "imf_weo"
    if ("census.gov" in url or "census bureau" in agency
            or subsource_id.startswith("CENSUS_")):
        return "census_ft900"
    if "shiller" in blob or subsource_id.startswith("SHILLER_"):
        return "shiller"
    if "damodaran" in blob or subsource_id.startswith("DAMODARAN_"):
        return "damodaran"
    # Bundled / offline inputs (book-period chopped tables, scans, transcriptions)
    return "bundled"


def script_for(phase_dir: Path, prefix: str, sid: str) -> str | None:
    """Exact per-series script path for a phase, or None if absent."""
    p = phase_dir / f"{prefix}_{sid}.py"
    if p.exists():
        return f"code/{phase_dir.name}/{p.name}"
    # longest-suffix variant e.g. P02_S201012_x.py — match any with _{sid}_
    hits = sorted(phase_dir.glob(f"{prefix}_{sid}_*.py"))
    if hits:
        return f"code/{phase_dir.name}/{hits[0].name}"
    return None


def primary_source(series: dict, subs: dict) -> dict:
    """Best single 'source' block for a series (template schema)."""
    subseries = series.get("subseries") or {}
    pick = None
    for role in ("book_primary", "book_secondary", "primary", "extension"):
        for sub in subseries.values():
            if sub.get("role") == role:
                pick = sub
                break
        if pick:
            break
    if pick is None and subseries:
        pick = next(iter(subseries.values()))
    if pick is None:
        return {"name": "internal construction (no external source)",
                "url": None, "retrieved": None, "license": None}

    meta = subs.get(pick.get("subsource_id"), {})
    return {
        "name": pick.get("source") or meta.get("full_title") or "unnamed source",
        "url": pick.get("source_url") or meta.get("url"),
        "retrieved": None,  # filled at top level (single retrieval epoch)
        "license": meta.get("license"),
    }


def transformations(series: dict) -> list[str]:
    ops = []
    for step in series.get("construction_steps") or []:
        op = step.get("op")
        if op and op not in ops:
            ops.append(op)
    return ops


def main() -> int:
    root_reg = json.loads(_common.ROOT_REGISTRY.read_text(encoding="utf-8"))
    sm = json.loads((_common.REPO_ROOT / "SUBSOURCE_METADATA.json")
                    .read_text(encoding="utf-8"))
    subs = sm["subsources"]

    l01_dir = _common.REPO_ROOT / "code" / "L01_loaders"
    p02_dir = _common.REPO_ROOT / "code" / "P02_processors"
    v03_dir = _common.REPO_ROOT / "code" / "V03_validators"

    out_series = []
    for sid in sorted(root_reg["series"]):
        s = root_reg["series"][sid]

        fetchers: list[str] = []
        for sub in (s.get("subseries") or {}).values():
            ssid = sub.get("subsource_id")
            fam = classify_subsource(subs.get(ssid, {}), ssid or "")
            if fam not in fetchers:
                fetchers.append(fam)

        yr = s.get("year_range") or [None, None]
        yrb = s.get("year_range_book") or [None, None]
        yre = s.get("year_range_extension") or [None, None]

        scripts = []
        for d, prefix in ((l01_dir, "L01"), (p02_dir, "P02"), (v03_dir, "V03")):
            rel = script_for(d, prefix, sid)
            if rel:
                scripts.append(rel)

        description = s.get("name", "")
        figures = s.get("figures") or []
        chapter = s.get("chapter")
        if figures:
            description += f" Underlies {', '.join(figures)} in Shaikh (2016)."
        if sid.startswith("XS"):
            description += " External-study series (XS)."
        elif chapter:
            description += f" Chapter {chapter}."

        out_series.append({
            "series_id": sid,
            "title": s.get("display_name") or s.get("name") or sid,
            "description": description.strip(),
            "source": primary_source(s, subs),
            "construction": {
                "method": s.get("construction", "direct"),
                "scripts": scripts,
                "fetchers": fetchers,
                "transformations": transformations(s),
            },
            "units": s.get("units"),
            "frequency": "annual",
            "coverage": {
                "start": yr[0],
                "end": yr[1],
                "book_period": yrb,
                "extension_period": yre,
            },
            "producible": (_common.CHOPPED_REFERENCE / f"{sid}.csv").exists(),
            "documentation": {
                "dpr": f"docs/series/{sid}_DPR.md",
                "epr": f"docs/series/{sid}_EPR.md",
            },
            "quality": {
                "status": s.get("status"),
                "notes": (s.get("notes") or "") or None,
            },
        })

    n_producible = sum(1 for s in out_series if s["producible"])
    fetched_epoch = sm.get("last_updated") or sm.get("generated_at")

    registry = {
        "schema_version": "1.0",
        "project": "shaikh-capitalism-data",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "anu/scripts/_build_registry.py",
        "derived_from": {
            "series_registry": "series_registry.json (canonical, repo root)",
            "subsource_metadata": "SUBSOURCE_METADATA.json",
            "source_retrieved_epoch": fetched_epoch,
        },
        "series_count": len(out_series),
        "producible_series_count": n_producible,
        "fetcher_inventory": {
            fam["script"]: sum(
                1 for s in out_series if f in s["construction"]["fetchers"]
            )
            for f, fam in _common.FAMILIES.items()
        },
        "series": out_series,
    }

    text = json.dumps(registry, indent=1, ensure_ascii=False)
    # Defense-in-depth: no workspace paths may ship in the generated registry.
    for token in ("D:\\\\", "D:/", "/Arcanum/", "\\\\Arcanum", "D:\\Arcanum"):
        if token in text:
            raise SystemExit(f"workspace path token leaked into registry: {token!r}")

    _common.ANU_REGISTRY.write_text(text + "\n", encoding="utf-8")
    print(f"wrote anu/series_registry.json: {len(out_series)} series, "
          f"{n_producible} producible")
    for script, n in registry["fetcher_inventory"].items():
        print(f"  {script:<32} {n:>3} series")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
