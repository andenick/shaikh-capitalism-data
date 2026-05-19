# S802 — Extension Provenance Record

**Series**: S802 — Percentage of Prices Increases or No Decreases during Contractions, in Relation to Concentration (Fig 8.2)
**Phase**: 6 (Extension)
**Construction classification**: `direct` (cross_sectional)
**Extension method**: not applicable — see §1
**Authored**: 2026-05-18
**Author**: opus-subagent-ch8-fanout
**Related**: `S802_DPR.md`

---

## 1. Classification

`content_type = cross_sectional`. The series consists of three discrete cross-sections (one per NBER contraction) of firms binned by CR4 midpoint. The three contractions are not a continuous time index; they are independent snapshots used by Shaikh to demonstrate the *sign flip* of the concentration-rigidity relation across the three episodes.

Per the playbook:

> "Extension: explicitly `not_applicable_cross_sectional` in EPR; extension_candidates empty in dossier (already true after Phase 4)."

## 2. Why no extension is attempted

- The Anu rule against extending non-time-series applies. S802 is a `cross_sectional` series.
- The book uses the cross-sections specifically to demonstrate temporal instability of the concentration-rigidity sign across three discrete recessions; appending a fourth recession is a new analytic exercise, not an extension of S802.
- Per Phase 4 Adequacy Report: "If a modern-recession analog is later commissioned, treat as a NEW cross-sectional series (e.g., S802b for 2007-09 / 2020), not as an extension of S802."

## 3. Method

N/A.

## 4. No-Proxy disclosure

**None.** The published Weston et al. / Semmler values are loaded directly from the chopped xlsx.

## 5. No-Synthetic disclosure

**None.** No interpolation, no extrapolation. Cells are loaded as published.

## 6. Failure-mode table

| Failure | Action |
|---|---|
| Loader cannot find xlsx | Returns `{"status": "FAIL", "error": ...}` |
| Cells parse as non-numeric | Loader fails fast; do not coerce |
| Validator finds divergence > 0.5% | FAIL — investigate xlsx vs. published Semmler 1984 Table 3.3 |

## 7. CD2 divergence pre-disclosure

No CD2 per-series CSV matches S802 content. The CD2-vs-RSCD comparison is not meaningful.

## 8. Recovery / future-work

A modern-recession analog (2007-09, 2020) would require:
1. BLS PPI industry data at sufficient frequency to compute price-change shares within each industry.
2. Census Concentration Ratios (CR4) for the matching Economic Census year.
3. NAICS-level industry partitioning into CR4 bins.

This would be a NEW series (proposed: S802b), not an extension of S802.
