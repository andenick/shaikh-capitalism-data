"""S00_cache — on-disk Parquet cache for API responses.

Cache key: SHA-256 of canonical JSON of the query dict, scoped by `source` name.
Storage: `Technical/data/raw/api_cache/<source>/<hash>.parquet` plus a sibling
`<hash>.meta.json` carrying TTL/fetched_at/etag.

Cache invalidation policy
-------------------------
- Default TTL: 30 days. Data from official statistical agencies (FRED, BEA, BLS)
  is revised but not deleted, so a 30-day stale window is acceptable for routine
  pipeline runs.
- A caller may pass `ttl_days=0` to force a fresh fetch (used by `--refresh`).
- A caller may pass `ttl_days=None` to disable expiry entirely (used for static
  historical series like Shaikh's chopped tables — never expire).
- When TTL expires, `get()` returns None so the loader re-fetches; the old file
  is overwritten on `put()`.
- Concurrency: this is single-process. Multi-agent runs should use --series
  partitioning, not shared cache writes on the same key.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import pandas as pd

from utils.paths import DATA_RAW

CACHE_ROOT = DATA_RAW / "api_cache"
DEFAULT_TTL_DAYS = 30


def _hash_query(query: dict[str, Any]) -> str:
    """Stable hash over canonical JSON of the query dict."""
    canon = json.dumps(query, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:32]


def _paths(source: str, query: dict) -> tuple[Path, Path]:
    h = _hash_query(query)
    base = CACHE_ROOT / source
    base.mkdir(parents=True, exist_ok=True)
    return base / f"{h}.parquet", base / f"{h}.meta.json"


def is_fresh(meta_path: Path, ttl_days: Optional[int]) -> bool:
    """Check TTL. None means never expire."""
    if ttl_days is None:
        return True
    if not meta_path.exists():
        return False
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        fetched = datetime.fromisoformat(meta["fetched_at"])
        age_days = (datetime.now(timezone.utc) - fetched).total_seconds() / 86400.0
        return age_days <= ttl_days
    except Exception:
        return False


def get(source: str, query: dict, ttl_days: Optional[int] = DEFAULT_TTL_DAYS) -> Optional[pd.DataFrame]:
    """Return cached DataFrame if present and fresh; else None."""
    parquet_path, meta_path = _paths(source, query)
    if not parquet_path.exists():
        return None
    if not is_fresh(meta_path, ttl_days):
        return None
    try:
        return pd.read_parquet(parquet_path)
    except Exception:
        return None


def put(source: str, query: dict, df: pd.DataFrame, extra_meta: Optional[dict] = None) -> Path:
    """Write DataFrame + metadata to cache. Returns the parquet path."""
    parquet_path, meta_path = _paths(source, query)
    df.to_parquet(parquet_path, index=False)
    meta = {
        "source": source,
        "query": query,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "rows": int(len(df)),
        "columns": list(df.columns),
    }
    if extra_meta:
        meta.update(extra_meta)
    meta_path.write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")
    return parquet_path


def clear(source: Optional[str] = None) -> int:
    """Delete cached files. Returns number of files removed."""
    n = 0
    if source:
        d = CACHE_ROOT / source
        if d.exists():
            for f in d.iterdir():
                f.unlink()
                n += 1
    else:
        if CACHE_ROOT.exists():
            for sub in CACHE_ROOT.iterdir():
                if sub.is_dir():
                    for f in sub.iterdir():
                        f.unlink()
                        n += 1
    return n


if __name__ == "__main__":
    print(f"Cache root: {CACHE_ROOT}")
    print(f"Default TTL: {DEFAULT_TTL_DAYS} days")
