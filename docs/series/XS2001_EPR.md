# XS2001 — Extension Provenance Record

**Series**: XS2001 — Shaikh (2020) Sraffa Price-Value Aggregates
**Construction**: `composite` (table verbatim + pipeline-derived in v1.1)
**Authored**: 2026-05-18

## 1. Extendability in principle

The paper's Tables 1-2 panel is sparse in time (6 benchmark years
1947-1998). Filling the missing BEA benchmark years (1977, 1982, 1987,
1992, 2002, 2007, 2012, 2017) is methodologically straightforward: it
requires re-running the same Sraffa-aggregate computation (eqs 6, 8, 10
of the paper) on each missing benchmark input-output (IO) matrix. The
result would be a near-quinquennial 1947-2017 time series of the Sraffa
Stochastic Effect (SSE) evidence.

## 2. v1.0 scope

Direct ingestion of Tables 1-2 verbatim. No extension years computed.
Validation compares processed parquet against the reconstructed CSV
cell-by-cell.

## 3. v1.1 plan: shared BEA-to-Sraffa pipeline

A shared US Bureau of Economic Analysis (BEA) benchmark-IO-to-Sraffa
pipeline module should be consumed by both XS2001 and XS2101. v1.1
implementation:

1. Build BEA Benchmark IO loader (Use/Make tables, 71/65/403/387-order
   per year).
2. Apply paper-Appendix-1 exclusions (owner-occupied dwellings, scrap,
   used/secondhand, non-comparable imports, RoW adjustment).
3. Construct A matrix; compute H = A(I-A)^-1; solve eigenvalue R and
   left-eigenvector p(R).
4. Compute Sraffa prices p(r) at r_obs; compute aggregate price-value
   ratios.
5. Fill missing benchmark years 1977/1982/1987/1992/2002/2007/2012/2017.
6. Regenerate Figures 1-9 (2002 403-sector price-value curves +
   Bienenfeld linear/quadratic approximations) per equations 6, 8, 10.

This is a multi-day engineering effort and is explicitly deferred.

## 4. Proxies

None. Tables 1-2 are the paper's own computed values.

## 5. Synthetic data

None. v1.0 is verbatim transcription only.

## 6. Conceptual continuity vs adjacent concepts

The extension proxy (v1.1 shared BEA-to-Sraffa pipeline) measures
`Sraffa aggregate price/value ratios at observed rates of profit` rather
than `nominal-vs-real GDP ratios` or `Marx-Tonak constant/variable
capital aggregates` because:
- Source agency choice: BEA Benchmark IO Use/Make tables are the input
  to the paper's eqs 6, 8, 10. No alternative agency exists for the
  industry-level technology matrix needed.
- Methodology continuity: the v1.0 verbatim Tables 1-2 panel and the
  v1.1 extended panel both run *the same* eigenvalue/left-eigenvector
  computation on *the same* BEA-IO matrix family. Adding 1977/1982/.../2017
  benchmark years is concept-identical, not concept-substituting.
- Disambiguation: aggregate price/value ratios are NOT cross-sectional
  Sraffa price curves p(r) — those are XS2101's empirical object.
  Tables 1-2 collapse the curve to a single scalar at r_obs per
  (model, year). Extension preserves the scalar concept; the curve
  concept lives in a sibling series.

The book's original concept (Shaikh 2020 p. 9, "The Six Benchmark Year
Tables") was: "the close empirical correspondence between Sraffa prices
and labor values across the entire empirically observed range of the rate
of profit". The modern series preserves the scalar aggregate-ratio
computation while permitting matrix-order discontinuities (71-order
for 1947-1972, 65-order for 1998, 403/171-order for 2002+). This is not
a proxy substitution because BEA IO is
the canonical and only source of the input; extension years use exactly
the same source family at successive vintages.

## 7. Source-URL substitutions

`anwarshaikhecon.org` was DNS-unreachable 2026-05-18. The canonical
source-of-record for XS2001 is the archival PDF of Shaikh (2020),
"An Empirically Sufficient Form for Sraffa Prices".

Festschrift volume metadata per paper's own reference list (p. 20):
Velupillai (ed.), Palgrave Macmillan. DOI pinning is a v1.1 task.
