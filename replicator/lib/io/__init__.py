"""Canonical anu-replicator v3.1 shared-helpers package: ``lib/io/``.

Output writers surface. NB: the RSCD chopped/extenbook writers carry run()
and are dispatched by the orchestrator from lib/O06_output/, so they remain there;
this dir is a spec-conformance pointer (the name `io` also shadows the stdlib,
so it is not a live import package). See lib/LAYOUT.md.

See lib/LAYOUT.md for the RSCD reality -> v3.1 spec mapping. Modules here are the
canonical implementations; the historical per-phase paths keep byte-stable
back-shims for import compatibility.
"""
