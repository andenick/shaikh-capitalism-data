"""P02_S205_construct - pass-through Ayres monthly (1867-1902)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from P02_processors._ayres_processor import process  # noqa: E402


def run() -> dict:
    return process("S205", "S205_AYRES_1867_1902.parquet")


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
