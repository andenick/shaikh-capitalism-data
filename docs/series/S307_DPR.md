# S307 -- Empirical Engel Curve for Food (Working Class Budgets, United Kingdom, 1904)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S307
**Status**: ingested
**Content type**: `cross_sectional`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave-a-ch3 (Phase 5-8 fanout)
**Related artifacts**:
- Research dossier: `Technical/research/S307_research.json`
- Adequacy: `Technical/docs/chapters/CH3_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S307_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S307`

---

## 1. Definition

**S307** is the absolute weekly expenditure on food (shillings/week) in UK working-class households in 1904, plotted against average weekly income. Same Board of Trade 1904 enquiry as S306; different y-axis (absolute spend rather than share). In Shaikh (2016) the series appears as **Fig3.9** on p. 95.

## 2. Why it matters in Chapter 3

Figure 3.9 is the absolute-expenditure Engel curve. Together with S306 (the share form) it is the empirical anchor of Ch 3. The shape — rising but flattening as income rises — is the real-world Engel saturation that Shaikh's analytic apparatus (S303/S305) is designed to derive.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S307-A** | 1904 (single cross-section) | Allen & Bowley (1935) Table 1; UK Board of Trade 1904 enquiry (Cd. 3864, 1908) | shillings per week (food expenditure) | library scan required (not in SalvagedInputs/) |

## 4. Construction

1. Loader checks for the same `Allen & Bowley Table 1` source file as S306.
2. If absent, emits metadata-only parquet with status `data_unavailable_pending_digitization`.
3. No interpolation; chopped CSV preserves the printed axis bounds [0, 35] shillings vs [0, 60] shillings income.

**No formula** — direct cross-sectional observation.

## 5. Year coverage

- **Single cross-section: 1904**.

## 6. Units

- **Output**: shillings per week (food expenditure).
- **x-axis**: shillings per week (income).

## 7. Caveats

1. Same data-availability constraint as S306.
2. The absolute-expenditure form is more sensitive to currency comparison than the share form. Any modern comparator (UK ONS LCF) requires a shillings -> GBP conversion AND careful concept-match for what is in 'food' (eating out, alcohol, etc.).
3. No proxy; no synthetic fill.

## 8. Cross-references

- **CD legacy ID**: none
- **Book reference**: Shaikh (2016), Ch. 3, Fig3.9 on p. 95
- **Knowledge Base**: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json` -> Fig3.9

## 9. Validation expectation

- **Tolerance**: PASS_CROSS_SECTIONAL_UNAVAILABLE pending digitisation. Verifies the year stamp is 1904 and that no synthetic values are present (value is NaN or within the axis bound [0, 35]).
