"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``transforms._ch7_xlsx_panels``.

This module is intentionally a thin identity-alias so existing imports
(``from L01_loaders._ch7_xlsx_panels import ...``) resolve unchanged. Do NOT add logic here;
edit ``transforms/_ch7_xlsx_panels.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("transforms._ch7_xlsx_panels")
_sys.modules[__name__] = _m
