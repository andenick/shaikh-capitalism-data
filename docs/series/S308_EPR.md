# S308 -- Extension Provenance Record

**Series**: S308 -- Necessary Good (x1) Demand Curves, Four Different Micro Foundations
**Phase**: 6 (Extension)
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Related**: `S308_DPR.md`, `Technical/research/S308_research.json`

---

## 1. Classification

`theoretical` (composite). No extension applies.

## 2. Method

**Extension method**: `none`. Theoretical curve regenerated from eq (3.5); NetLogo curves tabulated from the printed figure with documented per-model offsets. Both are static.

## 3. Worked example

At p1=1.0: x1_theoretical = (1-0.5)*10 + 0.5*200/1.0 = 5 + 100 = 105. At p1=1.5: 5 + 66.67 = 71.67. NetLogo curves at p1=1.0: S308-B = 104.79, S308-C = 105.32, S308-D = 104.475, S308-E = 105.525.

## 4. No-Proxy disclosure

No proxy substitution. See `S308_DPR.md` for source details.

## 5. No-Synthetic disclosure

No synthetic gap-filling in the prohibited sense. The DPR documents any
analytic regeneration or library-data dependence explicitly.

## 6. Failure-mode table

If NetLogo source code is ever obtained and re-simulated, the chopped CSV would replace the tabulated offsets with actual Monte-Carlo curve averages. Until then, the printed-figure tabulation is the best-available proxy.

## 7. CD2 divergence pre-disclosure

No CD2 predecessor.

## 8. Why no API extension applies

This series has no time dimension (theoretical/cross_sectional). The
Anu-framework rule on extension only applies to `time_series` series. The
chopped CSV is the final published deliverable.
