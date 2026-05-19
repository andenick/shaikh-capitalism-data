# S711 — Figure 7.21 — OECD Industry IROP Deviations, 1988–2003 (PPP-adjusted; OECD STAN 2003 + PWT 6.2)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S711
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch7-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S711_research.json`
- Adequacy: `Technical/docs/chapters/CH7_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S711_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S711`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `SHAIKH_2008_APPENDIX_7_2_OECD_IROP`

---

## 1. Definition

**S711** is the **PPP-adjusted OECD industry IROP deviation panel** for 1988–2005 (book figure plots 1988–2003 only). Each value is `IROP_i,t − IROP_avg,t` where IROP is computed after cross-country PPP aggregation. Appears as Fig7.21 in Shaikh (2016).

## 2. Why it matters in Chapter 7

S711 is the **third tier** of Shaikh's empirical case for turbulent equalization (after the US BEA panel S705-S710 and the Greek panel S707-S708). It uses a different geography (OECD-wide), a different vintage (STAN 2003), a different deflation method (PPP-adjusted International Dollars per PWT 6.2), and a methodologically asymmetric construction (no WEQ; STAN provides no capital stock so only IROP, not ROP, is computable). The convergence of all three tiers on the same qualitative pattern (IROPs cross repeatedly) is the chapter's strongest empirical case.

S711 also **resolves a long-standing alias collision**: CD2's `S038` was labelled "OECD IROP" but mislabelled as Greek in the stub set. Decision 0004 separated the OECD content into S711 and reassigned the Greek content to S707/S708.

## 3. Sources

| Subseries | Coverage | Source | Units |
|---|---|---|---|
| **S711-A** | 1988–2005 | Appendix 7.2 iropOECDPPP — 27 OECD industries (ISIC Rev 3) byte-exact | rate deviation (decimal; industry IROP minus All-Industries average IROP, PPP-adjusted International Dollars) |

The Phase 4 adequacy review verified the salvaged xlsx is present and that OECD STAN 2025 + PWT 10.01 endpoints return HTTP 200. Direct OECD STAN 2003 vintage is no longer hosted; Shaikh's pre-computed Appendix 7.2 sheet is the only byte-exact path.

## 4. Construction

`composite`. Per Appendix 7.1 V:
1. Country-industry GFCF and GOPS from OECD STAN 2003 vintage (currently irrecoverable; Shaikh's pre-computed sheet stands as byte-exact record).
2. PPP-convert to International Dollars via PWT 6.2.
3. Aggregate-before-ratio per industry: `GFCF_i,t = Σ_c GFCF_{c,i,t}`; same for GOPS.
4. Restrict to industries with 3+ countries reporting both variables.
5. `IROP_i,t = (GOPS_i,t − GOPS_i,t-1) / GFCF_i,t-1`.
6. `IROP_avg,t` = aggregate-before-ratio across retained industries.
7. `dev_i,t = IROP_i,t − IROP_avg,t`.
8. **No WEQ adjustment** (book p. 859 V.2: international data did not allow removal of self-employed income).

For Phase 5 we read the pre-computed deviation columns directly from Shaikh's `iropOECDPPP` sheet.

## 5. Year coverage

- **Book period plotted**: 1988–2003
- **Salvaged xlsx**: 1988–2005 (Shaikh's spreadsheet extends 2 years past the figure)
- **Extension period** (deferred): 2004–2023 via OECD STAN 2025 + PWT 10.01 with explicit ISIC Rev3→Rev4 crosswalk and country-coverage discontinuity (30 → 18 countries, excluding Canada and UK per book p. 859 V.3 verbatim). Concept Match Justification required.

## 6. Units

rate deviation (decimal; industry IROP minus All-Industries average IROP, PPP-adjusted International Dollars).

## 7. Caveats

1. **Discontinued primary source.** OECD STAN 2003 vintage is no longer hosted. The salvaged xlsx is the only byte-exact path.
2. **Country-coverage discontinuity** (30 → 18) is non-trivial; book p. 859 V.3 says this verbatim. Extension to current vintage requires explicit Concept Match Justification.
3. **No WEQ adjustment.** OECD IROP includes some self-employed income in GOPS that S705/S706/S709/S710 strip via WEQ; this is a known cross-country comparability gap.
4. **ISIC Rev 3 → Rev 4 crosswalk.** Shaikh's idiosyncratic industry labels ('Wood&publishing', 'sale.motor', etc.) need explicit mapping for any STAN 2025 extension.
5. **PWT 6.2 → 10.01 methodology drift.** CD2 reports MAE = 0.04 on the overlap window, suggesting cross-country aggregate effects largely wash out, but document.

## 8. Cross-references

- **CD2 legacy ID**: `S038`
- **Book reference**: Shaikh (2016), Ch. 7, p. 305, Appendix 7.1 V (pp. 858–859), Fig7.21.

## 9. Validation expectation

- **Tolerance**: ±1.0% per cell (time_series default).
- **Expected MAE** against `iropOECDPPP` columns: 0.0 (verbatim).
