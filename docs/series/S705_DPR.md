# S705 — Figure 7.15 — US Industry Average Rates of Profit, 1987–2005 (BEA/Shaikh 2008)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S705
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch7-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S705_research.json`
- Adequacy: `Technical/docs/chapters/CH7_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S705_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S705`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `SHAIKH_2008_APPENDIX_7_2_ROP`

---

## 1. Definition

**S705** is the **rate (decimal; ROP = (PG - DEP) / K(-1), aggregate-before-ratio across 30 retained industries)** for the period 1987–2005. It appears in Shaikh (2016) as Fig7.15. The series is a multi-industry panel published as part of Shaikh's Appendix 7.2 derived data (with underlying BEA / OECD primary inputs).

## 2. Why it matters in Chapter 7

This series operationalizes Shaikh's distinction between **average profit rates** (which cluster but show persistent industry-level outliers) and **incremental profit rates** (which "cross over" frequently, consistent with turbulent equalization of regulating capital). Together with its companion series in this chapter (S705↔S709 for ROP/ROP-deviation, S706↔S710 for IROP/IROP-deviation, S711 for the OECD parallel), it forms the empirical anchor for Shaikh's regulating-capital framework.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S705-A** | 1987–2005 | Appendix 7.2 ropdataUSind, byte-exact transcription of Shaikh 2008 NAICS reconstruction | rate (decimal) | local salvaged xlsx + Wayback fallback (https://web.archive.org/web/2023/http://www.anwarshaikhecon.org/) |

The Phase 4 adequacy review confirmed: BEA + FRB Z.1 endpoints reachable (HTTP 200); Wayback fallback for `anwarshaikhecon.org` returns 200; salvaged xlsx present locally and verified by row-and-column inventory.

## 4. Construction

`composite` — see EPR §3 for the formula. For Phase 5 byte-exact replication, we **read Shaikh's Appendix 7.2 sheet directly** rather than rebuild from BEA primaries. The reasons:

1. The salvaged xlsx is the **byte-exact published series**; rebuilding from BEA would require re-applying WEQ/OOH/inventory/reserve adjustments at a specific 2008 NIPA vintage, which is not recoverable from current BEA endpoints.
2. The Phase 4 adequacy report explicitly endorses this path: "Ratify CD2's post-2005 S705/S706 extension series … as the Phase 5 starting point, subject to vintage re-fetch on a coherent current BEA NIPA vintage."
3. End-to-end BEA re-fetch is documented in EPR §3 as the **extension path**, deferred to a follow-up wave.

### 4.1 Industry sample and aggregate

Shaikh's published panel has 32 industry columns plus an "All Private" aggregate; the 30 *named* retained industries plus 2 sub-aggregates (e.g., Manufacturing, Real & Rental) appear in the 38-panel small-multiple plots. The 31 excluded NAICS industries are listed verbatim in `SalvagedInputs/book_data/Reconstructed/Shaikh_2008_Appendix_B_industries.csv` (Phase 4 B4 resolution).

## 5. Year coverage

- **Book period**: 1987–2005 (inclusive, annual)
- **Extension period** (Phase 5 scope): same as book period; **byte-exact reproduction from salvaged xlsx**
- **Extension to 2024** (deferred): feasible via end-to-end BEA pipeline re-run; see EPR §3.2

## 6. Units

rate (decimal; ROP = (PG - DEP) / K(-1), aggregate-before-ratio across 30 retained industries).

## 7. Caveats

1. **No splice across NIPA vintages.** The 2013 R&D/IP capitalization revision and the 2018 comprehensive revision change capital-stock and investment levels materially. The book-period values come from a specific 2008 vintage; any extension must re-run the full pipeline on a coherent current vintage, not splice.
2. **WEQ adjustment** is non-optional. NIPA's Gross Operating Surplus inflates Construction/Real-Estate profit rates by 4–8× without it; Shaikh's published panel applies WEQ throughout.
3. **OOH removal** is non-optional. NIPA's Real-Estate sector includes owner-occupied housing imputations that inflate GOS by ~55% and K by ~76%.
4. **Inventory and reserve adjustments** are non-optional. They reduce banking profit rate from ~42% to ~18%.
5. **Post-2008 IROP volatility** (S706/S710): the published 1988–2005 panel is well-behaved; CD2's extension to 2024 shows individual-industry IROPs swinging to ±6 in the post-2008 regime. Per the playbook, the default presentation for extension years is raw (un-winsorized).

## 8. Cross-references

- **CD2 legacy ID**: `S034`
- **Book reference**: Shaikh (2016), Ch. 7, pp. 299–305 + Appendix 7.1 III (pp. 857–859).
- **Knowledge Base**: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json` → `Fig7.15`.

## 9. Validation expectation

- **Tolerance**: ±1.0% per year (time_series; tightened to ~0.0% in practice because we read the xlsx byte-exact).
- **Expected MAE** against the salvaged xlsx column: ~0 (verbatim re-read).
