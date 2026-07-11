---
decision_id: "0012"
title: "Ratify RSCD 5-Sheet Extenbook Layout as Documented Variant (D-5)"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "T4.2"
gate0_ruling: "D-5"
affected_series:
  - all
campaign_phases:
  - none_physical
---

# 0012 — Ratify RSCD 5-Sheet Extenbook Layout as Documented Variant (D-5)

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: D-5 (campaign plan §2; CAMPAIGN_STATE.json `gate0_ratified.rulings["D-5"]`).

## Context

Backlog item **T4.2**. The canonical `anu-extenbook` layout is 4 sheets (Data / Provenance / Research /
Construction). RSCD's extenbooks ship a **5-sheet** layout (Data / Methodology / Sources / Validation /
Provenance). The hyper-review asked whether to conform RSCD down to the canonical 4-sheet or ratify the
richer 5-sheet as an intentional project variant. The 5-sheet layout loses no honesty and physically
regenerating every extenbook to conform would be pure churn.

## Decision

**Ratify the RSCD 5-sheet extenbook layout as a documented project variant via this decision doc; defer
any physical regeneration.** Verbatim ruling:

> T4.2: ratify RSCD 5-sheet extenbook layout as documented variant via decision doc; physical regen deferred.

Operational specifics (ratified):
- The RSCD extenbook variant = **5 sheets**: Data, Methodology, Sources, Validation, Provenance.
- This is recorded as a documented deviation from the canonical `anu-extenbook` 4-sheet standard; honesty
  and completeness are preserved (the 5-sheet is a superset in intent).
- **Physical regeneration is deferred** to the next full extenbook rebuild — zero churn now.

## Consequences

- **No physical output change this campaign.** This doc is the ratifying record; the existing 5-sheet
  extenbooks stand as-is.
- When the next full extenbook rebuild happens, the 5-sheet layout is the intended RSCD target (not a
  regression back to 4-sheet).
- anu-doctor / anu-review treat the 5-sheet layout as a ratified variant, not a defect.
