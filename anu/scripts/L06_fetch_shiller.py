"""Fetch Shiller (Yale) datasets (ie_data long-run stock/home price series,
long interest rates, required-return constructions).

Thin per-source entry point over the replicator; see anu/scripts/_common.py.
The heavy lifting (caching, per-series loaders) lives in code/ and runs
through replicator/scripts/replicate.py.
"""
from __future__ import annotations

import _common

if __name__ == "__main__":
    raise SystemExit(_common.fetcher_cli("shiller"))
