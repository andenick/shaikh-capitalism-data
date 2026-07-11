# S215 -- Incremental Rates of Profit in US Manufacturing, 1960-1989

**Data Provenance Record (DPR)**

**Series ID**: S215
**Status**: extension_only_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S215`

---

## 1. Definition

Incremental profit rate r* = PG / IG(-1), where PG = gross profits and IG = gross investment lagged one year (footnote 6, p. 67).

In Shaikh (2016) the series appears as **Figure 2.13** in Chapter 2 ("Turbulent Trends and Hidden Structures").

## 2. Why it matters in Chapter 2

Companion to S214; introduces the *incremental* profit rate measure that becomes central to Chs 7, 14, 16.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S215-EXT** | 1988-2005 | Shaikh Appendix7_iropdataUSind (post-book IROP data) | rate (decimal) | salvaged chopped |

## 4. Construction

`formula` construction.

**Formula**: `r*[t] = PG[t] / IG[t-1]`

1. Same status as S214: book period 1960-1989 not in SalvagedInputs; post-book 1988-2005 IROP data emitted as S215-EXT.

## 5. Year coverage

- **Book period**: 1960-1989
- **Extension period**: N/A

## 6. Units

Rate (decimal)

## 7. Caveats

1. Book period data_unavailable; PASS_DATA_UNAVAILABLE in V03.
2. AMECO MEC uses gross output (not profits) in numerator -- do not splice without disclosure.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.13
- Knowledge Base: figure-linkage reference
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
