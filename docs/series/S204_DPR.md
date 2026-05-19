# S204 -- Business Cycles, 1831-1866 (Ayres Index, Fig 2.4A)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S204
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S204_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S204_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S204`

---

## 1. Definition

Monthly cyclical-component index of US business activity, 1831-1866 subperiod. Compiled by Cleveland Trust Co.; pre-NBER composite indicator.

In Shaikh (2016) the series appears as **Figure 2.4A** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

Documents pre-Civil War business cycle volatility; first of three Ayres subperiods in Fig 2.4.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S204-A** | 1831-1866 | Ayres (1939) Table 9, Appendix A, col. 1 | percent deviation from trend | salvaged chopped |

## 4. Construction

`direct` construction.

1. Read Ayres (1939) monthly values from salvaged Appendix2_Ayres.xlsx; filter to 1831-1866.

## 5. Year coverage

- **Book period**: 1831-1866
- **Extension period**: N/A

## 6. Units

Percent deviation from trend

## 7. Caveats

1. Discontinued: no modern continuation. NBER macrohistory (m12003 etc.) is a related but not equivalent series; do NOT splice.
2. Pre-NBER composite indicator; Ayres reconstructed from 10 annual series interpolated to monthly.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.4A
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
