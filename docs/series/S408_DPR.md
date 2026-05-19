# S408 — Cost Curves Chosen by 94% of Business People Surveyed (Fig 4.23)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S408
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch4-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S408_research.json`
- Adequacy: `Technical/docs/chapters/CH4_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S408_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S408`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `EITEMAN_GUTHRIE_1952`

---

## 1. Definition

**S408** is Shaikh's Figure 4.23 (book p. 163) — a reproduction of two of the eight cost-curve schematics (charts 6 and 7) from Eiteman & Guthrie's 1952 survey of business people. The survey-distribution finding it records is that **94% of 1,082 product-responses chose steadily-declining cost curves** (charts 6 or 7) over the U-shaped curves of neoclassical textbooks. Including the two respondents who chose the flat curve (chart 8), **94.3%** of respondents contradicted the U-shaped postulate.

This is a `cross_sectional` series — a single 1952 snapshot, not a time series.

## 2. Why it matters in Chapter 4

S408 supplies the survey-evidence pillar of Shaikh's empirical case against neoclassical cost theory. Together with S401–S407 (theoretical and Inman-simulation evidence), it constitutes Chapter 4's three-part empirical attack:
- S401–S403: theoretical derivation of spiky multi-shift cost curves
- S404–S407: Monte-Carlo simulation of an actual automotive plant (Inman 1995)
- S408: survey of practicing business people on the shape of their firms' cost curves (Eiteman & Guthrie 1952)

All three contradict the smooth-U-shape assumption.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S408-A** | single 1952 survey | Eiteman, W. J., & Guthrie, G. E. (1952). "The Shape of the Average Cost Curve." *American Economic Review* 42(5), 832–838. Table 3. | percentage of respondents | Numerical values transcribed verbatim from the quoted text on book p. 163 (verbatim_check=true in dossier) |

The survey itself reported `n=1,082` product-responses with:
- Charts 1–2 (rising costs): negligible share
- Charts 3–5 (U-shaped): 5.7% (per Shaikh's text)
- Charts 6–7 (steadily declining to capacity): **94.0%** (the headline figure of Fig 4.23)
- Chart 8 (flat): 0.3% (≈ 2 respondents)
- Steadily-declining or flat (charts 6–8): **94.3%**

These percentages are the entire numerical content of S408. The two chart shapes themselves (charts 6 and 7) are conceptual schematics — qualitative, not quantitative — and are not part of the persisted data.

## 4. Construction

`cross_sectional` / `direct`. The loader writes a single-year (`year=1952`) parquet with two rows:

```
year  value   subseries_id   source_id              units
1952  94.0    S408-A         EITEMAN_GUTHRIE_1952   pct_respondents
1952  94.3    S408-A         EITEMAN_GUTHRIE_1952   pct_respondents
```

The first row is the headline "94% chose charts 6 or 7" finding (Fig 4.23 caption). The second row is the broader "94.3% chose charts 6, 7, or 8" finding from Shaikh's surrounding text.

## 5. Year coverage

- **Book period**: 1952 (single year — the survey was published in AER vol. 42, no. 5, 1952). `year_range_book = [1952, 1952]`.
- **Extension period**: none. `year_range_extension = [null, null]`.

## 6. Units

Percentage of survey respondents (`pct_respondents`). Strictly bounded [0, 100].

## 7. Caveats

1. **Survey, not data series.** A single 1952 cross-section. The chart shapes themselves are conceptual; the data persisted is just the survey-distribution percentage.
2. **JSTOR stable ID provisional.** JSTOR returned HTTP 403 for both HEAD and GET probes during Phase 4 reachability check (uniform anti-bot policy). The bibliographic citation is well-established in the cost-curve literature; the stable_id `1812527` remains provisional pending interactive browser confirmation.
3. **Survey limitations Shaikh discusses (p. 164).** Eiteman & Guthrie's eight chart options did NOT permit a multi-shift spiky response, which is why the chosen curves look like single-shift segments rather than the full multi-shift pattern of S401–S407. This is documented in the dossier methodology_notes but does not affect the recorded value.
4. **Literature lineage (book footnote 36, p. 164).** Shaikh cites Bain 1948, Johnston 1960, Walters 1963, Dean 1976, Mansfield 1988, Kahn 1989, Lavoie 1992 as corroborating evidence for the same finding. These are recorded as `extension_candidates: []` (correctly empty per cross_sectional rule) but tracked in the dossier open_questions as a possible Phase 6 literature-review extension.

## 8. Cross-references

- **CD legacy ID**: none
- **CD2 legacy ID**: none
- **Book reference**: Shaikh (2016), Ch. 4, p. 163 (Fig 4.23 + surrounding text); footnote 36 p. 164.

## 9. Validation expectation

- **Tolerance**: ±0.5% (chapter playbook standard for `cross_sectional`).
- **Expected MAE**: 0 — the values `94.0` and `94.3` are direct from the book text.
- The V03 validator compares the processed parquet against the hardcoded book-quoted percentages.
