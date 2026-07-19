"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``data._imf_ifs_resolver``.

This module is intentionally a thin identity-alias so existing imports
(``from utils._imf_ifs_resolver import ...``) resolve unchanged. Do NOT add logic here;
edit ``data/_imf_ifs_resolver.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("data._imf_ifs_resolver")
_sys.modules[__name__] = _m
