"""L01_S404_load — Inman (1995) fig. 3 reproduction; data_unavailable.

S404 reproduces Shaikh's Fig 4.19 from Inman, R. R. (1995),
"Shape Characteristics of Cost Curves Involving Multiple Shifts in Automotive
Assembly Plants," The Engineering Economist 41(1), 53-67.

The underlying numerical simulation values are NOT publicly tabulated (figures
only) and the Taylor & Francis full text is paywalled. No salvaged dataset
exists. Per the chapter playbook's data_unavailable recipe and anti-fabrication
rules, we do NOT perform unauthorized figure digitization.

This loader returns SKIPPED. The processor and validator follow the same
posture; the extenbook is constructed from DPR+EPR+Sources only.
"""
from __future__ import annotations

SERIES_ID = "S404"
SOURCE_ID = "INMAN_1995_ENGINEERING_ECONOMIST"
REASON = (
    "Inman (1995, Engineering Economist 41(1), fig. 3) is paywalled and the "
    "underlying Monte-Carlo simulation values are not publicly tabulated. "
    "Anti-fabrication: no unauthorized figure digitization performed."
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
