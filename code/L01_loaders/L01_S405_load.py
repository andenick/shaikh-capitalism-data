"""L01_S405_load — Inman (1995) fig. 4 reproduction; data_unavailable.

S405 reproduces Shaikh's Fig 4.20 from Inman 1995, fig. 4 (marginal labor cost).
Same paywall + figures-only constraint as S404. Loader SKIPS.
"""
from __future__ import annotations

SERIES_ID = "S405"
SOURCE_ID = "INMAN_1995_ENGINEERING_ECONOMIST"
REASON = (
    "Inman (1995, Engineering Economist 41(1), fig. 4) paywalled; no tabulated "
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
