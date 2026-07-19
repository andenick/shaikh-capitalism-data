---
decision_id: "0017"
title: "decisions/ Directory + docs Substitution Canonical for ASSUMPTIONS.md / provenance_index.json (T3.9)"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "T3.9"
gate0_ruling: "T3.9 ratification"
affected_series:
  - all
campaign_phases:
  - phase_A
---

# 0017 — decisions/ Directory + docs Substitution Canonical in Lieu of ASSUMPTIONS.md / provenance_index.json (T3.9)

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: T3.9 ratification (campaign plan §2 / Phase A1.5; CAMPAIGN_STATE.json `gate0_ratified.rulings["T3.9"]`... recorded under item A1.5).

## Context

Backlog item **T3.9**. The generic Anu-project convention anticipates a standalone `ASSUMPTIONS.md` and a
`provenance_index.json` (surfaced by anu-doctor checks **P07** and **P08**). RSCD does not maintain those two
files as standalone artifacts — its assumptions and provenance narrative live in the `Technical/docs/`
tree and, decisively, in the versioned `Technical/docs/decisions/` decision-doc series (0001–NNNN, each with
P28-conformant YAML frontmatter). The hyper-review flagged the P07/P08 SKIPs and asked whether they represent
a real gap or an accepted architectural substitution.

## Decision

**The `Technical/docs/decisions/` directory + the `Technical/docs/` substitution is CANONICAL for this
project, in lieu of a standalone `ASSUMPTIONS.md` and `provenance_index.json`. The anu-doctor P07 / P08 SKIP
outcome is ACCEPTED — it is not a gap.**

Operational specifics (ratified):
- The versioned decision-doc series under `Technical/docs/decisions/` (P28-conformant frontmatter) is the
  canonical record of project assumptions and ratified rulings.
- Provenance narrative lives in `Technical/docs/` (methodology histories, chapter reports, per-series DPR/EPR/
  explainers) rather than a single `provenance_index.json`.
- anu-doctor **P07** ("validation/ directory absent (skipped)") and **P08** ("PROVENANCE_INDEX.json absent
  (skipped)") reporting SKIP/PASS is the **accepted** state — no ASSUMPTIONS.md / provenance_index.json is to
  be manufactured to satisfy them.

## Consequences

- **Phase A (A1.5 = T3.9)**: this doc is the ratifying record; no ASSUMPTIONS.md / provenance_index.json is
  created. The P07/P08 SKIP is documented as accepted, closing T3.9.
- Future anu-doctor runs treat P07/P08 SKIP as expected for RSCD (not a WARN/FAIL regression).
- Reinforces the Anu meta-principle "new decisions land in the canonical spec / decision-log, commit messages
  capture rationale" (`.claude/rules/anu-framework.md`).
