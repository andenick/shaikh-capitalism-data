---
decision_id: "0014"
title: "classification_vintage Tag + Loader Assertion + Chopped-Writer Mixed-Vintage Guard (D-7)"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "T4.4 / SI-3"
gate0_ruling: "D-7"
affected_series:
  - S216
  - S705
  - S706
  - S707
  - S708
  - S709
  - S710
  - S711
  - S901
  - S902
  - S903
  - XS2101
campaign_phases:
  - phase_G
---

# 0014 — classification_vintage Tag + Loader Assertion + Chopped-Writer Mixed-Vintage Guard (D-7)

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: D-7 (campaign plan §2; CAMPAIGN_STATE.json `gate0_ratified.rulings["D-7"]`).

## Context

Backlog item **T4.4** (structural investment **SI-3**). Series that carry an industry index span multiple
industry-classification eras (SIC 1971, NAICS 1965-basis, later NAICS vintages). The hyper-review's CH9-F4
finding showed that silently concatenating data across classification vintages is a latent splice error with
no machine guard. A `classification_vintage` tag plus enforcement makes cross-vintage splices mechanically
impossible — a prerequisite for SI-3.

## Decision

**Adopt a `classification_vintage` tag from a controlled vocabulary, assert it in every industry-index
loader, and add a chopped-writer guard that refuses to concatenate mixed vintages.** Verbatim ruling:

> T4.4: adopt classification_vintage in {SIC71, NAICS65, NAICS_<year>} tag + loader assertion +
> chopped-writer mixed-vintage concat guard.

Operational specifics (ratified):
- `classification_vintage ∈ {SIC71, NAICS65, NAICS_<year>}` on every `industry_index`-bearing artifact.
- **Loader assertion**: each L01 for an industry-index series asserts the fetched data's vintage matches
  the registered tag (the CH9-F4 fix; = build-spec "vintage guard").
- **Chopped-writer guard**: the long-form chopped writer refuses to concatenate rows of differing
  `classification_vintage` — a deliberate mixed-vintage concat attempt must FAIL.

## Consequences

- **Phase G (G3 = SI-3)**: implements the tag on ch9 / ch7 / XS2101 / S216 artifacts + loader assertions +
  the chopped-writer mixed-vintage guard. Phase-G gate = a deliberate mixed-vintage concat attempt FAILS
  (guard proof); anu-doctor 0/0.
- Prerequisite satisfied for the SI-3 structural investment; couples with the SI-2 `scheme_registry.csv`
  (G2) that records frozen/staged classification schemes.
