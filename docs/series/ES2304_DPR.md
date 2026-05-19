# ES2304 — RMB Misalignment Estimates, Extended PPP Approach (Literature Compilation)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: ES2304
**Content type**: `derived` (literature compilation scatter)
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-fanout-ES

## 1. Definition

ES2304 is the scatter compilation of RMB misalignment estimates that
appear in Weber & Shaikh (2020) Appendix Figure 4 (p. 454), filtered
to estimates that used an **extended PPP approach** (BEER-style
reduced-form equilibrium real exchange rate regressions).

Per paper note 17 (verbatim, p. 448), Figs 4 and 5 are compiled from
the same four literature reviews:

- Cline & Williamson (2007) PIIE
- Dunaway & Li (2005) IMF WP/05/202
- Cheung, Chinn & Fujii (2010a) La Follette WP
- Cheung (2012) CESifo WP 3797

Each estimate is one scatter point; ranges become two endpoint points.

## 2. Why it matters

Weber & Shaikh use the extreme spread of these estimates (-36% to +50%)
as evidence against the currency-manipulation hypothesis: economists
using extended-PPP methods cannot agree on the *sign* of RMB
misalignment, let alone the magnitude.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| ES2304-A | 1999–2010 | Literature compilation per paper note 17 | percent | `SalvagedInputs/book_data/Reconstructed/ES2304_literature_compilation.csv` |

The four cited literature reviews are publicly downloadable (URLs
verified HEAD 200/202 OK 2026-05-18; see
`Technical/Build/_ches_url_check_results.json`).

## 4. Construction

`composite` literature compilation. The chopped CSV is the canonical
data structure: each row is `(study, study_year, estimate_year,
misalignment_pct, methodology, source_paper, paper_text_anchor)`.
Subseries `ES2304-A` aggregates all extended-PPP estimates.

## 5. Year coverage

Paper window: 1999-2010 (the published scatter spans these years).
**Extension status**: `not_applicable_literature_compilation` —
intrinsically non-extensible by paper construction (the 4 cited
reviews are 2005-2012 snapshots; post-2014 RMB-misalignment debate
moved to IMF EBA model, methodologically distinct).

## 6. Units

`percent` (RMB misalignment; positive = undervalued vs equilibrium).

## 7. Caveats

1. **v1.0 scope is limited to named endpoint estimates** — only the
   high (+50% Coudert-Couharde 2007) and low (-36% Cheung 2012)
   estimates that Weber & Shaikh explicitly quote in body text are
   transcribed verbatim. The remaining ~30-35 scatter points are not
   tabulated in the paper; full reconstruction requires a literature
   extraction subagent (v1.1).
2. Per Anu Framework no-fabrication rule (and the playbook
   anti-pattern list), we do not chart-digitize the unnamed scatter
   points. The chopped CSV row count is therefore 2 (not ~35).
3. License: each individual estimate is published in its own
   peer-reviewed paper/working paper; we redistribute only the two
   named endpoints which Weber & Shaikh themselves quoted. v1.1
   literature extraction will follow paper note 17 fair-use academic
   compilation norms.

## 8. Cross-references

- Dossier: `Technical/research/ES2304_research.json`
- Companion: `ES2305` (macro-balance approach, same 4 reviews)
- Reconstructed: `SalvagedInputs/book_data/Reconstructed/ES2304_literature_compilation.csv`

## 9. Validation expectation

- Tolerance: 0.5% (verbatim transcription of named endpoints).
- Compares processed parquet against the chopped CSV row-by-row.
