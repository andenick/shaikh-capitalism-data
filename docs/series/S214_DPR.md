# S214 -- Average Rates of Profit in US Manufacturing, 1960-1989

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S214
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S214_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S214_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S214`

---

## 1. Definition

Sector-by-sector profit rates for 15 US manufacturing aggregates, 1960-1989. Source: Shaikh Appendix 7.2 hosted on anwarshaikhecon.org.

In Shaikh (2016) the series appears as **Figure 2.14** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

Empirical foundation for the cross-sector profit-rate distribution analysis in Ch 7 (real competition).

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S214-EXT** | 1987-2005 | Shaikh Appendix7_ropdataUSind (post-book industry data) | rate (decimal) | salvaged chopped |

## 4. Construction

`formula` construction.

**Formula**: `r_sector[t] = profit[t] / capital_stock[t]`


1. **BOOK PERIOD (1960-1989) DATA NOT IN SALVAGEDINPUTS.** Per anu-framework no-fabrication rule, we do not synthesize the missing 1960-1989 series.
2. We emit the post-book Appendix7 industry-level data (1987-2005) labeled S214-EXT (not S214-A), explicitly marked as post-book period only.
3. Remediation: when anwarshaikhecon.org Appendix 7.2 replica is added to SalvagedInputs, re-run L01 to populate 1960-1989.

## 5. Year coverage

- **Book period**: 1960-1989
- **Extension period**: N/A

## 6. Units

Rate (decimal)

## 7. Caveats

1. Book period 1960-1989 is data_unavailable; documented in V03 with status PASS_DATA_UNAVAILABLE.
2. OECD ISDB (1994 vintage referenced by CD2/Christodoulopoulos 1995) discontinued; STAN extension requires ISIC Rev3 -> Rev4 + NAICS crosswalk.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.14
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
