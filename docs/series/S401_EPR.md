# S401 — Extension Provenance Record

**Series**: S401 — Average and Marginal Costs with Wage Paid per Worker (Fig 4.16)
**Record type**: Extension Provenance Record
**Construction classification**: `derived`
**Extension method**: **not_applicable_theoretical**
**Authored**: 2026-05-18
**Author**: RSCD data-construction pipeline

---

## 1. Why this series is NOT extendable

S401 is a closed-form numerical illustration computed by Shaikh from Appendix 4.2 eq. (4.2.1) (a stylized quadratic productivity-per-hour curve) plus stylized prices (`pMK=100, pa=10, wN=100, p=7`). The horizontal axis is **cumulative daily output XR**, not calendar time. There is no calendar-year series to extend; there is no real-world data counterpart.

Per the chapter playbook recipe for `derived`:
> "Derived (e.g., Ch4 cost curves, S401-S407) — chopped CSV may be entirely book-truth values (no extension possible). Tolerance 0.5%."

## 2. Construction classification

`derived` / `formula`. The Anu lazy-splice prohibition is vacuous here because there is no observed series on either side of the calendar boundary.

## 3. Method

Not applicable.

## 4. Component re-fetching

Not applicable.

## 5. Proxies

**None.** No substitution required because no extension is attempted.

## 6. Synthetic data

**None.** The book values are themselves the only "data" in question; we ingest them verbatim from the reconstructed CSV. We do not back-solve eq. (4.2.1) at runtime — the CSV is the canonical source.

## 7. Failure modes & graceful degradation

| Failure | Detection | Action |
|---|---|---|
| Reconstructed CSV missing | The data-loading step checks that `Appendix_4_2_Table4.csv` exists | The data-loading step returns FAIL with the explicit path |
| CSV schema drift (column rename) | The data-loading step's explicit column list | The data-loading step returns FAIL with a missing-column report |
| Empty XR=0 row mis-parsed | The data-loading step preserves nulls in non-`afc` columns | The processing step passes through; the validation step treats nulls as not-compared |

## 8. Predecessor divergence

**Not applicable** — no earlier reconstruction of this project (internally called CD/CD2) contained any Chapter 4 series.

## 9. Forward roadmap

A possible later chapter-level visualization would re-derive the cost curves on a finer XR grid by re-implementing eq. (4.2.1) directly (with the back-solved `a1=2.40`); that re-derivation would be a visualization convenience, **not** an extension of S401, and is out of scope for the present data-construction work.
