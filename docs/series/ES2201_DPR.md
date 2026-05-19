# ES2201 — Econophysics Two-Class Income Distribution Parameters, US 2002-2016

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: ES2201
**Content type**: `time_series`
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-fanout-ES

## 1. Definition

ES2201 is the annual panel of five jointly-fitted parameters of the
econophysics two-class income distribution model, US tax years
2002-2016. Source: Shaikh & Jacobo (2020) "Economic Arbitrage and the
Econophysics of Income Inequality", Review of Behavioral Economics
7: 1-17, Table 1 (paper p. 5).

The five parameters per year:
- G' (Gini coefficient, bottom 97%)
- ⟨r⟩ (overall average AGI per return, thousands USD)
- ⟨w⟩ (bottom-97% mean / income temperature, thousands USD)
- f (top-3% income share, derived as 1 − ⟨w⟩/⟨r⟩)
- α (top-3% power-law exponent)

## 2. Why it matters

Each year's five parameters jointly characterize the empirical
income distribution under the two-class econophysics model
(Dragulescu-Yakovenko exponential bottom + Pareto top). The
remarkable stability of G' ≈ 0.49 across all 15 years is the
paper's headline empirical regularity — strong support for the
universal-arbitrage interpretation of personal income distribution.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| ES2201-G_prime | 2002-2016 | Shaikh-Jacobo (2020) Table 1 col G' | dimensionless | Reconstructed CSV |
| ES2201-r_mean | 2002-2016 | Table 1 col ⟨r⟩ | thousands USD | Reconstructed CSV |
| ES2201-w_mean | 2002-2016 | Table 1 col ⟨w⟩ | thousands USD | Reconstructed CSV |
| ES2201-f_top3 | 2002-2016 | Table 1 col f | dimensionless | Reconstructed CSV |
| ES2201-alpha | 2002-2016 | Table 1 col α | dimensionless | Reconstructed CSV |

Underlying primary data: IRS SOI Publication 1304 Table 1.4 (AGI bin
counts) and Table 1 (selected income items by size of AGI), tax years
2002-2016. Public domain.

## 4. Construction

`composite` — for v1.0 we ingest Table 1 verbatim. Each
`(year, parameter)` triple becomes one row.

## 5. Year coverage

Paper window: 2002-2016. Extension: re-fitting per year using the
same MLE protocol for 2017-2023 (IRS SOI release lag ~2-3 years).
v1.0 does not implement the MLE re-fit; that requires acquiring IRS
Pub 1304 Tables 1.4 + 1 for the missing years (~200 MB of PDFs).

## 6. Units

Mixed per row (see Sources table). The chopped CSV carries unit per
subseries.

## 7. Caveats

1. ⟨w⟩ is NOT a direct sample mean. Per paper appendix, it is the
   inverse slope of the MLE regression ln C(r) on r for the bottom
   section — a regression-derived "income temperature". Any extension
   must replicate this regression-based estimator, not substitute a
   direct bottom-97% sample mean.
2. f = 1 - ⟨w⟩/⟨r⟩ is an identity derived from ⟨w⟩ and ⟨r⟩, not
   independently estimated.
3. Bin midpoint convention for the top open-ended bin is not
   explicitly stated in the paper appendix; v1.1 extension must
   document a convention (Pareto-tail integral preferred).
4. TCJA (2017+) and CARES (2020+) AGI definition revisions may
   create methodological discontinuities for the extension years.
5. Brooks Gini-method notes URL (paper-cited) is 404; methodology
   reference substitution to Cowell (2011) ch. 5 or Wayback-archived
   Brooks PDF.

## 8. Cross-references

- Dossier: `Technical/research/ES2201_research.json`
- Book chapter ancestor: Ch17 (Theory of personal income distribution)
- Reconstructed: `SalvagedInputs/book_data/Reconstructed/ES2201_fitted_parameters.csv`

## 9. Validation expectation

- Tolerance: 0.5% (verbatim transcription).
