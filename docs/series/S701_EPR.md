# S701 — Extension Provenance Record

**Series**: S701 — Figure 7.11 — US Selling Price vs Unit Labor Cost (cross-section), 1923–1950

**Construction classification**: `direct` (cross_sectional)
**Extension method**: not applicable — see §1
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related**: `S701_DPR.md`

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

CD2 (the predecessor build) had no per-series CSV for legacy ID S030; no CD2 comparison is meaningful.

## Notation (plain-language key)

- **Cross-sectional** — a point-in-time comparison across industries, with no annual time axis; hence no time-extension applies.
- **Unit labour cost** — labour cost per unit of output.
- **BLS / PRS / ONS / PPI** — US Bureau of Labor Statistics / its labour-productivity (Productivity and Costs) program / UK Office for National Statistics / producer price index.
- **SIC1958 → SIC2007** — successive UK Standard Industrial Classification schemes; the reclassification breaks any clean mapping back to Salter's categories.
- **L01** — the load script.
- **CD2** — the predecessor build of this dataset (legacy ID S030).
- **Phase 6** — the Anu extension pipeline stage.
