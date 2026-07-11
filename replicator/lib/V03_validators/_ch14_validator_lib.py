"""Back-shim (A3 v3.1 layout): canonical impl relocated to ``validation._ch14_validator_lib``.

This module is intentionally a thin identity-alias so existing imports
(``from V03_validators._ch14_validator_lib import ...``) resolve unchanged. Do NOT add logic here;
edit ``validation/_ch14_validator_lib.py``. See lib/LAYOUT.md.
"""
import importlib as _il
import sys as _sys

_m = _il.import_module("validation._ch14_validator_lib")
_sys.modules[__name__] = _m
