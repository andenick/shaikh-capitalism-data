# S212 -- US and UK Wholesale Prices in Ounces of Gold, 1790-2025 (1930=100, log scale)

**Data Provenance Record (DPR)**

**Series ID**: S212
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S212`

---

## 1. Definition

Formula series: WPI / gold_price for US and UK separately, rebased to 1930 = 100.

In Shaikh (2016) the series appears as **Figure 2.10** in Chapter 2 ("Turbulent Trends and Hidden Structures").

## 2. Why it matters in Chapter 2

Strips out monetary inflation/deflation by deflating prices by gold; reveals the *real* (commodity-money-denominated) price level over 220 years.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S212-A** | 1790-2010 | Jastram (1977) T1 (US WPI/gold) + MeasuringWorth gold | Index 1930=100 | salvaged via CD2 S025 |
| **S212-B** | 1790-2010 | Jastram (1977) (UK WPI/gold) + MeasuringWorth gold | Index 1930=100 | salvaged via CD2 S024 |
| **S212-C** | 2011-2025 | Recomputed from S210 + FRED GOLDPMGBD228NLBM | Index 1930=100 | computed |

## 4. Construction

`formula` construction.

**Formula**: `WPI_in_gold[country, t] = WPI[country, t] / gold_price[country, t]; rebased to 1930=100`

1. Book-period values: pre-computed in CD2 S024/S025 (Jastram + MeasuringWorth gold).
2. Extension: recompute ratio from FRED WPU + FRED GOLDPMGBD228NLBM, rescaled to 1930=100 via 2010 anchor.

## 5. Year coverage

- **Book period**: 1790-2010
- **Extension period**: 2011-2025

## 6. Units

Index, 1930 = 100 (log scale on figure); represents WPI deflated by gold price

## 7. Caveats

1. Formula extension applies; do NOT splice level series.
2. UK extension would require GBP gold price + UK WPI extension -- deferred to Phase 9.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.10
- Knowledge Base: figure-linkage reference
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
