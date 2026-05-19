# S306 -- Extension Provenance Record

**Series**: S306 -- Empirical Expenditure Share on Food (Working Class Budgets, United Kingdom, 1904)
**Phase**: 6 (Extension)
**Content type**: `cross_sectional`
**Authored**: 2026-05-18
**Related**: `S306_DPR.md`, `Technical/research/S306_research.json`

---

## 1. Classification

`cross_sectional`. No extension applies; the only meaningful 'extension' would be a separate modern cross-section (UK ONS LCF) published in parallel, NOT a splice.

## 2. Method

**Extension method**: `not_applicable_cross_sectional`. Single year (1904).

## 3. Worked example

Not applicable. When/if Allen & Bowley Table 1 is digitised, the worked example will be the tabulation: each row maps an income band's average to a food-share percent.

## 4. No-Proxy disclosure

No proxy substitution. See `S306_DPR.md` for source details.

## 5. No-Synthetic disclosure

No synthetic gap-filling in the prohibited sense. The DPR documents any
analytic regeneration or library-data dependence explicitly.

## 6. Failure-mode table

Underlying tabulation not in SalvagedInputs (current state). Loader emits `data_unavailable_pending_digitization`. Future: substitute Cd. 3864 (1908) public-domain tabulation; rerun loader; expect non-empty data parquet.

## 7. CD2 divergence pre-disclosure

No CD2 predecessor; the entire S30* range is new in RSCD.

## 8. Why no API extension applies

This series has no time dimension (theoretical/cross_sectional). The
Anu-framework rule on extension only applies to `time_series` series. The
chopped CSV is the final published deliverable.
