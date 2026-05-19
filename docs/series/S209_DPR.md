# S209 -- US Unemployment Rate, 1890-2025

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S209
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S209_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S209_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S209`

---

## 1. Definition

Civilian unemployment rate, spliced from BEA LTEG (1890-1947) + ERP Table B-40 (1948-2010), extended via FRED UNRATE.

In Shaikh (2016) the series appears as **Figure 2.9** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

Standard cyclical indicator; complements the Ayres business-cycle subperiods with a continuous post-1890 record.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S209-A** | 1890-1947 | BEA LTEG B1-B2 | percent | salvaged chopped |
| **S209-B** | 1948-2010 | Economic Report of the President Table B-40 | percent | salvaged chopped |
| **S209-C** | 2011-2025 | FRED UNRATE | percent | FRED API |

## 4. Construction

`composite` construction.

1. BEA LTEG for 1890-1947 (before ERP starts).
2. ERP T B-40 for 1948-2010.
3. FRED UNRATE for 2011+ (no rescale; ERP and UNRATE are level-equivalent BLS CPS series).

## 5. Year coverage

- **Book period**: 1890-2010
- **Extension period**: 2011-2025

## 6. Units

Percent of civilian labor force

## 7. Caveats

1. Tolerance set at 0.15pp absolute (not relative) because unemployment rates near 1-2% would otherwise trigger false divergences.
2. Pre-1948 BEA LTEG and post-1948 BLS CPS use slightly different definitions of 'unemployed'; the splice is documented in BEA's own historical reconciliation.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.9
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
