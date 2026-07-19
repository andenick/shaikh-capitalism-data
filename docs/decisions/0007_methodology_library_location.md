---
id: "0007"
title: "Methodology Library storage location"
date: 2026-05-24
status: approved
approved_at: "2026-05-24T00:00:00Z"
deciders: [auto-default; user may override before M1 completes]
supersedes: []
superseded_by: []
related: [RSCD_EXPANDED_WISHLIST_PLAN.md]
---

## Context

Phase M0 of the expanded methodological wishlist plan requires a decision on where obtained PDFs (Categories A–L) land on disk. Two options were considered:

1. **SalvagedInputs/methodology_library/<cat>/** — extends the existing `SalvagedInputs/` convention for curated material. Writable today; no settings change.
2. **Inputs/MethodologyLibrary/<cat>/** — semantically cleanest ("things we did not produce"), but `Inputs/**` is deny-listed by `.claude/settings.json` `Write(Inputs/**)` rule. Would require adding a per-subpath allow-pattern.

## Decision

**Storage location: `SalvagedInputs/methodology_library/<category>/`**.

- 12 category subdirs created in Phase M0.1: `A_shaikh_pre2016/` through `L_vintages_dissertations/`.
- Tracker + dossiers + scripts live under `Technical/MethodologyLibrary/`.
- No change to `.claude/settings.json` required.

## Consequences

- ✅ Matches the existing precedent (SalvagedInputs already holds `book_data/`, `extension_benchmarks/`, `methodology_decisions/`, `figures_reference/`).
- ✅ Zero settings-file risk; no chance of accidentally widening write access to legacy CD/CD2 inputs.
- ✅ Continues the "single canonical copy" principle (per the workspace single-archive policy): the obtained PDF lives here, not duplicated to `Inputs/` or to `ArcArchive/`.
- ⚠️ Mild semantic stretch: `SalvagedInputs/` originally meant "material salvaged from CD/CD2." The expanded use covers newly-acquired external material too. The plan acknowledges this and adds a comment in `SalvagedInputs/methodology_library/README.md`.
- ⚠️ Anyone expecting `Inputs/MethodologyLibrary/` will need redirecting; cross-reference noted in `RSCD_EXPANDED_WISHLIST_PLAN.md` storage-layout table.

## Reversal cost

Low. A migration would be: rename `SalvagedInputs/methodology_library/` → `Inputs/MethodologyLibrary/` (or wherever); add allow-pattern to `.claude/settings.json`; update `METHODOLOGY_WISHLIST.csv` `workspace_path` column via a single `sed`/script pass; update plan + this decision doc.

## Status

ACCEPTED auto-default 2026-05-24. User may override before Phase M1 completes — reversal cost is low. After M1, costs rise (more rows referencing the paths).
