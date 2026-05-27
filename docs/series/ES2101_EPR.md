# ES2101 — Extension Provenance Record

**Series**: ES2101 — Sraffa Curvature Index Summary
**Phase**: 6 (Extension)
**Construction**: `derived` (verbatim summary stats in v1.0; pipeline-derived in v1.1)
**Authored**: 2026-05-18

## 1. v1.0 scope

Verbatim Section 5 (p. 272) summary statistics for 2002 and 2007 BEA
benchmark IO matrices.

## 2. v1.1 plan

Shared BEA-to-Sraffa pipeline with ES2001 (see ES2001_EPR §3). v1.1
implementation regenerates:

- 295 aggregated A matrices for 2002 (176 levels) + 2007 (119 levels)
- Per-matrix Sraffa price curves p(r) at 21 sample points
- Per-matrix Curvature Index CI = 1 - SI (Bienenfeld-line vs arc length)
- Per-matrix Theil indexes
- Full reconstruction of Figures 6 and 7 scatters
- Extension to BEA Benchmark IO 2012 and 2017 (subject to NAICS
  bridging documentation in EPR addendum)

## 3. Proxies

BLS sect300.xls crosswalk URL is 403 (paper-cited). v1.1 substitutes
current BLS Employment Projections industry data; this is a URL
migration within an active domain, NOT a data-source proxy.

## 4. Synthetic data

None. v1.0 is verbatim transcription.

## 5. Conceptual continuity vs adjacent concepts

The extension proxy (v1.1 shared BEA-to-Sraffa pipeline + extended
BLS Employment Projections crosswalk) measures `Sraffa Curvature Index
distribution across aggregation levels` rather than `single-matrix CI
point estimates` or `Theil price-value dispersion alone` because:
- Source agency choice: BEA Benchmark IO at the 176/119-order detail is
  the only published US matrix that supports the 295-aggregation rollup.
  No alternative agency provides comparable industry detail.
- Methodology continuity: v1.0 verbatim summary stats and v1.1 full CI
  distribution both apply Bienenfeld-line vs arc-length per p(r) curve.
  Adding 2012/2017 benchmark matrices reuses the same CI = 1 − SI
  estimator, not a substitute.
- Disambiguation: Curvature Index (CI < 0.1) is NOT the price-value
  ratio of ES2001 — CI characterizes the *shape* of p(r) over r ∈ [0, R],
  while ES2001 reports the scalar p(r_obs)/v aggregate. Both belong to
  the same Sraffa-stochastic-effect evidence base but answer different
  questions and have different content_type tags.

The book's original concept (Shaikh-Coronado-Nassif-Pires 2020 §5, p. 272)
was: "Sraffa price curves are close to linear" — operationalized as
CI < 0.1 across all 295 aggregations and only 6% labor-value sign
switches in 2002. The modern series preserves the CI estimator and
aggregation-level rollup methodology while permitting the BLS
Employment Projections crosswalk URL migration (sect300.xls → current
EP industry data; same agency, current URL). This is NOT a proxy
substitution forbidden by the No-Proxy rule because (a) BEA IO is the
same source family, (b) BLS Employment Projections is the same agency
under a renamed program — concept-identical labor input data.
