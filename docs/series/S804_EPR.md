# S804 — Extension Provenance Record

**Series**: S804 — Rate of Profit on Assets, Concentrated vs. Unconcentrated Industries, 1939-1957 (Stigler Fig 8.5)
**Phase**: 6 (Extension)
**Construction classification**: `direct` (time_series, discrete unequal bins)
**Extension method**: not attempted in Phase 5 — see §2
**Authored**: 2026-05-18
**Author**: opus-subagent-ch8-fanout
**Related**: `S804_DPR.md`

---

## 1. Classification

`content_type = time_series`. Six discrete multi-year bins from 1939 to 1957, with the two industry groups (concentrated, unconcentrated) treated as two subseries.

## 2. Why no extension is attempted in Phase 5

Per Phase 4 Adequacy Report recommendation (chapter_level_recommendations and per_series.S804 issues_outstanding):

> "Treat as historical illustration with optional modern parallel rather than continuous splice."

Reasons:

1. **SIC→NAICS classification break c. 1997.** Stigler's high-CR4 / low-CR4 partition was constructed in 1947-58 SIC categories; modern partitions in NAICS are not directly comparable.
2. **Changing CR definitions / Economic Census discontinuation.** The U.S. Census Concentration Ratios in Manufacturing series has gaps and methodology changes; post-2017 CR data has not yet been published for the 2022 Economic Census in CR-form (per Phase 4 url-check audit).
3. **Bin discontinuity.** Stigler's six 3-4 year bins cannot be naturally extended without re-aggregating modern annual IRS SOI data into matching windows — itself a modeling choice, not a passive splice.

Per the Anti-Degradation rule, any modern continuation would be methodologically separate, not a faithful extension. A NEW series (proposed: S804b) could be commissioned for a circa-2017 analytic note.

## 3. Method

N/A.

## 4. No-Proxy disclosure

**None.** The Stigler 1963 Table 17 values are loaded directly from the chopped xlsx.

## 5. No-Synthetic disclosure

**None.** No interpolation, no extrapolation. Cells are loaded as published.

## 6. Failure-mode table

| Failure | Action |
|---|---|
| xlsx missing | Loader returns `{"status": "FAIL", ...}` |
| Average row missing or shifted | Loader logs informational warning; sanity check skipped |
| Validator finds divergence > 1.0% | FAIL — investigate xlsx vs. Stigler 1963 Table 17 |
| Sanity check: computed means deviate from 7.067/6.892 by >1e-4 | Loader emits informational warning; not a hard fail |

## 7. CD2 divergence pre-disclosure

No CD2 per-series CSV matches S804 content (no genuine CD2 dossier for Ch8). The CD2-vs-RSCD comparison is not meaningful.

## 8. Recovery / future-work

Optional modern parallel (out of Phase 5 scope):
1. IRS SOI Corporation Complete Report (https://www.irs.gov/statistics/soi-tax-stats-corporation-complete-report — HTTP 200 confirmed; substitute for the deprecated Corporation Source Book slug, same as Ch6 AS009).
2. U.S. Census Economic Census Concentration Ratios via the active tables landing (https://www.census.gov/programs-surveys/economic-census/data/tables.html — HTTP 200 confirmed).
3. NAICS-level partition into high-CR4 / low-CR4 and re-aggregation of annual IRS profit rates into multi-year bins.

This would be a NEW series (proposed: S804b), not an extension of S804.
