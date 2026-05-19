# S903 — Extension Provenance Record

**Series**: S903 — Actual Wage-Profit Curves
**Phase**: 6 · **Construction**: `formula` over per-year benchmark cross-sections
**Extension**: `not_applicable_cross_sectional`
**Authored**: 2026-05-18

---

## 1. Why no extension applies

`content_type = "cross_sectional"` (Phase 4 ratified). Each year's wage-profit curve is a per-year benchmark cross-section over r-space. Extension = adding a new benchmark year (e.g., 2007, 2012, 2017), which requires:

1. Fresh BEA Use Table + Fixed Asset Tables IO + eigensystem solve for that year (S902-level work).
2. PWT productivity index recompute, plus the No-Lazy-Splices rule: the productivity multiplier applies to the *freshly-derived* σW(r), not to a re-scaled wr(r).
3. NAICS-vintage breaks make the 65-industry crosswalk discontinuous.

For these reasons no time-series-splice extension applies; the "extension" path is benchmark-addition, deferred.

## 2. Classification

`cross_sectional` (Phase 4 ratified, demoted from earlier `time_series`).

## 3. PWT 7.1 → PWT 10.01 splice strategy (when v2 implements an extension)

When a post-1998 benchmark is added, the productivity ratio yr_t / yr_0 should be computed as:

```
yr_t_v2 = PWT_10.01.RGDPO_per_EMP[t]
yr_0    = PWT_7.1.rgdpwok[1947]   (from Appendix9_PennWorldTables.xlsx, pre-computed)

# Bridge across PWT vintages via overlap year (anchor at 1998 or 2010):
bridge_anchor = 1998
scale = PWT_7.1.rgdpwok[bridge_anchor] / PWT_10.01.RGDPO_per_EMP[bridge_anchor]

yr_t_on_book_units = PWT_10.01.RGDPO_per_EMP[t] * scale

productivity_index_on_1947_base = yr_t_on_book_units / yr_0
```

The growth-rate splice is on the *productivity index*, not on the wage-profit curve. The freshly-derived σW(r) for year t is then multiplied by the spliced index. **This is mandatory** per the No-Lazy-Splices rule.

## 4. Proxies

None in book period. PWT 10.01 is not a proxy for PWT 7.1 — they are different vintages of the same Penn World Tables product (Groningen/Pennsylvania).

## 5. Synthetic data

None.

## 6. Failure modes

| Failure | Detection | Action |
|---|---|---|
| PennWorldTables2.xlsx missing | loader | FAIL |
| Required column (`r{YR}`, `wshr{YR}`, `wr{YR}`) missing | loader | FAIL |
| R_fixed values drift from Table 9.18 | validator | FAIL (sanity gate on R_t) |

## 7. CD2 divergence

CD2 `S049` was a stub with overflowing 11-figure list. S903 publishes the actual wage-profit-curve data from Shaikh's pre-computed columns and conforms to the Phase 4 trimmed figure list (Fig 9.8, 9.12, 9.19).
