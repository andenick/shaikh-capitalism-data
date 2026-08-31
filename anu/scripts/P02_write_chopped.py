"""P02 — stage the final chopped output into the anu package.

Copies the chopped CSVs produced by P01 (staged by the replicator under
replicator/data/final/chopped/) into anu/data/final/chopped/ and writes a
MANIFEST.csv recording file, series, sha256, rows and year range.

The shipped reference copy of the same output lives at the repo root in
chopped/ — this step reproduces it inside the package layout so the anu/
directory is self-contained.

Usage
-----
    python anu/scripts/P02_write_chopped.py            # from replicator staging
    python anu/scripts/P02_write_chopped.py --from-reference   # from chopped/
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common  # noqa: E402

STAGED = _common.REPLICATOR.parent.parent / "data" / "final" / "chopped"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def year_range(path: Path) -> tuple[str, str]:
    import csv
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    years = [int(float(r["year"])) for r in rows if r.get("year")]
    return (str(min(years)), str(max(years))) if years else ("", "")


def stage(src: Path, dst: Path) -> int:
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(src.glob("*.csv")):
        shutil.copy2(f, dst / f.name)
        n += 1
    return n


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="P02_write_chopped.py",
        description="Stage chopped CSVs into anu/data/final/chopped + MANIFEST.csv")
    parser.add_argument("--from-reference", action="store_true",
                        help="stage from the repo-root chopped/ reference "
                             "instead of the replicator staging area")
    args = parser.parse_args()

    src = _common.CHOPPED_REFERENCE if args.from_reference else STAGED
    if not src.exists():
        raise SystemExit(
            f"no chopped output found at {src.relative_to(_common.REPO_ROOT)}.\n"
            f"Run P01 first (python anu/scripts/P01_construct_series.py --all),\n"
            f"or pass --from-reference to stage the shipped output.")

    n = stage(src, _common.ANU_FINAL)
    print(f"[P02] staged {n} chopped CSVs -> anu/data/final/chopped/")

    lines = ["series_id,file,sha256,rows,year_min,year_max"]
    for f in sorted(_common.ANU_FINAL.glob("*.csv")):
        sid = f.stem
        y0, y1 = year_range(f)
        rows = sum(1 for _ in f.open(encoding="utf-8")) - 1
        lines.append(f"{sid},{f.name},{sha256(f)},{rows},{y0},{y1}")
    manifest = _common.ANU_FINAL.parent / "MANIFEST.csv"
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[P02] wrote {manifest.relative_to(_common.REPO_ROOT)} ({len(lines)-1} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
