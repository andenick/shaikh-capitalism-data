"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``transforms._ayres_helper``.

This module is intentionally a thin identity-alias so existing imports
(``from L01_loaders._ayres_helper import ...``) resolve unchanged. Do NOT add logic here;
edit ``transforms/_ayres_helper.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("transforms._ayres_helper")
_sys.modules[__name__] = _m
