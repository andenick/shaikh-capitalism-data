"""RSCD pipeline orchestrator.

CLI surface
-----------
    python run.py --list             enumerate all S00/L01/P02/V03/M04/A05/O06 scripts
    python run.py --health           check imports, API keys, registry parse, paths
    python run.py --series SID       run S00 + L01_{SID}_* -> P02_{SID}_* -> V03_{SID}_*
    python run.py --series SID --skip-validate
    python run.py --validate-only [--series SID]
                                     with --series: validate one series;
                                     without: run the FULL 118-series V03 batch
                                     (continue-on-fail, regenerates VALIDATION_REPORT.json,
                                     non-zero exit if any FAIL)
    python run.py --gate             CI gate: anu-doctor + anchor suite + full V03 batch
                                     (non-zero exit on any FAIL or anchor RED)
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
(e.g. `L01_S201.py` matches `--series S201`). S00 modules are always run
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
    sid_re = re.compile(r"_(XS\d{3,4}|S\d{3,4}|AS\d{3}|ES\d{4})(?:_|\.)")  # _XS003_, _XS2001_, _S201_, _S2010_, _AS101_, _ES2001_ (XS first so _XS### matches before the S alternative)
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
                if (f"_{series}_" not in p.name and f"_{series}." not in p.name and not p.name.startswith(f"{series}_")):
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


def _validator_sid(path: Path) -> Optional[str]:
    """Extract the series id from a V03_<SID>.py validator filename."""
    import re
    m = re.match(r"^V03_(XS\d{3,4}|S\d{3,4}|AS\d{3}|ES\d{4})\.py$", path.name)
    return m.group(1) if m else None


def _regenerate_report(rows: dict[str, dict]) -> Path:
    """Write the per-series results into VALIDATION_REPORT.json.

    Each V03 ``run()`` return dict is the authoritative row for that series (this
    mirrors what the individual validators self-write, and additionally covers the
    handful that do NOT self-write — S703/S704/S801 — so a full batch REGENERATES
    the whole report and clears report-staleness, doctor P43/P41, F-3B-02).
    """
    rpt_path = paths.TECHNICAL / "VALIDATION_REPORT.json"
    if rpt_path.exists():
        rpt = json.loads(rpt_path.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt.setdefault("series", {})
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
    for sid, row in rows.items():
        row = dict(row)
        row.setdefault("validated_at", stamp)
        rpt["series"][sid] = row
    rpt["generated_at"] = stamp
    rpt["generated_by"] = "run.py --validate-only (full batch)"
    rpt_path.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")
    return rpt_path


def cmd_validate_batch() -> int:
    """Run every V03 validator (all series), continue-on-fail, regenerate the report.

    Dispatches over the same per-series validator path as ``--series SID
    --validate-only`` but for all 118 series in SID order. Prints a summary table
    and exits non-zero if any series is FAIL/ERROR.
    """
    vdir = CODE_DIR / "V03_validators"
    validators: list[tuple[str, Path]] = []
    for p in sorted(vdir.iterdir()):
        if p.suffix != ".py" or p.name.startswith("_") or p.name == "__init__.py":
            continue
        sid = _validator_sid(p)
        if sid:
            validators.append((sid, p))
    validators.sort(key=lambda t: t[0])

    print(f"=== RSCD validate-only: full batch ({len(validators)} series) ===")
    t0 = time.time()
    rows: dict[str, dict] = {}
    results: list[tuple[str, str, float]] = []
    fails: list[str] = []
    for sid, path in validators:
        t = time.time()
        result = _load_and_run(path)
        dt = time.time() - t
        status = str(result.get("status", "OK"))
        rows[sid] = result
        results.append((sid, status, dt))
        if status in ("ERROR", "FAIL"):
            fails.append(sid)
        print(f"  {sid:8} {status:24} ({dt:5.1f}s)")

    rpt_path = _regenerate_report(rows)

    # Summary table by status
    from collections import Counter
    counts = Counter(s for _, s, _ in results)
    total = time.time() - t0
    print("\n=== SUMMARY ===")
    for status, n in sorted(counts.items()):
        print(f"  {status:28} {n:3}")
    print(f"  {'TOTAL':28} {len(results):3}")
    print(f"\n  report regenerated: {rpt_path}")
    print(f"  wall-clock: {total:.1f}s")
    if fails:
        print(f"\n  FAIL/ERROR series ({len(fails)}): {', '.join(fails)}")
        print("=== BATCH: FAIL ===")
        return 1
    print("=== BATCH: PASS (all series non-FAIL) ===")
    return 0


def cmd_gate() -> int:
    """Aggregate CI gate: anu-doctor (check_project) + anchor suite + full V03 batch.

    Exit non-zero if ANY of the three reports a failure (doctor FAIL, anchor RED,
    or any V03 FAIL/ERROR). Doctor P24/P36/P42 etc. are reported honestly — the
    gate does NOT special-case pending-P4 failures.
    """
    import subprocess
    print("############################################################")
    print("# RSCD --gate : doctor + anchor suite + V03 batch")
    print("############################################################")
    project_root = paths.PROJECT_ROOT
    parts: dict[str, int] = {}

    # 1) anu-doctor (check_project) — canonical wrapper, text mode for exit code.
    print("\n----- [1/3] anu-doctor (check_project --project Technical) -----")
    import os
    # Resolve the framework doctor (check_project.py) from the ANU_DOCTOR env var
    # so no workspace-internal path is hard-coded (v1.6.1: ported from replicator/lib/run.py;
    # the previous hard-coded absolute path leaked a workspace path into the publish bundle).
    doctor_env = os.environ.get("ANU_DOCTOR", "")
    doctor_py = Path(doctor_env) if doctor_env else None
    if doctor_py is None or not doctor_py.is_file():
        print("    SKIPPED - anu-doctor not available "
              "(set ANU_DOCTOR=/path/to/check_project.py to enable).")
        parts["doctor"] = 0
    else:
        try:
            proc = subprocess.run(
                [sys.executable, str(doctor_py), "--project", "Technical"],
                cwd=str(project_root), capture_output=True, text=True, timeout=600,
            )
            sys.stdout.write(proc.stdout)
            if proc.stderr.strip():
                sys.stderr.write(proc.stderr)
            parts["doctor"] = proc.returncode
        except Exception as exc:
            print(f"    ERROR running doctor: {exc}")
            parts["doctor"] = 1

    # 2) anchor suite (Decision 0011) — RED -> non-zero.
    print("\n----- [2/3] anchor suite (Decision 0011) -----")
    try:
        from V03_validators._v03_anchor_lib import run_anchor_suite, _print_summary
        report = run_anchor_suite()
        _print_summary(report)
        n_red = report["summary"]["total_red_series"]
        parts["anchors"] = 1 if n_red else 0
    except Exception as exc:
        print(f"    ERROR running anchor suite: {exc}")
        parts["anchors"] = 1

    # 3) full V03 batch (also regenerates the report).
    print("\n----- [3/3] V03 full batch -----")
    parts["v03_batch"] = cmd_validate_batch()

    # Aggregate
    print("\n############################################################")
    print("# GATE RESULT")
    print("############################################################")
    for name in ("doctor", "anchors", "v03_batch"):
        rc = parts.get(name, 1)
        print(f"  {name:12} {'PASS' if rc == 0 else 'FAIL'}  (exit {rc})")
    overall = 0 if all(rc == 0 for rc in parts.values()) else 1
    print(f"\n  GATE: {'PASS' if overall == 0 else 'FAIL'}")
    return overall


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
    parser.add_argument("--gate", action="store_true")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    if args.list:
        return cmd_list()
    if args.health:
        return cmd_health()
    if args.gate:
        return cmd_gate()
    if args.report:
        return cmd_report()
    if args.series:
        return cmd_series(args.series, validate_only=args.validate_only,
                          skip_validate=args.skip_validate)
    if args.validate_only:
        # No series specified — run the full 118-series batch (F-ORCH-01).
        return cmd_validate_batch()
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
