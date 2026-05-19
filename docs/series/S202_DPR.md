# S202 -- US Real Investment Index, 1832-2025

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S202
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S202_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S202_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S202`

---

## 1. Definition

Index of US real nonresidential business investment in fixed capital (equipment + structures excluding housing). Spliced at 1901, rebased to 1958=100. Chapter 2's leading-edge illustration of the more turbulent investment path relative to output.

In Shaikh (2016) the series appears as **Figure 2.2** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

Investment is more volatile than output (book p. 56). The series demonstrates 'growth is always turbulent, and the path of investment is far more turbulent than that of output'.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S202-A** | 1832-1975 | BEA (1977) Table B4, Investment in Fixed Nonres Bus Capital | Index 1970=100 | salvaged chopped (RealInvest1) |
| **S202-B** | 1901-2010 | BEA Wealth Table 4.8 line 1 | constant dollars (2011 vintage) | salvaged chopped (RealInvest2) |
| **S202-C** | 2011-2025 | BEA NIPA T1.1.6 line 9 (Real Nonresidential Fixed Investment) | chained 2017$ | BEA iTable API |

## 4. Construction

`composite` construction.

1. Rebase BEA 1977 series to anchor at 1901 = 100.
2. Rebase BEA Wealth Table 4.8 series to anchor at 1901 = 100.
3. Splice at 1901: BEA 1977 for 1832-1900, BEA Wealth for 1901-2010.
4. Re-anchor the spliced series to 1958 = 100.
5. Extension: rescale BEA NIPA T1.1.6 line 9 (2011-2025) at 2010 overlap.

## 5. Year coverage

- **Book period**: 1832-2010
- **Extension period**: 2011-2025

## 6. Units

Index, 1958 = 100

## 7. Caveats

1. Phase 4 substitution avoided: FRED GPDIC1 includes residential investment (silent proxy). BEA NIPA T1.1.6 line 9 is the concept-correct extension.
2. BEA's 2011 access vintage of Wealth Table 4.8 may differ from current BEA data; we preserve Shaikh's pulled values from the salvaged chopped table.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.2
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
