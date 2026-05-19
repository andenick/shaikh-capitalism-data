# S302 -- Extension Provenance Record

**Series**: S302 -- Expenditure Share of Necessaries, Case I
**Phase**: 6 (Extension)
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Related**: `S302_DPR.md`, `Technical/research/S302_research.json`

---

## 1. Classification

S302 is a `theoretical` series. It is the share form (eq 3.11) of the same Case I construction as S301. There is no time dimension; no extension applies.

## 2. Method

**Extension method**: `none`. Regenerated from eq (3.11) each loader run.

## 3. Worked example

Not applicable. Worked example for S302 is the curve itself: at y=1, share = 1.0; at y=60, share = 0.5 + 0.5 * (1/sqrt(60)) approx 0.565. The curve declines monotonically toward c=0.5.

## 4. No-Proxy disclosure

No proxy substitution. See `S302_DPR.md` for source details.

## 5. No-Synthetic disclosure

No synthetic gap-filling in the prohibited sense. The DPR documents any
analytic regeneration or library-data dependence explicitly.

## 6. Failure-mode table

Same failure-mode table as S301: calibration choice (x1min, c), bound violation at low y (handled by trimming the grid to y>=1), shape-check failure (would indicate a code bug in `_ch3_helpers.py`).

## 7. CD2 divergence pre-disclosure

No CD2 predecessor; CD2 comparison block omitted.

## 8. Why no API extension applies

This series has no time dimension (theoretical/cross_sectional). The
Anu-framework rule on extension only applies to `time_series` series. The
chopped CSV is the final published deliverable.
