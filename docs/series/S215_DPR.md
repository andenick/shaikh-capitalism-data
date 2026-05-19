# S215 -- Incremental Rates of Profit in US Manufacturing, 1960-1989

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S215
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S215_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S215_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S215`

---

## 1. Definition

Incremental profit rate r* = PG / IG(-1), where PG = gross profits and IG = gross investment lagged one year (footnote 6, p. 67).

In Shaikh (2016) the series appears as **Figure 2.15** in Chapter 2 ("The Wealth of Nations: A Long View").

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

- Book reference: Shaikh (2016), Ch. 2, Figure 2.15
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
