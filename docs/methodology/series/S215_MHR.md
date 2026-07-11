# S215 — Methodological History Report (MHR)

**Series**: S215 — Incremental Rates of Profit, US Manufacturing (Fig 2.13)
**Family**: Chapter-2 profit-rate family (S213 general rate; S214 average mfg; S215 incremental mfg)
**Authored**: 2026-06-30 · methodological-historian sub-agent (READ-ONLY except this file)
**Display name (registry)**: "Incremental Rates of Profit in US Manufacturing"
**Grounding convention**: every author-intent claim carries a citable path; where none exists this report says "author rationale not located in corpus."

---

## 1. What the series is

The **incremental rate of profit** (rate of return on *new* investment) within US manufacturing, plotted by Shaikh as **Figure 2.13** (Chapter 2, §VI "Turbulent Arbitrage") over the book period **1960–1989**, with a heavy line for the manufacturing sector as a whole.

Book definition (verbatim, book p.66; `Technical/research/S215_research.json` book_quotes[0]; KB `Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/Figures/ch02/ch02_fig_2.13.md`):

> "But the picture changes substantially when we consider the profit rates on new investment, that is, the incremental rate of return on capital (figure 2.13). This is measured here as the change in gross profits divided by the gross investment in the previous year (Christodoulopoulos 1995, 138–140; Shaikh 1998b, 395)."

Same 15 manufacturing aggregates as Fig 2.12 (KB fig 2.13.md).

**Deeper-chapter cross-reference (where the full method lives).** Chapter 2 is descriptive; full methodology is in **Chapter 7 / Appendix 7.1** and **Christodoulopoulos (1995, 138–140) / Shaikh (1998b, 395)**. The data-sources caption (book p.764; research book_quotes[1]) points to *"Appendix 7.2 Data Tables for Chapter 7 (anwarshaikhecon.org)"*, *"Discussed in chapter 7 in relation to figure 7.14."*

---

## 2. Source lineage

**Formula (book footnote 6, p.68 — verbatim in KB `Equations/ch02_equations.md` Eq 2.1 and registry `formula`):** `r*[t] = PG[t] / IG[t-1]`, where **PG = profits gross of depreciation** and **IG = gross investment** (lagged one year). Registry/research render the numerator as the *change* in gross profits ΔPG (book p.66 "change in gross profits divided by the gross investment in the previous year"); KB fig 2.13.md gives "ΔPG/IG(-1)". The robust form replaces the naïve `r = ΔP/ΔK` (which needs a capital-stock estimate) — see §3.

| Component | Source (as author-constructed) | Coverage | Native units | Path |
|---|---|---|---|---|
| **Gross profits PG** (numerator) by sector | Christodoulopoulos 1995 / Appendix 7.2 (OECD+BEA industry data) | 1960–1989 | percent / rate | research primary_source; registry `components[0]` |
| **Gross investment IG, lagged 1 year** (denominator) by sector | same | 1959–1988 | \$ | research components[1] |

**What actually ships (splice/recompute chain).** As with S214, the book-period 1960–1989 source is **NOT in SalvagedInputs** (registry `book_period_reason`; DPR §4). Nothing synthesized. The chopped CSV ships **only S215-EXT (1988–2005)** from Shaikh's Appendix-7 companion file **`Appendix7_iropdataUSind.xlsx`** (industry-level incremental ROP; registry `extension.provenance`; salvaged at `SalvagedInputs/book_data/Appendix7_iropdataUSind.xlsx`). `splice_method = not_applicable_book_data_unavailable`; `combined_subseries = output_subseries` (no book-period subseries to splice with).

Grounding for the incremental-rate concept and the AMECO parallel: `SalvagedInputs/methodology_library/A_shaikh_pre2016/WL-A-ProfitRate-003__Shaikh-profit-rate-FROP.html` (Shaikh on the profit rate) and `WL-A-RealComp-004__Shaikh-real-competition.html` (turbulent equalization). Shaikh 1998b and Christodoulopoulos 1995 themselves are cited by the book but not confirmed present as standalone corpus files — the formula grounding rests on book fn6 (KB equations) rather than those primary papers.

---

## 3. Why these sources — author's perspective (the key rationale)

- **Why the incremental measure over the average — and why THIS formula.** This is the series' most interesting methodological choice, and it is fully grounded. Book footnote 6 (p.68), captured verbatim in `Equations/ch02_equations.md`, states the naïve incremental rate `r = ΔP/ΔK` "requires estimates of the capital stock, which are dependent on a whole chain of assumptions for which there is often little basis except convenience." Shaikh's robust alternative `r* = ΔPG/IG(-1)` is chosen precisely because **both PG and IG are invariant to (a) the Capital Consumption Adjustment (true vs book depreciation) and (b) any estimate of useful life or capital stock** (KB equations §Advantages; research methodology_notes). So the incremental rate is preferred for **robustness to capital-stock / depreciation assumptions** — it measures the return on *new* investment without ever needing a contestable capital-stock series.
- **Why the incremental rate matters conceptually.** It reveals **profit-rate equalization in its true form**: incremental rates "cross over … again and again … even from positive to negative — a far cry from the placid 'margins' … turbulent equalization … with recurrent overshooting and undershooting" (KB fig 2.13.md Key Insight; book p.68). Average rates (S214) stay distinct; incremental rates equalize turbulently — this is Shaikh's evidence for real competition and it feeds stock/bond-price and interest-rate analysis (KB fig 2.13.md Implications; ch.10). This directly answers Fig 2.11's stated caveat that the average rate is "NOT a useful guide to future profitability of any investment" (KB fig 2.11.md).
- **Why the AMECO parallel is noted (and only as a concept-similar successor).** Book fn6 itself observes that the EU DG-ECFIN **AMECO Marginal Efficiency of Capital (MEC)** "follow[s] essentially the same procedure by defining the MEC as the ratio of the change in gross **output** to the lagged value of past investment" (KB equations §Note; research extension_candidates). Same lagged-investment procedure, **gross OUTPUT instead of profits** → concept-similar, **not identical** — hence flagged as a proxy, not a drop-in (see §5).

---

## 4. Methodological-change exposure

Same manufacturing-panel / classification exposure as S214. Cite `Technical/docs/methodology/_timelines/IO_CHANGE_TIMELINE.md`:

- **SIC→NAICS hard break.** Last SIC benchmark 1992, first NAICS 1997; pre-1997 tables "should not be used as a time series"; SIC and NAICS industry orders not conformable (IO timeline §"The SIC→NAICS break"). A continuous 1960–1989→modern incremental-rate panel is not simply spliceable across 1992/1997.
- **1997 = last benchmark capital-flow table.** No benchmark asset-by-industry matrix after 1997 (IO timeline §"Capital-flow benchmark matrix"). NOTE: S215's *robustness advantage* partly insulates the numerator/denominator from capital-stock estimation — but the sectoral **gross investment IG** still rides on BEA industry investment data whose benchmark I-O basis breaks at 1992/1997.
- **OECD STAN ISIC↔NAICS concordance dependency.** OECD ISDB 1994 vintage discontinued; modern extension needs OECD STAN + ISIC Rev3→Rev4 + NAICS crosswalk (registry `extension.provenance.vintage_note`), deferred (scope decision). The AMECO MEC route is a *different* concept (output-based), not a concordance fix.
- BEA industry-account comprehensive revisions (2009/2013/2018/2023; NIPA timeline) re-state the underlying gross-profit and gross-investment industry data.

---

## 5. Replication fidelity note

- **F-02 (HIGH, CH02_review.json) honored candidly.** Registry `status = book_period_validated`, but the chopped CSV ships **ONLY S215-EXT (1988–2005)**; the **book Fig 2.13 period 1960–1989 is entirely ABSENT**. The `reference_values` (1988 = 0.296976, 1997 = 0.114768, 2005 = 0.329528) validate the **extension source, not the book figure**. Honestly disclosed in name/EPR (no fabrication); the status label **overstates coverage** for the book period. Book period is **PASS_DATA_UNAVAILABLE** (registry `book_period_status: data_unavailable`; EPR `extension_status: data_unavailable`).
- **AMECO MEC is a gross-OUTPUT PROXY, not identical** (registry `adequacy.issues_outstanding`; research open_questions; EPR §3). Per the Anu no-proxy rule, if AMECO MEC is ever used to extend S215 it must be flagged `proxy: true` with a Concept-Match Justification spelling out the output-vs-profits difference. As shipped, S215 is `proxy: false` because it ships Shaikh's own profit-based Appendix-7 file, not AMECO.
- **No proxy, no synthetic in the shipped series** (EPR §3–4); missing book-period data stays missing.

---

## 6. Forward risk

- **Recovery of the book 1960–1989 incremental panel is blocked** on the anwarshaikhecon.org **Appendix 7.2** data tables (2026 availability uncertain) or **guided digitization** of the 15-line Fig 2.13 spaghetti (compare the S703/S704 guided-WebPlotDigitizer backlog for the sibling Ch7 figures). Until then, the `book_period_validated` label / coverage mismatch persists.
- **AMECO-MEC temptation**: the concept-similar successor is easy to grab but measures Δgross-output/lagged-investment, not Δprofits/lagged-investment — using it silently would violate the no-proxy rule; it must be proxy-flagged and justified if adopted.
- **OECD STAN crosswalk drift** (ISIC Rev3→Rev4 + NAICS) plus the post-1997 capital-flow gap affect any modern extension; the incremental formula's invariance to capital-stock assumptions mitigates the denominator problem for the *rate concept* but not the industry-classification concordance.
