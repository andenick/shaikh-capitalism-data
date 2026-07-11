# S304 -- Extension Provenance Record

**Series**: S304 -- Discretionary Propensity to Consume, Case II
**Record type**: Extension Provenance Record
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Related**: `S304_DPR.md`, research dossier

---

## 1. Classification

`theoretical`; c(y) declining functional form (Case II setup).

## 2. Method

**Extension method**: `none`. Re-evaluated each time the data-loading step runs.

## 3. Worked example

Pass-through; c(0) = 0.7, c(60) ~ 0.035. Monotone declining.

## 4. No-Proxy disclosure

No proxy substitution. See `S304_DPR.md` for source details.

## 5. No-Synthetic disclosure

No synthetic gap-filling in the prohibited sense. The companion Data Provenance Record (DPR) documents any analytic regeneration or library-data dependence explicitly.

## 6. Failure-mode table

Form choice (exponential vs alternative); bound violation; shape failure.

## 7. Predecessor divergence pre-disclosure

Predecessor series: none (first constructed in this dataset).

## 8. Why no API extension applies

This series has no time dimension (theoretical/cross_sectional). The
Anu-framework rule on extension only applies to `time_series` series. The
chopped CSV is the final published deliverable.
