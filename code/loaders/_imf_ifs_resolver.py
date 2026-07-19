"""
IMF IFS resolver — thin import shim (F-5A-03, RSCD v1.6 hygiene).

The canonical implementation lives at ``utils._imf_ifs_resolver`` (moved
2026-07-10). This shim re-exports the full public API so the four existing
importers (L01_S1504, L01_S1508, L01_S1509, V03_S1504) that use
``from loaders._imf_ifs_resolver import ...`` continue to resolve without
modification.

Do NOT add logic here. Edits go to ``utils/_imf_ifs_resolver.py``.
"""
from utils._imf_ifs_resolver import (  # noqa: F401
    LINE_TO_MODERN,
    FetchResult,
    resolve_ifs_line,
    describe_ifs_line,
    fetch_ifs_series,
    validate_against_shaikh,
)

__all__ = [
    "LINE_TO_MODERN",
    "FetchResult",
    "resolve_ifs_line",
    "describe_ifs_line",
    "fetch_ifs_series",
    "validate_against_shaikh",
]
