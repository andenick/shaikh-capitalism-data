"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``transforms._ch7_industry_panel_processor``.

This module is intentionally a thin identity-alias so existing imports
(``from P02_processors._ch7_industry_panel_processor import ...``) resolve unchanged. Do NOT add logic here;
edit ``transforms/_ch7_industry_panel_processor.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("transforms._ch7_industry_panel_processor")
_sys.modules[__name__] = _m
