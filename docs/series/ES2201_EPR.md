# ES2201 — Extension Provenance Record

**Series**: ES2201 — Econophysics Two-Class Income Parameters
**Phase**: 6 (Extension)
**Construction**: `composite` (verbatim Table 1 in v1.0)
**Authored**: 2026-05-18

## 1. Extendability

IRS SOI Pub 1304 Tables 1.4 and 1 are published annually with ~2-3
year lag. As of 2026, the latest available year is likely 2022 or
2023. Extension requires re-fitting the five Table-1 parameters per
year using the paper's MLE protocol — NOT growth-rate splicing of
already-fitted parameters (per Anu Framework No Lazy Splices rule,
since the five parameters are jointly estimated).

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
4. Re-fit per year; emit as ES2201-* extension rows.
5. Document TCJA/CARES AGI methodological discontinuities.

## 4. Proxies

Brooks Gini-method notes URL (paper-cited
`https://www3.nd.edu/~wbrooks/GiniNotes.pdf`) returns 404. v1.1
substitutes Cowell (2011) Measuring Inequality ch. 5 as open
methodology reference, or Wayback-archived Brooks PDF if recoverable.
This is a methodology-reference substitution, NOT a data-source proxy.

## 5. Synthetic data

None. v1.0 is verbatim transcription.
