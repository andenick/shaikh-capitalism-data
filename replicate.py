#!/usr/bin/env python3
"""Shaikh (2016) Data Replication Pipeline — Reproduce all empirical series.

Usage:
    python replicate.py                    # Full pipeline
    python replicate.py --chapter 2        # Single chapter
    python replicate.py --series S001      # Single series
    python replicate.py --dry-run          # Show plan without executing
    python replicate.py --load-only        # Loading phase only
    python replicate.py --process-only     # Processing phase only
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from lib import registry
from lib.extension import ExtensionEngine
from lib.result import LoadResult, SeriesResult


def load_chapters_config() -> dict:
    with open(ROOT / "config" / "chapters.json", encoding="utf-8") as f:
        return json.load(f)


def run_loading(chapter_num: int, reg: dict) -> list[LoadResult]:
    module_name = f"loading.ch{chapter_num:02d}"
    try:
        mod = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"  [skip] {module_name} not yet implemented")
        return []
    return mod.load_all(reg)


def run_processing(chapter_num: int, reg: dict, engine: ExtensionEngine) -> list[SeriesResult]:
    module_name = f"processing.ch{chapter_num:02d}"
    try:
        mod = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"  [skip] {module_name} not yet implemented")
        return []
    return mod.process_all(reg, engine)


def main():
    parser = argparse.ArgumentParser(description="Shaikh (2016) Data Replication Pipeline")
    parser.add_argument("--chapter", type=int, help="Process single chapter")
    parser.add_argument("--series", type=str, help="Process single series")
    parser.add_argument("--dry-run", action="store_true", help="Show plan only")
    parser.add_argument("--load-only", action="store_true")
    parser.add_argument("--process-only", action="store_true")
    args = parser.parse_args()

    reg = registry.load()
    chapters_cfg = load_chapters_config()
    processing_order = chapters_cfg["processing_order"]
    engine = ExtensionEngine(reg, ROOT / "data" / "cache")

    if args.chapter:
        processing_order = [args.chapter]

    if args.dry_run:
        print("=== DRY RUN ===")
        for ch in processing_order:
            ch_info = chapters_cfg["chapters"].get(str(ch), {})
            series_list = ch_info.get("series", [])
            deps = ch_info.get("depends_on", [])
            print(f"  Ch{ch} ({ch_info.get('title', '?')}): {len(series_list)} series, depends on {deps}")
        return

    t0 = time.time()
    total_loaded = 0
    total_processed = 0

    print("=" * 60)
    print("  Shaikh (2016) Replication Pipeline")
    print("=" * 60)

    if not args.process_only:
        print("\n── Loading Phase ──")
        for ch in processing_order:
            results = run_loading(ch, reg)
            ok = sum(1 for r in results if r.status == "ok")
            total_loaded += ok
            if results:
                print(f"  Ch{ch:02d}: {ok}/{len(results)} loaded")

    all_results = []
    if not args.load_only:
        print("\n── Processing Phase ──")
        for ch in processing_order:
            results = run_processing(ch, reg, engine)
            ok = sum(1 for r in results if r.status == "ok")
            total_processed += ok
            all_results.extend(results)
            if results:
                print(f"  Ch{ch:02d}: {ok}/{len(results)} processed")

        # Write outputs
        output_dir = ROOT / "data" / "output"
        series_dir = output_dir / "series"
        chopped_dir = output_dir / "chopped"
        for d in [series_dir, chopped_dir]:
            d.mkdir(parents=True, exist_ok=True)

        written = 0
        for r in all_results:
            if r.status != "ok" or not r.data:
                continue
            composite = r.data.get(r.series_id)
            if composite is not None and len(composite) > 0:
                composite.name = r.series_id
                out = series_dir / f"{r.series_id}_final.csv"
                composite.to_csv(out, header=True)
                written += 1

        print(f"\n── Output ──")
        print(f"  Written: {written} series CSVs to data/output/series/")

    elapsed = time.time() - t0
    print(f"\n── Complete ({elapsed:.1f}s) ──")
    print(f"  Loaded: {total_loaded}, Processed: {total_processed}")


if __name__ == "__main__":
    main()
