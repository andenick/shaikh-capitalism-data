# S705 — Figure 7.15 — US Industry Average Rates of Profit, 1987–2005 (BEA/Shaikh 2008)

**Data Provenance Record (DPR)**

**Series ID**: S705
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry → `series.S705`
- Subsource registry: subsource registry → `SHAIKH_2008_APPENDIX_7_2_ROP`

---

## 1. Definition

**S705** is the **rate (decimal; ROP = (PG - DEP) / K(-1), aggregate-before-ratio across 30 retained industries)** for the period 1987–2005. It appears in Shaikh (2016) as Fig7.15. The series is a multi-industry panel published as part of Shaikh's Appendix 7.2 derived data (with underlying BEA (US Bureau of Economic Analysis) / OECD primary inputs).

## 2. Why it matters in Chapter 7

This series operationalizes Shaikh's distinction between **average profit rates** (which cluster but show persistent industry-level outliers) and **incremental profit rates** (which "cross over" frequently, consistent with turbulent equalization of regulating capital). Together with its companion series in this chapter (S705↔S709 for ROP/ROP-deviation, S706↔S710 for IROP/IROP-deviation, S711 for the OECD parallel), it forms the empirical anchor for Shaikh's regulating-capital framework.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S705-A** (subseries — one data line within S705) | 1987–2005 | Appendix 7.2 ropdataUSind, byte-exact transcription of Shaikh 2008 NAICS reconstruction | rate (decimal) | local salvaged xlsx + Wayback fallback (https://web.archive.org/web/2023/http://www.anwarshaikhecon.org/) |

The adequacy review confirmed: BEA + FRB Z.1 endpoints reachable (HTTP 200); Wayback fallback for `anwarshaikhecon.org` returns 200; salvaged xlsx present locally and verified by row-and-column inventory.

## 4. Construction

`composite` — see EPR §3 for the formula. For Phase 5 byte-exact replication, we **read Shaikh's Appendix 7.2 sheet directly** rather than rebuild from BEA primaries. The reasons:

1. The salvaged xlsx is the **byte-exact published series**; rebuilding from BEA would require re-applying WEQ (wage-equivalent) / OOH (owner-occupied-housing) / inventory / reserve adjustments at a specific 2008 NIPA (US National Income and Product Accounts) vintage, which is not recoverable from current BEA endpoints.
2. The adequacy step report explicitly endorses this path: "Ratify CD2's post-2005 S705/S706 extension series … as the Phase 5 starting point, subject to vintage re-fetch on a coherent current BEA NIPA vintage."
3. End-to-end BEA re-fetch is documented in EPR §3 as the **extension path**, deferred to a follow-up wave.

### 4.1 Industry sample and aggregate

Shaikh's published panel has 32 industry columns plus an "All Private" aggregate; the 30 *named* retained industries plus 2 sub-aggregates (e.g., Manufacturing, Real & Rental) appear in the 38-panel small-multiple plots. The 31 excluded NAICS industries are listed verbatim in reconstructed book source data (Phase 4 B4 resolution).

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

- **CD2 legacy ID** (identifier in CD2, the predecessor build of this dataset): `S034`
- **Book reference**: Shaikh (2016), Ch. 7, pp. 299–305 + Appendix 7.1 III (pp. 857–859).
- **Knowledge Base**: figure-linkage reference → `Fig7.15`.

## Notation (plain-language key)

Short forms used above, in plain language (this record is a downloadable external artifact):

- **S### / -A** — series identifiers in this project (e.g. S705); a trailing letter (e.g. S705-A) marks a *subseries* — one data line within that series.
- **DPR / EPR** — Data Provenance Record (this file) / Extension Provenance Record (its companion).
- **Phase N** — Anu Framework pipeline stages: Phase 4 = adequacy/readiness review, Phase 5 = ingestion, Phase 6 = extension, Phase 9 = visualization.
- **L01 / P02 / V03** — the per-series load / process / validate scripts.
- **CD2** — the predecessor build of this dataset.
- **ROP** — (average) rate of profit.
- **IROP** — incremental rate of profit: the return on newly added capital (the year-to-year change in profit divided by the new investment that produced it).
- **BEA** — US Bureau of Economic Analysis.
- **NIPA** — US National Income and Product Accounts (published by the BEA).
- **NAICS** — North American Industry Classification System.
- **WEQ** — wage equivalent: an imputed labour income for self-employed / proprietors, adjusted out of surplus.
- **OOH** — owner-occupied housing: an adjustment removing imputed housing income.
- **GOS** — Gross Operating Surplus.
- **FRB Z.1** — Federal Reserve Board Z.1 (Financial Accounts of the United States).
- **MAE** — mean absolute error.

## 9. Validation expectation

- **Tolerance**: ±1.0% per year (time_series; tightened to ~0.0% in practice because we read the xlsx byte-exact).
- **Expected MAE** against the salvaged xlsx column: ~0 (verbatim re-read).
