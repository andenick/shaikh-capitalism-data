"""
v1.0 reconciliation — fix 3 registry vs chopped CSV inconsistencies surfaced
by the Stage 7 viz agent.

These are metadata fixes only; chopped CSVs (the source of truth for shipped
data) are unchanged.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths

FIXES = {
    "S203": {
        "year_range_actual": [1780, 2000],
        "rationale": (
            "Chopped CSV ships MeasuringWorth USGDP 1780-2000 only (S203-A). "
            "S203-B extension (FRED) was scaffolded but not wired in Phase 7. "
            "Registry year_range updated to match shipped coverage; S203-B "
            "marked extension_deferred_to_v1.1."
        ),
        "subseries_status_update": {"S203-B": "deferred_to_v1.1"},
    },
    "S211": {
        "year_range_actual": [1790, 1940],
        "rationale": (
            "Chopped CSV starts at 1790; registry declared 1780. Investigation "
            "shows MeasuringWorth USWPI source begins at 1790 (not 1780). "
            "Updated to match source reality."
        ),
        "subseries_status_update": {},
    },
    "S214": {
        "year_range_actual": [1987, 2005],
        "rationale": (
            "Series classified PASS_DATA_UNAVAILABLE for book period 1960-1989 "
            "(OECD ISDB 1994 discontinued; Christodoulopoulos data not in "
            "SalvagedInputs). Chopped CSV ships only the S214-EXT post-book "
            "extension 1987-2005 (BEA NAICS industry source). Registry "
            "year_range updated to reflect actual data coverage; "
            "book_period_data_unavailable flag added."
        ),
        "subseries_status_update": {},
        "extra_flags": {"book_period_data_unavailable": True, "book_period": [1960, 1989]},
    },
}


def main():
    reg = json.loads(paths.REGISTRY.read_text(encoding="utf-8"))
    changes = []
    for sid, fix in FIXES.items():
        s = reg["series"].get(sid)
        if not s:
            print(f"SKIP {sid}: not in registry")
            continue
        old_yr = s.get("year_range")
        new_yr = fix["year_range_actual"]
        if old_yr != new_yr:
            s["year_range_pre_v1_reconciliation"] = old_yr
            s["year_range"] = new_yr
            changes.append(f"{sid} year_range {old_yr} -> {new_yr}")
        for sub_id, status in fix.get("subseries_status_update", {}).items():
            sub = (s.get("subseries") or {}).get(sub_id)
            if sub:
                sub["status"] = status
                changes.append(f"{sid}.subseries.{sub_id}.status -> {status}")
        for k, v in fix.get("extra_flags", {}).items():
            s[k] = v
            changes.append(f"{sid}.{k} -> {v}")
        s.setdefault("reconciliation_notes", []).append({
            "date": "2026-05-19",
            "reason": fix["rationale"],
        })

    paths.REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Reconciliation complete:")
    for c in changes:
        print(f"  {c}")


if __name__ == "__main__":
    main()
