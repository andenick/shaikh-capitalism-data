# XS2201 — Extension Provenance Record

**Series**: XS2201 — Econophysics Two-Class Income Parameters
**Construction**: `composite` (verbatim Table 1 in v1.0)
**Authored**: 2026-05-18

## 1. Extendability

US Internal Revenue Service Statistics of Income (IRS SOI) Publication
1304 Tables 1.4 and 1 are published annually with a ~2-3 year lag. As of
2026, the latest available year is likely 2022 or
2023. Extension requires re-fitting the five Table-1 parameters per
year using the paper's MLE protocol — NOT growth-rate splicing of
already-fitted parameters, since the five parameters are jointly
estimated.

## 2. v1.0 scope

Direct verbatim ingestion of Shaikh-Jacobo (2020) Table 1 for
2002-2016. No re-fitting performed.

## 3. v1.1 plan

1. Acquire IRS SOI Pub 1304 Table 1.4 and Table 1 PDFs for tax years
   2017-2022 (current latest).
2. Implement MLE estimator for ⟨w⟩ (slope of ln C(r) on r, bottom
   section) and α (slope of ln C(r) on ln r, top section).
3. Document top-bin midpoint convention (Pareto-tail integral
   preferred).
4. Re-fit per year; emit as XS2201-* extension rows.
5. Document TCJA/CARES AGI methodological discontinuities.

## 4. Proxies

Brooks Gini-method notes URL (paper-cited
`https://www3.nd.edu/~wbrooks/GiniNotes.pdf`) returns 404. v1.1
substitutes Cowell (2011) Measuring Inequality ch. 5 as open
methodology reference, or Wayback-archived Brooks PDF if recoverable.
This is a methodology-reference substitution, NOT a data-source proxy.

## 5. Synthetic data

None. v1.0 is verbatim transcription.

## 6. Conceptual continuity vs adjacent concepts

The extension proxy (IRS SOI Pub 1304 Tables 1.4 and 1, re-fitted per
year using MLE) measures `two-class econophysics income distribution
parameters (G', ⟨r⟩, ⟨w⟩, f, α)` rather than `Gini coefficient on full
adjusted gross income (AGI) distribution` or `top-10% income share (Piketty-Saez)` because:
- Source agency choice: IRS SOI Pub 1304 is the only US administrative
  micro-data binned-tabulation source that supports the
  Dragulescu-Yakovenko exponential + Pareto MLE jointly. Survey-based
  CPS/PSID sources truncate the Pareto top tail and are not suitable.
- Methodology continuity: paper-window 2002-2016 parameters were MLE-fit
  on SOI bin midpoints; extension years (2017+) re-fit on the same Tables
  1.4 + 1, NOT growth-rate-spliced from the existing fitted parameters
  (these five parameters are jointly estimated, not directly observed).
- Disambiguation: G' is the *bottom-97%* Gini, NOT the full-population
  Gini (Census/CBO/World Bank report the latter); α is the *top-3%*
  Pareto exponent, NOT the Piketty-Saez top-share statistic; ⟨w⟩ is a
  regression-derived "income temperature" inverse slope, NOT a sample
  mean.

The book's original concept (Shaikh-Jacobo 2020 p. 5, Table 1) was:
"the parameters of the two-class income distribution model" estimated
under the universal-arbitrage interpretation. The modern series
preserves the five-parameter joint-MLE estimator and the bottom-97% /
top-3% split-point convention while permitting TCJA/CARES AGI definition
revisions in 2017+ to introduce documented methodological breaks. This
is not a proxy substitution because
IRS SOI Pub 1304 is exactly the data the paper uses; extension reruns
the paper's MLE estimator on later vintages of the same publication.
