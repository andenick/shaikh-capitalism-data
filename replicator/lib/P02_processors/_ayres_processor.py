"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``transforms._ayres_processor``.

This module is intentionally a thin identity-alias so existing imports
(``from P02_processors._ayres_processor import ...``) resolve unchanged. Do NOT add logic here;
edit ``transforms/_ayres_processor.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("transforms._ayres_processor")
_sys.modules[__name__] = _m
