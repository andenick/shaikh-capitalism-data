# S211 -- US and UK Wholesale Price Indexes, 1780-1940 (1930=100, log scale)

**Data Provenance Record (DPR)**

**Series ID**: S211
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S211`

---

## 1. Definition

Windowed view of S210 truncated at 1940 by analytical design. Used by Shaikh to focus on the gold-standard era prior to Bretton Woods.

In Shaikh (2016) the series appears as **Figure 2.9** in Chapter 2 ("Turbulent Trends and Hidden Structures").

## 2. Why it matters in Chapter 2

Sets up the 'turbulent monetary regulation' argument by displaying the strikingly stationary character of WPIs under the gold standard.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S211-A** | 1780-1940 | Jastram (1977) T7 (US WPI) | Index 1930=100 | salvaged via CD2 S022 |
| **S211-B** | 1780-1940 | Jastram (1977) T2 (UK WPI) | Index 1930=100 | salvaged via CD2 S022 |

## 4. Construction

`composite` construction.

1. Same source as S210 with 1780-1940 window.

## 5. Year coverage

- **Book period**: 1780-1940
- **Extension period**: N/A

## 6. Units

Index, 1930 = 100 (log scale)

## 7. Caveats

1. Windowed view; no extension by design.
2. If multi-period analysis is desired, use S210 (which extends to 2010+).

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.9
- Knowledge Base: figure-linkage reference
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
