"""P01 — construct all (or selected) series end-to-end.

Delegates to the self-contained replicator, which boots a workspace, runs the
per-series S00 -> L01 -> P02 -> V03 -> O06 chain, and stages chopped CSVs and
extenbook workbooks under replicator/data/final/.

Usage
-----
    python anu/scripts/P01_construct_series.py --all            # 118 series, ~45 min
    python anu/scripts/P01_construct_series.py --series S201    # single series
    python anu/scripts/P01_construct_series.py --fetcher fred   # one source family
    python anu/scripts/P01_construct_series.py --list           # show plan
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common  # noqa: E402


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="P01_construct_series.py",
        description="Construct series through the replicator pipeline")
    parser.add_argument("--all", action="store_true",
                        help="run all series end-to-end")
    parser.add_argument("--series", type=str, default=None,
                        help="comma-separated series IDs, e.g. S201,S305")
    parser.add_argument("--fetcher", type=str, default=None,
                        choices=sorted(_common.FAMILIES),
                        help="run only series served by this source family")
    parser.add_argument("--limit", type=int, default=None,
                        help="run at most N series (smoke test)")
    parser.add_argument("--list", action="store_true",
                        help="show the plan and exit")
    args = parser.parse_args()

    registry = _common.load_registry()

    sids: list[str] = []
    if args.series:
        sids = [x.strip() for x in args.series.split(",") if x.strip()]
    elif args.fetcher:
        sids = [s["series_id"]
                for s in _common.series_for_fetcher(registry, args.fetcher)]
    elif args.all:
        sids = [s["series_id"] for s in registry["series"]]
    else:
        known = {s["series_id"] for s in registry["series"]}
        sids = [s for s in sids if s in known] if sids else []
        if not sids:
            parser.print_help()
            return 2

    if args.limit:
        sids = sids[: args.limit]

    if args.list:
        print(f"plan: {len(sids)} series")
        for sid in sids:
            print(" ", sid)
        return 0

    if args.all and len(sids) == registry["series_count"]:
        print(f"[P01] running replicator --all ({len(sids)} series)")
        return _common.run_replicator(all_series=True)

    n_pass = n_fail = 0
    failed: list[str] = []
    for sid in sids:
        print(f"\n=== [P01] {sid} ===")
        rc = _common.run_replicator(series=sid)
        if rc == 0:
            n_pass += 1
        else:
            n_fail += 1
            failed.append(sid)
    print(f"\n[P01] {n_pass} PASS, {n_fail} FAIL of {len(sids)}")
    if failed:
        print("failed:", ", ".join(failed))
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
