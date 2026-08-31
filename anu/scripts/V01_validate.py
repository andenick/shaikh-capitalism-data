"""V01 — package-level validation gate.

Checks the chopped output against anu/series_registry.json:

  1. series presence — every producible series has a CSV
  2. count match     — no missing and no extra CSVs
  3. schema          — required columns present (year, value, subseries_id,
                       source_id, units); null years are failures
  4. unit sanity     — index series are strictly positive where defined
  5. coverage        — actual year range vs the registry's declared range
  6. null values     — reported as WARNINGS: empty values are honest gap
                       markers in this project (no synthetic fills), e.g.
                       undefined marginal cost at q=0 in the theoretical
                       cost-curve series

Default target is the shipped reference output (chopped/ at the repo root),
so this gate runs key-free in CI. Pass --dir anu/data/final/chopped to
validate a freshly reproduced copy.

Exit code 0 = PASS (warnings allowed), 1 = FAIL.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common  # noqa: E402

REQUIRED_COLUMNS = ("year", "value", "subseries_id", "source_id", "units")


def read_csv_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_series(sid: str, meta: dict, path: Path) -> tuple[list[str], list[str]]:
    """Return (failures, warnings) for one series CSV."""
    fails: list[str] = []
    warns: list[str] = []

    rows = read_csv_rows(path)
    if not rows:
        return ([f"{sid}: empty CSV"], [])

    header = rows[0].keys()
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing_cols:
        return ([f"{sid}: missing columns {missing_cols}"], [])

    years = []
    n_null_year = 0
    n_null_value = 0
    values_by_unit: dict[str, list[float]] = {}
    for r in rows:
        y, v, u = r.get("year"), r.get("value"), r.get("units") or ""
        if y is None or y == "":
            n_null_year += 1
            continue
        years.append(int(float(y)))
        if v is None or v == "":
            n_null_value += 1
        else:
            values_by_unit.setdefault(u, []).append(float(v))

    if n_null_year:
        fails.append(f"{sid}: {n_null_year} null years")
    if n_null_value:
        warns.append(f"{sid}: {n_null_value} null values (honest gap markers)")

    # Unit sanity: impossible values only. Rates outside [-1, 1] are reported
    # as warnings because several "rate"-labelled series legitimately hold
    # regression slopes or profit/capital ratios above 1.
    for u, vals in values_by_unit.items():
        ul = (u or "").lower()
        if ul.startswith("index") or "index_" in ul:
            if any(v <= 0 for v in vals):
                fails.append(f"{sid}: non-positive value in index units ({u})")
        elif ul.startswith("rate_decimal") or ul.startswith("decimal_rate"):
            if any(abs(v) >= 1.0 for v in vals):
                warns.append(f"{sid}: rate outside [-1,1] in {u} "
                             f"(slopes/ratios may legitimately exceed 1)")

    # Coverage
    cov = meta.get("coverage") or {}
    start, end = cov.get("start"), cov.get("end")
    if years:
        amin, amax = min(years), max(years)
        if start is not None and amin < start:
            fails.append(f"{sid}: starts {amin} before declared {start}")
        if end is not None and amax > end + 1:
            warns.append(f"{sid}: extends to {amax} beyond declared {end} "
                         f"(registry coverage stale; data is a superset)")
        if end is not None and amax < end - 1:
            warns.append(f"{sid}: ends {amax} before declared {end} "
                         f"(short extension)")

    # Cosmetic unit-label check: the registry sometimes carries a prose unit or
    # 'per_subseries' (units vary by subseries by design); the CSVs carry the
    # compact per-subseries label. Only warn on a genuine mismatch.
    units_declared = (meta.get("units") or "").lower()
    if units_declared and "per_subseries" not in units_declared \
            and len(values_by_unit) == 1:
        csv_unit = next(iter(values_by_unit))
        norm = lambda s: "".join(ch for ch in s.lower() if ch.isalnum())
        nd, nc = norm(units_declared), norm(csv_unit)
        if nd != nc and nd not in nc and nc not in nd:
            warns.append(f"{sid}: unit '{csv_unit}' vs declared '{units_declared}'")

    return fails, warns


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="V01_validate.py",
        description="Validate chopped output against anu/series_registry.json")
    parser.add_argument("--dir", type=str, default=None,
                        help="output directory to validate "
                             "(default: the shipped chopped/ reference; "
                             "pass anu/data/final/chopped after a run)")
    args = parser.parse_args()

    registry = _common.load_registry()
    target = Path(args.dir) if args.dir else _common.CHOPPED_REFERENCE
    if not target.is_absolute():
        target = (_common.REPO_ROOT / target).resolve()
    if not target.exists():
        raise SystemExit(f"target directory not found: {target}")

    series = {s["series_id"]: s for s in registry["series"]}
    producible = {sid for sid, s in series.items() if s.get("producible")}
    on_disk = {p.stem for p in target.glob("*.csv")}

    fails: list[str] = []
    warns: list[str] = []

    missing = sorted(producible - on_disk)
    extra = sorted(on_disk - set(series))
    for sid in missing:
        fails.append(f"{sid}: producible but no CSV in {target.name}/")
    for sid in extra:
        fails.append(f"{sid}: CSV present but not in registry")

    for sid in sorted(producible & on_disk):
        f, w = validate_series(sid, series[sid], target / f"{sid}.csv")
        fails.extend(f)
        warns.extend(w)

    print(f"=== V01 validation ===")
    print(f"registry   : {len(series)} series ({len(producible)} producible)")
    print(f"target     : {target}")
    print(f"CSVs found : {len(on_disk)}")
    print(f"failures   : {len(fails)}")
    print(f"warnings   : {len(warns)}")
    for f in fails:
        print(f"  FAIL  {f}")
    for w in warns:
        print(f"  WARN  {w}")

    if fails:
        print("\nV01: FAIL")
        return 1
    print("\nV01: PASS" + (f" ({len(warns)} warnings)" if warns else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
