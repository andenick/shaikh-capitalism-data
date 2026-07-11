---
decision_id: "0013"
title: "Ch7 Panels S705-S711 content_type=time_series + panel_dimension Note (D-6)"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "T4.3"
gate0_ruling: "D-6"
related:
  - 0004_ch7_additional_series.md
affected_series:
  - S705
  - S706
  - S707
  - S708
  - S709
  - S710
  - S711
campaign_phases:
  - phase_E
---

# 0013 — Ch7 Panels S705–S711 content_type=time_series + panel_dimension Note (D-6)

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: D-6 (campaign plan §2; CAMPAIGN_STATE.json `gate0_ratified.rulings["D-6"]`).

## Context

Backlog item **T4.3**. The Chapter 7 industry panels S705–S711 carried an ambiguous `content_type`
(`cross_sectional` vs `time_series`). The classification matters because extension eligibility follows
`content_type` (only `time_series` is extendable). Every S705–S711 EPR treats these as time series, and the
IO-compendium's recommendation 2 concurs; the panels are industry × year, i.e. time series with an industry
panel dimension.

## Decision

**Classify S705–S711 as `content_type=time_series`, matching the EPRs, with a `panel_dimension: industry`
note.** Verbatim ruling:

> T4.3: ch7 panels S705-S711 content_type=time_series (matches EPRs) + panel_dimension:industry note.

Operational specifics (ratified):
- `content_type: time_series` for S705, S706, S707, S708, S709, S710, S711.
- Add a `panel_dimension: industry` note on each so the industry axis is explicit.
- Extension eligibility follows the EPRs (time_series → extendable, per each series' EPR).

## Consequences

- **Phase E (E5 registry backfill)**: the `content_type` + `panel_dimension` fields for S705–S711 are set
  in `series_registry.json`; anu-doctor content-type checks pass against the EPRs.
- Extension pipeline treats S705–S711 as extendable per their EPRs (was previously ambiguous).
- Coordinates with Decision 0004 (which added S709–S711 to Ch7).
