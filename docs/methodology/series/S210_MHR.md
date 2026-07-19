# S210 — US & UK Wholesale Price Indexes, 1780–2010 — Methodological History Report (MHR)

**Group:** ch2 (Turbulent Trends and Hidden Structures) · **Construction:** composite · **Status:** book_period_validated
**Figure:** 2.8 · **Predecessor:** CD/CD2 S010 (reproduced via CD2 S023) · **Publish:** true · **Book period:** 1780–2010 · **Extension (shipped):** US 2011–2026; UK 2011–2022
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S210_research.json`), the DPR/EPR (`Technical/docs/series/S210_{DPR,EPR}.md`),
> the registry (`Technical/series_registry.json` → `series.S210`), the book KB (Body_Text
> `ch02_turbulent_trends.md`, Figure `ch02_fig_2.8.md`), the predecessor dossier
> (`SalvagedInputs/methodology_decisions/CD2_research_md/S023.md`), the CH2 review
> (`Technical/methodology_review/CH02_review.json`), and the Phase-0 NIPA timeline
> (`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`). Where a rationale is not present in
> the corpus it is marked **"author rationale not located in corpus."**

---

## 1. What the series is

S210 is the annual **US and UK wholesale price indexes, 1780–2010**, both rebased to **1930 = 100** and plotted
on a **log scale** as **Figure 2.8** (KB `Figures/ch02/ch02_fig_2.8.md`, book p. 63) in the section "Prices,
Inflation, and the Golden Wave." Shaikh introduces it (book p. 62, `S210_research.json` book_quotes[0],
role=definition) as a way to put "inflation" in historical perspective — the figure "displays UK and US
wholesale price indexes, along with corresponding indexes of gold prices, over long intervals (**305 years for
the United Kingdom and 205 for the United States**)." The analytical point (KB `ch02_fig_2.8.md`, body text
lines 365–383): pre-1940 prices show **distinct long swings with no overall trend**, whereas only in the
postwar period do price levels "rise without end" — inflation is "a modern phenomenon." Two co-plotted country
lines, ~490 chopped rows.

The authoritative source line is **Appendix 2.1 "Data Sources and Methods" (book p. 764)**, transcribed
verbatim in `S210_research.json` book_quotes[1] (role=source, verbatim_check=true). Per the research JSON
methodology_notes and the registry `predecessor_artifacts.cd2_source_file`
(`ch05/Appendix5_DATALRprices.csv`), **Appendix 2.1 explicitly cross-references the same underlying data to
"Appendix 5.3 Data Tables for Chapter 5, figures 5.3, 5.4, 16.1"** — i.e. the WPI/gold family is *shared with
Chapter 5* (long waves / the general price level). The canonical deep dossier therefore lives in Ch5; Ch2's
Fig 2.8 is the "distant view" of the same construction. RSCD reproduces S210 from the Ch5 predecessor **CD2
S023** ("US and UK Wholesale Price Indexes, 1790–2010," Fig 5.4 — `CD2_research_md/S023.md`).

Final units: **Index, 1930 = 100** (log scale on figure), annual (`S210_DPR.md` §6).

## 2. Source lineage

Per Appendix 2.1 (book p. 764) and `S210_research.json` components[], the composite splices, per country:

**UK line (S210-B):**
| Segment | Coverage | Source / id | Native units | Operation |
|---|---|---|---|---|
| UK WPI historical | 1780–1938 | **Jastram (1977) Golden Constant, Table 2** (Table 2 spans 1560–1976) | Index 1930=100 | native basis |
| UK WPI gap-fill | 1939–1945 | **NBER macrohistory `m04053.dat`** ("UK PPI, All commodities", monthly) | growth rate | missing Jastram years filled using implicit annual growth rates of m04053 |
| UK WPI historical | 1946–1976 | Jastram (1977) Table 2 | Index 1930=100 | native basis |
| UK PPI extension | 1977–2010 | **ONS `PLLU`** ("Price Index of UK Output of Mfg Goods", statbase) | growth rate | extended via implicit growth rates of PLLU |

**US line (S210-A):**
| Segment | Coverage | Source / id | Native units | Operation |
|---|---|---|---|---|
| US WPI backfill | 1706/1780–1799 | **MeasuringWorth US CPI** (see Fig 2.5 sources) rescaled by the **1800 ratio of WPI/CPI** | Index 1930=100 | interpolated (CPI carries the pre-1800 movement; rescaled to WPI basis at 1800) |
| US WPI historical | 1800–1976 | **Jastram (1977) Golden Constant, Table 7** (pp. 145–146) | Index 1930=100 | native basis |
| US PPI extension | 1977–2010 | **BLS `WPS00000000`** (PPI All Commodities) | growth rate | extended via implicit growth rates of WPS |

Both country lines are on Jastram's **1930 = 100** basis throughout; the interpolation and both forward
extensions are **growth-rate splices** onto that basis, not level substitutions. Gold-price companions (used
for the Fig 2.8 gold overlays and, downstream, for S212) come from **MeasuringWorth** (Officer & Williamson,
"The Price of Gold, 1257–2010"); for **1780–1785 US** the gold price is estimated using the **1786 US/UK gold
ratio** (essentially constant to 1800). Grounding for the data houses is in the methodology library:
NBER macrohistory `SalvagedInputs/methodology_library/D_data_methodology/WL-D-NBERMH-001..004`, Census HSUS
`WL-D-HSUS-001..004`, Jordà-Schularick-Taylor `WL-D-JST-001..004`, and BLS `WL-D-BLS-*`. (The Jastram 1977
volume itself is referenced from HathiTrust `Record/000404889`, not held in the salvaged corpus.)

## 3. Why these sources — author's perspective

Shaikh's concept is **long-wave price behavior under different monetary regimes**, and the demonstration needs
the longest possible price record. That drives every source choice:

- **Why Jastram (1977) *The Golden Constant*.** Jastram's Tables 2 (UK) and 7 (US) are multi-century wholesale
  price indexes already anchored to a common **1930 = 100** basis and constructed *alongside* a matching gold
  series — exactly the two ingredients Shaikh needs to later divide price by gold (Fig 2.10 / S212). Its UK
  reach (from 1560) is what makes the "305 years" claim (book p. 62) possible. The choice is implicit in the
  concept; an explicit statement of *why Jastram over alternatives* (e.g. HSUS, NBER-only, or JST macrohistory)
  is **author rationale not located in corpus** — the salvaged methodology library holds the alternative data
  houses (HSUS, JST, NBER) but no Shaikh text rejecting them.
- **Why add the UK at all.** Shaikh's stated meta-rationale (book p. 56) is that the US "is the preeminent
  advanced country and … generally has the best available data" — yet here he *deliberately adds the UK* because
  the UK price record reaches ~125 years further back, and the long-wave/no-trend pattern is far more convincing
  over three centuries than over two. The paired US/UK lines also set up the gold transformation in §2.10 where a
  *common international standard* is needed across two currencies.
- **Why the specific extensions (BLS WPS, ONS PLLU).** These are the direct national successors to the historical
  wholesale-price concept, spliced by growth rate so Jastram's level basis is preserved. This is a fidelity
  choice (continue the same concept forward), not a proxy.

## 4. Methodological-change exposure

- **BLS WPI → PPI rename/renumber (the WPS→WPU issue).** BLS renamed the *Wholesale Price Index* to the
  *Producer Price Index* (1978) and re-based/renumbered its aggregates. Shaikh's cited US extender
  **`WPS00000000` is a legacy code that BLS froze (last obs ~1974 in the modern feed)**; its live successor is
  **`WPU00000000`** (FRED `PPIACO`). RSCD therefore extends the US line post-1974 with **WPU00000000** — a
  **direct BLS successor under the same PPI program, NOT a proxy** (`S210_EPR.md` §3, `S210_DPR.md` §4 step 2,
  `CH02_review.json` chapter rollup). PPI re-basing (1982 = 100 native) is handled by growth-rate splice, so the
  1930 = 100 basis is untouched.
- **ONS UK price-index revisions.** The UK extender `PLLU` is subject to ONS re-basing/relabelling; the registry
  flags it as still published but requires re-verification of successor identity (`series_registry.json`
  adequacy.issues_outstanding; `S210_research.json` extension_candidates).
- **NIPA / IO timelines DO NOT apply.** S210 is built entirely from **BLS/ONS price indexes and Jastram's
  historical tables — none of it is NIPA or benchmark I-O data.** The BEA comprehensive-revision events cataloged
  in `NIPA_CHANGE_TIMELINE.md` (1999–2023, incl. the T7.11 line-shifts) **do not touch this series**; the
  relevant "vintage" event is the BLS WPI→PPI rename, not any NIPA revision. Stated explicitly per the task
  contract.
- **Gold-price source.** MeasuringWorth (Officer & Williamson) is a **stable, frozen historical compilation**
  ("The Price of Gold, 1257–2010"); it is periodically extended but historical values are not revised, so it is
  low methodological-change risk.

## 5. Replication fidelity note

- **Truth basis:** RSCD reproduces the book-period values from **CD2 S023** (Fig 5.4 counterpart —
  `CD2_research_md/S023.md`), which itself replicates Jastram + BLS/ONS extensions; `S210_DPR.md` §3 records
  "salvaged via CD2 S023." Registry `reference_values` spot-checks: 1780 = 115.048, 1903 = 69.1
  (`series_registry.json` validation), matching CD2 S023's 1780 = 115.0485.
- **WPU-substitutes-frozen-WPS:** US extension uses **FRED WPU00000000/PPIACO** as the direct successor to the
  frozen WPS00000000 (not a proxy) — Shaikh's own growth-rate splice method is preserved (`S210_EPR.md` §3).
- **UK ONS extension SHIPPED (502 deferral resolved):** the shipped chopped extends the **UK line to 2022**
  via the **ONS `PLLU`** growth-rate splice (`S210-B` source_id `JASTRAM_1977_T2_PLUS_ONS_PLLU`), and the US
  line to **2026** via the BLS PPI splice (`S210-A` source_id `JASTRAM_1977_T7_PLUS_BLS_PPI_EXT`). The earlier
  transient-502 deferral no longer describes what ships (`S210_DPR.md` §3–§5, §7). The UK line stops at 2022
  only because that is ONS PLLU's last available annual observation — a data-availability boundary, not a
  deferral. (Note: the L01_S210 / P02_S210 code still reflect the older US-only-via-FRED path; that
  code-vs-chopped divergence is flagged for the code owner.)
- **No-synthetic disclosure:** where the extension API returns NaN, the NaN propagates; no placeholder values
  (`S210_EPR.md` §4).

## 6. Forward risk

- **BLS PPI re-basing / renumber:** any future PPI reference-year change or aggregate renumber affects only the
  growth-rate splice input, not the 1930 = 100 basis — low risk, but re-verify `WPU00000000`/`PPIACO` identity
  each refresh.
- **ONS series discontinuation:** `PLLU` is the highest-risk extender (has thrown a transient 502 before);
  it is currently spliced through 2022 in the shipped chopped — re-verify it is the unchanged successor on each
  refresh and extend the UK line as new ONS PLLU annual observations publish.
- **Gold-source updates:** MeasuringWorth may extend but rarely revises history; verify the through-year on
  refresh (`S212_research.json` open_questions).
- **Jastram base is frozen:** the historical (pre-1977) segment is fixed forever; no forward risk there.
