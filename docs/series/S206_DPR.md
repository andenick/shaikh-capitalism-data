# S206 -- Business Cycles, 1903-1939 (Ayres Index, Fig 2.4C)

**Data Provenance Record (DPR)**

**Series ID**: S206
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S206`

---

## 1. Definition

Monthly Ayres cyclical-component index, 1903-1939 subperiod.

In Shaikh (2016) the series appears as **Figure 2.4C** in Chapter 2 ("Turbulent Trends and Hidden Structures").

## 2. Why it matters in Chapter 2

Documents 20th-century business cycle volatility through the Great Depression and the New Deal.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S206-A** | 1903-1939 | Ayres (1939) Table 9, Appendix A, col. 1 | percent deviation from trend | salvaged chopped |

## 4. Construction

`direct` construction.

1. Same monthly Ayres source as S204/S205, windowed to 1903-1939.

## 5. Year coverage

- **Book period**: 1903-1939
- **Extension period**: N/A

## 6. Units

Percent deviation from trend

## 7. Caveats

1. Discontinued; same notes as S204/S205.
2. Last subperiod of Ayres index; ends 1939 (book publication year).

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.4C
- Knowledge Base: figure-linkage reference
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
