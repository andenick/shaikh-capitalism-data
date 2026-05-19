"""P02_S404_construct — data_unavailable; no processed parquet written."""
from __future__ import annotations

SERIES_ID = "S404"


def run() -> dict:
    return {
        "status": "SKIPPED",
        "reason": "data_unavailable",
        "detail": "Inman 1995 underlying simulation not publicly tabulated; "
                  "no figure digitization. See S404_DPR.md §7 and §9.",
        "series_id": SERIES_ID,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
