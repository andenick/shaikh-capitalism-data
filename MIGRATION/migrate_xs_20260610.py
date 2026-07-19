#!/usr/bin/env python3
"""AS/ES -> XS series-ID migration (Series ID Spec v2.2) for RSCD.

One-off mechanical rewriter. Applies a pure prefix swap with digit counts
preserved:
    \\bAS(\\d{3})  -> XS\\1   (AS003   -> XS003,   AS003-A      -> XS003-A)
    \\bES(\\d{4})  -> XS\\1   (ES2301  -> XS2301,  ES2301-world -> XS2301-world)

The leading word boundary + fixed digit counts prevent false positives such as
the method codename "AS2" or any "AS"/"ES" word that is not followed by the
exact digit count.

Operates on BOTH file CONTENTS (text files) and FILENAMES, restricted to the
in-scope directories listed in IN_SCOPE. Out-of-scope trees (Inputs, Handoffs,
tmp, predecessor_sweep, MethodologyLibrary, WL1_*, Outputs, .git, __pycache__,
and MIGRATION history) are never touched.

PROTECTED_TOKENS holds exact IDs that must NOT be rewritten even though they
match the regex -- currently the single foreign-project reference ES1001
(RMWND's own series, cited verbatim in the RSCD-vs-RMWND comparison narrative).

Usage:
    python migrate_xs_20260610.py --dry-run   # report only, no writes
    python migrate_xs_20260610.py             # apply
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Technical/ root (this script lives in Technical/MIGRATION/)
TECH = Path(__file__).resolve().parent.parent

# In-scope top-level directories under Technical/.
IN_SCOPE = [
    "series_registry.json",  # single file, handled specially below
    "research",
    "docs",
    "chopped",
    "replicator",
    "code",
    "config",
    "viz",
    "extenbooks",   # .xlsx filenames only -- contents are binary, never edited
    "Build",
    "tools",
    "reports_latex",
]

# Directory names that are pruned anywhere in the walk.
PRUNE_DIRS = {"__pycache__", ".git", ".ipynb_checkpoints"}

# Text-file extensions whose CONTENTS we rewrite.
TEXT_EXTS = {
    ".json", ".md", ".py", ".csv", ".yaml", ".yml", ".toml",
    ".txt", ".r", ".tex", ".cff", ".env", ".example",
}

# Exact tokens that match the regex but must be preserved verbatim.
PROTECTED_TOKENS = {"ES1001"}  # RMWND foreign-project reference

AS_RE = re.compile(r"\bAS(\d{3})")
ES_RE = re.compile(r"\bES(\d{4})")
# Filename forms. Unlike \b, an explicit "left separator" lookbehind so that
# `_AS001` / `_ES2001` (the L01_/P02_/V03_ script naming, where the underscore
# is a word char and therefore defeats \b) are matched. Left edge may be the
# start of the basename or one of _ - . / \  ; right edge is just the fixed
# digit count, so AS003-A / ES2301-world filenames are handled too. The digit
# count still blocks AS2-style false positives.
AS_RE_NAME = re.compile(r"(?:(?<=^)|(?<=[_\-./\\]))AS(\d{3})")
ES_RE_NAME = re.compile(r"(?:(?<=^)|(?<=[_\-./\\]))ES(\d{4})")


def _swap(text: str) -> tuple[str, int]:
    """Return (rewritten_text, n_replacements), honoring PROTECTED_TOKENS."""
    n = 0

    def as_sub(m: re.Match) -> str:
        nonlocal n
        n += 1
        return "XS" + m.group(1)

    def es_sub(m: re.Match) -> str:
        nonlocal n
        tok = m.group(0)
        if tok in PROTECTED_TOKENS:
            return tok  # leave protected token untouched
        n += 1
        return "XS" + m.group(1)

    text = AS_RE.sub(as_sub, text)
    text = ES_RE.sub(es_sub, text)
    return text, n


def _swap_name(name: str) -> str:
    """Filename swap (protected tokens still apply)."""
    def es_sub(m: re.Match) -> str:
        if m.group(0) in PROTECTED_TOKENS:
            return m.group(0)
        return "XS" + m.group(1)
    name = AS_RE_NAME.sub(lambda m: "XS" + m.group(1), name)
    name = ES_RE_NAME.sub(es_sub, name)
    return name


def iter_files(roots: list[Path]):
    for root in roots:
        if root.is_file():
            yield root
            continue
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if any(part in PRUNE_DIRS for part in p.parts):
                continue
            if p.is_file():
                yield p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = args.dry_run

    roots = [TECH / d for d in IN_SCOPE]

    # Per-top-level-dir tallies.
    stats: dict[str, dict[str, int]] = {}

    def bucket(p: Path) -> str:
        try:
            rel = p.relative_to(TECH)
        except ValueError:
            return "<other>"
        return rel.parts[0]

    # Pass 1: content edits (text files only).
    for p in iter_files(roots):
        b = bucket(p)
        st = stats.setdefault(b, {"renamed": 0, "edited": 0, "repl": 0})
        if p.suffix.lower() in TEXT_EXTS:
            try:
                orig = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            new, n = _swap(orig)
            if n > 0:
                st["edited"] += 1
                st["repl"] += n
                if not dry:
                    p.write_text(new, encoding="utf-8")

    # Pass 2: filename renames (deepest first so parent dirs untouched here;
    # only files are renamed, no directory renames are needed for this project).
    all_files = sorted(iter_files(roots), key=lambda p: len(p.parts), reverse=True)
    for p in all_files:
        new_name = _swap_name(p.name)
        if new_name != p.name:
            b = bucket(p)
            st = stats.setdefault(b, {"renamed": 0, "edited": 0, "repl": 0})
            st["renamed"] += 1
            target = p.with_name(new_name)
            if not dry:
                if target.exists():
                    print(f"  !! COLLISION: {p} -> {target} (target exists, skipped)")
                    continue
                p.rename(target)

    # Report.
    mode = "DRY-RUN" if dry else "LIVE"
    print(f"=== migrate_xs_20260610 [{mode}] ===")
    tot_r = tot_e = tot_n = 0
    for b in sorted(stats):
        s = stats[b]
        tot_r += s["renamed"]; tot_e += s["edited"]; tot_n += s["repl"]
        if s["renamed"] or s["edited"]:
            print(f"  {b:18s}  renamed={s['renamed']:4d}  edited={s['edited']:4d}  replacements={s['repl']:5d}")
    print(f"  {'TOTAL':18s}  renamed={tot_r:4d}  edited={tot_e:4d}  replacements={tot_n:5d}")
    print(f"  protected tokens (left verbatim): {sorted(PROTECTED_TOKENS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
