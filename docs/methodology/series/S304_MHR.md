# S304 — Discretionary Propensity to Consume, Case II — Methodological History Report (MHR)

**Group:** ch3 (Micro Foundations and Macro Patterns) · **Construction:** formula (analytic) · **Status:** book_period_validated
**Figure:** 3.6 (book p. 94) · **Predecessor:** none · **Publish:** true
**Reasoning stance:** from Shaikh's own perspective.

> Grounding: `Technical/research/S304_research.json`; KB body text
> (`.../HDARP_v3.3_Campaign/Body_Text/ch03_micro_foundations.md`, eqs. 3.4/3.5 p. 91, 93);
> `CH3_RESEARCH_SUMMARY.md`; `CH03_review.json` (F-CH3-01, F-CH3-09, F-CH3-10, F-CH3-11);
> `S304_{DPR,EPR}.md`; `L01_S304.py` (2026-05-27 recalibration), `_ch3_helpers.py`. No claim invented.

---

## 1. What it is

S304 is the **analytic curve behind Figure 3.6**: the discretionary propensity to consume necessaries, `c(y)`,
drawn as a **declining** function of income `y ∈ [0, 60]` (dimensionless, axis 0–0.8). It is the parameter
driver of Case II. Not empirical. Shaikh defines `c` verbatim (`research.book_quotes[0]`, eq. 3.4, p. 91):
`c ≡ (x1 − x1min)/(x1max − x1min) = (p1x1 − p1x1min)/(y − p1x1min)`, `0 ≤ c ≤ 1`, and states the Case-II
mechanism (`book_quotes[1]`, p. 93): rewriting eq. (3.4) as `(p1x1 − p1x1min) = c(y − p1x1min)`, *"as c falls
the curve gets flatter"* — i.e. a declining `c(y)` is an alternative route to Engel saturation. S304 supplies
the `c(y)` profile that S305 then feeds through the Engel equation.

## 2. Source lineage

Single source: **Shaikh (2016), eq. (3.4), p. 91; discussion p. 93; Figure 3.6, p. 94.** No external agency.
`L01_S304.py` evaluates `c(y) = c0·exp(−k·y)` on a `np.linspace` grid — pure formula. `subsource_id =
SHAIKH_2016_EQ_3_4_3_11`.

**Calibration history (important — 2026-05-27 recalibration).** The current, book-matched calibration is
`c(y) = 0.80·exp(−0.014·y)`, giving `c ≈ 0.70 at y=10 → 0.40 at y=50`, read off Shaikh's *printed* Fig 3.6.
This **superseded** the earlier shared `c_case_ii` (`c0 = 0.7`, `k = 0.05`) which decayed far too fast
(`c ≈ 0.06` by `y=50`) and did not match the book (`L01_S304.py` inline note; `S305` loader docstring). The
per-series recalibration is a **genuine fidelity improvement**, not a defect.

| Input | Source | Role |
|---|---|---|
| `y` (income grid) | author simulation, 0–60 model units | abscissa |
| `c(y)` | Shaikh 2016 eq. 3.4 p. 91; profile read off printed Fig 3.6 | output |
| `c0 = 0.80`, `k = 0.014` | calibrated 2026-05-27 to Fig 3.6 (0.70@y10→0.40@y50) | parameters |

## 3. Why this source — Shaikh's rationale + rejected alternatives

- **Why a declining `c(y)` at all.** Case II is Shaikh's *second, independent* demonstration that saturation
  need not come from `x1min(y)` (Case I): even with a fixed necessary minimum, a discretionary propensity that
  falls with income bends the Engel curve. Presenting both cases is the over-determination argument.
- **Why exponential decay `c0·exp(−k·y)`.** The book states only the qualitative behaviour ("c declines with
  income", "the curve gets flatter"); it does **not** print an algebraic `c(y)`. Exponential decay is the
  simplest monotone-declining one-parameter family, and its constants were pinned to Shaikh's own *plotted*
  Fig 3.6 read-off — so the choice is disciplined by the book's figure even though the formula is not in the text.
- **Rejected alternative — the fast-decay shared helper.** The abandoned `c_case_ii` (`c0=0.7, k=0.05`) is
  exactly the calibration that was *rejected* for collapsing `c` to ~0.06 by y=50, contradicting Fig 3.6. It
  now survives only as a dead helper (F-CH3-10, LOW) and must not be re-imported.
- **Rejected alternative — a stated calibration.** Author rationale for an exact `c(y)` formula is *not located
  in the corpus* — only the figure and its axis bounds constrain it.

## 4. Methodological-change exposure

**None.** No NIPA line, no I-O account, no concordance. Analytic evaluation of a book equation; fully insulated
from every NIPA comprehensive revision and SIC→NAICS break (`NIPA_CHANGE_TIMELINE.md`). The *only* "change"
in S304's history is internal: the 2026-05-27 recalibration of `c0,k` to match Fig 3.6.

## 5. Replication fidelity

- **Curve is book-matched** after the recalibration: chopped `c = 0.80 / 0.5256 / 0.3454` at idx 1/… (declining
  as Fig 3.6 requires) (`CH03_review.touchpoints` S304).
- **STALE registry reference_values (F-CH3-01, HIGH).** `series.S304.validation.reference_values` still carry
  the *pre-recalibration* numbers (`0.7 / 0.156 / 0.0349`) and now contradict the published chopped by a wide
  margin. The **code is correct; the registry refs were never regenerated** after 2026-05-27. This is a stale-
  metadata defect, not a data-authenticity problem.
- **Why the stale refs passed silently (F-CH3-11, HIGH).** V03's theoretical validator checks only shape/bounds
  (`VALIDATOR_TOL_PCT = 0.5`) and **never compares against `registry.reference_values`**, so the contradiction
  was invisible to the gate. V03 tol (0.5%) is also decoupled from registry tol (1%) (F-CH3-13, LOW).
- **Doc drift (F-CH3-09, LOW).** `CH3_RESEARCH_SUMMARY.md` still documents the pre-2026-05-27 calibration
  (`c0=0.7, k=0.05, x1min=5`).
- **F-CH3-05 / F-CH3-07 (MEDIUM):** `x_value` dropped from chopped; triage reason wrongly says ch03 unextracted.

## 6. Forward risk

- **Regenerate `reference_values` from the current loader (F-CH3-01, HIGH, blocking a clean audit).** Repopulate
  `S304.validation.reference_values` to `0.80 / 0.5256 / 0.3454` from the recalibrated `L01_S304.py`, then
  update `CH3_RESEARCH_SUMMARY.md` (F-CH3-09).
- **Add a reference-value check to V03 (F-CH3-11).** Have the theoretical validator compare emitted values to
  `registry.reference_values` (reconciling the 0.5% / 1% tolerances, F-CH3-13) so a future stale-ref/recalibration
  divergence cannot pass silently again.
- **Delete the dead `c_case_ii` helper (F-CH3-10)** to remove the risk of a future loader importing the rejected
  fast-decay curve.
- **Not extensible** (analytic); restore x_value + repair triage reason (F-CH3-05/07).
