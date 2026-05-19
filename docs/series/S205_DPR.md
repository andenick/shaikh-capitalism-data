# S205 -- Business Cycles, 1867-1902 (Ayres Index, Fig 2.4B)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S205
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S205_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S205_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S205`

---

## 1. Definition

Monthly Ayres cyclical-component index, 1867-1902 subperiod.

In Shaikh (2016) the series appears as **Figure 2.4B** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

Documents post-Civil-War / Gilded Age business cycle volatility; covers the Long Depression (1873-1879).

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S205-A** | 1867-1902 | Ayres (1939) Table 9, Appendix A, col. 1 | percent deviation from trend | salvaged chopped |

## 4. Construction

`direct` construction.

1. Same monthly Ayres source as S204, windowed to 1867-1902.

## 5. Year coverage

- **Book period**: 1867-1902
- **Extension period**: N/A

## 6. Units

Percent deviation from trend

## 7. Caveats

1. Discontinued; same notes as S204.
2. Includes Long Depression (1873-1879) and Panic of 1893 troughs.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.4B
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
