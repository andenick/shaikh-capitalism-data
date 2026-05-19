# ES2001 — Sraffa Price-Value Aggregates, US 1947-1998 (Shaikh 2020 Tables 1-2)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: ES2001
**Content type**: `time_series` (aggregate-ratio panel)
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-fanout-ES

## 1. Definition

ES2001 is the panel of aggregate price/value ratios at observed rates
of profit, for two Sraffa-price models (circulating and fixed capital),
across the six US BEA benchmark IO years Shaikh (2020) covers:
1947, 1958, 1963, 1967, 1972, 1998. Source: Shaikh (2020) "An
Empirically Sufficient Form for Sraffa Prices", Tables 1 and 2
(paper p. 10).

The panel has 12 rows (2 models × 6 years), each carrying nine
aggregate ratios (r_obs, r_obs/R, constant capital, variable capital,
surplus value, value added, rate of surplus value, rate of profit,
maximum rate R). All ratios fall in [0.94, 1.08].

## 2. Why it matters

The Tables-1/2 panel is the paper's empirical evidence for the
**Sraffa Stochastic Effect** (SSE): statistical compensation of large
numbers makes price and labor-value aggregates essentially identical
across all 6 benchmark years and both capital-stock models. This is
the time-series content of the paper.

The paper's Figures 1-9 — illustrative 403-sector Sraffa price-value
curves and Bienenfeld linear/quadratic approximations from the 2002
BEA 403-order matrix — are a **separate** empirical object (cross-
sectional, 2002-only) deferred to v1.1 (see EPR §3).

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| ES2001-circ-* | 1947, 1958, 1963, 1967, 1972, 1998 | Shaikh (2020) Table 1 (circulating capital) | dimensionless ratio | `SalvagedInputs/book_data/Reconstructed/ES2001_aggregate_ratios.csv` |
| ES2001-fixed-* | same 6 years | Shaikh (2020) Table 2 (fixed capital) | dimensionless ratio | same CSV |

Underlying primary data: BEA Benchmark IO 1947-1972 (71-order) and 1998
(65-order), plus Shaikh (1998) Appendix 15.2 and Shaikh (2012) Data
Appendix for physical bundles. Per CHES adequacy: ES2001 and ES2101
share this BEA-to-Sraffa pipeline (deferred shared module to v1.1).

## 4. Construction

For v1.0: direct ingestion of Tables 1-2 verbatim from the published
PDF. Each `(model, year, aggregate)` triple becomes one row; subseries
naming convention is `ES2001-{circ|fixed}-{aggregate_key}`.

## 5. Year coverage

Paper window: 1947-1998 (6 sparse benchmark years per model). Extension
to additional BEA benchmark years (1977, 1982, 1987, 1992, 2002, 2007,
2012, 2017) deferred to v1.1 — requires shared BEA-to-Sraffa pipeline.

## 6. Units

All ratios dimensionless. `r_obs` and `r_obs/R` are rates of profit
(decimal). The other 7 columns are price-aggregate / value-aggregate
ratios in [0.94, 1.08].

## 7. Caveats

1. **Sparse benchmark years** (1947, 1958, 1963, 1967, 1972, 1998).
   Intermediate years not computed in the paper.
2. **Matrix-size discontinuity**: 71-order for 1947-1972, 65-order for
   1998. Documented as a column in the chopped CSV.
3. The 1998 column in Table 2 has Rate of Profit = 0.98 and Max Rate
   R = 1.00 — the only sub-unit Max Rate in the panel; this is per
   the paper, not a transcription error.
4. The paper's Figures 1-9 (403-sector cross-sectional curves) are
   NOT in this series; see ES2001_EPR §3 for v1.1 plan.

## 8. Cross-references

- Dossier: `Technical/research/ES2001_research.json`
- Companion: `ES2101` (Shaikh-Coronado-Nassif-Pires 2020, 295-matrix
  CI distribution) — shares BEA-to-Sraffa pipeline
- Reconstructed: `SalvagedInputs/book_data/Reconstructed/ES2001_aggregate_ratios.csv`
- Decision 0001 (ES scope)

## 9. Validation expectation

- Tolerance: 0.5% (verbatim transcription).
- Compares processed parquet against the reconstructed CSV cell-by-cell.
