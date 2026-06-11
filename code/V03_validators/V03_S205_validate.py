"""V03_S205_validate - Ayres 1867-1902 (Fig 2.4B)."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from V03_validators._ayres_validator import validate  # noqa: E402


def run() -> dict:
    return validate("S205", 1867, 1902)


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
