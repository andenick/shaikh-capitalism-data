"""L01_S406_load — Inman (1995) fig. 5 reproduction; data_unavailable.

S406 reproduces Shaikh's Fig 4.21 from Inman 1995, fig. 5 (average cost).
Same posture as S404.
"""
from __future__ import annotations

SERIES_ID = "S406"
SOURCE_ID = "INMAN_1995_ENGINEERING_ECONOMIST"
REASON = (
    "Inman (1995, Engineering Economist 41(1), fig. 5) paywalled; no tabulated "
    "underlying data; no unauthorized figure digitization performed."
)


def run() -> dict:
    return {
        "status": "SKIPPED",
        "reason": "data_unavailable",
        "detail": REASON,
        "source_id": SOURCE_ID,
        "series_id": SERIES_ID,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
