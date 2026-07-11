# S501 — US and UK Wholesale Price Indexes, 1790–1940 — Methodological History Report (MHR)

**Group:** ch5 (Exchange, Money, and Price) · **Construction:** composite (published as a *direct* chronological slice of S502) · **Status:** book_period_validated
**Figure:** 5.3 · **Predecessor:** CD/CD2 S022 · **Publish:** true · **Book period:** 1790–1940 · **Extension:** none (frozen window)
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S501_research.json`), the DPR/EPR (`Technical/docs/series/S501_{DPR,EPR}.md`),
> the chapter summary (`Technical/docs/chapters/CH5_RESEARCH_SUMMARY.md`), the book KB (Body_Text
> `ch05_exchange_money_price.md`, Figure `ch05/ch05_fig_5.3.md`, Equations `ch05_equations.md`), the
> Ch5 review (`Technical/methodology_review/CH05_review.json`), and the Phase-0 timelines
> (`Technical/docs/methodology/_timelines/{NIPA,IO}_CHANGE_TIMELINE.md`). Where a rationale is not present
> in the corpus it is marked **"author rationale not located in corpus."**

---

## 1. What the series is

S501 is the annual **US and UK wholesale price indexes, 1790–1940**, both on Jastram's **1930 = 100** basis,
plotted on a **log scale** (50–300) as **Figure 5.3** (KB `Figures/ch05/ch05_fig_5.3.md`). Shaikh introduces
it at the head of the empirical section "Classical Theories of Money and the National Price Level" (book p. 188,
KB `ch05_exchange_money_price.md` lines 1026–1034; `S501_research.json` book_quotes[0], role=definition,
verbatim_check=true): the figure "displays the wholesale price indexes of the two leading countries of the
capitalist world (United States and United Kingdom) from 1790 to 1940 **as previously displayed in chapter 2,
figure 2.9**." Three things are "notable": the similarity of the two country lines, the presence of the long
cycles from which long-wave theory derives (van Duijn 1983), and "the striking fact that there is **no long-run
trend** in these price indexes for the whole 150-year interval." Shaikh clinches the point with Jastram's own
observation (book p. 188, book_quotes[1]) that in the UK "the purchasing power of gold 'in the middle of the
twentieth century was remarkably the same as in the midst of the seventeenth century.'" ~302 chopped rows
(151 US + 151 UK).

S501 is **explicitly a re-presentation of Ch2 Figure 2.9 (RSCD series S211)** and a **chronological subset of
S502** (Fig 5.4). Its purpose is the *pre-fiat baseline*: it isolates the 1790–1940 metallic-money epoch to
show that, before the 1939/40 break documented in S502, national price levels fluctuated without secular trend.
Final units: **Index, 1930 = 100**, annual (`S501_DPR.md` §6).

## 2. Source lineage

S501 carries **no independent source of its own** — it is exactly the 1790–1940 window of S502's two country
columns, read from the same workbook (`S501_DPR.md` §4, single-loader policy; `S501_EPR.md` §2–3). The
underlying composite construction (per `S501_research.json` components[] and Appendix 5.2, book pp. 788–789)
is, per country:

**US line (S501-A), 1790–1940:**
| Segment | Coverage | Source / id | Native units | Operation |
|---|---|---|---|---|
| US WPI backfill | 1790–1799 | **US CPI** (Fig 2.5 sources) rescaled by the **1800 WPI/CPI ratio** | Index 1930=100 | interpolated (CPI carries pre-1800 movement, rescaled to WPI basis at 1800) |
| US WPI historical | 1800–1940 | **Jastram (1977) *The Golden Constant*, Table 7** (pp. 145–146; Table 7 spans 1800–1976) | Index 1930=100 | native basis (truncated at 1940 here) |

**UK line (S501-B), 1790–1940:**
| Segment | Coverage | Source / id | Native units | Operation |
|---|---|---|---|---|
| UK WPI historical | 1790–1938 | **Jastram (1977) Table 2** (Table 2 spans 1560–1976) | Index 1930=100 | native basis |
| UK WPI gap-fill | 1939–1940 | **NBER macrohistory `m04053.dat`** ("UK PPI, All commodities", monthly) | growth rate | Jastram's missing 1939–1945 filled via implicit annual growth rates of m04053; only 1939–1940 fall inside S501's window |

Retrieval is from the salvaged canonical workbook `SalvagedInputs/book_data/ShaikhChoppedTables/
Appendix5_DATALRprices.xlsx`, columns `USWPI` and `UKWPI` (`S501_DPR.md` §3). Per Phase 4 ratification
(`CH5_RESEARCH_SUMMARY.md` §Phase 5–8), anwarshaikhecon.org's DNS does not resolve; the local XLSX is
canonical and the Internet Archive snapshot 2024-03-11 is the web citation. NBER macrohistory grounding sits in
the methodology library (`SalvagedInputs/methodology_library/D_data_methodology/WL-D-NBERMH-001..004`); the
Jastram 1977 volume itself is referenced, not held in the salvaged corpus.

## 3. Why these sources — author's perspective

Shaikh's concept here is **the price level under a metallic-money regime, over the longest horizon that admits
a clean "no-trend" reading**. That dictates every choice:

- **Why Jastram (1977) *The Golden Constant*.** Jastram's Tables 2 (UK) and 7 (US) are multi-century wholesale
  price indexes already anchored to a common **1930 = 100** basis and — crucially for the rest of the chapter —
  built *alongside a matching gold-price series*. Jastram is the canonical gold/price history; his UK Table 2
  reaches back to 1560, which is what makes the "no long-run trend for the whole 150-year interval" claim
  credible. An explicit statement of *why Jastram over modern best-vintage compilations* (Officer/Williamson's
  full WPI, HSUS, Jordà-Schularick-Taylor) is **author rationale not located in corpus** — the chapter summary
  flags this deliberate-fidelity-vs-modern-data tension as an open question (`CH5_RESEARCH_SUMMARY.md`
  open-question 2), but no Shaikh text rejecting the alternatives exists in the corpus.
- **Why co-plot the UK with the US.** Shaikh's default is the US ("the preeminent advanced country … best
  available data," book p. 56), but for the price-level argument he *deliberately adds the UK* because the UK
  record reaches further back and the near-identical movement of two independent national price levels is far
  stronger evidence of a common structural regularity than one country alone. The paired lines also set up the
  gold decomposition of Figs 5.5/5.6 (S503/S504), which needs a common international standard across two
  currencies.
- **Why window at 1940.** The truncation *is* the analytical device: 1790–1940 is the metallic-money regime in
  which p' (the golden price of commodities, made explicit in S503/S504) and the pegged money-price of gold both
  hold, so the price level is trendless. Extending past 1939/40 (which S502 does) is a *different* regime and a
  *different* figure. This is the exact role S211 plays in Ch2.

## 4. Methodological-change exposure

- **NIPA / IO timelines DO NOT apply.** S501 is built entirely from **Jastram's historical WPI tables plus a
  US-CPI backfill and an NBER-macrohistory gap-fill — none of it is NIPA or benchmark I-O data.** The BEA
  comprehensive-revision events cataloged in `NIPA_CHANGE_TIMELINE.md` (1999–2023) and the SIC→NAICS benchmark
  wall in `IO_CHANGE_TIMELINE.md` **do not touch this series.** Stated explicitly per the task contract.
- **The one relevant "vintage" axis — BLS WPI→PPI (WPS→WPU) — never actually bites here.** Because S501 stops at
  **1940**, it lies entirely inside Jastram's frozen historical archive and **never reaches** the 1977-onward
  BLS/ONS extension segment where the WPI→PPI rename and WPS00000000→WPU00000000 renumber occur (contrast S502,
  which does reach it). So the concordance risk is present in the *parent* construction but does not affect
  S501's published window (mirrors S211, `CH02_methodology.json` S211 concordance_touch).
- **Frozen source.** Jastram (1977), the pre-1800 US-CPI rescale, and the 1939–1940 NBER m04053 fill are all
  fixed historical values; there is no live upstream inside the 1790–1940 window.

## 5. Replication fidelity note

- **Truth basis:** RSCD reads the truth columns `USWPI`/`UKWPI` directly from `Appendix5_DATALRprices.xlsx`;
  V03 compares the processed parquet to the same columns → MAE 0.0% at ±1.0% tolerance (`S501_DPR.md` §9;
  `CH05_review.json` hand_check, D13 = 100). CD2 S022 reference values (US 1790 = 74.40, 1850 = 66.6,
  1940 = 90.8) reproduce exactly (`S501_EPR.md` §7).
- **Two documented in-book interpolations (NOT proxies, NOT fabrication):** the 1790–1799 US values
  (`proxy_flag=pre1800_uswpi_via_uscpi`) and the 1939–1940 UK values
  (`proxy_flag=wartime_interpolated_NBER_m04053`) are Jastram/Shaikh-documented historical fills *inside* the
  book period, flagged at ingestion, not modern substitutions (`S501_DPR.md` §7, `S501_EPR.md` §4).
- **Single-loader identity:** S501 shares the workbook read with S502 and produces byte-identical values up to
  1940, enforced to prevent divergence (`S501_DPR.md` §7.3, `CH5_RESEARCH_SUMMARY.md` cross-refs).
- **No extension, no synthetic data** (`S501_EPR.md` §1, §5).

## 6. Forward risk

- **Essentially frozen.** As a windowed historical view with no live extender, the only thing that could move
  S501 is a *transcription/truth correction* to Jastram's tables or to Shaikh's DATALRprices workbook — mirrors
  S211's risk profile.
- **Companion-site fragility.** anwarshaikhecon.org (Appendix 5.3 / DATALRprices) is DNS-dead in 2026; the
  salvaged local XLSX is the sole canonical copy. Loss of that salvage would block re-derivation
  (`CH5_RESEARCH_SUMMARY.md` open-question 1).
- **If ever re-cut against modern price histories** (the open Jastram-vs-best-vintage decision), the pre-1900
  segments would shift; but that would be a *variant*, not an extension, and would break the S211/Fig-2.9
  identity.
