# S213 — Methodological History Report (MHR)

**Series**: S213 — US Corporate / General Rate of Profit, 1947–2011 (Fig 2.11)
**Family**: Chapter-2 profit-rate family (S213 general rate; S214 average mfg; S215 incremental mfg)
**Authored**: 2026-06-30 · methodological-historian sub-agent (READ-ONLY except this file)
**Display name (registry)**: "US General Rate of Profit"
**Grounding convention**: every author-intent claim carries a citable path; where none exists this report says "author rationale not located in corpus."

---

## 1. What the series is

The real US **general (average) rate of profit** for the corporate sector, 1947–2011, plotted by Shaikh as **Figure 2.11** in Chapter 2 ("Turbulent Trends and Hidden Structures", §V "The General Rate of Profit").

Book definition (verbatim, book p.65; `Technical/research/S213_research.json` book_quotes[0], and KB `Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/Figures/ch02/ch02_fig_2.11.md`):

> "Figure 2.11 displays the path of the real US general rate of profit, defined here, in OECD terminology, as the aggregate net operating surplus divided by the net capital stock, both in constant dollars (appendix 6.7). We see that from 1947 to 1982, the US rate of profit falls by more than 45%, and then reverses course thereafter."

**Deeper-chapter cross-reference (where the full method lives).** Chapter 2 is descriptive only; the caption in the book's data-sources section (Appendix 2.1 region, book p.764; research book_quotes[1]) directs the reader onward: *"Figure 2.11 US Corporate Rate of Profit, 1947–2011. Discussed in chapter 16 in relation to figure 16.2."* The **full construction methodology is in Appendix 6.7** (the general-rate-of-profit computation), and the same underlying series feeds **Ch16 Fig 16.2** (research methodology_notes). So S213 is a Chapter-2 exhibit of an Appendix-6.7 construction.

---

## 2. Source lineage

**Formula (registry `formula`, DPR §4):** `r[t] = NOS_corporate[t] / K_net[t-1]` — i.e. r = NOS / K_net, both in constant dollars, per Appendix 6.7 (OECD definition). (The research JSON states the concept as `r = NOS / K_net`; the registry/DPR encode a one-year capital lag `K_net[t-1]`.)

| Component | Agency / table id | Coverage | Native units | Path |
|---|---|---|---|---|
| **Net Operating Surplus (Corporate)** — numerator | **BEA NIPA Table 1.14**, line 18 (registry `components`) / research: "NIPA T1.14 line 18" | 1947–2011 (book); 2012–2025 available | \$ (constant) | `Technical/research/S213_research.json` primary_source |
| **Net Stock of Private Nonresidential Fixed Assets (current-cost)** — denominator | **BEA Fixed-Asset Table 4.1** | 1925–2011 (denominator available from 1925) | \$ | research components[1] |

**Provenance / retrieval chain.** Book-period values (1947–2011) are reproduced from the **CD2 S026 replication of the Appendix-6.7 computation** (DPR §3–4: "Book values reproduced from CD2 S026, which itself replicates the Shaikh Appendix 6.7 computation"; registry `predecessor_artifacts.cd2_source_file = ch06/Appendix6_Table68II7.csv`). Live BEA components for any extension are mirrored via Robin BEA (`Table_1_14_Corporate_2012_2025.csv`, `Table_4.1_CurrentCost_Net_1925_2023.csv`; registry `predecessor_artifacts.hdarp_sources`) plus the 1993 DoC *Fixed Reproducible Tangible Wealth* tables (A1–A8, 1925–1989).

**Splice / recompute chain.** Classified `construction: formula` — **not** a directly observed rate. Per the Anu no-lazy-splice rule (research extension_candidates concern; `.claude/rules/anu-framework.md`), any extension must **recompute** `NOS/K_net` from extended BEA components, never growth-rate-splice a published rate. The registry ships only the book-period subseries **S213-A (1947–2011)**; the 2012→ extension is **DEFERRED** (line resolver pending — see §4).

Grounding for the source choice (BEA NIPA + Fixed Assets are the canonical constant-dollar NOS and net-capital-stock sources): `SalvagedInputs/methodology_library/D_data_methodology/WL-D-NIPA-001__BEA-NIPA.pdf` (BEA NIPA methodology) and `WL-D-FA-002__BEA-Fixed-Assets.pdf` (BEA Fixed-Asset net-stock methodology); Shaikh's own profit-rate theory in `A_shaikh_pre2016/WL-A-ProfitRate-003__Shaikh-profit-rate-FROP.html`.

---

## 3. Why these sources — author's perspective

- **The concept: general rate = NOS ÷ net capital stock, OECD terms.** Shaikh defines the aggregate rate as total net operating surplus over the total net stock of fixed capital (KB fig 2.11.md "General (Average) Rate of Profit"; book p.65). Choosing **NOS** (surplus net of the capital-consumption allowance) over gross profit and **net** capital stock is exactly the OECD standard-national-accounts definition — this is why the numerator is NIPA T1.14 NOS and the denominator is Fixed-Asset T4.1 *net* stock. Cited: book p.65 ("in OECD terminology"); Appendix 6.7 (full method, per research methodology_notes). Shaikh's broader rationale for the profit rate as the driver of accumulation: KB fig 2.11.md ("waves in growth … primarily driven by the rate of profit") and `WL-A-ProfitRate-003__Shaikh-profit-rate-FROP.html`.
- **Why the *general* (average) rate here, and why a *separate* incremental measure follows.** The KB text (fig 2.11.md "Distinction: General vs. Incremental Rate") records Shaikh's own caveat: the average rate blends "surviving vintages of all past investments (from 30 years ago to 1 year ago)" and so is "a useful guide to the health of capital as a whole" but "NOT a useful guide to future profitability of any investment under current consideration." That stated limitation is precisely what motivates S215's incremental measure — so S213's role is the long-run "health of capital" trend, deliberately distinct from the new-investment equalization story.
- **Why NIPA T1.14 + FA T4.1 specifically.** These are the only official US series that yield NOS and net fixed-capital stock on a consistent constant-dollar corporate basis; Appendix 6.7 fixes them at the 2011 vintage (see §4). Author rationale for the exact table choice is given at the concept level (OECD terminology, App 6.7) but the *line-level* recipe is inherited from CD2 S026, not re-derived from the book in the Ch2 corpus — noted honestly.

---

## 4. Methodological-change exposure

S213's formula `r = NOS/K_net` draws **both** numerator and denominator from BEA accounts that BEA re-states at comprehensive revisions — so a revision boundary moves numerator *and* denominator simultaneously. Cite `Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`:

- **2011-vintage freeze.** Appendix 6.7 fn.1 fixes all BEA data at the **2011 vintage** (NIPA timeline §"Why this matters"). This is the coherent baseline S213-A is built on.
- **2013 Comprehensive (14th).** Capitalized **R&D + entertainment/artistic originals** as new **Intellectual Property Products**; raised **fixed-asset / capital-stock levels** and restated NOS/CFC; **≈ +\$400B to GDP level**. → Post-2011 extension changes BOTH the S213 numerator (NOS) and denominator (K_net). NIPA timeline row 2013.
- **2018 Comprehensive (15th).** Incorporated 2012 benchmark I-O; **inserted a new monetary-interest sub-row in T7.11 → every subsequent line +1** (T7.11 shift). Line-number recipes (incl. the NOS line reference) break here; resolve by BEA `LineDescription` label, not line number (`NIPA_T711_FISIM_remap.md`).
- **2023 Comprehensive (16th).** Reference year → **2017**; harmonized NIPA + industry accounts. Constant-dollar levels re-based → not splice-compatible with a 2011-vintage constant-dollar series.

**Rule (NIPA timeline + DPR §7):** NEVER splice S213 across a comprehensive-revision boundary — recompute end-to-end on one vintage. I-O touch is indirect (2009/2013/2018/2023 NIPA revisions each incorporate a benchmark I-O; `IO_CHANGE_TIMELINE.md`) but S213 uses NIPA aggregates, not the industry I-O panel, so the SIC→NAICS break is not on its critical path.

---

## 5. Replication fidelity note

- **CD2 S026 is the canonical truth source** for the 1947–2011 book period (DPR §3–4; registry `cd2_source_file`). Ships as subseries **S213-A**, `status: book_period_validated`, `publish: true`.
- **Tolerance 0.005 absolute** (DPR §7 caveat 3: profit rates ~0.10–0.20, so relative tolerance is inappropriate near zero). Registry `validation.tolerance` carries 0.01 as the playbook default; the DPR's tighter 0.005 absolute is the series-specific fidelity bar. Reference anchors (registry `validation.reference_values`): 1947 = 0.141066, 1986 = 0.071994, 2024 = 0.062879.
- **Corporate-vs-business-sector OPEN QUESTION.** The caption says "Corporate" (T1.14) but Appendix 6.7 may use the broader nonfinancial-business aggregate (research open_questions; registry `adequacy.issues_outstanding`; CH02_review.json S213 note). **Resolution adopted as canonical: the CD2 S026 interpretation (strictly NIPA T1.14 corporate)** per DPR §7 caveat 1 — noted here candidly as an unresolved conceptual ambiguity, not a settled fact.
- **Line-mapping extension DEFERRED** (EPR `extension_status: deferred`; DPR §7 caveat 2): the 2012→ extension is not shipped because NIPA T1.14 line numbers shift across vintages (Phase-9 specialist work). No fabrication — the NaN/absence propagates rather than being filled (EPR §4).

---

## 6. Forward risk

- The **next NIPA comprehensive revision** will again re-state NOS (numerator) and the net-capital-stock levels (denominator) and may shift line numbers again — any future extension must be recomputed end-to-end on the then-current single vintage, and the T7.11-style line-resolver kept label-based.
- Resolving the **corporate-vs-business-sector** ambiguity could shift the whole level of the series; until Appendix 6.7 is read line-by-line into the corpus, the CD2-S026 (strict T1.14) reading remains an assumption, not a verified match to Shaikh's aggregate.
- Extension remains blocked on the deferred **T1.14/T4.1 line resolver**; risk is silent mis-mapping across the 2013/2018/2023 boundaries if that work is done without honoring the timeline.
