# S902 — Extension Provenance Record

**Series**: S902 — Integrated Output-Capital Ratios and Standard Prices
**Phase**: 6 · **Construction**: `composite` of eigensystem-derived per-year vectors
**Extension**: `not_applicable_cross_sectional`
**Authored**: 2026-05-18

---

## 1. Why no extension applies

Same as S901: `content_type = "cross_sectional"`. Adding a benchmark year (e.g., 2007) is conceptually possible but requires a fresh full eigensystem solve (KT eigenvalue + standard-price vector), not a splice. Documented structural obstacles:

1. BEA discontinued the full benchmark capital flow matrix after 1997 — approximation from BEA Detailed Fixed Asset Tables (Type × Industry) under the g_j-uniform-growth assumption is necessary.
2. NAICS revisions break the 65-industry crosswalk across vintages.
3. OOH correction must be re-derived for the new year.

## 2. Classification

`cross_sectional`. Extension = benchmark-addition, deferred.

## 3. Method

None in v1.

## 4. Proxies

None.

## 5. Synthetic data

None.

## 6. Failure modes

| Failure | Detection | Action |
|---|---|---|
| Any Appendix9 workbook missing | loader | FAIL |
| `tp(r)`, `tv`, `Index` column missing | loader | FAIL |
| ObservedProfitRates workbook missing | loader | FAIL (R_obs values cannot be inferred from book table only) |

## 7. Future-work note

A v2 implementation should:
1. Read raw 65-industry A', l', K, D matrices from the original BEA tables (Use + Fixed Asset).
2. Compute KT = K·(I-(A+D))^-1 and its dominant eigenvalue R = 1/λ_max.
3. Solve the standard-price system at observed r to recover tp(r).
4. Validate against Shaikh's Table 9.18 R_t values within numerical tolerance.

This is documented in the Phase 4 ratification "Phase 5 must verify dominant-eigenvalue solve" as a downstream replication target — not a Phase 5 blocker per the playbook's static-data treatment.
