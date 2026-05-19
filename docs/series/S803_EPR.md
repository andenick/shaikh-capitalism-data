# S803 — Extension Provenance Record

**Series**: S803 — Rate of Profit on Equity vs. CR8, Bain 42-Industry Sample, 1936-1940 (Figs 8.3 and 8.4)
**Phase**: 6 (Extension)
**Construction classification**: `composite` (cross_sectional)
**Extension method**: not applicable — see §1
**Authored**: 2026-05-18
**Author**: opus-subagent-ch8-fanout
**Related**: `S803_DPR.md`

---

## 1. Classification

`content_type = cross_sectional`. The 42 industry observations are a single 1936-1940 cross-section; Fig 8.4 is the same cross-section re-binned with Demsetz's corrections, not a second time point.

Per the playbook recipe (cross_sectional):

> "Extension: explicitly `not_applicable_cross_sectional` in EPR; extension_candidates empty in dossier (already true after Phase 4)."

## 2. Why no extension is attempted

- The Anu rule against extending non-time-series applies.
- The Bain 1951 sample is a specific 42-industry list constructed for the 1935 Census CR8 / 1936-40 ROE pairing. The industry list itself is partially defined by Bain's exclusion criteria (industries with <3 firms or limited data); reconstructing the same cross-section for a modern year would require matching exclusion rules and is methodologically separate, not an extension.
- Per Phase 4 Adequacy Report: a "circa-2017" replication would be a NEW cross-sectional series, not an extension of S803.

## 3. Method

N/A.

## 4. No-Proxy disclosure

**None.** The Bain 1951 and Demsetz 1973b published values are loaded directly from the chopped xlsx.

## 5. No-Synthetic disclosure

**None.** No interpolation, no extrapolation. Cells are loaded as published.

## 6. Failure-mode table

| Failure | Action |
|---|---|
| Any of three xlsx files missing | Loader returns `{"status": "FAIL", ...}` |
| Industry name / Census number row mismatch | Loader fails fast |
| Validator finds divergence > 0.5% | FAIL — investigate xlsx vs. Bain 1951 / Demsetz 1973b |

## 7. CD2 divergence pre-disclosure

No CD2 per-series CSV matches S803 content. The stub's `cd_id = S041` was a stale carryover from a Ch10 interest-rate series and `cd2_id` was nulled.

## 8. Recovery / future-work

A modern (e.g., 2017 Economic Census) replication would require:
1. IRS SOI Corporation Source Book industry profit rates (NAICS).
2. U.S. Census Concentration Ratios in Manufacturing (CR8) for the matching Economic Census year.
3. NAICS-level industry partitioning and matching Bain's exclusion rules.

This would be a NEW cross-sectional series (proposed: S803b), not an extension of S803.
