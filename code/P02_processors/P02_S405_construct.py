"""P02_S405_construct — data_unavailable; no processed parquet written."""
from __future__ import annotations

SERIES_ID = "S405"


def run() -> dict:
    return {
        "status": "SKIPPED",
        "reason": "data_unavailable",
        "detail": "Inman 1995 fig. 4; same posture as S404.",
        "series_id": SERIES_ID,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
