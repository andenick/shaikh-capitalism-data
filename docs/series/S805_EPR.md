# S805 — Extension Provenance Record

**Series**: S805 — Rates of Return and Concentration (CR4), 1963 and 1969 (Demsetz Fig 8.6)
**Phase**: 6 (Extension)
**Construction classification**: `direct` (cross_sectional)
**Extension method**: not applicable — see §1
**Authored**: 2026-05-18
**Author**: opus-subagent-ch8-fanout
**Related**: `S805_DPR.md`

---

## 1. Classification

`content_type = cross_sectional`. Two non-adjacent year-snapshots (1963 and 1969), each an industry cross-section binned by CR4. The two years are not a continuous time index; they are used by Shaikh specifically to demonstrate the *sign reversal* of the concentration-profit relation between two adjacent years.

Per the playbook recipe (cross_sectional):

> "Extension: explicitly `not_applicable_cross_sectional` in EPR; extension_candidates empty in dossier (already true after Phase 4)."

## 2. Why no extension is attempted

- The Anu rule against extending non-time-series applies.
- The book uses the two cross-sections specifically to demonstrate temporal instability of the concentration-profit relation; appending a third year (e.g., 1992 or 2017) is a new analytic exercise, not an extension.
- Per Phase 4 Adequacy Report: "If a modern (e.g., 1992 / 2002 / 2017) re-snapshot is later commissioned, treat as a NEW cross-sectional series (S805b) not as an extension."

## 3. Method

N/A.

## 4. No-Proxy disclosure

**None.** The Demsetz 1973b Table 4 values are loaded directly from the chopped xlsx.

## 5. No-Synthetic disclosure

**None.** No interpolation, no extrapolation. Cells are loaded as published.

## 6. Failure-mode table

| Failure | Action |
|---|---|
| xlsx missing | Loader returns `{"status": "FAIL", ...}` |
| CR4 bin labels parse anomalously | Loader fails fast — do not coerce |
| Validator finds divergence > 0.5% | FAIL — investigate xlsx vs. Demsetz 1973b Table 4 |

## 7. CD2 divergence pre-disclosure

No CD2 per-series CSV matches S805 content. The CD2-vs-RSCD comparison is not meaningful.

## 8. Recovery / future-work

A modern (1992 / 2002 / 2017) re-snapshot would require:
1. IRS SOI Corporation Complete Report (https://www.irs.gov/statistics/soi-tax-stats-corporation-complete-report — HTTP 200, substitute for deprecated Source Book slug).
2. U.S. Census Concentration Ratios in Manufacturing (CR4) for the matching Economic Census year.
3. NAICS-level industry partitioning into CR4 bins and re-aggregation.

This would be a NEW cross-sectional series (proposed: S805b), not an extension of S805.

## 9. Cross-reference

S803 also consumes Demsetz 1973b (a different table, p. 12 corrections to Bain). S805 and S803 share the source publication but not the source table.
