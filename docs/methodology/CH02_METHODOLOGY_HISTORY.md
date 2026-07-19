# Chapter 2 — Methodological History: "Turbulent Trends and Hidden Structures"

**Project:** RSCD — replication of Anwar Shaikh, *Capitalism: Competition, Conflict, Crises* (Oxford University Press, 2016).
**Scope:** 18 series, S201–S218 (Figures 2.1–2.17).
**Author:** Phase-2 methodological-historian agent (2026-06-30).
**Companion artifacts:** per-series MHRs at `Technical/docs/methodology/series/S2##_MHR.md`; machine-readable digest `Technical/methodology_review/CH02_methodology.json`; review findings `Technical/methodology_review/CH02_review.json`; change timelines `Technical/docs/methodology/_timelines/{NIPA,IO}_CHANGE_TIMELINE.md`.

This dossier reads Chapter 2 *from Shaikh's own perspective*: why he chose each data source, which alternatives he rejected, and how vintage/reclassification history exposes each series. Every author-intent claim in the per-series MHRs is grounded in a citable path (book KB, `SalvagedInputs/methodology_library/`, or the research JSONs); where the corpus contains no rejection rationale, the MHRs say so rather than inventing one.

---

## 1. What the chapter is for, and what that implies for sourcing

Chapter 2 is the book's "distant view." Shaikh's stated purpose (book p.56, KB `Body_Text/ch02_turbulent_trends.md`) is to display "characteristic long-run economic patterns in developed capitalist countries" so that "recurrence and turbulent regulation arise quite naturally." That framing dictates the sourcing strategy for the whole chapter:

- **Very long horizons (100–400 years).** Almost every series reaches back a century or more, which forces Shaikh off any single modern agency feed and onto **composite splices** of an out-of-print historical monograph + a live modern series.
- **Log-scale display.** He plots strongly-trended variables on a log scale "which means that the rate of growth … is represented by the slope" (p.56). This makes *reindexing to a common base year* — not level continuity — the operative splicing discipline.
- **US as default, but not dogmatically.** His meta-rationale (book p.56, quoted verbatim in the S201/S207/S209 MHRs) is: "I will often use the United States as the primary illustration because it is the preeminent advanced country and because it generally has the best available data." He breaks this deliberately when the concept demands it — adding the **UK** for the 305-year price record (S210–S212) and going fully **global via Maddison** for the convergence/divergence argument (S217–S218).
- **Author's own data appendix is the ground truth for provenance.** Shaikh documents every figure's sources in **Appendix 2.1 "Data Sources and Methods" (book pp.763–766)**, with the digitized values promised in **Appendix 2.2** at `anwarshaikhecon.org` (2026 availability uncertain — a standing replication risk noted across the MHRs). Appendix 2.1 is the primary grounding for source choice throughout.

## 2. The four construction archetypes in Chapter 2

The 18 series fall into four provenance archetypes, and the same archetype recurs across chapters:

**(A) Historical-monograph → live-agency composite splice** (S201 IP, S202 investment, S207 productivity, S209 unemployment, S210 WPI). The signature pattern: an out-of-print BEA/BLS/Jastram historical table for the early decades, spliced to a live Fed/BLS/BEA/FRED series at an overlap year, both reindexed to a common base (1958=100 for the industrial/investment/productivity block; 1930=100 for prices; 1889=100 for the productivity/compensation index). Shaikh consistently lets the **modern authority govern the overlap** — e.g. S201 takes the FRB value (24.31), not the BEA value (24.77) or an average, at the 1919 splice.

**(B) Direct port of a synthesizing third-party dataset** (S203 MeasuringWorth GDP/cap; S217/S218 Maddison world GDP/cap). Where no single official series spans the needed horizon, Shaikh adopts an established scholarly synthesis (Officer & Williamson's MeasuringWorth; Maddison 2003's "monumental work," p.70) rather than assembling his own. The trade-off: he inherits that third party's revisions and, in one case, a corrupted salvaged copy (S203, see §4).

**(C) Formula / derived series** (S208 RULC = real comp ÷ productivity; S212 WPI ÷ gold; S213 r = NOS ÷ K_net; S215 r* = PG ÷ IG(–1); S218 richest-4/poorest-4 ratio). These carry **no external source of their own** — they are computed from other series' components. The governing replication rule (Anu no-lazy-splice) is that their extension must **recompute the formula from extended components**, never splice the ratio. The MHRs enforce this pointedly for S208 (must not substitute nominal FRED ULCMFG) and S212/S213 (must not splice the ratio across a base change or NIPA-revision boundary).

**(D) Frozen historical exhibits with no successor** (S204–S206 Ayres business cycles; S211 windowed WPI; S216 single-year 1972 I-O scatter). These are historical-only by design and are **never extended**. For the Ayres trio the source has no modern equivalent; for S211 the truncation at 1940 *is* the analytical point; for S216 each BEA benchmark year is a separate frozen cross-section, so "extension" would mean adding a new scatter, not continuing a line.

## 3. Shared sources and the author's source-selection logic

A handful of upstream sources recur and tie the chapter together:

- **BEA *Long Term Economic Growth* (1966)** anchors the early decades of S201 (Table A15/Series A173), S207 (Series A173 productivity), and S209 (Series B1–B2 unemployment). It is Shaikh's go-to for pre-WWII US aggregates because it is a single internally-consistent official back-history — now accessible only via HathiTrust/library archives (out of print).
- **BEA Fixed-Asset accounts** anchor S202 (Table 4.8 / Fixed Reproducible Tangible Wealth 1977) and S213 (Table 4.1 net capital stock).
- **MeasuringWorth (Officer & Williamson)** supplies S203 (GDP/cap), the compensation and CPI legs of S207/S208, the US pre-1800 WPI backfill in S210, and the gold prices in S212.
- **Maddison (2003)** supplies both S217 (regions) and S218 (country panel) — the same underlying dataset cut two ways.
- **FRED** is the standard live extender (INDPRO, GPDIC1-rejected/T1.1.6-preferred, OPHMFG, COMPRMS, UNRATE, WPU, gold), but the MHRs stress that FRED is only ever the *transport layer* for an underlying agency series; concept identity, not convenience, decides whether a FRED handle is a clean successor or a proxy.

**The most instructive rejected-alternative decisions** (all grounded in the research JSONs / DPRs / CH2 review):

1. **S202 rejects FRED GPDIC1 for BEA NIPA T1.1.6 line 9.** GPDIC1 bundles *residential* investment; Shaikh's concept is *nonresidential business* fixed investment. RSCD elevates this to a formal CH2 review touchpoint — a deliberate anti-silent-proxy choice.
2. **S208 rejects FRED ULCMFG.** ULCMFG is *nominal* unit labor cost; Shaikh's Figure 2.6 is *real* unit labor cost (the wage share of the value of output, book fn3). Splicing ULCMFG would silently swap the concept, so the extension recomputes real comp ÷ productivity.
3. **S215 rejects the naïve incremental rate ΔP/ΔK — by Shaikh himself.** Book footnote 6 (p.68) prefers `r* = PG/IG(–1)` precisely because gross profits and lagged gross investment are *invariant to the Capital Consumption Adjustment and to any capital-stock / useful-life estimate*. AMECO's MEC is the concept-similar modern successor but uses gross *output* not profits — flagged as a proxy, not adopted.
4. **S216 rejects a fitted regression line and a multi-year price panel.** Shaikh explicitly notes the 45° line is "not a fitted regression line" (p.70), and the single-year 1972 benchmark is chosen because 1972 is the **last conformable year of his Ochoa 71-order panel** before the SIC→NAICS wall.
5. **S204–S206: the source itself was a personal referral.** The entire 108-year business-cycle record traces to a tip from Ravi Batra (book p.57, fn1, verbatim), and Shaikh chose the continuous Cleveland Trust/Ayres (1939) deviation-from-trend composite over NBER reference-cycle dates because only a continuous monthly index renders the *shape and depth* of the recurrent "Great Depressions" (1840s/1870s/1930s) on one axis.

Where the book/corpus does **not** state why an alternative was rejected (e.g. Jastram over HSUS/JST for S210; Maddison over PWT/WDI/GGDC for S217/S218; Kendrick 1961 for S207), the MHRs record "author rationale not located in corpus" rather than manufacture one.

## 4. Methodological-change exposure — the chapter's shared vintage story

The two Phase-0 timelines drive the exposure analysis:

- **NIPA comprehensive revisions (1999/2003/2009/2013/2018/2023).** The book fixes all BEA data at the **2011 vintage** (Appendix 6.7 fn1). The high-impact boundary is **2013** (R&D + entertainment capitalized → new IPP category, ≈ +$400B GDP, fixed-asset/capital-stock *levels rise*), which touches every BEA-sourced series' extension — most consequentially **S213**, where the 2013 revision restates *both* the numerator (NOS) and the denominator (K_net) of the profit rate. The **2018** update inserted the **T7.11 +1 line shift** (resolve by `LineDescription`, not line number) and **2023** moved the reference year to 2017. The cross-cutting rule the MHRs repeat: **never splice an extension across a comprehensive-revision boundary — recompute end-to-end on one vintage.**
- **BEA benchmark I-O + SIC→NAICS (the "Ch9 wall").** Benchmarks appear every 5 years (years ending 2/7). The hard classification break is **last SIC benchmark 1992, first NAICS 1997**; pre-1997 tables "should not be used as a time series," and the **1997 benchmark was the last capital-flow table**. This governs **S216** (each benchmark is a frozen scatter; Ochoa-71 vs BEA-65 non-conformable) and blocks the modern extension of **S214/S215** (sectoral capital-by-industry must be approximated post-1998; OECD STAN needs an ISIC→NAICS crosswalk).
- **Index re-basing rather than restatement.** The pure-index series (S201, S207, S208) are insulated from NIPA *level* restatements but exposed to **reference-year re-basing** (FRED INDPRO 2007→2012→2017; OPHMFG rebasings). The discipline is to reindex at the live overlap on every load, never cache a rebased level.
- **Price-index rename/renumber.** S210/S212 ride BLS **WPI→PPI** (WPS→WPU) and ONS UK price-index revisions — *not* NIPA — so the NIPA/IO timelines are explicitly marked non-applicable for those series.
- **Base-year + reaggregation discontinuity.** S217/S218 face the **Maddison 2003 (1990 GK$) → MPD 2023 (2011 PPP)** base change *plus* redrawn regional aggregates — a concordance dependency, not a simple splice. Notably, the S218 **ratio** (Fig 2.17) is base-invariant and survives a re-base, whereas the level series do not.
- **Insulated exhibits.** S204–S206 (frozen 1939 Ayres compilation) and S211 (windowed pre-1940 view) have *no live upstream*, so their only "change" risk is source-transcription fidelity.

## 5. Replication fidelity — honest limits carried from the review

The Phase-1 review (`CH02_review.json`, integration score 84.7, D13 PASS-conditional) surfaced findings the MHRs carry candidly rather than paper over:

- **S203 — F-01 (HIGH), source corruption.** Real GDP/cap *rises* through the Great Depression (1929→1934, 8188→14706), which is economically impossible. The RSCD chopped is byte-faithful to a **corrupted salvaged MeasuringWorth workbook**, and V03 round-trips the same corrupted source (MAE 0.0 "PASS" is meaningless — the gate is structurally blind). Remediation = fresh MeasuringWorth re-pull + an out-of-source sanity assert (1929 > 1933); **block external publish until fixed.** (F-04: the registry name also omits "per Capita.")
- **S214 / S215 — F-02 (HIGH), coverage overstatement.** Both ship only their **–EXT (1987/1988–2005)** extensions; the **book Fig 2.12/2.13 period 1960–1989 is entirely absent** (the source, `anwarshaikhecon.org` Appendix 7.2, is not in SalvagedInputs). Marked `PASS_DATA_UNAVAILABLE` — no values were fabricated — but the `book_period_validated` status label overstates coverage until a true book subseries is digitized. S215 additionally carries a formula-rendering discrepancy flag (registry `r*=PG/IG(-1)` vs the book/KB numerator being the *change* in gross profits).
- **S207 — F-09 (LOW), proxy concept-narrowing.** The book's productivity source (BLS International Labor Comparisons, a 19-country program) was **sunset in 2013**; the only faithful extender, FRED **OPHMFG**, silently narrows the concept to US-manufacturing-only. Correctly flagged `proxy=true`; the MHR now spells out the narrowing.
- **S213 — open question.** Whether "Corporate" means strictly NIPA T1.14 or the broader business sector (App 6.7) is unresolved; the CD2 S026 interpretation is adopted as canonical, and the line-mapping extension is deferred pending a `LineDescription`-based resolver.
- **Structural (F-03):** no per-series `*_DECOMPOSITION.md` exist project-wide; construction lives in DPR §4 + registry `construction_steps`/`subseries`. These MHRs partly fill that documentation gap for the provenance dimension.

## 6. Forward risk — what breaks next

- **Next NIPA comprehensive revision** re-restates S213's NOS and K_net (and could move the whole profit-rate level via the corporate-vs-business question) and shifts T7.11-style line numbers again — extensions must re-resolve by caption.
- **Next FRED/FRB re-basing** (INDPRO 2017→2022 ~2027; OPHMFG) breaks S201/S207/S208 only if a rebased level is cached instead of reindexed at the live overlap.
- **ONS PLLU discontinuation** (already threw a 502) is the top live-source risk for the S210/S212 UK legs.
- **MPD revisions** re-base and redraw regions, breaking the S217 regional lines and shifting S218's exclusion-set membership (Macao/Luxembourg are modern candidates) — the ratio survives, the levels do not.
- **Out-of-print / companion-site fragility.** BEA (1966) LTEG, BEA (1977) Fixed Reproducible Tangible Wealth, and Ayres (1939) are non-recoverable except via library/HathiTrust archives, and the `anwarshaikhecon.org` Appendix 2.2/7.2 data tables of uncertain 2026 status are the blocking dependency for the S214/S215 book-period recovery.

## Series index

| SID | Figure(s) | Concept | Archetype | Key exposure |
|---|---|---|---|---|
| S201 | 2.1 | US industrial production 1860–2010 | A splice | index re-basing |
| S202 | 2.2 | US real nonres. fixed investment 1832–2010 | A splice | NIPA 2013 IPP uplift |
| S203 | 2.3 | US real GDP/capita 1889–2010 | B port | **F-01 source corruption** |
| S204 | 2.4A | Ayres business cycles 1831–1866 | D frozen | none (frozen 1939) |
| S205 | 2.4B | Ayres business cycles 1867–1902 | D frozen | none (frozen 1939) |
| S206 | 2.4C | Ayres business cycles 1903–1939 | D frozen | none (frozen 1939) |
| S207 | 2.5 | Mfg productivity + real compensation 1889–2010 | A splice | **BLS FLS sunset 2013** |
| S208 | 2.6 | Mfg real unit labor cost 1889–2010 | C formula | recompute, not ULCMFG |
| S209 | 2.7 | US unemployment rate 1890–2010 | A splice | CPS re-benchmark |
| S210 | 2.8 | US+UK WPI 1780–2010 | A splice | ONS PLLU discontinuation |
| S211 | 2.9 | US+UK WPI 1780–1940 (windowed) | D frozen | none (windowed) |
| S212 | 2.10 | US+UK WPI in ounces of gold 1790–2010 | C formula | recompute the ratio |
| S213 | 2.11 | US corporate rate of profit 1947–2011 | C formula | **NIPA 2013 (NOS+K_net)** |
| S214 | 2.12 | Avg mfg profit rates 1960–1989 | C formula | **F-02 book period unavailable** |
| S215 | 2.13 | Incremental mfg profit rates 1960–1989 | C formula | **F-02 book period unavailable** |
| S216 | 2.14 | Prices vs ULC, US 1972 (71 sectors) | D cross-section | SIC→NAICS wall |
| S217 | 2.15 | GDP/cap of 5 world regions 1600–2008 | B port | Maddison→MPD re-base |
| S218 | 2.16/2.17 | Richest-4/poorest-4 GDP/cap + ratio | C formula | MPD re-base + exclusion rule |

---

*Grounding discipline: all author-intent claims trace to `Inputs/Capitalism Data/.../Knowledge_Base/HDARP_v3.3_Campaign/` (book KB), `Technical/research/S2##_research.json`, `Technical/docs/series/S2##_{DPR,EPR}.md`, or `SalvagedInputs/methodology_library/`. Unlocated rationales are marked "not located in corpus." READ-ONLY pass — no registry/code/data/Inputs were modified.*
