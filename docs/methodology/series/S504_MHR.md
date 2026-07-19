# S504 — US WPI in Gold and US Gold Price, 1800–2009 — Methodological History Report (MHR)

**Group:** ch5 (Exchange, Money, and Price) · **Construction:** formula (p = p′·pG, eq. 5.9) · **Status:** book_period_validated
**Figure:** 5.6 · **Predecessor:** CD/CD2 S025 · **Publish:** true · **Book period:** 1800–2009 (data 1780–2010) · **Extension:** not_attempted_v1
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S504_research.json`), the DPR/EPR (`Technical/docs/series/S504_{DPR,EPR}.md`),
> the chapter summary (`Technical/docs/chapters/CH5_RESEARCH_SUMMARY.md`), the book KB (Body_Text
> `ch05_exchange_money_price.md`, Figure `ch05/ch05_fig_5.6.md`, Equations `ch05_equations.md` eq. 5.9),
> the Ch5 review (`Technical/methodology_review/CH05_review.json`), and the Phase-0 timelines
> (`Technical/docs/methodology/_timelines/{NIPA,IO}_CHANGE_TIMELINE.md`). Where a rationale is not present
> in the corpus it is marked **"author rationale not located in corpus."**

---

## 1. What the series is

S504 is the **US analogue of S503** — the empirical implementation of Marx's decomposition (equation 5.9,
`p = p′ · pG`) for the United States — plotted as **Figure 5.6** ("US Wholesale Price Indexes in Gold Ounces and
US Dollar Price of Gold, 1800–2009", 1930 = 100, log scale 10–10,000; KB `Figures/ch05/ch05_fig_5.6.md`). Two
co-plotted lines (`S504_DPR.md` §1):
- **p′_US** — US WPI expressed **in ounces of gold** (the golden price), 1930=100;
- **pG_US** — the **$ price of gold** per ounce, 1930=100.

Together: `USWPI = p′_US · pG_US / 100`. Shaikh's purpose (book p. 199, `S504_research.json` book_quotes[0],
role=definition, verbatim_check=true) is to examine "the same two variables for the United States from 1800 to
2009" and show that, despite the global shocks *plus* a run of US wars (War of 1812, the Civil War, Korea,
Vietnam, the two Gulf Wars), "the movements of p′ over the whole period from 1800 to 2008 are relatively
modest." The drama again lives in pG: the KB records pG_US "relatively stable until 1933," the **1934 jump**
when the US "effectively went off a national gold standard in 1933 (Jastram 1977, 51)" (book p. 199,
book_quotes[1]), the Bretton Woods fixed price 1944–1971, and the **sharp exponential rise after 1971** when
dollar convertibility was abandoned (`ch05_fig_5.6.md`, "rose almost 47-fold from 1933 to 2009"). ~422 chopped
rows over 1800–2010. Feeds Ch16 Fig 16.1 / Ch17 Fig 17.1 as "US golden waves."

## 2. Source lineage — the formula and its inputs

S504 is a **formula series**: p′ and pG are **pre-computed by Shaikh in DATALRprices on the 1930=100 base**;
RSCD reads them directly (`S504_DPR.md` §3–4). The inputs behind Shaikh's columns, per Appendix 5.2 (book
p. 788, `S504_research.json` book_quotes[2–3], verbatim_check=true):

| Component (column) | Coverage | Source / id | Operation |
|---|---|---|---|
| **USWPI** (numerator of p′) | 1800–2010 | S502 leg A — **Jastram (1977) Table 7** + BLS `WPS00000000` (1977–2010), 1930=100 | shared with S502-A |
| **US gold price $/oz** (= pG_US) | 1780–1785 | **estimated** from the UK Jastram gold price via the **1786 US/UK gold-price ratio** (≈ constant to 1800) | imputed |
| | 1786–1790 | **MeasuringWorth** — the **official** US price | native |
| | 1791–2010 | **MeasuringWorth** — the **market** price (London Fix / LBMA underlying) | native |
| **p′_US** (`USPPIGold`) | 1790–2010 | **computed** `USWPI / pG_US`, rebased 1930=100 by Shaikh | ratio |
| **pG_US** (`USGoldpriceindex`) | 1790–2010 | US $-gold-price rebased 1930=100 by Shaikh | reindex |

Retrieval: columns `USPPIGold` and `USGoldpriceindex` from `Appendix5_DATALRprices.xlsx` (`S504_DPR.md` §3).
MeasuringWorth is cited per scholarly-use license; the official→market regime for 1786–1790 is preserved as-is
(`S504_research.json` methodology_notes[2]).

## 3. Why these sources — author's perspective

**Why the gold decomposition (same analytical core as S503).** Shaikh's classical/Marxian theory (book
pp. 194–195, `ch05_exchange_money_price.md` lines 1322–1389; eq. 5.9 in `ch05_equations.md`) holds that the
long-run price level is the *product of two fairly independent factors* — the golden price of commodities p′
(regulated by competition and structural/technical conditions, the price-of-production apparatus of Part II) and
the money price of gold pG (fixed by the monetary regime). Decomposing the US WPI into p′·pG **tests** that
theory against the Quantity Theory: if the theory holds, p′ stays modest while pG carries the regime shocks. The
US case is the *sharpest possible test* because the US monetary history contains **two clean, datable regime
breaks** that should show up entirely in pG and not in p′:
- the **1934 FDR devaluation** — the Gold Reserve Act raised the official price from **$20.67 to $35.00/oz**
  (+69.4%) after the US "effectively went off a national gold standard in 1933" (book p. 199); and
- the **1971 Bretton Woods collapse**, after which the inconvertible dollar let pG float and trend exponentially.
Both are visible in Fig 5.6's pG line and *absent* from the modest p′ line — which is precisely *why* Shaikh
builds the ratio rather than reading the raw USWPI. The US also had "vast reserves of gold" out of WWI that let
it hold $35/oz for ~40 years (Harrod 1969; Galbraith 1975, cited book p. 199) — a natural-experiment span of a
fixed pG.

**Why these specific gold/price sources over alternatives:**
- **MeasuringWorth (Officer & Williamson, "The Price of Gold, 1257–2010")** is the canonical scholarly gold-price
  synthesis spanning the needed horizon, carrying the official-vs-market distinction for the early US price and
  continuing forward to 2010; Jastram supplies the pre-1786 anchor via the near-constant US/UK ratio. As with
  S503, no single official feed spans 1800–2010 for a US gold price, so a scholarly synthesis is the only
  faithful option.
- **Rejected/absent alternatives:** the CD2 predecessor listed **"COMEX/LBMA"** as the post-Jastram gold source;
  Appendix 5.2 specifies **MeasuringWorth** as the canonical citation (which itself uses the London Fix/LBMA as
  its underlying), so RSCD corrected the attribution in Phase 3 and ratified it in Phase 4 — MeasuringWorth
  canonical, LBMA underlying (`S504_research.json` methodology_notes[4], `S504_EPR.md` §7,
  `CH5_RESEARCH_SUMMARY.md` S504 entry). This is a *documentation correction*, not a Shaikh-rejected alternative;
  an explicit in-book rejection of other gold histories is **author rationale not located in corpus**.

## 4. Methodological-change exposure

- **NIPA / IO timelines DO NOT apply.** S504 is built from **Jastram + MeasuringWorth gold + BLS WPI — none of
  it is NIPA or benchmark I-O data.** The events in `NIPA_CHANGE_TIMELINE.md` and `IO_CHANGE_TIMELINE.md` **do
  not touch this series.** Stated explicitly per the task contract.
- **BLS WPI→PPI (WPS→WPU) rides in through the numerator only.** p′_US's numerator is USWPI (S502-A), which uses
  the frozen `WPS00000000` in the book and would extend via `WPU00000000`/FRED `PPIACO` — the denominator (gold)
  does not touch BLS at all.
- **1934 FDR devaluation is a real feature, not an artifact.** The data move `USGoldpriceindex` 118.2 (1933) →
  169.0 (1934), i.e. ×1.4302 ≈ the $20.67→$35.00 revaluation — reproduced faithfully (`S504_DPR.md` §7.1). A
  convention caveat: the RSCD **annual-average** jump ratio is **1.4296**, whereas the official **end-of-year**
  revaluation is **1.6933** ($35/$20.67); the gap is expected (annual-average vs end-of-year, MeasuringWorth
  interpolated within 1934), not an error (`CH5_RESEARCH_SUMMARY.md` §Phase 5–8, open question 3;
  `CH05_review.json` book_claim FDR_1934/1933 = 1.4296).
- **Pre-1786 US imputation.** 1780–1785 US gold is imputed from the UK Jastram price via the 1786 US/UK ratio;
  those years sit **outside** Fig 5.6's 1800 start, so the default S504 window does not plot them, but they are
  flagged `proxy_flag=pre1786_usgold_imputed_via_uk_ratio` if included (`S504_DPR.md` §7.2, `S504_EPR.md` §4).
- **MeasuringWorth gold** is a stable, frozen compilation — low methodological-change risk on the denominator.

## 5. Replication fidelity note

- **Truth basis:** RSCD reads truth columns `USPPIGold`/`USGoldpriceindex` directly; V03 MAE 0.0% at ±1.0%
  (`S504_DPR.md` §9; `CH05_review.json` D13 = 100). **Internal-consistency (eq. 5.9) check passes:** `USWPI ≈
  USPPIGold · USGoldpriceindex / 100` at 1930 (100·100/100 = 100) and 2010 (20.84·5950.65/100 = 1240.0 = USWPI)
  — max relative % = 0.0 in the hand-check (`S504_DPR.md` §9, `CH05_review.json` hand_check eq_5_9 US = 0.0).
- **Formula-series discipline (No Lazy Splices on Derived Quantities):** any post-2010 extension of p′ must
  **recompute the ratio from extended USWPI and extended US gold price**, never growth-splice p′ itself
  (`S504_DPR.md` §4, `S504_EPR.md` §1).
- **Extension honestly deferred (`not_attempted_v1: missing_lbma_helper`):** the numerator (USWPI via FRED
  `WPU00000000`) is already available through S502-C but not re-fetched for S504 v1; the **denominator (US $-gold
  price via LBMA Gold Price PM USD annual average) has no helper built**, so the ratio cannot be recomputed and
  the loader publishes book period only (`S504_EPR.md` §2). No proxies, no synthetic fill.
- **CD2 correction ratified:** post-Jastram gold = MeasuringWorth canonical (LBMA underlying), not CD2's raw
  "COMEX/LBMA"; reproduces book values because it reads Shaikh's pre-computed columns (`S504_EPR.md` §7).

## 6. Forward risk

- **Formula-recompute discipline must hold** — the chief replication hazard is a future growth-splice of p′
  across the book/extension boundary; recompute from components (`S504_EPR.md` §1).
- **LBMA March-2015 reform** (London Gold Fixing → LBMA Gold Price PM) is the documented structural splice point
  when the pG_US denominator is finally extended; same auction concept, `proxy: false` (`S504_DPR.md` §7.4,
  `S504_EPR.md` §3–4).
- **Frequency convention open question:** annual-average vs year-end for the US gold price is unresolved in
  Appendix 5.2 and directly drives the 1.4296-vs-1.6933 FDR-jump gap; document the chosen convention on any
  extension (`S504_research.json` open_questions, `CH5_RESEARCH_SUMMARY.md` open-question 3).
- **Caption-vs-coverage:** Fig 5.6 caption says 1800–2009 while DATALRprices covers 1786–2010; ensure the
  plotted slice matches the caption (`S504_research.json` open_questions).
- **Companion-site fragility:** the salvaged `Appendix5_DATALRprices.xlsx` is the sole canonical copy of
  Shaikh's pre-computed p′/pG columns (anwarshaikhecon.org DNS-dead).
