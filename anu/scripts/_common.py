"""Shared machinery for the anu/ replication-package scripts.

Everything here resolves paths relative to the repository root (the directory
containing ``series_registry.json`` and ``replicator/``). No absolute paths,
no environment-specific configuration.

The anu/ scripts are a thin, per-source orchestration layer over the
self-contained runner in ``replicator/scripts/replicate.py``. They add:

- per-source fetch entry points (L01..L08) driven by ``anu/series_registry.json``
- package-level construction and output staging (P01, P02)
- a package-level validation gate (V01)

They deliberately do NOT duplicate any fetch or construction logic; the
canonical per-series loaders/processors/validators live in ``code/`` and are
executed through the replicator's bootstrapped workspace.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
ANU_ROOT = REPO_ROOT / "anu"
REPLICATOR = REPO_ROOT / "replicator" / "scripts" / "replicate.py"
ROOT_REGISTRY = REPO_ROOT / "series_registry.json"
ANU_REGISTRY = ANU_ROOT / "series_registry.json"
CHOPPED_REFERENCE = REPO_ROOT / "chopped"          # shipped reference output
ANU_FINAL = ANU_ROOT / "data" / "final" / "chopped"  # produced by P01+P02


# --------------------------------------------------------------------------
# Source families -> fetcher scripts
# --------------------------------------------------------------------------

FAMILIES: dict[str, dict[str, Any]] = {
    "fred": {
        "script": "L01_fetch_fred.py",
        "name": "FRED (Federal Reserve Economic Data, St. Louis Fed)",
        "key": "FRED_API_KEY",
        "keyless": "works keyless via fredgraph CSV for many series",
    },
    "bea_api": {
        "script": "L02_fetch_bea.py",
        "name": "BEA API (NIPA, Fixed Assets, GDP-by-Industry, Input-Output)",
        "key": "BEA_API_KEY",
        "keyless": "not keyless; free registration",
    },
    "worldbank": {
        "script": "L03_fetch_worldbank.py",
        "name": "World Bank Open Data API",
        "key": None,
        "keyless": "open, no key required",
    },
    "imf_weo": {
        "script": "L04_fetch_imf_weo.py",
        "name": "IMF (World Economic Outlook / IFS / Monetary Financial Stats)",
        "key": None,
        "keyless": "open, no key required",
    },
    "census_ft900": {
        "script": "L05_fetch_census_ft900.py",
        "name": "U.S. Census Bureau FT-900 foreign trade releases",
        "key": None,
        "keyless": "open, no key required",
    },
    "shiller": {
        "script": "L06_fetch_shiller.py",
        "name": "Robert Shiller (Yale) online data library",
        "key": None,
        "keyless": "open, no key required",
    },
    "damodaran": {
        "script": "L07_fetch_damodaran.py",
        "name": "Aswath Damodaran (NYU Stern) posted datasets",
        "key": None,
        "keyless": "open, no key required",
    },
    "bundled": {
        "script": "L08_load_bundled_inputs.py",
        "name": "Bundled book-period inputs (SalvagedInputs)",
        "key": None,
        "keyless": "offline; shipped inside the repo",
    },
}


def load_registry() -> dict:
    """Load the anu package registry (generated; see _build_registry.py)."""
    if not ANU_REGISTRY.exists():
        raise SystemExit(
            f"anu/series_registry.json not found. Generate it first:\n"
            f"    python anu/scripts/_build_registry.py"
        )
    return json.loads(ANU_REGISTRY.read_text(encoding="utf-8"))


def series_for_fetcher(registry: dict, family: str) -> list[dict]:
    """Series entries whose construction involves the given source family."""
    out = []
    for s in registry["series"]:
        fetchers = s.get("construction", {}).get("fetchers", [])
        if family in fetchers:
            out.append(s)
    return out


def api_key_status(family: str) -> str:
    """Report whether the API key for a family is configured."""
    fam = FAMILIES[family]
    key = fam.get("key")
    if key is None:
        return "no key required"
    env_file = REPO_ROOT / "replicator" / "config" / "api_keys.env"
    if os.environ.get(key):
        return f"{key}: set in environment"
    if env_file.exists():
        text = env_file.read_text(encoding="utf-8", errors="replace")
        if re.search(rf"^\s*{key}\s*=\s*\S", text, flags=re.M):
            return f"{key}: set in replicator/config/api_keys.env"
    return f"{key}: MISSING (copy replicator/config/api_keys.env.example -> replicator/config/api_keys.env)"


def run_replicator(series: Optional[str] = None, all_series: bool = False) -> int:
    """Run the self-contained replicator for one series or all series."""
    cmd = [sys.executable, str(REPLICATOR)]
    if all_series:
        cmd.append("--all")
    elif series:
        cmd += ["--series", series]
    else:
        cmd.append("--health")
    return subprocess.call(cmd, cwd=str(REPO_ROOT))


def fetcher_cli(family: str) -> int:
    """Standard CLI for an L## per-source fetcher.

    Default  : print the source dossier (what it serves, key status).
    --list   : print the series IDs served by this source.
    --fetch  : actually fetch, by running the replicator per served series.
    """
    import argparse

    fam = FAMILIES[family]
    parser = argparse.ArgumentParser(
        prog=fam["script"],
        description=f"Fetch data served by {fam['name']}",
    )
    parser.add_argument("--list", action="store_true",
                        help="only list the series served by this source")
    parser.add_argument("--fetch", action="store_true",
                        help="fetch by running the replicator for each served series")
    parser.add_argument("--limit", type=int, default=None,
                        help="fetch at most N series (smoke tests)")
    args = parser.parse_args()

    registry = load_registry()
    served = series_for_fetcher(registry, family)

    print(f"=== {fam['script']} — {fam['name']} ===")
    print(f"Series served : {len(served)} of {len(registry['series'])}")
    print(f"Access        : {fam['keyless']}")
    print(f"Key status    : {api_key_status(family)}")
    print(f"Provenance    : see anu/dpr/ (per-source DPR) and SUBSOURCE_METADATA.json")

    if args.list or not args.fetch:
        for s in served:
            print(f"  {s['series_id']:>8}  {s['title']}")
        if not args.fetch:
            print("\n(dry run — pass --fetch to download through the pipeline)")
        return 0

    targets = served[: args.limit] if args.limit else served
    n_pass = n_fail = 0
    failed: list[str] = []
    for s in targets:
        sid = s["series_id"]
        print(f"\n--- {sid} ({s['title']}) ---")
        rc = run_replicator(series=sid)
        if rc == 0:
            n_pass += 1
        else:
            n_fail += 1
            failed.append(sid)
    print(f"\n{fam['script']}: {n_pass} PASS, {n_fail} FAIL of {len(targets)}")
    if failed:
        print("failed:", ", ".join(failed))
    return 1 if n_fail else 0
