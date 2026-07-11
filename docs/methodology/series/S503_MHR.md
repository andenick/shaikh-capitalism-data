# S503 — UK WPI in Gold and UK Gold Price, 1790–2009 — Methodological History Report (MHR)

**Group:** ch5 (Exchange, Money, and Price) · **Construction:** formula (p = p′·pG, eq. 5.9) · **Status:** book_period_validated
**Figure:** 5.5 · **Predecessor:** CD/CD2 S024 · **Publish:** true · **Book period:** 1790–2009 (data 1780–2010) · **Extension:** not_attempted_v1
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S503_research.json`), the DPR/EPR (`Technical/docs/series/S503_{DPR,EPR}.md`),
> the chapter summary (`Technical/docs/chapters/CH5_RESEARCH_SUMMARY.md`), the book KB (Body_Text
> `ch05_exchange_money_price.md`, Figure `ch05/ch05_fig_5.5.md`, Equations `ch05_equations.md` eq. 5.9),
> the Ch5 review (`Technical/methodology_review/CH05_review.json`), and the Phase-0 timelines
> (`Technical/docs/methodology/_timelines/{NIPA,IO}_CHANGE_TIMELINE.md`). Where a rationale is not present
> in the corpus it is marked **"author rationale not located in corpus."**

---

## 1. What the series is

S503 is the **empirical implementation of Marx's price-level decomposition (equation 5.9, `p = p′ · pG`) for
the United Kingdom**, plotted as **Figure 5.5** ("UK Wholesale Price Indexes in Gold Ounces and Pound Sterling
Price of Gold, 1790–2009", 1930 = 100, log scale 10–100,000; KB `Figures/ch05/ch05_fig_5.5.md`). It carries two
co-plotted lines (`S503_DPR.md` §1):
- **p′_UK** — the UK WPI expressed **in ounces of gold** (the "golden price" of the average commodity), 1930=100;
- **pG_UK** — the **£ price of gold** itself, 1930=100.

Together they reconstruct the UK price level: `UKWPI = p′_UK · pG_UK / 100`. Shaikh's stated purpose (book
p. 198, `S503_research.json` book_quotes[0–1], role=definition/method, verbatim_check=true) is to "decompose the
UK price index from 1790 to 2008 into the two basic components suggested by Marx's theory": the relative price
of commodities with respect to gold (p′) and the £ price of gold (pG). His empirical claim: the movements of p′
over 1790–2009 are "**modest** enough to be consistent with the hypothesis that the long-run price of commodities
relative to gold is driven by slowly changing structural factors" — *despite* the golden price reflecting "major
shocks due to the Long Depression of the 1870s, World War I, the Great Depression of the 1930s, World War II, the
Great Stagflation of the 1970s, and the sharp run-up in gold prices prior to the current crisis." The KB flags
the **1931 break** (Britain toppled off the gold standard) as the point where pG's trend detaches
(`ch05_fig_5.5.md`). ~442 chopped rows over 1790–2010. Ch16 Fig 16.1 and Ch17 Fig 17.1 re-use this decomposition
as de-trended/HP-smoothed "golden waves" (`CH5_RESEARCH_SUMMARY.md` cross-refs).

## 2. Source lineage — the formula and its inputs

S503 is a **formula series**: both p′ and pG are **pre-computed by Shaikh in the DATALRprices workbook on the
1930=100 base**, and RSCD reads them directly (`S503_DPR.md` §3–4). The inputs behind Shaikh's columns, per
Appendix 5.2 (book p. 788, `S503_research.json` book_quotes[2–3], verbatim_check=true):

| Component (column) | Coverage | Source / id | Operation |
|---|---|---|---|
| **UKWPI** (numerator of p′) | 1790–2010 | S502 leg B — **Jastram (1977) Table 2** + NBER `m04053` (1939–45) + ONS `PLLU` (1977–2010), 1930=100 | shared with S502-B |
| **UK gold price £/oz** (= pG_UK) | 1780–1785 | **Jastram (1977)** | native |
| | 1786–1949 | **MeasuringWorth** (Officer & Williamson, "The Price of Gold, 1257–2010"), quoted **in £** | native |
| | 1950–2010 | MeasuringWorth quotes UK gold **in US$** thereafter → converted to **£ via Officer's dollar-pound exchange series** (same site) | FX conversion |
| **p′_UK** (`UKPPIGold`) | 1790–2010 | **computed** `UKWPI / pG_UK`, rebased 1930=100 by Shaikh | ratio |
| **pG_UK** (`UKGoldpriceindex`) | 1790–2010 | UK £-gold-price rebased 1930=100 by Shaikh | reindex |

Retrieval: columns `UKPPIGold` and `UKGoldpriceindex` from `Appendix5_DATALRprices.xlsx` (`S503_DPR.md` §3).
MeasuringWorth is cited per its scholarly-use license; the £/$ conversion for 1950+ is Officer's dollar-pound
series (`S503_research.json` primary_source, methodology_notes[2]).

## 3. Why these sources — author's perspective

**Why the gold decomposition at all (the analytical heart of the chapter):** Shaikh's theory of the price level
(book pp. 194–195, `ch05_exchange_money_price.md` lines 1322–1389) says the long-run price level is "the product
of **two fairly independent factors**: (1) the relative price of these commodities vis-à-vis gold determined by
structural factors and competition; and (2) the money price of gold determined by monetary and macroeconomic
factors." The first "moment" (p′) is regulated by the *same competitive profit-rate-equalization apparatus* that
governs prices of production (Part II of the book, Sraffa 1960); the second (pG) is fixed by the *monetary
regime* — pegged under convertible tokens, floating under inconvertible ones. Equation 5.9 (`p = p′ · pG`,
`ch05_equations.md`) is therefore not an accounting identity dressed up — it is the *testable structure* of the
classical/Marxian theory, and it stands directly **against the Quantity Theory** (the price level is set by
p′·pG, not by M/XR·v). Fig 5.5 is the test: if the theory is right, p′ should be modest and slow-moving while
all the dramatic post-1931/1939 inflation should live in pG. That is exactly what the UK data show — which is
*why* Shaikh builds the ratio rather than just plotting the raw WPI.

**Why these specific long-run gold/price sources over alternatives:**
- **Jastram + MeasuringWorth are the two canonical multi-century series that were *built to be divided*.**
  Jastram's *Golden Constant* pairs a WPI and a gold-price series on the same 1930=100 basis; MeasuringWorth
  (Officer & Williamson) is the standard scholarly synthesis that *continues the gold price forward* to 2010 and
  supplies the dollar-pound FX needed for the post-1949 currency-quote switch. No single official feed spans
  1780–2010 for a national gold price, so a scholarly synthesis is the only option — the same "port an
  established synthesis" logic Shaikh uses for Maddison elsewhere.
- **Rejected/absent alternatives:** an explicit statement of *why Jastram over* his own *Silver: The Restless
  Metal* or modern best-vintage gold histories is **author rationale not located in corpus**. Note the CD2
  predecessor **mis-attributed the UK gold-price extension to "BLS PPI"** — this is a *documentation error*, not
  a Shaikh alternative; Appendix 5.2 is explicit that the UK gold price is MeasuringWorth + Officer FX, and RSCD
  corrected the attribution in Phase 3 and ratified it in Phase 4 (`S503_research.json` methodology_notes[3],
  `S503_EPR.md` §7, `CH5_RESEARCH_SUMMARY.md` S503 entry).

## 4. Methodological-change exposure

- **NIPA / IO timelines DO NOT apply.** S503 is built from **Jastram + MeasuringWorth gold + ONS/NBER price
  series — none of it is NIPA or benchmark I-O data.** The events in `NIPA_CHANGE_TIMELINE.md` and
  `IO_CHANGE_TIMELINE.md` **do not touch this series.** Stated explicitly per the task contract.
- **BLS/ONS WPI→PPI rename rides in through the numerator only.** p′_UK's numerator is UKWPI (S502-B), so it
  inherits the **ONS `PLLU` re-basing** exposure for any post-1976 recomputation; the denominator (gold) does
  not touch BLS/ONS at all.
- **The 1950 currency-quote transition** (MeasuringWorth switches UK gold from £ to US$) is a **structural
  splice point** bridged by Officer's dollar-pound FX; QA it against Bank of England historical FX
  (`S503_research.json` methodology_notes[2], `S503_DPR.md` §7.2).
- **WW2 UK gold-market suspension (1939–1945) — Shaikh's own interpolation.** The London gold market was
  suspended during the war, so there are no market prices for these years; **MeasuringWorth's Officer-Williamson
  series interpolates them, and Shaikh adopts the interpolation.** RSCD flags **all 1939–1945 observations**
  with `proxy_flag=ww2_gold_suspension_interpolated_measuringworth` at ingestion. This is disclosed
  **source-interpolation, not fabricated data** — the Ch5 review's D13 gate PASSES precisely because it is
  flagged as interpolation rather than presented as raw (`S503_DPR.md` §7.1, `S503_EPR.md` §5,
  `CH05_review.json` D13 basis; `CH5_RESEARCH_SUMMARY.md` S503 entry, 7 years flagged). Note the *same* wartime
  window is *also* NBER-m04053-filled on the UKWPI leg — two independent WW2 interpolations meet in this series.
- **MeasuringWorth gold compilation** is a stable, frozen historical dataset (values extended, not revised) —
  low methodological-change risk on the denominator.

## 5. Replication fidelity note

- **Truth basis:** RSCD reads truth columns `UKPPIGold`/`UKGoldpriceindex` directly; V03 MAE 0.0% at ±1.0%
  (`S503_DPR.md` §9; `CH05_review.json` D13 = 100). **Internal-consistency (eq. 5.9) check passes:** `UKWPI ≈
  UKPPIGold · UKGoldpriceindex / 100` to within 0.025% at sample years (1930: 100 ≈ 100·100/100; 2010: 5726.7 ≈
  30.8·18588.7/100 = 5725.3) — max relative % = 0.0 in the hand-check (`S503_DPR.md` §9,
  `CH05_review.json` hand_check eq_5_9 UK = 0.0).
- **Formula-series discipline (No Lazy Splices on Derived Quantities):** any post-2010 extension of p′ must
  **recompute the ratio from extended UKWPI and extended UK gold price**, never growth-splice p′ itself
  (`S503_DPR.md` §4, `S503_EPR.md` §1, §3).
- **Extension honestly deferred (`not_attempted_v1`):** requires BOTH an extended UKWPI (ONS PLLU — blocked by
  CDN 502) AND an extended UK £-gold price (LBMA Gold Price PM ÷ BoE `XUDLGBD` FX — no helper built yet); the
  loader publishes book period only with explicit per-component reasons (`S503_EPR.md` §2, §6). No proxies, no
  synthetic fill.
- **CD2 correction ratified:** UK gold-price extension = MeasuringWorth + Officer FX (not CD2's "BLS PPI");
  reproduces book values because it reads Shaikh's pre-computed columns (`S503_EPR.md` §7).

## 6. Forward risk

- **Formula-recompute discipline must hold.** The single biggest replication hazard is a future maintainer
  growth-splicing p′ across the book/extension boundary or across a base change — forbidden; recompute
  end-to-end from components (`S503_EPR.md` §1).
- **Two live-source dependencies for the deferred extension:** ONS `PLLU` (already 502; top risk) for the
  numerator, and LBMA Gold Price PM + BoE `XUDLGBD` FX for the denominator — the **LBMA March-2015 reform**
  (London Gold Fixing → LBMA Gold Price) is a documented structural splice point for the overlap-anchor
  (`S503_research.json` extension_candidates, `S503_EPR.md` §4).
- **Frequency convention open question:** Appendix 5.2 does not state annual-average vs year-end for the gold
  price; the working assumption is Officer/Williamson annual averages (`S503_research.json` open_questions,
  `CH5_RESEARCH_SUMMARY.md` open-question 7).
- **Companion-site fragility:** the salvaged `Appendix5_DATALRprices.xlsx` is the sole canonical copy of
  Shaikh's pre-computed p′/pG columns (anwarshaikhecon.org DNS-dead).
