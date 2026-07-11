# XS2101 — Sraffa Price Curvature Indexes, US BEA 2002 + 2007 (Shaikh-Coronado-Nassif-Pires 2020)

**Data Provenance Record (DPR)**
**Series ID**: XS2101
**Content type**: `derived`
**Status**: study_complete
**Authored**: 2026-05-18

This series was previously catalogued under the identifier ES2101.

## 1. Definition

XS2101 represents the headline summary statistics of Shaikh, Coronado &
Nassif-Pires (2020) "On the empirical regularities of Sraffa prices",
EJEEP 17(2): 265-275. Sraffa prices are production prices derived from
an economy's input-output structure. The paper computes the **Curvature
Index (CI)** distributions and the **label-switching statistics** (share
of prices that switch sign relative to their labor value, and share that
switch relative to the Bienenfeld line) across 295 aggregations of US
input-output (IO) benchmark matrices from the US Bureau of Economic
Analysis (BEA) for 2002 and 2007.

For v1.0, XS2101 ships the verbatim named summary statistics quoted in
paper Section 5 (p. 272) — the shipped `statistic` column carries
`avg_CI_lower_bound`/`avg_CI_upper_bound`, `n_prices_switching_value`(_pct),
`n_prices_switching_bienenfeld`(_pct), and `max_bienenfeld_deviation_pct`
(no Theil statistic is present). The full ~295-point CI and label-switching
scatters (Figures 6 and 7) require the shared BEA-to-Sraffa pipeline and are
deferred to v1.1 alongside XS2001.

## 2. Why it matters

CI < 0.1 across all aggregations is the paper's headline empirical
finding: Sraffa price curves are nearly linear, validating Bienenfeld's
(1988) linear approximation. The fact that only 6% of 2002 prices
switch labor-value sign, and only 1% switch the Bienenfeld line (none
with >1% deviation), is independent confirmation of the Sraffa
Stochastic Effect already shown in XS2001 at the aggregate level.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| XS2101-A | 2002, 2007 | Paper Section 5 (p. 272) verbatim summary statistics | dimensionless / counts / percent | reconstructed CSV |

Underlying primary data: BEA Benchmark IO 1977/1982/1987/1992/1997/2002/
2007 detailed tables; US Bureau of Labor Statistics (BLS) Employment
Projections industry data for skill-adjusted labor coefficients. Shared
with XS2001 (v1.1 pipeline).

## 4. Construction

`derived` — v1.0 verbatim transcription of summary statistics. v1.1 will
recompute the full 295-matrix CI distribution.

## 5. Year coverage

2002 and 2007 (the two benchmark years for which the CI and
label-switching distributions are computed in the paper).

## 6. Units

Mixed per row: dimensionless (CI averages), count (n_prices), percent
(switching shares, Bienenfeld max deviation).

## 7. Caveats

1. **Full distribution NOT computed in v1.0.** Figures 6 and 7
   require the shared BEA-to-Sraffa pipeline deferred to v1.1.
2. The "295 matrices" total = 176 (2002 aggregation levels) + 119
   (2007 aggregation levels) per paper Appendix 1; this is a
   methodology constant, not a data point.
3. BLS sect300.xls crosswalk URL (paper-cited) is 403; v1.1 must
   locate current BLS Employment Projections industry data successor.

## 8. Cross-references

- Companion: `XS2001` (Shaikh 2020 aggregate ratios) — shares the BEA-to-Sraffa pipeline

## 9. Validation expectation

- Tolerance: 0.5% (verbatim transcription of named summary stats).
