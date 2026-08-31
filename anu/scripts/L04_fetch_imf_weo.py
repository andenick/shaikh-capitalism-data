"""Fetch IMF-served series (WEO current-account, IFS, monetary stats) used
by the Chapter 11 and external-study series.

Thin per-source entry point over the replicator; see anu/scripts/_common.py.
The heavy lifting (caching, per-series loaders) lives in code/ and runs
through replicator/scripts/replicate.py.
"""
from __future__ import annotations

import _common

if __name__ == "__main__":
    raise SystemExit(_common.fetcher_cli("imf_weo"))
