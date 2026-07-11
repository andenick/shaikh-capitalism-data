# Chapter 5 — Methodological History: "Exchange, Money, and Price"

**Project:** RSCD — replication of Anwar Shaikh, *Capitalism: Competition, Conflict, Crises* (Oxford University Press, 2016).
**Scope:** 4 series, S501–S504 (Figures 5.3–5.6).
**Author:** Phase-2 methodological-historian agent (2026-06-30).
**Companion artifacts:** per-series MHRs at `Technical/docs/methodology/series/S50#_MHR.md`; machine-readable digest `Technical/methodology_review/CH05_methodology.json`; comprehensive review `Technical/methodology_review/CH05_review.json`; research JSONs `Technical/research/S50#_research.json`; per-series DPR/EPR `Technical/docs/series/S50#_{DPR,EPR}.md`; chapter summary `Technical/docs/chapters/CH5_RESEARCH_SUMMARY.md`.

This dossier reads Chapter 5 *from Shaikh's own perspective*: why he decomposes the price level into gold, why he chose Jastram and MeasuringWorth over the alternatives, and how vintage/reclassification history exposes each series. Every author-intent claim in the per-series MHRs is grounded in a citable path (book KB, research JSONs, DPR/EPR, or the Ch5 review); where the corpus contains no rejection rationale, the MHRs say so rather than inventing one. **Chapter 5 scored EXEMPLARY (integration 95.3, D13 PASS = 100)** — the data is exact (754 book-period cells at MAE 0.0), so this dossier's job is to capture the *deep source story*, not to remediate.

---

## 1. What the chapter is for, and what that implies for sourcing

Chapter 5 is where Shaikh lays out the **classical/Marxian theory of money and the general price level** and confronts it with data. The book's own division of labor (book p. 189, `S502_research.json` book_quotes[1]) is between "the theory of relative prices (governed in the long run by prices reflecting competitively equalized rates of profit) and the theory of the general price level." The empirical heart is a **four-figure narrative arc** (Figs 5.3–5.6) that all draws on a **single shared spreadsheet** — Shaikh's Appendix 5.3 `DATALRprices`. That framing dictates the sourcing strategy:

- **Very long horizons (150–220 years).** The whole argument is about *long-run* regime behavior, so no single modern agency feed suffices; Shaikh goes onto **composite splices** of an out-of-print historical monograph (Jastram 1977) + a live modern feed (BLS WPS / ONS PLLU / MeasuringWorth).
- **Log-scale display, 1930 = 100.** Every figure is log-scaled with Jastram's 1930=100 base, so the operative splicing discipline is **growth-rate reindexing to a common base**, never level continuity.
- **The gold decomposition is the point.** Where Chapter 2 merely *displays* the WPI and WPI-in-gold (Figs 2.8–2.10), Chapter 5 *derives* them from equation 5.9 (`p = p′ · pG`) and uses them to test the theory. **The CH2 MHRs (S210/S212) explicitly name Chapter 5 as the canonical deep home of the WPI/gold family** — this dossier is that home.
- **Author's own data appendix is ground truth for provenance.** Every figure's sources are in **Appendix 5.2 "Data Sources and Methods" (book pp. 788–789)**, transcribed verbatim in the research JSONs; the digitized values live in **Appendix 5.3 `DATALRprices`** at anwarshaikhecon.org — **DNS-dead in 2026**, with the salvaged local `Appendix5_DATALRprices.xlsx` promoted to canonical (Internet Archive snapshot 2024-03-11 as the web citation).

## 2. The two construction archetypes in Chapter 5

The four series fall into two archetypes (the same archetypes recur across the book):

**(A) Historical-monograph → live-agency composite splice** — **S501, S502.** Jastram's Tables 2 (UK) / 7 (US) for the early decades, spliced by *implicit growth rate* to a live BLS/ONS feed at 1977, both on 1930=100. **S502** is the full 1790–2010 parent; **S501** is a *direct chronological slice* of S502 windowed to 1790–1940 (the pre-fiat baseline, identical to Ch2 Fig 2.9). Two documented in-book gap-fills sit *inside* the book period and are not proxies: US 1790–1799 via US-CPI rescaled at the 1800 WPI/CPI ratio, and UK 1939–1945 via NBER macrohistory `m04053`.

**(C) Formula / derived series** — **S503, S504.** The empirical implementation of **equation 5.9** (`p = p′ · pG`) for the UK and US respectively. Each carries **no external source of its own** — p′ (WPI-in-gold) and pG (money-price-of-gold) are pre-computed by Shaikh from other components and read directly. The governing replication rule (Anu **No Lazy Splices on Derived Quantities**) is that their extension must **recompute the ratio from extended WPI and extended gold-price**, never growth-splice p′ itself.

There is **no frozen-exhibit or direct-port archetype in this chapter** (contrast Ch2's Ayres cycles and Maddison ports). All four series ride the same `DATALRprices` spine, so the **loader dependency is a strict tree: `S502 → {S501, S503, S504}`** — S501 is its 1790–1940 window, and S503/S504 consume its UKWPI/USWPI legs as the numerators of p′.

## 3. Shared sources and the author's source-selection logic

Three upstream sources tie the whole chapter together:

- **Jastram (1977), *The Golden Constant*** — Tables 2 (UK, from 1560) and 7 (US, from 1800), both on **1930 = 100** and built *alongside a matching gold-price series*. This pairing is the whole reason Shaikh chose Jastram: it gives him a WPI **and** a gold price on one basis, which is exactly what equation 5.9 needs to form p′ = WPI/gold. The UK reach (1560) is what makes the "no long-run trend for the whole 150-year interval" claim credible (book p. 188).
- **MeasuringWorth (Officer & Williamson), "The Price of Gold, 1257–2010" + the dollar-pound exchange series** — the canonical scholarly synthesis that *continues the gold price forward* to 2010 and supplies the **FX conversion** needed when MeasuringWorth switches the UK gold quote from £ to US$ after 1949. No single official feed spans two centuries of a national gold price, so a scholarly synthesis is the only faithful option (the same "port an established synthesis" logic Shaikh uses for Maddison in Ch2).
- **BLS `WPS00000000` (US) and ONS `PLLU` (UK)** — the direct national successors to the historical wholesale-price concept, growth-rate-spliced onto Jastram's 1930=100 base for 1977–2010. **NBER macrohistory `m04053`** fills the one wartime UK gap (1939–1945).

**The most instructive source decisions (all grounded in the research JSONs / DPR-EPR / Ch5 review):**

1. **Why decompose the price level into gold at all (S503/S504).** Shaikh's theory (book pp. 194–195, `ch05_exchange_money_price.md` lines 1322–1389) says the long-run price level is the *product of two fairly independent factors* — p′ (regulated by competition/structural conditions) and pG (fixed by the monetary regime). Equation 5.9 is the *testable structure* of the classical/Marxian theory **against the Quantity Theory** (eq. 5.7): the price level is set by p′·pG, not by M/XR·v. Figs 5.5/5.6 are the test, and they pass — p′ is modest while all the post-1931/1939 inflation lives in pG.
2. **Why Jastram over modern best-vintage price histories** — a *deliberate fidelity* choice (Jastram is the canonical gold/price history with a matching WPI), but the **explicit rejection of Officer/Williamson's own WPI, HSUS, or JST is author rationale not located in corpus**; the chapter summary flags the fidelity-vs-data-quality tension as an open decision.
3. **Two CD2 documentation errors corrected, NOT Shaikh alternatives.** CD2 S024 mis-attributed the UK gold-price extension to "BLS PPI"; CD2 S025 listed "COMEX/LBMA" as the US gold source. Appendix 5.2 is explicit that both gold prices come from **MeasuringWorth** (+ Officer FX for the UK £ conversion; LBMA is only the *underlying* of MeasuringWorth's market price). RSCD corrected both in Phase 3 and ratified in Phase 4.
4. **Why the US case is the sharpest test (S504).** US monetary history contains two clean, datable regime breaks — the **1934 FDR devaluation** ($20.67→$35.00/oz) and the **1971 Bretton Woods collapse** — that should, and do, show up entirely in pG and not in p′.

## 4. Methodological-change exposure — the chapter's shared vintage story

- **NIPA and I-O timelines are NON-APPLICABLE across the entire chapter.** Every Ch5 series is built from **BLS/ONS price indexes, Jastram's historical tables, and MeasuringWorth gold — none of it is NIPA or benchmark I-O data.** The BEA comprehensive-revision events cataloged in `NIPA_CHANGE_TIMELINE.md` (1999–2023) and the SIC→NAICS benchmark wall in `IO_CHANGE_TIMELINE.md` **do not touch any of S501–S504.** This is stated explicitly in each MHR per the task contract, and mirrors the CH2 treatment of the same data family (S210/S212 marked NIPA/IO non-applicable).
- **The one live concordance axis is BLS WPI→PPI (WPS→WPU) + ONS PLLU re-basing.** Shaikh's US extender `WPS00000000` is a **legacy code BLS froze** (≈1974); its live successor under the same PPI All-Commodities program is `WPU00000000` (FRED `PPIACO`), which RSCD uses as a **direct within-agency successor, `proxy: false`**, verified live through 2026-04. This axis **bites only where a series reaches the post-1976 extension segment**: it is real for **S502** (US extension) and rides *through the numerator* into **S503/S504**; it is **latent-but-never-reached for S501**, which stops at 1940 inside Jastram's frozen archive.
- **The WW2 UK gold interpolation is Shaikh's own (S503).** The London gold market was suspended 1939–1945, so MeasuringWorth's Officer-Williamson series **interpolates** those years and **Shaikh adopts the interpolation**. RSCD flags all 7 years `proxy_flag=ww2_gold_suspension_interpolated_measuringworth` — disclosed **source-interpolation, not fabrication** (the Ch5 D13 gate passes *because* it is flagged as interpolation). The same wartime window is *also* NBER-m04053-filled on the UKWPI leg, so two independent WW2 interpolations meet in S503.
- **Two structural splice points on the gold denominators:** the **1950 £→US$ currency-quote switch** in MeasuringWorth (bridged by Officer's dollar-pound FX, S503) and the **LBMA March-2015 reform** (London Gold Fixing → LBMA Gold Price PM, the documented overlap-anchor for any future S503/S504 extension).
- **MeasuringWorth gold and Jastram's historical base are frozen compilations** (extended, not revised) — low methodological-change risk; the whole chapter's vintage risk is concentrated in the two live PPI feeds.

## 5. Replication fidelity — honest limits carried from the review

The Ch5 comprehensive review (`CH05_review.json`, integration 95.3, **EXEMPLARY**, D13 PASS = 100) found the data exact — so the honest limits here are about *coverage and convention*, not correctness:

- **Formula-series extensions deferred, not faked (S503/S504, finding L5).** Both ship `not_attempted_v1`: S503 needs an extended UKWPI (ONS PLLU — blocked by CDN 502) AND an extended UK £-gold price (LBMA PM ÷ BoE FX — no helper); S504 needs the US $-gold denominator (no LBMA helper). No proxies, no synthetic fill; honestly documented.
- **S502 UK extension NaN (finding L5).** ONS PLLU CDN 502 → UK 2011+ left NaN; the US line extends to 2026 via FRED `PPIACO` while the UK line stops at the book's 2010. No different-concept UK PPI substituted.
- **S502 extension-block convention (finding L4).** The US extension ships as `S502-C` rather than a formal `-EXT` block, sidestepping the Decision 0003 `-EXT` invariant; internally consistent under the long-form canonical (Decision 0005).
- **FDR jump convention (S504, open question 3).** The RSCD annual-average 1934/1933 gold ratio is **1.4296**; the official end-of-year revaluation is **1.6933** ($35/$20.67). The gap is *expected* (annual-average vs end-of-year, MeasuringWorth interpolated within 1934), not an error — worth a one-line callout in any figure narrative.
- **D14 BORDERLINE (finding M2).** The published DPR/EPR/research carry undefined internal jargon (Phase N, CD2, L01/P02/V03, `not_attempted_v1`, "from our IP"); the web EXPLAINER is clean. Scrub/gloss if the Publish tree backs a public website.
- **No ch5 viz/figure artifacts (finding M1).** No per-figure CSVs / SUBSERIES_METADATA / shiny export; figure repro is documented via `FIGURE_REPRO_ch05.md` (Figs 5.3–5.6 MATCH 4/4).

## 6. Forward risk — what breaks next

- **ONS PLLU discontinuation** (already threw a 502) is the top live-source risk — it blocks the UK legs of S502, S503 (and, through the numerator, the UK WPI-in-gold).
- **The No-Lazy-Splice discipline on S503/S504** is the chief *maintainer* hazard: a future growth-splice of p′ across the book/extension boundary would silently corrupt the decomposition; extensions must recompute the ratio from extended components.
- **Frequency convention** (annual-average vs year-end for the gold price) is unresolved in Appendix 5.2 and directly drives the S504 FDR-jump magnitude; document the chosen convention on any extension.
- **BLS PPI re-basing / renumber** affects only the growth-rate input, not the 1930=100 basis — low risk, but re-verify `WPU00000000`/`PPIACO` identity each refresh.
- **Companion-site fragility.** The salvaged `Appendix5_DATALRprices.xlsx` is the **sole canonical copy** of Shaikh's pre-computed WPI, p′, and pG columns (anwarshaikhecon.org DNS-dead) — the single blocking dependency for re-deriving the entire chapter.

## Series index

| SID | Figure | Concept | Archetype | Key exposure |
|---|---|---|---|---|
| S501 | 5.3 | US+UK WPI 1790–1940 (pre-fiat baseline; = Fig 2.9) | A splice (published as direct slice of S502) | frozen window; WPI→PPI latent-but-never-reached |
| S502 | 5.4 | US+UK WPI 1790–2010 (the 1939/40 regime break; 58×/14×) | A splice | **BLS WPS→WPU**; ONS PLLU 502 |
| S503 | 5.5 | UK WPI-in-gold p′ + £-price-of-gold pG (eq. 5.9) | C formula | **WW2 UK gold interpolation (Shaikh's own)**; recompute-not-splice |
| S504 | 5.6 | US WPI-in-gold p′ + $-price-of-gold pG (eq. 5.9) | C formula | **1934 FDR + 1971 breaks**; recompute-not-splice; LBMA reform |

---

*Grounding discipline: all author-intent claims trace to `Inputs/Capitalism Data/.../Knowledge_Base/HDARP_v3.3_Campaign/` (book KB: Body_Text `ch05_exchange_money_price.md`, Equations `ch05_equations.md`, Figures `ch05/`), `Technical/research/S50#_research.json`, `Technical/docs/series/S50#_{DPR,EPR}.md`, `Technical/docs/chapters/CH5_RESEARCH_SUMMARY.md`, or `Technical/methodology_review/CH05_review.json`. Unlocated rationales are marked "author rationale not located in corpus." READ-ONLY pass — no registry/code/data/Inputs were modified.*
