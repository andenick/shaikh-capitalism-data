"""RSCD pipeline orchestrator.

CLI surface
-----------
    python run.py --list             enumerate all S00/L01/P02/V03/M04/A05/O06 scripts
    python run.py --health           check imports, API keys, registry parse, paths
    python run.py --series SID       run S00 + L01_{SID}_* -> P02_{SID}_* -> V03_{SID}_*
    python run.py --series SID --skip-validate
    python run.py --validate-only [--series SID]
    python run.py --report           print summary table from VALIDATION_REPORT.json

Phase discovery
---------------
The orchestrator walks each phase directory in order:
    code/S00_setup, code/L01_loaders, code/P02_processors,
    code/V03_validators, code/M04_manual, code/A05_analysis, code/O06_output

For each `.py` file (excluding `__init__.py` and files starting with `_`), it
imports the module and looks for a top-level `run()` function. If found, it
calls it. The return value (expected to be a dict) is appended to a per-run log.

For `--series SID`, files are filtered by a `SID_` substring in the basename
(e.g. `L01_S201_load.py` matches `--series S201`). S00 modules are always run
regardless of series filter (they are infrastructure).

A return dict like `{"status": "PASS"|"FAIL"|"OK"|"SKIPPED", ...}` is expected
from every `run()`; missing keys are tolerated but logged as warnings.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Optional

# Make sibling packages importable without installing
CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))

from utils import paths  # noqa: E402


PHASE_DIRS = [
    "S00_setup",
    "L01_loaders",
    "P02_processors",
    "V03_validators",
    "M04_manual",
    "A05_analysis",
    "O06_output",
]


def _discover(phase: str, series: Optional[str] = None) -> list[Path]:
    """Return sorted .py files in a phase dir, excluding __init__/private.

    Filename convention
    -------------------
    Per-series scripts encode the SID in the basename: `L01_{SID}_*.py`,
    `P02_{SID}_*.py`, etc. Series-generic scripts (e.g. O06 writers, A05
    cross-series analytics that walk multiple series) do NOT contain a SID
    pattern; they are matched on every series run and are expected to be
    idempotent / per-series-filterable internally if desired.
    """
    import re
    d = CODE_DIR / phase
    if not d.exists():
        return []
    sid_re = re.compile(r"_(S\d{3,4}|AS\d{3}|ES\d{4})_")  # _S201_, _S2010_, _AS101_, _ES2001_
    out = []
    for p in sorted(d.iterdir()):
        if p.suffix != ".py":
            continue
        if p.name == "__init__.py" or p.name.startswith("_"):
            continue
        if series is not None and phase != "S00_setup":
            has_any_sid = bool(sid_re.search(p.name))
            if has_any_sid:
                # script is for some series — must match the requested one
                if f"_{series}_" not in p.name and not p.name.startswith(f"{series}_"):
                    continue
            # else: series-generic script — always include
        out.append(p)
    return out


def _load_and_run(path: Path) -> dict:
    """Import a phase script and call its top-level run() if defined."""
    mod_name = f"_rscd_phase_{path.parent.name}_{path.stem}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        return {"status": "ERROR", "error": f"cannot load spec for {path}"}
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:
        return {"status": "ERROR", "error": f"import failed: {exc}",
                "traceback": traceback.format_exc()}
    if not hasattr(mod, "run"):
        return {"status": "SKIPPED", "reason": "no run() defined"}
    try:
        result = mod.run()
        if not isinstance(result, dict):
            result = {"status": "OK", "value": result}
        return result
    except Exception as exc:
        return {"status": "ERROR", "error": str(exc),
                "traceback": traceback.format_exc()}


def cmd_list() -> int:
    print("RSCD pipeline scripts:")
    for phase in PHASE_DIRS:
        files = _discover(phase)
        print(f"\n  [{phase}]  ({len(files)} script(s))")
        for f in files:
            print(f"    {f.name}")
    return 0


def cmd_health() -> int:
    print("=== RSCD health check ===")
    ok = True

    print("\n[1] Required paths")
    try:
        paths.assert_paths_exist()
        print("    OK — all required paths present")
    except Exception as exc:
        print(f"    FAIL — {exc}")
        ok = False

    print("\n[2] Python imports")
    try:
        import pandas, numpy, pyarrow, openpyxl, requests  # noqa: F401
        print("    OK — core deps importable")
    except Exception as exc:
        print(f"    FAIL — {exc}")
        ok = False

    print("\n[3] Registry parse")
    try:
        with paths.REGISTRY.open(encoding="utf-8") as fh:
            reg = json.load(fh)
        print(f"    OK — {reg.get('series_count', '?')} series in registry")
    except Exception as exc:
        print(f"    FAIL — {exc}")
        ok = False

    print("\n[4] API keys")
    try:
        from S00_setup import S00_config, S00_apis
        S00_config.install_template_if_missing()
        cfg = S00_config.status()
        for k, present in cfg.items():
            print(f"    {k}: {'SET' if present else 'MISSING (degradation will apply)'}")
        if cfg.get("FRED_API_KEY"):
            probe = S00_apis.fred_health()
            print(f"    FRED probe: {probe}")
    except Exception as exc:
        print(f"    FAIL — {exc}")
        ok = False

    print("\n[5] Phase script discovery")
    for phase in PHASE_DIRS:
        files = _discover(phase)
        print(f"    {phase}: {len(files)} script(s)")

    print("\n=== Result: " + ("HEALTHY" if ok else "ISSUES") + " ===")
    return 0 if ok else 1


def cmd_series(series: str, validate_only: bool = False, skip_validate: bool = False) -> int:
    print(f"=== RSCD pipeline: --series {series} ===")
    log: list[dict] = []
    overall = "PASS"
    t0 = time.time()

    phases = ["V03_validators"] if validate_only else PHASE_DIRS

    for phase in phases:
        if skip_validate and phase == "V03_validators":
            continue
        files = _discover(phase, series=None if phase == "S00_setup" else series)
        if not files:
            print(f"\n[{phase}] no scripts for {series}")
            continue
        print(f"\n[{phase}]")
        for path in files:
            t = time.time()
            print(f"  -> {path.name} ... ", end="", flush=True)
            result = _load_and_run(path)
            dt = time.time() - t
            status = result.get("status", "OK")
            print(f"{status}  ({dt:.1f}s)")
            if status in ("ERROR", "FAIL"):
                overall = "FAIL"
                # show concise error
                for k in ("error", "reason"):
                    if k in result:
                        print(f"     {k}: {result[k]}")
                if "traceback" in result:
                    # one indented line summary
                    last_line = result["traceback"].strip().splitlines()[-1]
                    print(f"     last: {last_line}")
            log.append({"phase": phase, "script": path.name, "elapsed_s": round(dt, 2), **result})

    total = time.time() - t0
    print(f"\n=== {series}: {overall} in {total:.1f}s ===")

    # Write per-run log
    log_dir = paths.TECHNICAL / "Build"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / "STEP_LOG.jsonl"
    with log_path.open("a", encoding="utf-8") as fh:
        for entry in log:
            fh.write(json.dumps({"series": series, **entry}, default=str) + "\n")

    return 0 if overall == "PASS" else 1


def cmd_report() -> int:
    rpt_path = paths.TECHNICAL / "VALIDATION_REPORT.json"
    if not rpt_path.exists():
        print("No VALIDATION_REPORT.json — run validators first.")
        return 1
    rpt = json.loads(rpt_path.read_text(encoding="utf-8"))
    print(f"=== VALIDATION_REPORT (generated {rpt.get('generated_at', '?')}) ===")
    print(f"{'SID':6}  {'STATUS':6}  {'MAE':>10}  {'MAX_ABS':>10}  {'N':>5}  notes")
    for sid, row in sorted(rpt.get("series", {}).items()):
        notes = ""
        if row.get("divergence_years"):
            notes = f"div={len(row['divergence_years'])}y"
        # mae/max_abs_err can be None for PASS_DATA_UNAVAILABLE rows; render '-'
        mae_str = "-" if row.get("mae") is None else f"{row.get('mae')}"
        max_abs_str = "-" if row.get("max_abs_err") is None else f"{row.get('max_abs_err')}"
        n_str = "-" if row.get("n_compared") is None else f"{row.get('n_compared')}"
        status = str(row.get("status", "?"))[:24]
        print(f"{sid:6}  {status:24}  {mae_str:>10}  {max_abs_str:>10}  {n_str:>5}  {notes}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="run.py", description="RSCD pipeline orchestrator")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--health", action="store_true")
    parser.add_argument("--series", type=str, default=None)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--skip-validate", action="store_true")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    if args.list:
        return cmd_list()
    if args.health:
        return cmd_health()
    if args.report:
        return cmd_report()
    if args.series:
        return cmd_series(args.series, validate_only=args.validate_only,
                          skip_validate=args.skip_validate)
    if args.validate_only:
        # No series specified — error
        print("--validate-only requires --series (full-batch validation not yet implemented)")
        return 2
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
