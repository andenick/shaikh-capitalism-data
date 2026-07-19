# S214 — Methodological History Report (MHR)

**Series**: S214 — Average Rates of Profit, US Manufacturing (Fig 2.12)
**Family**: Chapter-2 profit-rate family (S213 general rate; S214 average mfg; S215 incremental mfg)
**Authored**: 2026-06-30 · methodological-historian sub-agent (READ-ONLY except this file)
**Display name (registry)**: "Average Rates of Profit in US Manufacturing"
**Grounding convention**: every author-intent claim carries a citable path; where none exists this report says "author rationale not located in corpus."

---

## 1. What the series is

The sector-by-sector **average profit rates within US manufacturing**, plotted by Shaikh as **Figure 2.12** (Chapter 2, §VI "Turbulent Arbitrage") over the book period **1960–1989**, with a heavy line for the manufacturing sector as a whole.

Book definition (verbatim, book p.66; `Technical/research/S214_research.json` book_quotes[0]; KB `Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/Figures/ch02/ch02_fig_2.12.md`):

> "Figure 2.12 depicts the average profit rates of sectors within US manufacturing, with the heavy line representing that of the manufacturing sector as a whole (chapter 7 and appendix 7.1). We can see that turbulence is normal to profitability."

The figure plots **15 manufacturing aggregates** — `USMANAVG` (heavy line) + 14 sub-sectors (`USACHE, USAMAI, USAFOD, USAMNM, USAMIO, USATEX, USABMI, USAMEL, USAWOD, USAMEQ, USAMTR, USAPAP, USABMA, USAMOT`; KB fig 2.12.md; research primary_source).

**Deeper-chapter cross-reference (where the full method lives).** Chapter 2 is descriptive; the full methodology is in **Chapter 7 and Appendix 7.1** (and Christodoulopoulos 1995), with the book's data-sources caption (book p.764; research book_quotes[1]) pointing to *"Appendix 7.2 Data Tables for Chapter 7 (available online at anwarshaikhecon.org)"* and noting the figure is *"Discussed in chapter 7 in relation to figure 7.14."*

---

## 2. Source lineage

**Formula (registry `formula`, DPR §4):** `r_sector[t] = profit[t] / capital_stock[t]` — a per-sector average rate of profit, full definition in Appendix 7.1.

| Component | Source (as author-constructed) | Coverage | Native units | Path |
|---|---|---|---|---|
| **Sectoral profit** (numerator), 15 mfg aggregates | anwarshaikhecon.org **Appendix 7.2** data tables | 1960–1989 (book) | percent / rate | research primary_source; registry `components[0]` |
| **Sectoral capital stock** (denominator) | **OECD ISDB (1994 vintage)** industry data | 1960–1989 | \$ | registry `components[1]`; research vintage_note |

Underlying construction is Shaikh/Christodoulopoulos from **OECD + BEA industry-level data** (research primary_source.agency; methodology_notes: "Christodoulopoulos 1995, 138–140; Shaikh 1998b, 395"). Sector codes follow **OECD ISIC** convention (research open_questions).

**What actually ships (the splice/recompute chain).** The book-period 1960–1989 source (anwarshaikhecon.org App 7.2 + OECD ISDB 1994) is **NOT in SalvagedInputs** (registry `book_period_reason`; DPR §4.1). Per the Anu no-fabrication rule nothing is synthesized. The chopped CSV therefore ships **only the post-book extension subseries S214-EXT (1987–2005)** from Shaikh's Appendix-7 companion file **`Appendix7_ropdataUSind.xlsx`** (industry-level ROP; registry `extension.provenance`; salvaged at `SalvagedInputs/book_data/Appendix7_ropdataUSind.xlsx`). `splice_method = not_applicable_book_data_unavailable`; `combined_subseries = output_subseries` because there is no book-period subseries to splice with (registry `extension.note`). Same author, same `r = profit/capital` formula, same industry-mean concept; overlaps the original only at 1987–1989.

---

## 3. Why these sources — author's perspective

- **The concept: turbulence, not smooth equalization.** Shaikh's stated purpose (KB fig 2.12.md Main Observations; book p.66) is to show that *average* sector rates, though clustered, "often remain persistently different across sectors" — motivating **real competition** as the point of departure: "Real competition, not perfect competition, must therefore be the point of departure for the analysis of technical change ('choice of technique')" (KB fig 2.12.md). The average rate is deliberately the foil to the *incremental* rate of Fig 2.13 (S215), which by contrast "cross[es] over" repeatedly (KB fig 2.12.md "Contrast with Figure 2.13").
- **Why sector-level manufacturing panels from OECD/BEA industry data.** The cross-sector distribution of profit rates *is* the empirical object; that requires an industry panel, for which OECD ISDB (with BEA industry data) was the available 1960–1989 source underlying Christodoulopoulos (1995) and Appendix 7.1. Cited: book p.66 (ch.7 & app.7.1); research methodology_notes (Christodoulopoulos 1995, 138–140; Shaikh 1998b, 395).
- **Why the Appendix-7 companion file for the shipped segment.** With the 1960–1989 source unavailable, the author's *own* post-book Appendix-7 industry ROP file is the only verifiable same-author, same-formula continuation — chosen over any proxy (registry `extension.provenance.conceptual_continuity`; EPR §3 no-proxy disclosure). Author rationale for the *specific* OECD ISDB vintage vs alternatives is not elaborated in the Ch2 corpus beyond the Appendix-7.1 pointer — noted honestly.

---

## 4. Methodological-change exposure

S214 is a **manufacturing sector panel** tied to BEA benchmark I-O and the SIC→NAICS classification break, plus an OECD-STAN concordance dependency for any modern recovery. Cite `Technical/docs/methodology/_timelines/IO_CHANGE_TIMELINE.md` (and the NIPA timeline for the industry-account revisions):

- **SIC→NAICS hard break (the Ch9 wall, applies to Ch7 panels too).** Last SIC benchmark = **1992**; first NAICS benchmark = **1997**. BEA states pre-1997 historical benchmark tables *"should not be used as a time series"*; SIC-order and NAICS-order industries are not conformable (IO timeline §"The SIC→NAICS break"). A single continuous 1960–1989→modern manufacturing panel cannot simply be spliced across 1992/1997.
- **1997 = last benchmark capital-flow table.** The asset-by-industry (use-type × using-industry) capital-flow matrix ends at 1997; no benchmark capital-flow table exists for 2002+ (IO timeline §"Capital-flow benchmark matrix"). → Post-1998 **fixed-capital-by-industry (the S214 denominator) must be approximated** from detailed Fixed-Asset type×industry tables — a structural obstacle to extension.
- **OECD STAN ISIC↔NAICS concordance dependency.** Book sector codes (USACHE, USAMAI…) follow OECD **ISIC**; the OECD **ISDB 1994 vintage is discontinued**, so a modern extension requires OECD STAN with an **ISIC Rev3→Rev4 + NAICS crosswalk** (registry `adequacy.issues_outstanding`; `extension.provenance.vintage_note`; CH02_review.json touchpoints S214 concordance note). This crosswalk is the deferred long-term extension target (scope decision required).
- BEA industry-account revisions (2009/2013/2018/2023 incorporate 2002/2007/2012/2017 benchmark I-O; NIPA timeline) each re-state the industry data any recovery would rest on.

---

## 5. Replication fidelity note

- **F-02 (HIGH, CH02_review.json) honored candidly.** The registry `status = book_period_validated`, but the chopped CSV ships **ONLY S214-EXT (1987–2005)** — the **book Fig 2.12 period 1960–1989 is entirely ABSENT**. The `reference_values` (1987 = 0.165742, 1996 = 0.200915, 2005 = 0.213122) validate the **extension source, not the book figure**. This is honestly disclosed in the series name and EPR (no fabrication), but **the status label overstates coverage** for the book period. The hand-check verdict is `FLAG` (CH02_review.json hand_checks S214).
- **Book period is PASS_DATA_UNAVAILABLE.** 1960–1989 source (anwarshaikhecon.org App 7.2 / OECD ISDB 1994) is not in SalvagedInputs (registry `book_period_data_unavailable: true`; DPR §7; EPR `extension_status: data_unavailable`). Per Anu no-fabrication, nothing is synthesized; the gap is documented, not filled.
- **No proxy, no synthetic** (EPR §3–4). Where data is missing it stays missing (`.claude/rules/anu-framework.md` No-Synthetic rule). Tolerance: registry 0.01; DPR §7 expects MAE < 0.5% when pulled directly from the chopped table.

---

## 6. Forward risk

- **Recovery of the book 1960–1989 panel is blocked** on the anwarshaikhecon.org **Appendix 7.2** data tables (2026 availability uncertain) or **guided digitization** of Fig 2.12 (F-02 remediation path). Until then the status label / coverage mismatch persists.
- **OECD STAN crosswalk drift**: any modern extension inherits ISIC Rev3→Rev4 + NAICS concordance risk and the post-1997 capital-flow-table gap (denominator must be approximated) — high risk of silent concept drift if built without honoring `IO_CHANGE_TIMELINE.md`.
- If/when App 7.2 lands in SalvagedInputs, the loader must be regenerated and a genuine book-period **S214-A** subseries added, at which point the `book_period_validated` label finally becomes accurate.
