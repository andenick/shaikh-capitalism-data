# 0003 — Crosswalk Mismap Cleanup

**Status**: CLOSED
**Date opened**: 2026-05-18 (Phase 3 close, Ch7/Ch8 subagent findings)
**Date closed**: 2026-05-18
**Decided by**: mechanical (no judgment needed)

## Issue

The Phase 2 `_phase2_taxonomy_builder.py` grouped figures by CD's
`HDARP_SERIES_LINKAGE.json`. In a few cases the linkage attributed a figure
to a wrong CD2 series (CD2's S041/S042 are actually Ch10 interest-rate series,
not Ch8 price series). The Phase 2 builder inherited those wrong names.

Phase 3 subagents corrected the dossiers but the crosswalk still records
the stale links.

## Mismapped rows

| RSCD | wrong CD2 link | correct disposition |
|---|---|---|
| S707 | S038 (CD2 OECD STAN IROP, Ch7 Fig 7.21) | belongs to Ch7 Fig 7.19 per book — Phase 3 ratified rename; CD2 ancestor unclear |
| S801 | S042 (CD2 US Long-Run Interest Rates, Ch10) | Eichner price paths (Ch8 Fig 8.1); CD2 has no direct ancestor — null |
| S803 | S041 (CD2 Interest Rates Prices Equity, Ch10) | Bain ROE/CR8 (Ch8 Fig 8.3); CD2 has no direct ancestor — null |

## Decision

**Mechanical fix:**
1. In `MIGRATION/CD2_to_RSCD_crosswalk.csv`:
   - Remove the rows mapping S041→S803 and S042→S801 (they should stay `unmapped` in the CD2-to-RSCD direction)
   - Add a note column entry explaining the Phase 3 finding
2. In `series_registry.json`:
   - Set `S707.predecessor_ids.cd2_id` = null (or keep with note "CD2 ancestor disputed; see Phase 3 finding")
   - Set `S801.predecessor_ids.cd2_id` = null
   - Set `S803.predecessor_ids.cd2_id` = null
3. In `SERIES_CORRESPONDENCE_MATRIX.json`:
   - Update `by_cd2_id` to remove the wrong S041/S042 mappings

## Consequences

No data loss. The Phase 3 dossiers are already correct (subagents ignored
the stale stub names and authored against the actual book figures). This is
purely metadata hygiene.
