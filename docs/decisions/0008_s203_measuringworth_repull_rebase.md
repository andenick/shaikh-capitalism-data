---
decision_id: "0008"
title: "S203 MeasuringWorth Re-pull + Rebase Policy (D-1)"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "T1.2"
gate0_ruling: "D-1"
affected_series:
  - S203
campaign_phases:
  - phase_B
  - phase_C
---

# 0008 — S203 MeasuringWorth Re-pull + Rebase Policy (D-1)

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: D-1 (campaign plan §2; CAMPAIGN_STATE.json `gate0_ratified.rulings["D-1"]`).

## Context

Backlog item **T1.2** and the hyper-review (`RSCD_HYPER_REVIEW_2026-05-19.md`; S203_MHR §6) found the
S203 real-GDP-per-capita 1929–1934 column corrupt in the CD2-inherited source workbook — the values
do not fall through the Great Depression as the underlying macro history requires. The corrupt vintage
produces an implausible 1929→1933 rise, and V03 for S203 lacks any sanity assertion to catch it.

## Decision

**Re-pull the current MeasuringWorth real-GDP-per-capita series and re-base it into the book-period base
by an overlap reindex at 2010; block `publish` until the re-pull lands; and add the missing plausibility
assertion.** Verbatim ruling:

> T1.2 S203: re-pull current MeasuringWorth real GDP/capita; re-base 2017$->book base via overlap reindex
> at 2010; block publish until landed; add 1929>1933 sanity assertion.

Operational specifics (per campaign plan §2 D-1 recommendation, ratified):
- Re-pull the **current** MeasuringWorth real-GDP-per-capita vintage (not the corrupt CD2 workbook column).
- Re-base 2017$ → book-period base by **overlap reindex at 2010**.
- Set `publish` to block (false) for S203 until the re-pulled + re-based series is landed and validated.
- Add the **1929 > 1933** sanity assertion (Depression-must-fall) that V03 currently lacks — this becomes
  a `plausibility_rules[]` entry consumed by the D-4 level-plausibility check (Decision 0011).

## Consequences

- **Phase B** (Decision 0011 machinery): S203 is registered as a `known_reds` expected-FAIL — the current
  Depression-rise trips the new level-plausibility check, which is the proof the plausibility guard works.
- **Phase C (C4 = T1.2)**: consumes this ruling — re-pull + re-base + assertion; success = the Phase-B
  plausibility check flips red→green and 1929–1933 is strictly falling; hand-check vs book; new repro hash.
- Registry `year_range`, `reference_values` (realized values only), and the extension/`publish` block for
  S203 are reconciled as part of C4.
