"""Standalone runner for the Decision-0011 independent-anchor validation suite.

Runs ``_v03_anchor_lib.run_anchor_suite`` across every series carrying anchors,
plausibility rules, or a book->extension splice, and writes
``Technical/remediation_campaign/ANCHOR_SUITE_REPORT.json``.

This does NOT touch run.py's per-series flow. Per-series V03 wiring (individual
V03_<sid>.py files importing the lib) is a later wave; this wrapper lets the suite
be run on its own::

    python code/run_anchor_suite.py

Equivalent to::

    python code/V03_validators/_v03_anchor_lib.py --run
"""
from __future__ import annotations

import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))

from V03_validators._v03_anchor_lib import run_anchor_suite, _print_summary  # noqa: E402


def main() -> int:
    report = run_anchor_suite()
    _print_summary(report)
    s = report["summary"]
    # exit non-zero if any RED so CI / callers can gate on it
    return 1 if s["total_red_series"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
