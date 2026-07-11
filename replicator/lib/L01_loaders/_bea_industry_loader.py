"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``data._bea_industry_loader``.

This module is intentionally a thin identity-alias so existing imports
(``from L01_loaders._bea_industry_loader import ...``) resolve unchanged. Do NOT add logic here;
edit ``data/_bea_industry_loader.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("data._bea_industry_loader")
_sys.modules[__name__] = _m
