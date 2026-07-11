---
decision_id: "0011"
title: "V03 Independent Anchors, 1% Canonical Tolerance, and Two New Check Types (D-4)"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "T4.1 / SI-4"
gate0_ruling: "D-4"
related:
  - 0002_ch6_gpim_variants_disposition.md
  - 0004_ch7_additional_series.md
affected_series:
  - S604
  - S903
  - S1006
  - S1007
  - S1508
  - S1509
  - S1405
  - S1408
  - S1401
  - S203
campaign_phases:
  - phase_B
  - phase_C
  - phase_D
---

# 0011 — V03 Independent Anchors, 1% Canonical Tolerance, and Two New Check Types (D-4)

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: D-4 (campaign plan §2; CAMPAIGN_STATE.json `gate0_ratified.rulings["D-4"]`).

## Context

Backlog item **T4.1 / SI-4** and the hyper-review found the V03 validation layer effectively tautological:
several V03 scripts re-read the same book XLSX they were meant to check against, and the tolerance policy was
inconsistent (a 0.5% divergence competing with the registry's canonical 1%). The fix is to anchor V03 to
**independent** book-published values and to add structural guards the current suite lacks (splice-break and
level-plausibility). This is the machinery that Phase C's data fixes are validated under.

## Decision

**The six named book anchors are authoritative; registry 1% is the canonical tolerance (V03 conforms — the
0.5% divergence is killed); and V03 gains two new check types.** Verbatim ruling:

> T4.1: six anchors authoritative (T6.24->S604, T9.18->S903, T10.1/10.2->S1006/S1007,
> Harberger/Ramamurthy->S1508/S1509, S1405 Phillips a/c/R2, S1408 T14.3); registry 1% canonical tolerance;
> new V03 check types: splice-continuity (|dSplice| > max(3x trailing 5yr sigma, 5%)) + level-plausibility
> (MHR s5 hooks).

### The six authoritative anchors

| Anchor (book) | Wired to |
|---|---|
| Table 6.24 | `V03_S604` |
| Table 9.18 | `V03_S903` |
| Table 10.1 / 10.2 | `V03_S1006` / `V03_S1007` |
| Harberger / Ramamurthy | `V03_S1508` / `V03_S1509` |
| Phillips a / c / R² | `V03_S1405` |
| Table 14.3 | `V03_S1408` |

Each anchor value is located in `SalvagedInputs/book_data/`, registered as `reference_values` (per Decision
0002 the registry must carry them even though V03 reads the XLSX at runtime), asserted, and run.

### Tolerance

Registry **1% is canonical**; V03 conforms to it. The competing 0.5% divergence is removed.

### Two new V03 check types (implemented once in `_v03_anchor_lib.py`, per Decision 0004 naming)

1. **splice-continuity** — flag if `|Δ(splice-year)| > max(3 × trailing-5-yr σ, 5%)`, driven by a new
   registry block `validation.independent_anchors[]`.
2. **level-plausibility** — per-series monotonic/sign/range assertions from the MHR §5 economic-sanity
   hooks (e.g. "Depression-must-fall"), driven by a new registry block `validation.plausibility_rules[]`.

## Consequences

- **Phase B**: B1 architects `_v03_anchor_lib.py` (`check_splice_continuity` + `check_level_plausibility`),
  reconciles tolerance to registry-1%; B2 (6 agents) wires the six anchors; B3 applies both checks to every
  extension-block series. The checks MUST fail on current **S1401** (−22.2% splice break) and **S203**
  (Depression rise) — those documented `known_reds` are the proof the tautology is broken. P32 stays PASS.
- **Phase C**: every Tier-1 fix is re-validated **under this Phase-B validator**; S1401 (C1) and S203 (C4,
  Decision 0008) flip red→green.
- **Phase D**: D0's structural-break table and the per-series skeptical protocol consume the same threshold
  and hooks; new breaks beyond the D-4 threshold become findings.
