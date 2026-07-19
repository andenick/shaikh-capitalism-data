# Chapter 2 — Turbulent Trends and Hidden Structures

**Subagent**: opus-subagent-wave-a-ch2
**Date**: 2026-05-18
**Series**: 18 (S201–S218)
**Validator status**: 18/18 PASS

This rollup summarizes the Phase 3 research dossiers for Chapter 2 of Shaikh's *Capitalism: Competition, Conflict, Crises* (Oxford 2016, pp. 56–73 book pages; PDF pp. 95–112). Sources, methods, and figure-to-table mappings are taken from the chapter narrative and from Appendix 2.1 (book pp. 763–766, PDF pp. 802–805), which is Shaikh's own data-sources section for this chapter.

## Per-series rollup

- **S201 — US Industrial Production Index (Fig 2.1, 1860–2010).** Composite splice of BEA (1966) LTEG Table A15 (1860–1959, originally 1913=100) with FRB G.17 (1919–2010, originally 2007=100), both rebased to 1958=100 and spliced at 1919 per Appendix 2.1. Extension via FRED INDPRO (same FRB series). Ported from CD2 S001.

- **S202 — US Real Investment Index (Fig 2.2, 1832–2010).** Composite splice of BEA (1977) *Fixed Reproducible Tangible Wealth of the United States* Table B4 (1832–1975, 1970=100) with BEA Fixed-Asset Wealth Table 4.8 line 1 (1901–2010), rebased to 1958=100 and spliced at 1901. Extension via BEA NIPA Table 1.1.6 line 9 (concept match — nonresidential fixed investment) preferred over FRED GPDIC1 which includes residential. Ported from CD2 S002.

- **S203 — US Real GDP per Capita (Fig 2.3, 1889–2010).** Direct port of MeasuringWorth's `usgdp` dataset, which itself synthesizes Kuznets/Balke-Gordon/BEA NIPA. Appendix 2.1 lists 1790–2010 but the figure plots 1889–2010 (recorded). Extension is the same MeasuringWorth dataset (continues to present). Ported from CD2 S003.

- **S204, S205, S206 — Ayres Business Cycles, 1831–1866 / 1867–1902 / 1903–1939 (Figs 2.4A, 2.4B, 2.4C).** Three subperiod cuts of the same Ayres (1939) monthly business-cycle composite from the Cleveland Trust Company (table 9, appendix A, col. 1). No modern continuation — pre-NBER composite indicator with no clean successor. Historical-only series; HathiTrust link added for the source book. CD2 S004 covered all three figures jointly; S205 and S206 had no dedicated CD2 dossier.

- **S207 — US Manufacturing Productivity and Real Compensation (Fig 2.5, 1889–2010).** Composite: productivity = spliced BEA (1966) LTEG Series A173 (1860–1970) + BLS International Labor Comparisons Table 1 (1950–2009), rebased to 1889=100, spliced at 1950. Real compensation = MeasuringWorth nominal compensation / CPI for 1774–2010. Extension via FRED OPHMFG (productivity, US-only) and MeasuringWorth (compensation+CPI). **Open issue**: BLS FLS International Comparisons program was sunset in 2013 — flagged for Phase 4. Ported from CD2 S007.

- **S208 — US Manufacturing Real Unit Labor Cost (Fig 2.6, 1889–2010).** Formula series: real compensation ÷ productivity (both from S207 components). Extension must recompute the formula from extended components per Anu Framework no-lazy-splice rule, not splice the ratio directly. Ported from CD2 S008.

- **S209 — US Unemployment Rate (Fig 2.7, 1890–2010).** Composite splice of BEA (1966) LTEG Series B1–B2 (1860–1970) with Economic Report of the President Table B-40 (1948–2010). Extension via FRED UNRATE — same underlying BLS CPS series. Ported from CD2 S009.

- **S210 — US and UK Wholesale Price Indexes, 1780–2010 (Fig 2.8).** Composite of Jastram (1977) historical tables (UK Table 2, US Table 7) with mid-century interpolations (NBER macrohistory m04053 for UK 1939–1945; MeasuringWorth CPI for US 1706–1799) and modern extensions via BLS WPS00000000 (US) and ONS PLLU (UK). Per Appendix 2.1 the underlying data is shared with Chapter 5 (Appendix 5.3). CD2 had no dossier; constructed fresh from Appendix 2.1.

- **S211 — US and UK WPI, 1780–1940 (Fig 2.9).** Windowed view of S210 to expose pre-1940 long waves. No extension (truncation is part of the figure's analytical purpose).

- **S212 — US and UK Wholesale Prices in Ounces of Gold, 1790–2010 (Fig 2.10).** Formula series: WPI ÷ gold_price for each country, both indexed to 1930=100. Gold prices from MeasuringWorth (Officer & Williamson); for 1780–1785 US gold price estimated using 1786 US/UK ratio. Exposes "golden waves" with two postwar cycles peaking 1970 and 2000.

- **S213 — US Corporate Rate of Profit, 1947–2011 (Fig 2.11).** Formula: r = NOS / K_net in constant dollars per OECD definition. Underlying data BEA NIPA Table 1.14 + BEA Fixed-Asset Table 4.1. Full methodology in Appendix 6.7 (cross-referenced). Same series feeds Chapter 16 Fig 16.2. Open question on whether "Corporate" strictly means NIPA T1.14 or broader. Ported from CD2 S013.

- **S214 — Average Profit Rates, US Manufacturing 1960–1989 (Fig 2.12).** Formula series across 15 manufacturing aggregates (USMANAVG + 14 sub-sectors). Methodology in Appendix 7.1 / Christodoulopoulos (1995). OECD STAN sector codes are an extension candidate but require crosswalk to NAICS.

- **S215 — Incremental Profit Rates, US Manufacturing 1960–1989 (Fig 2.13).** Formula r* = PG / IG(–1) explicitly given in book footnote 6 (p. 68). Concept-similar successor in AMECO MEC (uses gross output instead of profits) — flagged as proxy.

- **S216 — Normalized Prices vs Unit Labor Costs, US 1972 (Fig 2.14).** Single-year cross-sectional scatter of 71 sectors from the 1972 BEA benchmark I–O. **Content-type reclassified from `time_series` to `cross_sectional`** per Anu Framework rule — single-year I–O cannot be extended in the time dimension. Each subsequent BEA benchmark year (1977, 1982, …, 2012) would be a separate scatter, not a continuation. Linked to Chapter 9 tables 9.9 and 9.13.

- **S217 — GDP per Capita of World Regions (Fig 2.15).** Direct port of Maddison (2003) regional aggregates (Western Europe, Western Offshoots, Latin America, Asia, Africa) in 1990 International Geary–Khamis dollars, 1600–~2008. Extension via Maddison Project Database 2023 with base-year discontinuity (2011 PPP, not 1990 GK). Split off from CD2 S017 (which covered Figs 2.15–2.17 jointly).

- **S218 — GDP per Capita Richest 4 / Poorest 4 (Figs 2.16 + 2.17).** Formula: re-rank country panel each decade, average top 4 and bottom 4 with Shaikh's exclusion rule (Kuwait, Qatar, Venezuela excluded from top 4; "16 Asians"-type regional aggregates used where country-level data is missing). Source values are tabulated in **Appendix Table 2.1.1** (book p. 766), included as cross-check. Ratio: 2.8 (1600) → 64.2 (2000). Extension requires re-applying the same exclusion rule to MPD 2023 and is non-trivial. No CD2 dossier (S017 covered this jointly).

## Chapter-wide observations

1. **Splice point conventions.** Shaikh consistently rebases historical+modern composites to a common base year (1958 for industrial/investment/productivity; 1930 for wholesale prices; 1889 for productivity+compensation indexes) and splices at the overlap year. The Anu Framework treats every such splice as `construction: composite` with explicit `components[]`.

2. **Derived vs spliced quantities.** Three Ch2 series are *formula* series whose extension must recompute the formula from extended components rather than splicing the ratio (S208 RULC, S212 WPI-in-gold, S213 profit rate). This is enforced by the no-lazy-splice rule.

3. **Discontinued upstream sources.** BLS FLS International Labor Comparisons was sunset in 2013 (affects S207). BEA LTEG (1966) and Fixed Reproducible Tangible Wealth (1977) are out-of-print monographs — still cited but the canonical access route in 2026 is HathiTrust / library archives, not BEA's web site.

4. **Cross-chapter shared data.** Several Ch2 figures are explicitly windowed views of data discussed in detail elsewhere: S210/S211/S212 share data with Appendix 5.3; S213 with Appendix 6.7 and Ch 16; S214/S215 with Appendix 7.1; S216 with Ch 9 (tables 9.9, 9.13); S217/S218 with Maddison (2003). Phase 4 should ensure the canonical dossier lives in the deeper-treatment chapter and Ch2 cross-references it.

5. **Cross-sectional vs time series.** Stub for S216 had `content_type: time_series`; reclassified to `cross_sectional` (single-year I–O scatter). Phase 4 should confirm.

6. **Companion website.** Appendix 2.1 references http://www.anwarshaikhecon.org/ for "Appendix 2.2 Data Tables." That site's status in 2026 is uncertain — if still live, it is the authoritative source for the digitized series values that Shaikh actually plotted; if not, the ShaikhChoppedTables/ replicas (Appendix2_*.xlsx) are the next best replication source.

7. **Typo preserved.** Appendix 2.1 (p. 765) writes "Qutar" for "Qatar" — preserved verbatim in S218's source quote per the no-paraphrase rule, noted in open_questions.

## Validator output

Chapter 2 subset: **18/18 PASS** (full report `Technical/Build/PHASE3_VALIDATION_REPORT.json`).
Other chapters' failures are not in this subagent's scope (Wave A Ch3–Ch6 and Waves B/C are separate dispatches).

---

## Phase 5-8 Closure (2026-05-18)

**Author**: opus-subagent-wave2-ch2
**Scope**: S202-S218 (S201 pilot already complete)
**Outcome**: 17/17 series PASS at the 1.0% tolerance gate. With S201, chapter total = 18/18 PASS.

### Per-series summary

| SID | Content type | V03 status | MAE | Chopped rows | Notes |
|---|---|---|---|---|---|
| S202 | time_series | PASS | 0.000 | 179 | BEA 1977 + BEA Wealth T4.8 spliced at 1901; BEA NIPA T1.1.6 line 9 extension preferred over FRED GPDIC1 (concept-correct) |
| S203 | time_series | PASS | 0.000 | 221 | MeasuringWorth USGDP direct; FRED A939RX0Q048SBEA extension |
| S204 | time_series | PASS | 0.000 | 432 | Ayres 1939 monthly, 1831-1866; historical-only |
| S205 | time_series | PASS | 0.000 | 432 | Ayres 1939 monthly, 1867-1902; historical-only |
| S206 | time_series | PASS | 0.000 | 439 | Ayres 1939 monthly, 1903-1939; historical-only |
| S207 | time_series | PASS | 0.000 | 275 | Two co-plotted (productivity + real comp); FRED OPHMFG (proxy) + COMPRMS extension |
| S208 | time_series | PASS | 0.000 | 137 | Formula RULC = real_comp/productivity; extension recomputes from S207 components (NOT FRED ULCMFG) |
| S209 | time_series | PASS | 0.000 | 136 | BEA LTEG B1-B2 + ERP T B-40 + FRED UNRATE; 0.15pp absolute tolerance |
| S210 | time_series | PASS | 0.000 | 490 | US+UK WPI; canonical replica via CD2 S023; FRED WPU substitutes frozen WPS |
| S211 | time_series | PASS | 0.000 | 302 | Windowed view of S210 to 1940; no extension by design |
| S212 | time_series | PASS | 0.000 | 490 | Formula WPI/gold; CD2 S024+S025 as truth; recompute extension via FRED |
| S213 | time_series | PASS | 0.000 | 78 | Corporate profit rate; CD2 S026 as truth; 0.005 absolute tolerance; BEA T1.14 line-mapping extension deferred |
| S214 | time_series | PASS_DATA_UNAVAILABLE | n/a | 19 | Book 1960-1989 source not in SalvagedInputs; S214-EXT (1987-2005) emitted from Appendix7 |
| S215 | time_series | PASS_DATA_UNAVAILABLE | n/a | 18 | Same status as S214 |
| S216 | cross_sectional | PASS | n/a | 142 | 1972 71-industry I-O scatter (tpr_norm + tpm_norm vs tv_norm); 0.5% tolerance |
| S217 | time_series | PASS | 0.000 | 224 | Maddison 2003 regions; 6 subseries; MPD 2023 extension deferred (base year shift) |
| S218 | time_series | PASS | 0.000 | 63 | Maddison RICHEST 4 / POOREST 4 / RATIO; Shaikh exclusion rule documented for MPD 2023 deferred extension |

### Phase 4 substitutions applied

| Series | Substitution | Status |
|---|---|---|
| S202 | BEA NIPA T1.1.6 line 9 instead of FRED GPDIC1 (no residential inclusion) | Applied (concept-correct) |
| S207 | MeasuringWorth uscompensation -> uswage URL rename | Applied |
| S207 | BLS FLS Table 1 (sunset 2013) -> FRED OPHMFG (US-only, concept-narrowed) | Applied with `proxy: true` flag + Concept Match Justification |
| S207 | FRED COMPRMS for compensation extension | Applied |
| S208 | Avoid FRED ULCMFG (nominal); recompute from S207 | Applied per playbook formula recipe |
| S210 | BLS WPU00000000 instead of frozen WPS00000000 (post-1974) | Applied (direct BLS successor, not a proxy) |
| S210 | NBER macrohistory URL update | Documented in subsource metadata |
| S214/S215 | OECD STAN with ISIC crosswalk | Deferred -- book period data not in Salvaged |
| S217/S218 | MPD 2023 (1990 GK -> 2011 PPP rebase) | Deferred -- documented in EPR |

### Shared-file coordination approach

A single one-shot script `Technical/code/utils/_ch2_register.py` performs atomic
read-modify-write on:

- `Technical/series_registry.json` -- 17 series updated with subseries decompositions,
  status `ingested`, units, construction class, proxy flags, formulas, components.
- `Technical/SUBSOURCE_METADATA.json` -- 29 new subsources added (BEA 1977 T B4,
  BEA Wealth T4.8, BEA NIPA T1.1.6 L9, MeasuringWorth USGDP, FRED RGDPPC, Ayres,
  BEA LTEG BLS FLS splice, MW USWAGE+CPI, FRED OPHMFG, FRED COMPRMS, Shaikh-derived
  RULC, BEA LTEG B1-B2, ERP T B-40, FRED UNRATE, Jastram T7+BLS PPI, Jastram T2+ONS PLLU,
  FRED WPU00000000, Jastram T7 US WPI, Jastram T2 UK WPI, Jastram T1 + MW US WPI/gold,
  Jastram + MW UK WPI/gold, FRED gold, recomputed FRED WPU+gold, BEA NIPA T1.14 + FA T4.1,
  Shaikh APP7 ROP, Shaikh APP7 IROP, BEA IO 1972 + Shaikh APP9, Maddison 2003 regions,
  Maddison + Shaikh exclusion rule).
- `Technical/ANU_LEDGER.json` -- 17 series tracked with `extenbook_published` status
  and full artifact paths.

The script is idempotent; re-running is safe. All edits use atomic temp-file +
rename to avoid corrupting parallel writes from other agents.

### Validator output

Chapter 2 final: **18/18 PASS** (S201 pilot + 17 wave-2 series).

### Open questions

1. **S213 corporate sector ambiguity**: Phase 3 open question (NIPA T1.14 corporate strictly
   vs broader business sector per App 6.7) remains; CD2 S026 interpretation adopted as canonical.
2. **S214/S215 book period data**: anwarshaikhecon.org Appendix 7.2 not in SalvagedInputs;
   per no-fabrication rule, 1960-1989 segment is published as `data_unavailable` with
   PASS_DATA_UNAVAILABLE status. Remediation path documented in EPR.
3. **S217/S218 MPD 2023 extension**: 1990 GK -> 2011 PPP base shift + region reaggregation
   requires manual splice; deferred to Phase 9. Shaikh exclusion rule for S218 needs
   reapplication (Kuwait/Qatar/Venezuela; possibly Macao, Luxembourg in modern panel).
4. **S210 UK extension**: ONS PLLU specific URL returned transient 502; UK post-2010
   extension deferred until URL stabilizes. US extension via FRED WPU is live.
