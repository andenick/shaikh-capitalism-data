---
decision_id: "0002"
title: "Ch6 GPIM Construction Internals Disposition"
status: approved
proposed_at: "2026-05-18T00:00:00Z"
approved_at: "2026-05-18T00:00:00Z"
decided_by: user
affected_series:
  - XS001
  - XS002
  - XS003
  - XS004
  - XS005
  - XS006
  - XS007
  - XS008
  - XS009
  - S601
  - S602
  - S603
  - S604
affected_stages:
  - phase_3
---

# 0002 — Ch6 GPIM Construction Internals Disposition

**Status**: CLOSED
**Date opened**: 2026-05-18 (Phase 3 close, Ch6 subagent recommendation)
**Date closed**: 2026-05-18
**Decided by**: user

## Context

CD2 tracked 9 separate series (S206–S214) for the Chapter 6 profit-rate
construction pipeline. None are figure-linked in the book — they are
construction internals (GDP/GDI decomposition, wage equivalent, imputed
interest splits, GPIM capital stock measurement, and 4 sensitivity variants).

RSCD's Phase 2 builder marked all 9 as `unmapped` because the candidate
algorithm grouped by figure linkage. They need a home.

## Decision

**Option A — AS-prefixed analytical-support series.**

Register 9 new analytical series (XS001–XS009) corresponding to the CD2
construction pipeline. Cross-reference from S601–S604 dossiers via the
`components` field.

| New ID | CD2 ID | Name |
|---|---|---|
| XS001 | S206 | GDP/GDI Decomposition and Business NOS |
| XS002 | S207 | Wage Equivalent and Corporate/Noncorporate Split |
| XS003 | S208 | Imputed Interest Adjustment and Sectoral Profit Rates |
| XS004 | S209 | GPIM Corporate Capital Stock |
| XS005 | S210 | GPIM Variant — BEA 2011 Initial Value |
| XS006 | S211 | GPIM Variant — BEA 1993 vs 2011 |
| XS007 | S212 | GPIM Variant — IRS Adjusted |
| XS008 | S213 | GPIM Variant — Interwar Adjusted |
| XS009 | S214 | IRS Corporate Inventories and Total Capital Stock |

## Rationale (user-confirmed)

Preserves CD2's analytical granularity. Users can inspect e.g. the wage-equivalent
calculation independently from the final profit rate, and the 4 GPIM sensitivity
variants stay exposed for replication. Subseries-of-S6xx would hide the variants;
dropping them would materially weaken the replication's methodological transparency.

## Consequences

- `series_registry.json` gains 9 XS001–XS009 entries with `content_type: derived`,
  `construction: composite`, and `components` referencing the relevant BEA tables.
- `CD2_to_RSCD_crosswalk.csv` updated: 9 previously-unmapped rows now map.
- Each S601–S604 dossier's `components` field references the relevant AS series.
- Effort: ~5 hours of new Phase 3 work (CD2 had research for some; ports first, originals as needed).
