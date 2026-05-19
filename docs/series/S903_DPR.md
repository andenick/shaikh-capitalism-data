# S903 — Actual Wage-Profit Curves, US 1947-1998

**DPR** · **Phase**: 5 · **Series ID**: S903 · **Status**: ingested · **Authored**: 2026-05-18

---

## 1. Definition

**S903** is the empirical wage-profit (w-r) curve, computed for each benchmark year by solving the fixed-capital price system and scaling the wage share by a PWT 7.1 real-output-per-worker productivity index so that curves at different years can be compared on a common real axis. Each year's curve covers r ∈ [0, R_t] where R_t is that year's maximum profit rate. The published outputs are:

- The 1998 wage-profit curves for the circulating model (Fig 9.8) and fixed model (Fig 9.12)
- The multi-year real-wage curves (Fig 9.19) for 1947, 1958, 1963, 1967, 1972, 1998

## 2. Why it matters

Shaikh's central Sraffian empirical result: the actual w-r curves are near-linear (slightly convex) — meaning the standard Sraffian "wage frontier" geometry survives at real capital intensities, with the divergence from a straight line bounded by ≤(r/R)² · (sub-dominant eigenvalues). Combined with productivity scaling, the curves intersect rather than nest, capturing the technical-change shift.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S903-WRCURVE-{YEAR}** for YEAR ∈ {47, 58, 63, 67, 72, 98fix, 98circ} | 100+ (r, w(r)) points per year | Pre-computed by Shaikh in `Appendix9_PennWorldTables2.xlsx`, columns `r{YR}`, `wr{YR}` | dimensionless (r in decimal, wr in productivity-index ratio) | XLSX columns |
| **S903-WSHARE-{YEAR}** for same YEAR | 100+ (r, wshare(r)) points | same workbook, column `wshr{YR}` | wage share (dimensionless) | same |
| **S903-PWT** | 6 (year, RGDPperworkerindex) anchor values | PWT 7.1 archived | dimensionless productivity index | same workbook, column `RealGDPperworkerindex` |
| **S903-R** | 7 (year, R_t) pairs | Table 9.18 | decimal max profit rate | same workbook, columns `R_fixed`, `R_circ` |

Note on PWT variable: the workbook column `rgdpwok` in `Appendix9_PennWorldTables.xlsx` is the PWT 7.1 standard "Real GDP per worker, chain-weighted" — disambiguating the truncated "Real" reference in the book (Appendix 9.2 p. 869).

## 4. Construction

**Formula** series, but the pre-computed `wr{YR}` columns in PennWorldTables2.xlsx already encode:
```
wr(r)_t = wshr(r)_t · (yr_t / yr_0)
       = (1 - r/R_t) · (PWT_RGDPperworker(t) / PWT_RGDPperworker(base))
```
where base = 1947 (with R_47 = 1.088 from KT eigensystem solve), and the wage share at r is the Sraffa-standard linear `1 - r/R_t`. We read the pre-computed columns directly.

## 5. Year coverage

- 6+1 benchmark years × ~100 r-points each = ~700 wage-profit-curve rows; plus 6 anchor productivity-index rows; plus 7 R_t rows.

## 6. Units

`dimensionless` (wage share, productivity index, decimal r and R_t).

## 7. Caveats

1. **PWT 7.1 vs PWT 10.01.** The book uses PWT 7.1 (Heston/Summers/Aten 2012). PWT 10.01 (Feenstra/Inklaar/Timmer 2023) uses different base year (2017 vs 2005) and different PPP reference round. EPR §3 documents the growth-rate splice strategy for any future extension, with the No Lazy Splices rule applied so that the productivity multiplier is recomputed on the **freshly-derived** σW(r), never on a previously-derived wr(r).
2. **1947 R = 1.088 > 1.** Mathematically admissible: R is 1/λ_max of KT, and λ_max in 1947 (with the labor-intensive Ochoa SIC table) is below 1, yielding R above 100% profit rate. The x-axis range for Fig 9.19 extends to r = 1.134, matching Shaikh's plot.
3. **Pre-computed curves, not re-solved.** Same posture as S902 — the eigenvalue replication is documented as a downstream concern, not a v1 blocker. Reading `wr{YR}` from the workbook reproduces the book exactly.
4. **PWT 7.1 RGDPperworkerindex starts 1950.** The 1947 anchor used by Shaikh is constructed by extending PWT 7.1 1950 backward via BEA Long Term Economic Growth A163 (a footnote in the workbook header explicitly says "1947 value = 1950 index adjusted by NBER output/labor 1948/1950, Long Term Eco Growth A163, pp. 208-209"). We adopt the workbook's pre-computed `RealGDPperworkerindex[1947] = 0.322501` rather than re-deriving it.
5. **No proxies.**

## 8. Cross-references

- CD/CD2 legacy ID: `S049`.
- Book: Shaikh (2016) Ch9 pp.422-423; Appendix 9.1 + 9.2 pp.868-869.
- Figure list (Phase 4 trimmed): Fig 9.8, 9.12, 9.19. (Original CD2 catch-all of 11 figures pruned per Phase 4 ratification.)
- Sibling: S902 (R_t values shared; eigensystem common).

## 9. Validation expectation

- Tolerance: **±0.5%** per (year, r-point).
- Truth source: same `Appendix9_PennWorldTables2.xlsx` columns (`r{YR}`, `wshr{YR}`, `wr{YR}`).
- Expected MAE: 0% (read-the-truth-column pattern).
- Diagnostic: confirm `R_fixed` values match Table 9.18: [1.088, 0.9734, 0.8547, 0.7644, 0.7033, 0.7317] — confirmed at ingestion.
