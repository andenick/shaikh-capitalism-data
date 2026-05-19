# S213 -- US Corporate Rate of Profit, 1947-2011

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S213
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S213_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S213_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S213`

---

## 1. Definition

Average rate of profit for the US corporate sector, r = NOS_corporate / K_net (constant dollars), per Shaikh Appendix 6.7 methodology.

In Shaikh (2016) the series appears as **Figure 2.13** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

The book's first long-run profit-rate series; setup for the central-tendency-vs-incremental analysis in Chs 6, 7.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S213-A** | 1947-2011 | Derived from BEA NIPA T1.14 + FA T4.1 | rate (decimal) | salvaged via CD2 S026 |

## 4. Construction

`formula` construction.

**Formula**: `r[t] = NOS_corporate[t] / K_net[t-1]`


1. Book values reproduced from CD2 S026 (which itself replicates the Shaikh Appendix 6.7 computation).
2. Extension: BEA T1.14/T4.1 API line-mapping under review (Phase 3 open question); marked as data_unavailable until Phase 9.

## 5. Year coverage

- **Book period**: 1947-2011
- **Extension period**: N/A

## 6. Units

Rate (decimal; e.g. 0.15 = 15%)

## 7. Caveats

1. Phase 3 open question: 'Corporate' here = NIPA T1.14 strictly per CD2 interpretation; outstanding ambiguity vs broader business sector documented in adequacy report.
2. BEA API extension deferred: NIPA T1.14 line numbers shifted across vintages; needs Phase 9 specialist work.
3. Tolerance 0.005 absolute (profit rates ~0.10-0.20; relative tolerance inappropriate near zero).

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.13
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
