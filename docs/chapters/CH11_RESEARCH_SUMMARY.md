# Chapter 11 Research Summary — International Competition and the Theory of Exchange Rates

**Wave**: C
**Subagent**: opus-subagent-wave-c-ch11
**Date**: 2026-05-18
**Series count**: 4 (S1101–S1104)
**Book pages**: 523–534 (figures), 875–880 (Appendix 11.1)

## Chapter focus

Shaikh develops a classical theory of real exchange rates: REERs are not stationary (rejecting PPP) but gravitate around relative real unit labor costs (adjusted for nontradable/tradable composition). All four series in this chapter use the same underlying multi-country panel (Appendix 11.1) built from BLS International Comparisons, World Bank PPI, IMF IFS trade and exchange-rate data, with author-side weighting and rebasing.

## Series-level notes

### S1101 — Trade Balances in Major Countries (Fig 11.2)
Direct port of CD2 S060. Source confirmed as **IMF International Financial Statistics** (exports/imports in USD), with Belgium 1960–1992 backfilled from **AMECO**. Construction: per-country X/M ratios across 15 OECD countries. CD2 added China as a 5th US-comparator subseries (S060-E → S1101-E); this is NOT in Shaikh's original 15 and is flagged for Phase 4 review. Extension via IMF DOTS is straightforward.

### S1102 — Real Effective Exchange Rates (PPI), US and Japan (Fig 11.3)
Direct port of CD2 S061. Composite multilateral REER built from **BLS International Comparisons** Tables 9 (ULC) and 11 (exchange rates), **World Bank WDI** PPI, and **IMF IFS** trade weights per equation (11.16). Construction reclassified as `formula` (composite of 3 inputs). **Critical extension issue**: BLS International Labor Comparisons program was **discontinued in 2013**, so direct continuation is impossible. Extension candidates: BIS REER (PPI-based) or IMF INS REER, with caveats about differing trade-weight baskets.

### S1103 — Law of One Price at Aggregate Level (Fig 11.6)
Direct port of CD2 S062. Series is a **derived ratio**: `rxr1 / rulcadjratio1rescaled` per Appendix 11 Documentation sheet. Construction reclassified from `direct` (stub default) to `formula`. Inherits all S1102 extension issues plus a parallel discontinuation issue for the ULC denominator (BLS ILC). Modern extension requires coordinated reconstruction of both numerator (REER) and denominator (adjusted RULC) from BIS + OECD/Conference Board sources.

### S1104 — US Balance of Trade, Real Exchange Rate, Relative GDP (Fig 11.7)
Direct port of CD2 S063. Three-line overlay chart for US only: trade balance (= S1101-A), REER (= S1102-B), and **new** relative GDP US/EU12. **Two open issues flagged**:
1. CD2 markdown reports negative trade-balance values (−0.606 etc.) which are inconsistent with the X/M ratio used in Fig 11.2 — likely the series here is `(X-M)/(X+M)` net-trade ratio, not pure X/M. Needs direct cell inspection of `Appendix11_USJPNdata.xlsx`.
2. Source of "RelGDPR" is listed in Appendix 11.1.II raw-data items but **not described** in the documentation prose. Likely OECD QNA or World Bank WDI for US and EU12 real GDP; Phase 4 must resolve and EU12 composition must be decided (historical 12 members vs. modern Euro Area aggregate).

## Cross-series dependencies

| Component | Used by |
|---|---|
| IMF IFS X, M (per country) | S1101 (all subseries), S1104-A |
| BLS ILC Table 9 ULC | S1102, S1103 |
| BLS ILC Table 11 e | S1102, S1103, S1104-B |
| World Bank WDI PPI | S1102, S1103, S1104-B |
| IMF IFS trade weights | S1102, S1103, S1104-B |
| S1102 (REER PPI) | S1103 (numerator), S1104-B (same data) |
| S1101-A (US X/M) | S1104-A (likely; see units open question) |

S1104-C (US/EU12 relative GDP) is the only **new** data demand introduced in this chapter — every other input chains back to Appendix 11.1 raw inputs already required for S1101–S1103.

## Chapter-wide open questions

1. **BLS International Labor Comparisons discontinued (2013)** — affects S1102, S1103, S1104-B. Phase 4 must adopt a canonical replacement (BIS or Conference Board or IMF INS) and document the splice.
2. **China in Shaikh's 15-country panel** — Appendix 11.1.I lists 15 countries explicitly, none of which is China. CD2 added China to S060-E (now S1101-E). Decide whether to keep as comparator or drop.
3. **Trade-balance units** in S1104-A vs S1101: ratio (X/M) vs net-trade ((X−M)/(X+M)) — needs resolution from the workbook columns.
4. **RelGDPR source not explicit** in Appendix 11.1 prose; Phase 4 must identify.
5. **EU12 vs Euro Area** for relative-GDP extension — composition break.

## Validator status

All 4 series in scope passed Phase 3 validation (see `Technical/Build/PHASE3_VALIDATION_REPORT.json`).

---

## Phase 5-8 Closure (2026-05-18)

**Author**: opus-subagent-wave2-ch11-13-17

| SID | Content type | V03 status | MAE | Max %err | Chopped rows | Extension status (v1) |
|-----|--------------|------------|-----|----------|--------------|------------------------|
| S1101 | time_series | PASS | 0.0 | 0.0% | 766 | not_attempted_v1 (IMF DOTS deferred) |
| S1102 | time_series | PASS | 0.0 | 0.0% | 100 | data_unavailable_bls_ilc_discontinued (BIS PPI EER deferred) |
| S1103 | time_series | PASS | 0.0 | 0.0% | 100 | data_unavailable_bls_ilc_discontinued (formula recomp deferred) |
| S1104 | time_series | PASS | 0.0 | 0.0% | 100 | partial (S1104-C deferred) |

**Key resolutions**

- **BLS ILC substitution**: All Phase 4 CMJs (BIS PPI EER for REER; OECD ULC + Conference Board for ULC denominator) are documented in the per-series EPRs. v1 emits book-period values verbatim from the Appendix 11.1 workbooks; post-2009 BIS/OECD/Conference Board recomposition is deferred to a Phase 9 enrichment sprint with explicit `proxy: true` flags pre-registered.
- **S1104-A unit correction applied**: loader computes `(X-M)/(X+M)` from US X and M columns; CD2 negative sample values confirmed by V03.
- **S1103 formula audit**: V03 verifies `rxr1 / rulcadjratio1rescaled` reproduces `rxrrulcratio1` to <0.01% (formula-construction consistency).
- **S1101-E China kept as `cd2_addition: true` flag**: no salvage data for China available v1; placeholder preserved for Phase 9 IMF IFS fetch.

**Artifacts**

- DPR + EPR per series (8 + 8 markdown files in `Technical/docs/series/`)
- L01 + P02 + V03 per series (12 Python files in `Technical/code/{L01_loaders, P02_processors, V03_validators}/`)
- Chopped CSVs in `Technical/chopped/` and extenbooks in `Technical/extenbooks/`
- Registry bulk update via `Technical/code/utils/_phase5_ch11_13_17_register.py`

**Open items for Phase 9**

1. BIS PPI EER broad index fetch (US, JP) + reindex to 2002=100 at 1994-2009 overlap.
2. OECD ULC_QUA fetch for S1103_open variant; Conference Board ILC for S1103_hifi.
3. WDI NY.GDP.MKTP.KD per-country backfill for shaikh_pre1995_eu12 basket → S1104-C.
4. China IMF IFS X+M re-fetch for S1101-E.
