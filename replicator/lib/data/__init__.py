"""Canonical anu-replicator v3.1 shared-helpers package: ``lib/data/``.

API/cache readers + source resolvers (FRED/BEA/BLS clients, response
cache, NIPA/IMF-IFS line resolvers, BEA-industry + ch6-appendix loaders).

See lib/LAYOUT.md for the RSCD reality -> v3.1 spec mapping. Modules here are the
canonical implementations; the historical per-phase paths keep byte-stable
back-shims for import compatibility.
"""
