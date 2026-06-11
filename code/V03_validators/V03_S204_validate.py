"""V03_S204_validate - Ayres 1831-1866 (Fig 2.4A)."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from V03_validators._ayres_validator import validate  # noqa: E402


def run() -> dict:
    return validate("S204", 1831, 1866)


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
