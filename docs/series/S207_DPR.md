# S207 -- US Manufacturing Productivity and Production Worker Real Compensation, 1889-2025

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S207
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S207_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S207_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S207`

---

## 1. Definition

Two co-plotted index series (both Index 1889 = 100): (a) manufacturing labor productivity, (b) production-worker real compensation per hour. Used by Shaikh to demonstrate divergence between productivity growth and worker wages.

In Shaikh (2016) the series appears as **Figure 2.7** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

Central to the labor-share-and-productivity-divergence argument that runs through Chapters 2, 6, 14, 15.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S207-A** | 1889-2010 | BEA LTEG A173 (1860-1970) + BLS FLS Table 1 (1950-2009) | Index 1889=100 | salvaged chopped |
| **S207-B** | 1889-2010 | MeasuringWorth uswage + CPI | Index 1889=100 | salvaged chopped |
| **S207-C** | 2010-2025 | FRED OPHMFG (US-only Mfg Real Output Per Hour) | Index 2017=100 | FRED API |
| **S207-D** | 2010-2025 | FRED COMPRMS (Mfg Real Compensation per Hour) | Index 2017=100 | FRED API |

## 4. Construction

`composite` construction.

1. Productivity (S207-A): spliced from BEA LTEG A173 (1889-1949) + BLS FLS Table 1 (1950-2009), rebased to 1889=100 in the chopped table.
2. Real compensation (S207-B): nominal MW compensation / CPI, rebased to 1889=100.
3. Extension: FRED OPHMFG and FRED COMPRMS each anchored at 2009 (BLS FLS last observation) and rescaled.

## 5. Year coverage

- **Book period**: 1889-2010
- **Extension period**: 2011-2025

## 6. Units

Two units co-plotted: Index 1889=100 (productivity); Index 1889=100 (real compensation index).

## 7. Caveats

1. Phase 4 substitutions: MeasuringWorth /datasets/uscompensation/ -> /datasets/uswage/ (URL rename only, values unchanged).
2. BLS FLS International Comparisons program sunset 2013; FRED OPHMFG continues the BLS Productivity & Costs concept but in US-only form (narrower than the 19-country book series). Proxy flag set on S207-C.
3. Units field splits into productivity (Index 1889=100) and compensation (Index 1889=100) for the loader contract.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.7
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
