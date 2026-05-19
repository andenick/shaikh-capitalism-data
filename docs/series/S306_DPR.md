# S306 -- Empirical Expenditure Share on Food (Working Class Budgets, United Kingdom, 1904)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S306
**Status**: ingested
**Content type**: `cross_sectional`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave-a-ch3 (Phase 5-8 fanout)
**Related artifacts**:
- Research dossier: `Technical/research/S306_research.json`
- Adequacy: `Technical/docs/chapters/CH3_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S306_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S306`

---

## 1. Definition

**S306** is the share of weekly household expenditure spent on food in UK working-class households in 1904, plotted against average weekly income (in shillings) by income band. The source is Allen & Bowley (1935), Table 1, derived from the UK Board of Trade 1904 Cost-of-Living Enquiry (Cd. 3864, 1908). In Shaikh (2016) the series appears as **Fig3.8** on p. 95.

## 2. Why it matters in Chapter 3

Figure 3.8 is one of the two genuinely empirical figures in Ch 3 (with S307/Fig 3.9). It anchors the chapter's theoretical apparatus to a real cross-section showing Engel's Law in action: the share of expenditure on food declines with income, from ~70 percent at the lowest income band to ~56 percent at the highest. The pattern matches the qualitative prediction of S301-S305.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S306-A** | 1904 (single cross-section) | Allen & Bowley (1935) Table 1; UK Board of Trade 1904 enquiry (Cd. 3864, 1908) | percent of weekly expenditure on food | library scan required (not in SalvagedInputs/) |

## 4. Construction

1. Loader checks for `SalvagedInputs/book_data/AllenBowley1935_Table1.csv` (or similar).
2. If absent (current state), loader writes an empty data parquet with one metadata row carrying year=1904, x_value=NaN, value=NaN, marked status='data_unavailable_pending_digitization'.
3. Per the anu-framework rule: 'If data truly cannot be obtained, mark the series as "data_unavailable" with an empty CSV — do not fabricate values.'
4. The chopped CSV preserves only the axis-bound metadata (the printed figure's y-range 56-70 percent over x-range 0-60 shillings) for downstream visualisation overlays.

**No formula** — direct cross-sectional observation (when ingested).

## 5. Year coverage

- **Single cross-section: 1904** (per Allen & Bowley 1935, drawing on UK Board of Trade 1904 enquiry).

## 6. Units

- **Output**: percent of total weekly household expenditure on food.
- **x-axis**: average weekly income, shillings.

## 7. Caveats

1. **Data not yet ingested.** The Allen & Bowley (1935) Table 1 is NOT currently in `SalvagedInputs/book_data/`. Internet Archive URL returns 404 (Phase 4 adequacy check). Loader emits status='data_unavailable_pending_digitization'; processed parquet contains metadata rows only. Per the anu-framework: no synthetic interpolation of figure points.
2. **Future remediation**: library scan of Cd. 3864 (1908) preferred over Allen & Bowley monograph for copyright/provenance reasons (Cd. 3864 is Crown Copyright -> public domain; Allen monograph still under UK copyright until 2054).
3. **Concept-match note for any future modern comparator** (UK ONS LCF): not a splice; would be published as a separate cross-section with explicit Concept Match Justification per anu-framework.

## 8. Cross-references

- **CD legacy ID**: none
- **Book reference**: Shaikh (2016), Ch. 3, Fig3.8 on p. 95
- **Knowledge Base**: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json` -> Fig3.8

## 9. Validation expectation

- **Tolerance**: PASS_CROSS_SECTIONAL_UNAVAILABLE. The validator records that the underlying tabulation is not in SalvagedInputs and verifies that no synthetic values have been inserted (value column is empty or NaN; any non-NaN value lies within the printed axis range [56, 70]).
