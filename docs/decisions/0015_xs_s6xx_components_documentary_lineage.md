---
decision_id: "0015"
title: "XS->S6xx Components Re-scoped as Documentary Lineage; GPIM Recompute Deferred (D-8)"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "T4.5"
gate0_ruling: "D-8"
related:
  - 0002_ch6_gpim_variants_disposition.md
affected_series:
  - S601
  - S602
  - S603
  - S604
  - XS001
  - XS002
  - XS003
  - XS004
  - XS005
  - XS006
  - XS007
  - XS008
  - XS009
campaign_phases:
  - phase_E
---

# 0015 — XS→S6xx Components Re-scoped as Documentary Lineage; GPIM Recompute Deferred (D-8)

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: D-8 (campaign plan §2; CAMPAIGN_STATE.json `gate0_ratified.rulings["D-8"]`).

## Context

Backlog item **T4.5**. The `series_registry.json` `components` field on the S6xx GPIM profit-rate series
implies a live computational linkage from the XS001–XS009 GPIM construction internals (Decision 0002) into
S601–S604. In reality the linkage is a **transcription pattern** — the S6xx curves were transcribed from the
book/CD2, not live-recomputed from the XS component pipeline. The hyper-review asked whether to wire the
linkage for real or re-scope it honestly.

## Decision

**Re-scope the registry `components` as documentary lineage (disclose the transcription pattern); keep live
GPIM recompute on the roadmap (Phase L); note the future anu-variant VPR pair as its designated vehicle.**
Verbatim ruling:

> T4.5: re-scope registry components as documentary lineage (transcription disclosed); live GPIM recompute
> stays roadmap Phase L; future anu-variant VPR pair (IPP-in @2011V vs IPP-out) noted.

Operational specifics (ratified):
- Registry `components` on S601–S604 re-labeled as **documentary lineage** — the XS001–XS009 → S6xx
  relationship is disclosed as a transcription pattern, not a live recompute; loader docstrings aligned.
- **Live GPIM recompute stays roadmap Phase L** (needs the BEA-1993 archive; a §6 non-goal for this campaign).
- The **future anu-variant VPR pair** — GPIM **IPP-in @2011 vintage** vs **IPP-out @post-2013** — is noted
  as the designated vehicle for when live recompute lands.

## Consequences

- **Phase E (E5 registry backfill per D-8)**: `components`/`formula`/`extension` fields on S601–S604 are
  re-scoped to documentary-lineage wording; loader docstrings aligned; no live recompute wired.
- **Deferred (§6, later session)**: GPIM live recompute + the anu-variant IPP-in/out VPR pair (Phase L).
- Preserves CD2's analytical granularity (Decision 0002) while stating the linkage honestly.
