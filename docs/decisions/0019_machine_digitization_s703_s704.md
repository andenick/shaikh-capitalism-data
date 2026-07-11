---
decision_id: "0019"
title: "Machine Digitization Recovers S703/S704 (Christodoulopoulos Fig 7.13/7.14 aggregate lines); Human returns/ Path Remains Superseding"
status: approved
proposed_at: "2026-07-02T00:00:00Z"
approved_at: "2026-07-02T00:00:00Z"
decided_by: user
ratification: "user ruling 2026-07-02 — 'keep it safe, do what you want with it'"
amends: 0018_tier5_s703_s704_guided_digitization_scheduling.md
related:
  - 0018_tier5_s703_s704_guided_digitization_scheduling.md
  - 0005_discontinued_apis_deferred.md
  - 0011_independent_anchor_validation.md
affected_series:
  - S703
  - S704
---

# 0019 — Machine Digitization Recovers S703/S704; Human returns/ Path Remains Superseding

**Status**: APPROVED — user authorized 2026-07-02 ("keep it safe, do what you want with it").
**Decided by**: user. **Amends**: Decision 0018 (which reserved S703/S704 for guided human
digitization and forbade proxies). 0018's proxy prohibition SURVIVES untouched; its "human pass
only" reservation is relaxed to "machine digitization is now authorized, and the human pass
remains an optional, superseding path forever."

## Context

S703 (Fig 7.13, World manufacturing average rate of profit — WORLDAVG line) and S704 (Fig 7.14,
US manufacturing average rate of profit — USMANAVG line) were the last two `data_unavailable`
series among the chapter-7 Christodoulopoulos (1995) / OECD ISDB exhibits. The raw data are
unrecoverable (unpublished NSSR working paper; OECD ISDB 1994 vintage discontinued); only the
printed 9-line "spaghetti" figures remain. Decision 0018 scheduled a guided human WebPlotDigitizer
session and forbade proxies. On 2026-07-02 the user authorized recovering the two aggregate lines
by **machine digitization** under strict safety + honesty invariants, keeping the human path open.

## Decision

**Recover S703/S704 by machine digitization of the printed aggregate line, under adversarial
verification; publish both; keep the human `returns/` path superseding forever; never proxy.**

### Method (per figure)

1. **Dual independent extraction** — two agents traced the target line with different techniques
   (geometry-first axis calibration + marker/stroke tracing; sampling-first per-year column scan),
   each blind to the other's output, each emitting a calibration record + annotated overlay.
2. **Cross-validation + adjudication** — a mechanical per-year agreement test; every disagreeing
   point re-examined at high zoom with a fresh local pixel measurement and ruled per point (never
   silently averaged).
3. **Adversarial verification** — a third agent, seeing only the figure + the consensus, rebuilt
   the calibration from scratch and tried to REFUTE the curve (wrong line? bad calibration?
   missing/extra years?). Both figures returned **CONFIRMED, no point refuted**.

### Outcome

| Series | Line | Coverage | Confidence | Gate |
|---|---|---|---|---|
| S703 | WORLDAVG open-circle, avg panel | 1970–1990, 20 pts (1974 omitted) | MEDIUM-HIGH, ~±0.005 decimal, mean conf 0.666 | M2 raw PASS (95%); M3 CONFIRMED |
| S704 | USMANAVG boldest markerless, avg panel | 1960–1989, 30 pts (1990 omitted) | HIGH, ~±0.5pp, mean conf 0.757 | M2 raw FAIL (53%) fully diagnosed → resolved; M3 CONFIRMED |

Both flip `data_unavailable → book_period_validated`, `publish: false → true`. Values are stored
in the project's canonical rate convention (decimal; S704's figure-percent is divided by 100 to
match sibling S705/S706). Honest gaps stay gaps: **S703 1974** is omitted (no defensible open-circle
marker on the steep 1973→1975 descent); **S704 1990** is omitted (a 31st data column exists but the
markerless USMANAVG vertex is occluded by a triangle marker — see `machine/S704_1990_omission_ruling.md`).

### Publish justification (recorded verbatim per the campaign mandate)

> S703 passed the M2 gate raw (95%); S704's raw gate failure was fully diagnosed (extractor-B
> calibration error) and the values carry three independent agreeing measurements (extractor-A, the
> M2 crop re-measurement, and the adversarial verifier's data-anchored rebuild) — record this
> reasoning verbatim in the decision doc.

Elaborated: **S703** cleared the mechanical agreement gate at its raw threshold (19/20 = 95%, need
≥85%); the adversarial verifier independently landed the consensus on the correct open-circle marker
at every tested year. **S704**'s raw agreement gate failed (16/30 = 53%, need ≥90%) — but the failure
was **entirely** extractor-B's systematic **+1-year x-offset** (B mis-numbered the tick ladder; the
first tick sits ~1 yr right of the printed "1960" label). Every failing point was re-measured by the
boldest-markerless-stroke criterion and resolved to extractor-A, and the adversarial verifier then
rebuilt the x-calibration from scratch — data-anchored on the evenly-spaced annual marker comb — and
independently confirmed extractor-A's registration (peak 1965, trough 1982), ruling out the +1-yr
shift. Each of the 30 S704 values therefore carries **three agreeing measurements**. A diagnosed and
resolved gate failure with triple-corroborated values is publishable; an undiagnosed one would not be.

### Precedence rule (permanent)

The human path is preserved forever. If a hand-digitized CSV is ever filed at
`digitization_packet/returns/S70x_aggregate_digitized.csv`, a future session ingests it as the
**superseding** source (provenance rank: `human_guided` > `machine_digitized`). The `L01_S70x`
loaders already implement this returns-precedence guard; the packet `index.html` records the rule.

## Consequences

- RSCD `data_unavailable` count falls **4 → 2** (S703/S704 recovered; **S306/S307**, the 1904 UK
  working-class-budget Engel series, remain `data_unavailable` — a separate, unrelated open item).
  The chapter-7 profit-rate exhibits are now complete.
- Provenance is honest end-to-end: every recovered value is tagged `machine_digitized` with method,
  image source, calibration record, and a per-series transcription-confidence grade; gaps are gaps.
- The recovered series ship to the public site with explainers that state the values were recovered
  by digitizing the printed figure and carry a transcription tolerance.
- Nothing was moved or deleted; all work lives in the new `digitization_packet/machine/` directory
  and standard `_backups/`. The packet, its `images/`, and the reserved `returns/` contract are
  intact.

## Amendment to 0018

0018's status line is updated to **superseded-in-part** by this decision: machine digitization is
authorized and executed; 0018's no-proxy rule and the standing option of a superseding guided human
pass both remain in force.
