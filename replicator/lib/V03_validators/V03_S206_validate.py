"""V03_S206_validate - Ayres 1903-1939 (Fig 2.4C)."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from V03_validators._ayres_validator import validate  # noqa: E402


def run() -> dict:
    return validate("S206", 1903, 1939)


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
