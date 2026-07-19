---
decision_id: "0009"
title: "Project-wide Forecast Policy: Flag, Don't Truncate (D-2)"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "T1.3 + T1.4"
gate0_ruling: "D-2"
related:
  - 0005_discontinued_apis_deferred.md
affected_series:
  - XS2302
  - S1701
campaign_phases:
  - phase_C
---

# 0009 — Project-wide Forecast Policy: Flag, Don't Truncate (D-2)

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: D-2 (campaign plan §2; CAMPAIGN_STATE.json `gate0_ratified.rulings["D-2"]`).

## Context

Backlog item **T1.3** (XS2302 WEO forecast rows 2025–2031) posed the question: truncate the forecast rows
or flag them? The hyper-review noted this is not an XS2302-local question but a project-wide policy gap —
several extended series can carry forward-looking (forecast/projection) rows, and the long-form chopped
writer (backlog **T1.4**) has no channel to carry a forecast marker. Coordinates with **Decision 0005**
(the canonical `chopped_format: "long"` column set).

## Decision

**Adopt one project-wide policy: FLAG, don't truncate.** Verbatim ruling:

> Project-wide forecast policy: FLAG, don't truncate. is_forecast carried through long-form chopped writer
> (T1.4 serves T1.3+S1701); reference_values realized-years-only; year_range reconciled.

Operational specifics (ratified):
- Forecast/projection rows are **retained**, not deleted — every value stays traceable to its source vintage.
- An `is_forecast` boolean is **carried through the long-form chopped writer** (the T1.4 schema fix). This
  single writer change serves both T1.3 (XS2302) and S1701, and any future forecast-bearing series.
- `reference_values` in the registry are **restricted to realized years only** — no forecast value is ever
  registered as an anchor/benchmark (would poison V03 and the D-4 anchors of Decision 0011).
- Registry `year_range` is reconciled to the full (realized + flagged-forecast) span; DPR §5 reconciled.

## Consequences

- **Phase C (C2 = T1.4)**: long-form chopped writer gains `status`/`is_forecast` columns; no numeric change,
  byte-stable except the new column; coordinates with Decision 0005 (long-form canonical).
- **Phase C (C3 = T1.3 XS2302)**: rows 2025–2031 flagged `is_forecast=true`; `reference_values` realized-only;
  `year_range` + DPR §5 reconciled; V03 green with no forecast value used as a reference.
- Policy binds every future forecast-bearing series project-wide (not just XS2302/S1701).
