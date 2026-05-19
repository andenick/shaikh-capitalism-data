"""RSCD Replicator entrypoint.

Runs the full Shaikh (2016) replication pipeline end-to-end:
    S00 setup → L01 load → P02 construct → V03 validate → O06 output

Produces 109 chopped CSVs + 109 extenbook XLSXs under data/final/.

Usage
-----
    # 1) Copy the API keys template and fill in FRED_API_KEY
    cp config/api_keys.env.example config/api_keys.env
    # edit config/api_keys.env

    # 2) Install deps in a clean venv
    python -m venv .venv
    .venv/Scripts/activate    # Windows  (source .venv/bin/activate on Unix)
    pip install -r requirements.txt

    # 3) Run
    python scripts/replicate.py --all              # all 118 series
    python scripts/replicate.py --series S201      # single series
    python scripts/replicate.py --health           # diagnostics only
    python scripts/replicate.py --list             # enumerate scripts

Notes
-----
- The replicator is a self-contained mirror of the canonical pipeline. It
  bundles SalvagedInputs/ (book chopped tables + extension benchmarks +
  figures reference) and the series registry so no external repo is needed.
- Raw API responses are cached under data/raw/ between runs.
- Processed intermediate frames go to data/processed/.
- Final chopped CSVs + extenbooks land in data/final/{chopped,extenbooks}/.
- Run time on a clean cache: ~45 min wall-clock for all 109 series (depends
  on FRED/BEA latency). Cached re-runs: ~5 min for validation+output only.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from pathlib import Path

# Resolve the replicator root and wire imports
REPLICATOR_ROOT = Path(__file__).resolve().parents[1]
LIB_DIR = REPLICATOR_ROOT / "lib"
INPUTS_BUNDLED = REPLICATOR_ROOT / "inputs_bundled"

sys.path.insert(0, str(LIB_DIR))


def _bootstrap_filesystem() -> Path:
    """Stand up a Technical/ tree that satisfies utils.paths assertions.

    The canonical pipeline expects PROJECT_ROOT.name == "RSCD" and a Technical/
    subtree with SalvagedInputs/ at PROJECT_ROOT level. We replicate that layout
    inside the replicator by creating a workdir/ that mimics the project root.
    """
    work = REPLICATOR_ROOT / "workdir" / "RSCD"
    technical = work / "Technical"
    technical.mkdir(parents=True, exist_ok=True)

    # Symlink-or-copy the lib/ to Technical/code/
    code_dst = technical / "code"
    if not code_dst.exists():
        try:
            os.symlink(LIB_DIR, code_dst, target_is_directory=True)
        except (OSError, NotImplementedError):
            shutil.copytree(LIB_DIR, code_dst)

    # Wire SalvagedInputs at PROJECT_ROOT
    salv_src = INPUTS_BUNDLED / "SalvagedInputs"
    salv_dst = work / "SalvagedInputs"
    if not salv_dst.exists():
        try:
            os.symlink(salv_src, salv_dst, target_is_directory=True)
        except (OSError, NotImplementedError):
            shutil.copytree(salv_src, salv_dst)

    # Empty Inputs/ (only needed for path assertions; CD/CD2 legacy not used)
    (work / "Inputs").mkdir(exist_ok=True)
    (work / "Outputs").mkdir(exist_ok=True)

    # Copy registries to Technical/ root
    for fname in (
        "series_registry.json",
        "SUBSOURCE_METADATA.json",
        "SERIES_CORRESPONDENCE_MATRIX.json",
        "PIPELINE_STATE.json",
        "ANU_LEDGER.json",
        "VALIDATION_REPORT.json",
    ):
        src = INPUTS_BUNDLED / fname
        dst = technical / fname
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

    # Stand up other Technical/ dirs the pipeline writes into
    for sub in ("Build", "chopped", "extenbooks", "research", "docs",
                "data/raw", "data/processed", "config",
                "MIGRATION", "tmp", "Handoffs"):
        (technical / sub).mkdir(parents=True, exist_ok=True)

    # KB stubs the path assertions check
    figures_ref = work / "SalvagedInputs" / "figures_reference"
    chap_idx = technical / "docs" / "chapters" / "CHAPTER_FIGURE_TABLE_INDEX.json"
    chap_idx.parent.mkdir(parents=True, exist_ok=True)
    if not chap_idx.exists():
        chap_idx.write_text("{}", encoding="utf-8")

    # Wire api_keys.env if user filled it in
    user_env = REPLICATOR_ROOT / "config" / "api_keys.env"
    cfg_dir = technical / "config"
    if user_env.exists():
        shutil.copy2(user_env, cfg_dir / "api_keys.env")
    # Also copy template
    tpl = REPLICATOR_ROOT / "config" / "api_keys.env.example"
    if tpl.exists():
        shutil.copy2(tpl, cfg_dir / "api_keys.env.template")

    return work


def _stage_final_outputs(technical: Path) -> dict:
    """After the pipeline finishes, copy chopped/extenbooks to data/final/."""
    final_root = REPLICATOR_ROOT / "data" / "final"
    chopped_dst = final_root / "chopped"
    exten_dst = final_root / "extenbooks"
    chopped_dst.mkdir(parents=True, exist_ok=True)
    exten_dst.mkdir(parents=True, exist_ok=True)

    n_chopped = 0
    src = technical / "chopped"
    if src.exists():
        for f in src.glob("*.csv"):
            shutil.copy2(f, chopped_dst / f.name)
            n_chopped += 1

    n_exten = 0
    src = technical / "extenbooks"
    if src.exists():
        for f in src.glob("*.xlsx"):
            shutil.copy2(f, exten_dst / f.name)
            n_exten += 1

    return {"chopped": n_chopped, "extenbooks": n_exten}


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="replicate.py",
        description="RSCD self-contained replicator")
    parser.add_argument("--all", action="store_true",
                        help="Run all 118 series end-to-end")
    parser.add_argument("--series", type=str, default=None,
                        help="Run a single series, e.g. S201")
    parser.add_argument("--health", action="store_true",
                        help="Diagnostics only")
    parser.add_argument("--list", action="store_true",
                        help="Enumerate pipeline scripts")
    parser.add_argument("--report", action="store_true",
                        help="Print validation summary")
    args = parser.parse_args()

    print("=" * 60)
    print("RSCD Replicator — Shaikh (2016) Replication v1.0")
    print("=" * 60)

    print("\n[1] Bootstrapping workspace ...")
    work = _bootstrap_filesystem()
    technical = work / "Technical"
    print(f"    PROJECT_ROOT: {work}")
    print(f"    Technical:    {technical}")

    # Import run.py from the bootstrapped tree so utils.paths resolves correctly
    import importlib.util
    run_path = technical / "code" / "run.py"
    spec = importlib.util.spec_from_file_location("rscd_run", run_path)
    if spec is None or spec.loader is None:
        print(f"FATAL: cannot import {run_path}")
        return 2
    # Make the run module's CODE_DIR refer to the bootstrapped tree
    sys.path.insert(0, str(technical / "code"))
    run_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run_mod)

    t0 = time.time()

    if args.list:
        return run_mod.cmd_list()
    if args.health:
        return run_mod.cmd_health()
    if args.report:
        return run_mod.cmd_report()

    if args.series:
        rc = run_mod.cmd_series(args.series)
        staged = _stage_final_outputs(technical)
        print(f"\nStaged {staged['chopped']} chopped CSVs + "
              f"{staged['extenbooks']} extenbooks to data/final/")
        print(f"Total wall-clock: {time.time() - t0:.1f}s")
        return rc

    if args.all:
        import json
        reg = json.loads((technical / "series_registry.json").read_text(encoding="utf-8"))
        # series_registry.json schema: {"series": {SID: {...}}, ...}
        sids = sorted(reg.get("series", {}).keys())
        print(f"\n[2] Running {len(sids)} series end-to-end ...")
        n_pass = n_fail = 0
        for sid in sids:
            print(f"\n--- {sid} ---")
            rc = run_mod.cmd_series(sid)
            if rc == 0:
                n_pass += 1
            else:
                n_fail += 1
        staged = _stage_final_outputs(technical)
        print(f"\n=== Replicator complete ===")
        print(f"  Series: {n_pass} PASS, {n_fail} FAIL of {len(sids)}")
        print(f"  Staged: {staged['chopped']} chopped + "
              f"{staged['extenbooks']} extenbooks -> data/final/")
        print(f"  Total wall-clock: {(time.time() - t0)/60:.1f} min")
        return 0 if n_fail == 0 else 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
