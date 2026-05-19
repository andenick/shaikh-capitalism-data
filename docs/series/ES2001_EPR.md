# ES2001 — Extension Provenance Record

**Series**: ES2001 — Shaikh (2020) Sraffa Price-Value Aggregates
**Phase**: 6 (Extension)
**Construction**: `composite` (table verbatim + pipeline-derived in v1.1)
**Authored**: 2026-05-18

## 1. Extendability in principle

The paper's Tables 1-2 panel is sparse in time (6 benchmark years
1947-1998). Filling the missing BEA benchmark years (1977, 1982, 1987,
1992, 2002, 2007, 2012, 2017) is methodologically straightforward: it
requires re-running the same Sraffa-aggregate computation (eqs 6, 8, 10
of the paper) on each missing benchmark IO matrix. The result would be
a near-quinquennial 1947-2017 time series of the SSE evidence.

## 2. v1.0 scope

Direct ingestion of Tables 1-2 verbatim. No extension years computed.
Validation compares processed parquet against the reconstructed CSV
cell-by-cell.

## 3. v1.1 plan: shared BEA-to-Sraffa pipeline

CHES adequacy explicitly recommends a shared
`BEA_benchmark_IO_to_Sraffa_pipeline` module consumed by both ES2001
and ES2101. v1.1 implementation:

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

## 6. Source-URL substitutions

Per decision 0005 / CHES adequacy: `anwarshaikhecon.org` was DNS-
unreachable 2026-05-18. The canonical URL-of-record for ES2001 is
the archival PDF at:
`Inputs/Capitalism Data/Technical/data/raw/01_SOURCE_MATERIALS/Web Folders/Shaikh Publications/[2020] Shaikh - An Empirically Sufficient Form for Sraffa Prices.pdf`

Festschrift volume metadata per paper's own reference list (p. 20):
Velupillai (ed.), Palgrave Macmillan. DOI pinning is a v1.1 task.
