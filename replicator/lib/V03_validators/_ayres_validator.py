"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``validation._ayres_validator``.

This module is intentionally a thin identity-alias so existing imports
(``from V03_validators._ayres_validator import ...``) resolve unchanged. Do NOT add logic here;
edit ``validation/_ayres_validator.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("validation._ayres_validator")
_sys.modules[__name__] = _m
