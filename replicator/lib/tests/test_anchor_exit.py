"""Smoke test for the F-6D-02 fix: `_v03_anchor_lib.py --run` must exit non-zero
when any anchor/splice/plausibility check is RED, and zero when all-GREEN.

Run standalone (no pytest needed):

    python code/tests/test_anchor_exit.py

Exit 0 = all assertions pass; exit 1 = a regression.

This test does NOT touch the registry or processed data — it exercises the CLI's
exit-code logic by monkeypatching ``run_anchor_suite`` to return synthetic reports,
so it is deterministic and offline.
"""
from __future__ import annotations

import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from V03_validators import _v03_anchor_lib as lib  # noqa: E402


def _run_main_with(report: dict) -> int:
    """Invoke lib.main() with argv=['--run'] and run_anchor_suite stubbed."""
    orig_suite = lib.run_anchor_suite
    orig_argv = sys.argv
    try:
        lib.run_anchor_suite = lambda *a, **k: report  # type: ignore[assignment]
        sys.argv = ["_v03_anchor_lib.py", "--run"]
        return lib.main()
    finally:
        lib.run_anchor_suite = orig_suite  # type: ignore[assignment]
        sys.argv = orig_argv


def _report(anchor_red=None, splice_red=None, plausibility_red=None) -> dict:
    anchor_red = anchor_red or []
    splice_red = splice_red or []
    plausibility_red = plausibility_red or []
    total = len(set(anchor_red) | set(splice_red) | set(plausibility_red))
    return {
        "summary": {
            "series_checked": 3,
            "anchor_red": anchor_red,
            "splice_red": splice_red,
            "plausibility_red": plausibility_red,
            "total_red_series": total,
        },
        "report_path": "(stub)",
    }


def main() -> int:
    failures = []

    # 1. All-GREEN -> exit 0
    rc = _run_main_with(_report())
    if rc != 0:
        failures.append(f"all-GREEN report should exit 0, got {rc}")

    # 2. anchor RED -> exit 1
    rc = _run_main_with(_report(anchor_red=["S214"]))
    if rc != 1:
        failures.append(f"anchor-RED report should exit 1, got {rc}")

    # 3. splice RED -> exit 1
    rc = _run_main_with(_report(splice_red=["S999"]))
    if rc != 1:
        failures.append(f"splice-RED report should exit 1, got {rc}")

    # 4. plausibility RED -> exit 1
    rc = _run_main_with(_report(plausibility_red=["S704"]))
    if rc != 1:
        failures.append(f"plausibility-RED report should exit 1, got {rc}")

    # 5. multiple/overlapping RED -> exit 1
    rc = _run_main_with(_report(anchor_red=["S214"], plausibility_red=["S214", "S704"]))
    if rc != 1:
        failures.append(f"multi-RED report should exit 1, got {rc}")

    if failures:
        print("FAIL: test_anchor_exit")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS: test_anchor_exit (5/5 assertions) — F-6D-02 exit-code propagation verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
