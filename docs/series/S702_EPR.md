# S702 — Extension Provenance Record

**Series**: S702 — Figure 7.12 — UK Selling Price vs Unit Labor Cost (cross-section), 1954–1963 (Reddaway Addendum)
**Phase**: 6 (Extension)
**Construction classification**: `direct` (cross_sectional)
**Extension method**: not applicable — see §1
**Authored**: 2026-05-18
**Author**: opus-subagent-ch7-fanout
**Related**: `S702_DPR.md`

---

## 1. Classification

`content_type = cross_sectional`. The series is a two-period industry comparison drawn from Salter (1969); there is **no time-axis to extend**. Per the playbook recipe for `cross_sectional`:

> "Extension: explicitly `not_applicable_cross_sectional` in EPR; extension_candidates empty in dossier."

## 2. Method

N/A. Each industry's (Selling Price ratio, Unit Labour Cost ratio) is a single bivariate observation; the dossier publishes those observations directly from the salvaged xlsx.

## 3. Why a modern proxy is not used

Salter's 1920s/1950s/1960s industry schema cannot be one-to-one matched to modern BLS PRS or ONS Productivity series. The PPI/BLS coverage gaps pre-1947 (US) and the SIC1958→SIC2007 reclassification (UK) prevent any back-extension of Salter's panel. Substituting modern PPI/PRS would constitute a proxy that violates the Anu No-Proxy rule.

## 4. No-Proxy disclosure

**None.** No substitution attempted.

## 5. No-Synthetic disclosure

**None.** No interpolation or projection.

## 6. Failure-mode table

| Failure | Action |
|---|---|
| Salvaged xlsx missing | L01 returns FAIL (re-download from Wayback / Internet Archive Salter 1969 entry) |
| Salter's NaN cells | Preserved as NaN — no imputation |

## 7. CD2 divergence pre-disclosure

CD2 had no per-series CSV for S031; no CD2 comparison is meaningful.
