---
decision_id: "0010"
title: "S1006 SBBI publish:false + Damodaran-NYU Public Surface (D-3)"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "T2.1"
gate0_ruling: "D-3"
related:
  - 0005_discontinued_apis_deferred.md
affected_series:
  - S1006
campaign_phases:
  - phase_E
---

# 0010 — S1006 SBBI publish:false + Damodaran-NYU Public Surface (D-3)

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: D-3 (campaign plan §2; CAMPAIGN_STATE.json `gate0_ratified.rulings["D-3"]`).

## Context

Backlog item **T2.1**. The S1006 series carries Ibbotson **SBBI** columns, now licensed commercially through
Morningstar (see Decision 0005). Publishing SBBI values on the public surface is a licensing exposure. The
hyper-review flagged this as the "S1006 class" licensing risk (non-redistributable source `publish:true`).

## Decision

**Both: mark the SBBI columns `publish:false` AND switch the public surface to the open Damodaran-NYU
alternates; grep-verify no SBBI values remain in the published bundle.** Verbatim ruling:

> T2.1 S1006: SBBI columns publish:false AND public surface -> open Damodaran-NYU -ext alternates;
> grep-verify Publish/ SBBI-clean.

Operational specifics (ratified):
- SBBI columns → `publish:false` in `series_registry.json`.
- Public surface substitutes the **open Damodaran-NYU** `-ext` alternate series (concept-matched, openly
  redistributable) per the Decision 0005 reference substitution list.
- **grep-verify** that no SBBI values (and no "SBBI" string) remain anywhere in `Outputs/Publish/`.

## Consequences

- **Phase E (E4 = T2.1)**: applies this ruling — SBBI `publish:false`, Damodaran-NYU public surface, and the
  Publish/ SBBI grep-clean gate (no SBBI values in the published tree).
- **Phase F (F1/F2)**: the static site + web export publish-filter (Decision 0016 / D-9) must exclude the
  SBBI columns; the F1 leak-grep gate includes "SBBI" alongside the 7 publish:false SIDs.
- The published series count may shift (110 vs 111) once the S1006 SBBI columns are demoted; the hub
  dataset arithmetic (`anu-vizsite/datasets/rscd.json`) is kept honest against the post-D-3 publish flags.
