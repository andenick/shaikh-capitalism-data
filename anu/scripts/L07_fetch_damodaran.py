"""Fetch Damodaran (NYU Stern) historical-return datasets (stocks, Baa
corporate bonds, long government bonds).

Thin per-source entry point over the replicator; see anu/scripts/_common.py.
The heavy lifting (caching, per-series loaders) lives in code/ and runs
through replicator/scripts/replicate.py.
"""
from __future__ import annotations

import _common

if __name__ == "__main__":
    raise SystemExit(_common.fetcher_cli("damodaran"))
