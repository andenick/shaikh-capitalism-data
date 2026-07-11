"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``data.S00_apis``.

This module is intentionally a thin identity-alias so existing imports
(``from S00_setup.S00_apis import ...``) resolve unchanged. Do NOT add logic here;
edit ``data/S00_apis.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("data.S00_apis")
_sys.modules[__name__] = _m
