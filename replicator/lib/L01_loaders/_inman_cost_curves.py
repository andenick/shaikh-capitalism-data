"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``transforms._inman_cost_curves``.

This module is intentionally a thin identity-alias so existing imports
(``from L01_loaders._inman_cost_curves import ...``) resolve unchanged. Do NOT add logic here;
edit ``transforms/_inman_cost_curves.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("transforms._inman_cost_curves")
_sys.modules[__name__] = _m
