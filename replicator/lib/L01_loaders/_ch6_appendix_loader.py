"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``data._ch6_appendix_loader``.

This module is intentionally a thin identity-alias so existing imports
(``from L01_loaders._ch6_appendix_loader import ...``) resolve unchanged. Do NOT add logic here;
edit ``data/_ch6_appendix_loader.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("data._ch6_appendix_loader")
_sys.modules[__name__] = _m
