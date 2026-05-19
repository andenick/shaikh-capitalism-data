# S301 — Extension Provenance Record

**Series**: S301 — Change in Expenditure on Necessaries Relative to Change in Income, Case I
**Phase**: 6 (Extension)
**Content type**: `theoretical`
**Extension classification**: `not_applicable_theoretical`
**Authored**: 2026-05-18
**Related**: `S301_DPR.md`, `Technical/research/S301_research.json`

---

## 1. Classification

S301 is a `theoretical` series (per Phase 3 re-typing, ratified in `CH3_ADEQUACY_REPORT.json`). It is an analytic curve derived from Shaikh's equations (3.5)-(3.11) under Case I, plotted over a synthetic income grid. There is no time dimension.

## 2. Method

**Extension method**: `none`. The series is regenerated from the published equations on every loader run. There is nothing to splice forward.

## 3. Worked example

Not applicable. The "extension" of a theoretical curve is the curve itself — recomputed each run from the same equations and parameters. If Shaikh ever publishes additional Case I material (e.g., a Case I-bis with a different x1min(y) profile), this would constitute a *variant* of S301, not an *extension* — it would be authored as a new series or as a methodology variant under the Anu variant infrastructure.

## 4. No-Proxy disclosure

No proxy substitution. The "data" are Shaikh's own equations evaluated on the income grid. The only judgement call is the calibration of x1min(y) and c, which are documented in `S301_DPR.md` §4.

## 5. No-Synthetic disclosure

No synthetic data in the prohibited sense (anu-framework §No Synthetic Data). The curve values are the deterministic output of evaluating eq (3.5) at each grid point — this is the *documented analytical method* of the original source (Shaikh's own equations). Per the framework: "No approximations or interpolations unless they are the documented analytical method of the original source." Evaluating the published equation at grid points IS the documented method.

The income grid itself (y in (0, 60]) is an arbitrary discretisation; Shaikh's Figure 3.3 also presents the curve on a continuous axis without publishing a tabulated grid. Our 121-point grid is denser than the printed figure and chosen for chopped-CSV convenience; the curve at any specific y is exactly the analytic value, not an interpolant.

## 6. Failure-mode table

| Failure | Detection | Action |
|---|---|---|
| Calibration choice (x1min(y), c) departs from book's apparent figure | V03 shape/bounds checker flags out-of-range values | Re-calibrate; document new choice in DPR |
| Numeric overflow at y=0 (square-root singularity) | Loader filters y<=0.5 | Trim grid to y in [0.5, 60]; documented as a known artefact |
| Disagreement with empirical analogs (S306/S307) | Out of scope for V03 of S301; tracked in chapter-level analysis (Phase 9) | Not a S301 failure — the theoretical claim is compatibility with shape, not exact agreement with the 1904 cross-section |

## 7. CD2 divergence pre-disclosure

Not applicable. S301 has no CD2 predecessor (`predecessor_ids.cd2_id == null`). The chapter as a whole was not in the CD2 registry's S30* range. The V03 validator omits the CD2 comparison block for this series.

## 8. Why no API extension applies

Theoretical curves are not extendable in the time-series sense. There is no agency or release schedule that "publishes new values" of a closed-form expression. The Anu Framework rule on extension applies only to `time_series` series.

This series will be re-evaluated on every loader run from the same equations — that is the only meaningful sense in which it is "kept current."
