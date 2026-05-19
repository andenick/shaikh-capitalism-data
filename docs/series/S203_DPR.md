# S203 -- US Real GDP per Capita (MeasuringWorth), 1889-2025

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S203
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S203_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S203_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S203`

---

## 1. Definition

Real GDP per capita on MeasuringWorth's continuously-updated annual reconstruction (Officer & Williamson). Plotted 1889-2010 in the book.

In Shaikh (2016) the series appears as **Figure 2.3** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

Third leg of Shaikh's opening trio (industrial production, investment, GDP/cap); illustrates 150-year secular growth in per-capita real output.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S203-A** | 1889-2010 | MeasuringWorth Real GDP per Capita | real 2005 dollars | salvaged chopped |
| **S203-B** | 2011-2025 | FRED A939RX0Q048SBEA (Real GDP per Capita, chained 2017$) | chained 2017$ | FRED API |

## 4. Construction

`direct` construction.

1. Read MeasuringWorth Real GDP per Capita column from salvaged chopped table.
2. Extension: rescale FRED A939RX0Q048SBEA at 2010 overlap.

## 5. Year coverage

- **Book period**: 1889-2010
- **Extension period**: 2011-2025

## 6. Units

Real GDP per capita, constant 2005 dollars (per MeasuringWorth methodology)

## 7. Caveats

1. MeasuringWorth license is academic-use with attribution.
2. MeasuringWorth occasionally revises historical estimates; document access date.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.3
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
