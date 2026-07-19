# S208 -- US Manufacturing Real Unit Production Labor Cost Index, 1889-2025

**Data Provenance Record (DPR)**

**Series ID**: S208
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S208`

---

## 1. Definition

RULC = real compensation per hour / productivity, rescaled to 1889 = 100. Equivalent to (S207-B / S207-A) * 100.

In Shaikh (2016) the series appears as **Figure 2.6** in Chapter 2 ("Turbulent Trends and Hidden Structures").

## 2. Why it matters in Chapter 2

Key Marxian indicator: real unit labor cost is the wage share when productivity and real wages are both real. Tracks the 'labor share' over 120 years.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S208-A** | 1889-2010 | Shaikh-derived RULC from S207 components | Index 1889=100 | salvaged chopped |
| **S208-B** | 2011-2025 | Recomputed from extended S207-A/S207-C (productivity) + S207-B/S207-D (real comp) | Index 1889=100 | formula recompute |

## 4. Construction

`formula` construction.

**Formula**: `RULC[t] = (real_compensation[t] / productivity[t]) * 100`

1. Read book-period RULC directly from chopped column 'Mfgrealunitlaborcost'.
2. Extension: recompute formula from S207-C / S207-D for each post-2010 year, rescaled so the 2010 extension value equals the 2010 book value.

## 5. Year coverage

- **Book period**: 1889-2010
- **Extension period**: 2011-2025

## 6. Units

Index, 1889 = 100

## 7. Caveats

1. Lazy-splice prohibition applies: extension MUST recompute the formula from S207 components, NOT splice FRED ULCMFG (which is nominal ULC -- silent proxy).
2. Extension depends on S207-C and S207-D being populated (FRED API success).

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.6
- Knowledge Base: figure-linkage reference
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
