# S408 — Extension Provenance Record

**Series**: S408 — Cost Curves Chosen by 94% of Business People Surveyed (Fig 4.23)
**Phase**: 6 (Extension)
**Construction classification**: `cross_sectional`
**Extension method**: **not_applicable_cross_sectional**
**Authored**: 2026-05-18
**Author**: opus-subagent-ch4-fanout

---

## 1. Why this series is NOT extendable

S408 is a single 1952 survey snapshot. There is no time axis to extend forward; there is no recurring data series that re-asks the same question annually. The chapter playbook's `cross_sectional` recipe applies:

> "extension is explicitly `not_applicable_cross_sectional` in EPR; extension_candidates empty in dossier."

## 2. Construction classification

`cross_sectional` / `direct`. Lazy-splice prohibition vacuous.

## 3. Method

Not applicable.

## 4. Component re-fetching

Not applicable.

## 5. Proxies

**None.** A 2020s survey of similar shape (if one existed) would not be the same observation — it would be different respondents, different industries, a different decade. Per anti-proxy rules we do not invent a substitute.

## 6. Synthetic data

**None.**

## 7. Failure modes & graceful degradation

The processed parquet is computed from hardcoded book-quoted values (94.0 and 94.3 percent). There is no API to fail; the only failure mode is dossier/code drift (book quote vs. hardcoded constant). The V03 validator guards against this by comparing against the same constants.

## 8. CD2 divergence

Not applicable (no CD2 predecessor).

## 9. Forward roadmap — literature-review extension (deferred)

Book footnote 36 (p. 164) cites a literature lineage on cost-curve shape (Bain 1948, Johnston 1960, Walters 1963, Dean 1976, Mansfield 1988, Kahn 1989, Lavoie 1992). A Phase 9 enrichment task could collect summary findings from each into a corroborating-evidence block alongside S408. That would be a research deliverable, not a "data extension" — and is explicitly out of scope for the present Phase 5–8 fanout.
