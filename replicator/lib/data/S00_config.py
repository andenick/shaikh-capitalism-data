"""S00_config — load API keys and global runtime configuration.

Reads `Technical/config/api_keys.env` (gitignored) into the process environment
without overwriting variables already set. Provides helpers for the rest of the
pipeline to check key availability and degrade gracefully.

Pattern: all loaders use `S00_config.have_key('FRED_API_KEY')` instead of bare
`os.environ.get(...)` so that the degradation path is centralized and consistent.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from utils.paths import CONFIG_DIR

KEYS_FILE = CONFIG_DIR / "api_keys.env"
KEYS_TEMPLATE = CONFIG_DIR / "api_keys.env.template"

KNOWN_KEYS = ("FRED_API_KEY", "BEA_API_KEY", "BLS_API_KEY")

_loaded = False


def load(force: bool = False) -> None:
    """Load api_keys.env into os.environ (no overwrite). Idempotent unless force=True."""
    global _loaded
    if _loaded and not force:
        return
    if KEYS_FILE.exists():
        for raw in KEYS_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            if v and not os.environ.get(k):
                os.environ[k] = v
    _loaded = True


def have_key(name: str) -> bool:
    """True iff `name` is set to a non-empty string in os.environ."""
    load()
    return bool(os.environ.get(name, "").strip())


def get_key(name: str) -> Optional[str]:
    """Return the key value or None if missing/empty."""
    load()
    v = os.environ.get(name, "").strip()
    return v or None


def status() -> dict:
    """Report which known keys are present."""
    load()
    return {k: bool(os.environ.get(k, "").strip()) for k in KNOWN_KEYS}


def install_template_if_missing() -> bool:
    """If api_keys.env does not exist but the template does, copy template to .env.

    Returns True iff a copy was made. Used by --health to bootstrap new clones.
    """
    if KEYS_FILE.exists():
        return False
    if not KEYS_TEMPLATE.exists():
        return False
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    KEYS_FILE.write_text(KEYS_TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    return True


if __name__ == "__main__":
    print("Config status:")
    for k, present in load().items():
        print(f"  {k}: {'SET' if present else 'MISSING'}")
