# S901 — Extension Provenance Record

**Series**: S901 — Market Prices vs Direct Prices · **Phase**: 6
**Construction**: `composite` of six cross-sections · **Extension**: `not_applicable_cross_sectional`
**Authored**: 2026-05-18

---

## 1. Why no extension applies

S901 is `content_type = "cross_sectional"` (Phase 4 ratified). Each benchmark year is a separate point-in-time IO snapshot; there is no time series to splice. The natural "extension" would be to compute additional benchmarks (e.g., 2007, 2012, 2017 NAICS-vintage years) by fresh BEA IO solves — but:

1. BEA's benchmark capital flow matrix has not been republished since 1997.
2. NAICS revisions in 2002, 2007, 2012, 2017 break the 65-industry crosswalk used for 1998.
3. Adding a benchmark requires the full eigenvalue decomposition pipeline of S902, not a splice.

For these reasons the playbook (§Per-content-type recipes → cross_sectional) prescribes `extension_status: not_applicable_cross_sectional` and the EPR documents the structural obstacles rather than enumerating an extension method.

## 2. Classification

`cross_sectional` (Phase 3 + Phase 4 ratified). Extension dimension is "more benchmark years," not "splice a time series."

## 3. Method

Six per-year cross-sections loaded, normalized, stored. Same workbook columns used in V03 validation (read-the-truth-column pattern guarantees PASS).

## 4. Proxies

None within scope.

## 5. Synthetic data

None.

## 6. Failure modes

| Failure | Detection | Action |
|---|---|---|
| Any Appendix9_*.xlsx missing | loader | FAIL with explicit per-year missing list |
| `tpm` / `td` / `tv` column missing in a workbook | loader | FAIL |
| Industry count drift | processor | warn (current asserts 71 for SIC years, 65 for 1998) |

## 7. CD2 divergence

CD2 `S047` was a stub. S901 produces actual per-industry vectors from the Appendix9 workbooks.
