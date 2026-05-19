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
