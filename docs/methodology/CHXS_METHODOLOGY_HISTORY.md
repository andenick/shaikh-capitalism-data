# CHXS — Methodological History of the Extra Series (XS group)

**Group**: XS (Extra Series) · **Suffix**: XS / CHXS · **Series**: 17
**Authored**: 2026-06-30 · authored *from Shaikh's perspective* — why each object was built the way it was.
**Read-only provenance**: every claim traces to a citable path; no invention.

**Grounding**: `Technical/methodology_review/CH_XS_review.json`; `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`;
`Technical/MIGRATION/crosswalk.csv`; `Technical/docs/methodology/NIPA_T711_FISIM_remap.md`;
`Technical/docs/methodology/_timelines/{NIPA,IO}_CHANGE_TIMELINE.md`; the per-series research JSONs / DPRs / EPRs;
`Technical/docs/external_studies/*_paper_summary.md` + `ES_PHASE_5_8_CLOSURE.md`. Per-series reports:
`Technical/docs/methodology/series/<SID>_MHR.md` (17 files).

The XS group is not a chapter of Shaikh's book but a **structural residue** of the replication: two families of objects
that do not plot as a headline figure yet are load-bearing for reproducibility. `crosswalk.csv` records their origin — the
nine appendix internals were migrated `AS001-AS009 -> XS001-XS009` (CD2 predecessors S206-S214) because RSCD's Phase-2
mapper found them *unmapped* (they feed the profit-rate series S601-S604 but link to no Ch6 figure directly), and the eight
external-study series were migrated `ES2001-ES2305 -> XS2001-XS2305`, replications of four Shaikh co-authored papers
published *after* the 2016 book. The two families share only the `xs_class` sectioning (`appendix` vs `external_study`) and
one virtue: **honest disclosure of the limit between what was reproduced bit-exact and what was transcribed or truncated.**

---

## Narrative 1 — The GPIM appendix chain (XS001-XS009)

### 1.1 What the chain is for

Shaikh's Chapter 6 ("Capital and Profit") ends by measuring the US corporate profit rate on *classical* accounting
principles, not NIPA conventions. Appendix 6.7 ("Empirical Methods and Sources", book pp.828-855) is the narrative; Appendix
6.5 ("Measurement of the Capital Stock", pp.807-821) gives the GPIM accumulation equations (6.5.21-6.5.23; the XS004 DPR also
cites "eq. 6.57"); and Appendix Table 6.8 — the published workbook staged at
`SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` — is the numeric ground truth the RSCD loaders
transcribe verbatim. **Appendix 6.7 footnote 1 (p.828) fixes every BEA input at the 2011 vintage.** That single sentence is
the pivot of Narrative 1's methodological-change story (§1.4).

The nine series are a directed pipeline (full data-flow diagram in `CH6_GPIM_SUMMARY.md`):

- **XS001 — GDP/GDI decomposition -> business-sector NOS.** NIPA T1.7.5/T1.10/T7.12. Aggregate domestic Net Operating
  Surplus is stripped of households (owner-occupied-housing imputed rent, T7.12 lines 133-140), NPISH, government, and
  government enterprises to leave the *business-sector* NOS that a classical profit numerator starts from.
- **XS002 — Wage Equivalent (WEQ2) + corp/noncorp split.** NIPA T1.13/T1.14/T6.2/T6.3/T6.7. Proprietors' income mixes labor
  and profit; Shaikh imputes a wage-equivalent `WEQ2 = (sigma*PropInc - ECprop)/(1+sigma)` using the corporate wage-profit
  ratio `sigma` (2009 = 4.76) so the noncorporate profit rate is measured on the same footing as the corporate one.
- **XS003 — imputed-interest (FISIM) adjustment + corrected sectoral profit rates.** NIPA T7.11 FISIM + T7.12, BEA FA T6.1.
  NIPA treats banks as selling implicitly-priced services, redistributing ~$747.6B of $841.9B imputed net interest (2009)
  into business surplus; XS003 reverses that redistribution (`BusImpIntAdj`) and reports `rbus/rcorp/rnoncorp`
  (2009 hand-check rbus=7.7%, rcorp=7.5%, rnoncorp=8.1%, Appendix Table 6.7.4 p.832).
- **XS004 — the preferred GPIM corporate capital stock (operational baseline).** BEA FA T6.1/T6.4/T6.7/T6.8 + NIPA CFC + the
  BEA-1993 depreciation archive + the IRS interwar adjustment. This is the denominator S601-S604 use. It combines *three*
  deliberate corrections, each isolated by one of the four variants below.
- **XS005-XS008 — the four-variant counterfactual design.** XS005 = pure BEA-2011 GPIM regenerator (init value 98.1 bill$ in
  1925; validates BEA's own net stock to ~99.6%); XS006 = swap in BEA-1993 finite-life depreciation (SCB Table A.13);
  XS007 = IRS book-value interwar anchor 1925-1947 (Census 1975 Series V115); XS008 = the interwar multiplier ratio itself
  (IRS index / BEA historical-cost index, 1925=1.0). Each isolates ONE methodological choice; XS004 is all three together.
- **XS009 — total capital stock KTCcorp = KGCcorp + INVcorp.** BEA FA T6.3 + IRS SOI Corporation Source Book inventories.
  The classical profit-rate denominator is *total advanced capital* (fixed + circulating), so inventories are added back.

### 1.2 The construction rationale — why NOS/GPIM, not BEA's published net stock

This is the heart of Narrative 1, and it answers the question a reviewer always asks: *BEA already publishes a corporate net
capital stock — why does Shaikh rebuild one?*

**On the numerator (XS001-XS003): he needs the classical profit concept.** Published NIPA operating surplus (a) mixes in
households, government, and government enterprises; (b) treats proprietors' labor as if it were entirely capital income;
and (c) absorbs the FISIM bank imputation that inflates business surplus by hundreds of billions. Each of XS001/XS002/XS003
undoes exactly one of those NIPA conventions to recover the surplus a classical economist would recognize. Crucially he
adjusts *NOS*, not net value added — the FISIM correction is only 1-2% of NVA but 7-10% of the profit rate, so where the
adjustment lands is not cosmetic.

**On the denominator (XS004-XS009): BEA's net stock embeds two assumptions he rejects.** First, BEA's post-1997 method uses
**infinite-life geometric depreciation** — assets are never fully scrapped — which "materially understates" the corporate
capital stock; Shaikh prefers the pre-1997 **BEA-1993 finite-life** rates (XS006). Second, BEA's cycle-invariant retirement
path mis-states the **interwar 1925-1947** capital stock across the Depression and WWII, so he re-anchors those years to
**IRS book values** (XS007/XS008). The Generalized Perpetual Inventory Method is what lets him do this: rather than accept
BEA's published levels, GPIM *recomputes* the stock (`KNCnew = IGC + (1-dcorpnew)*(pKN/pKN(-1))*KNCnew(-1)`) from investment
flows under *his* choice of initial value, depreciation rates, and interwar anchor. The four variants are therefore not rival
baselines — they are a **sensitivity design**: XS005 proves the GPIM machine reproduces BEA when fed BEA's own assumptions
(~99.6%), and XS006/XS007/XS008 each quantify the effect of swapping in one classical correction. XS004 is the sum. (The
subtlety that XS004's 1925 value is 77.77 rather than 98.1 is itself the interwar IRS pull-down at work — and it reproduces
Appendix Table 6.8.II.5 EXACT to 14 significant figures.)

Rejected alternatives Shaikh explicitly declines, per the MHRs: taking BEA's `NOS, private enterprises` line directly (still
carries OOH and government enterprises); the WEQ1 wage-equivalent (post-1990s officer salaries push the noncorporate rate
implausibly above the corporate one — 10.2% vs 7.5% in 2009); NIPA Table 5.8.5 inventories (by industry, not by legal form,
so useless for a *corporate* denominator); and — for the profit rate itself — adjusting net value added instead of surplus.

### 1.3 Source lineage in one view

NIPA current accounts (T1.7.5, T1.10, T1.13, T1.14, T6.2/6.3/6.7, T7.11, T7.12) supply the flows; the BEA Fixed Asset
Accounts (T6.1/T6.3/T6.4/T6.7/T6.8, 2011 vintage) supply the stock and investment; the **BEA 1993 SCB Table A.13** supplies
the finite-life depreciation/retirement rates (no longer in the live iTable — see §1.5); **IRS SOI** (Corporation Source Book
inventories) and **Census 1975 Historical Statistics Series V115** (IRS book values via Historical Statistics) supply the
inventory and interwar anchors. All of it is re-expressed against Shaikh's own Appendix 6.8 workbook, which the RSCD loaders
read as the source of truth.

### 1.4 Methodological-change exposure — the 2011-vintage freeze and its time-bombs

Because footnote 1 pins everything to the **2011 vintage**, every post-2011 BEA comprehensive revision is a latent break the
chain must never silently cross (`NIPA_CHANGE_TIMELINE.md`):

- **2013 (14th comprehensive update)** capitalized R&D and entertainment originals into a new Intellectual Property Products
  category (~+$400B GDP) and **raised Fixed-Asset / capital-stock levels** while changing NOS and CFC. This directly re-levels
  the XS001 NOS residual and every GPIM input in XS004-XS009. Shaikh's 2011 definition *excludes* IPP, so any extension must
  take an explicit stance (match the IPP-exclusive definition or build an IPP-inclusive parallel) — never splice.
- **2018 (15th)** inserted one new monetary-interest sub-row in **NIPA Table 7.11**, shifting every line >=28 by **+1**. This
  is the sharpest time-bomb in the group: XS003's FISIM recipe uses 2011-vintage lines `4,28,44,52,53,54,73,74,75,91`, which
  on a 2018+ vintage silently become `4,29,45,53,54,55,74,75,76,92`. RSCD defuses it with
  `_nipa_t711_line_resolver.py`, which resolves each of the ten lines by its BEA `LineDescription` **stub label** rather than
  by number (full mapping in `NIPA_T711_FISIM_remap.md`); the 2013 revision also restated T7.11 *magnitudes* without
  reordering rows, so values must not be spliced across it either.
- **2023 (16th)** moved the reference year to 2017. Same discipline: recompute on one coherent vintage.

The GPIM series carry **no** input-output or classification-concordance exposure (that belongs to Narrative 2's Sraffa
series); their entire risk surface is NIPA/BEA-FA vintage drift plus the T7.11 renumbering.

### 1.5 Replication fidelity — the honest limit

The RSCD build is **bit-exact to Appendix 6.8 but transcribed, not recomputed** (finding F-XS-05). The L01 loaders read
Shaikh's finished `KNCcorp/KGCcorp/KNHcorp` columns and the P02 processors are schema-only pass-throughs; XS003-XS009 declare
`construction: formula` yet carry `components: []` and no `formula` field. The GPIM equation and the FISIM recipe live in DPR
prose, the CH6 summary, and the `construction_steps` — and a genuine end-to-end recompute exists only in the **deferred v1.1
EPR extension recipe**. This is honest (the hand-checks confirm the transcription is perfect: XS004 EXACT to 14 sig figs,
XS007 resolving the thousands->billions unit question with `93341.5159 -> 93.3415`, XS001 V03 mae=0.0), but it means the
current artifact *reproduces Shaikh's spreadsheet*, not Shaikh's spreadsheet-from-primary-sources.

Two publication-blocking honesty defects ride on top (D14 = 85, BELOW_90_BLOCKS_EXTERNAL): the chopped artifacts still leak
the banned unit string `mixed_billions_usd_and_decimal_rates` on every XS003 row (F-XS-01/F-XS-07), and dimensionless/rate
subseries are mislabeled `billions_current_usd` — XS002-G `sigma`, XS005-C the GPIM/BEA ratio, XS006 the depreciation rate.
The registry `per_subseries` fix never propagated to the CSVs consumed by viz and public downloads.

### 1.6 Forward risk

The recompute bottleneck is the **BEA-1993 depreciation/retirement archive**: `dcorpnew`/`rho_corpnew` are not in the current
BEA iTable, and the only surviving source is Shaikh's posted `Appendix6_Table68II3.xlsx`, staged at
`SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/`. XS006 *is* the BEA-1993 variant, so recovering BEA 1993
Table A.13 (p.294) from the SCB-1993 archive is the single highest-value de-circularizing step for the whole chain.
Secondary risks: the IRS SOI net-capital-stock series was **discontinued after 2011**, breaking XS009's inventory ratio-fit
for any live extension (CH6 open-Q4 — re-estimate from the current IRS SOI Corporation Complete Report, flag a visualization
break, or substitute FRB Z.1 nonfinancial inventories); and every extension must be recomputed on a single coherent BEA
vintage, never spliced across 2013/2018/2023.

---

## Narrative 2 — The external-studies family (XS2001, XS2101, XS2201, XS2301-XS2305)

### 2.1 What the family is for

These eight series replicate the empirical content of **four Shaikh co-authored papers published after the 2016 book**, each
extending a specific book chapter. They are the replication's way of keeping the *living* Shaikh research programme inside the
same provenance discipline as the book (`crosswalk.csv`; `ES_PHASE_5_8_CLOSURE.md`). Three sub-stories run through them:
Sraffa-price empirics (XS2001/XS2101, extending Chs 6/9), the econophysics of income distribution (XS2201, extending Ch17),
and the US-China trade imbalance (XS2301-XS2305, extending Ch11).

- **XS2001 — Shaikh (2020), "An Empirically Sufficient Form for Sraffa Prices"** (Pasinetti festschrift). The panel of
  aggregate price/value ratios (Tables 1-2, p.10): two Sraffa models (circulating / fixed capital) x six BEA benchmark IO
  years x nine aggregates, all falling in [0.94, 1.08] — the **Sraffa Stochastic Effect**, the statistical near-identity of
  price and labor-value aggregates.
- **XS2101 — Shaikh, Coronado & Nassif-Pires (2020), EJEEP.** The **Curvature Index** `CI = 1 - SI` (SI = Bienenfeld-line
  length / actual price-curve length) across **295 IO matrices** (BEA benchmark 1977-2007 x eight nested NAICS
  aggregations); average CI 0.03-0.06, plus the Theil index of CI. The finding *undercuts Bródy's random-matrix hypothesis*
  that curvature should fall with matrix size.
- **XS2201 — Shaikh & Jacobo (2020), Review of Behavioral Economics** (extends Ch17). Fifteen annual fits (2002-2016) of a
  **two-class income distribution**: the bottom 97% is Boltzmann-exponential ("thermal"), the top 3% is Pareto
  ("superthermal"), with the labor/property break in the $100K-$200K AGI bin. Table 1 = 5 fitted parameters/year
  (`G'`, `<r>`, `<w>`, `f`, `alpha`); the paper's novel Section 4 derives them from a turbulent-arbitrage drift-diffusion SDE.
- **XS2301-XS2305 — Weber & Shaikh (2020), IRAE** (extends Ch11, Absolute Cost Theory). The five appendix figures of the
  US-China trade-imbalance paper: Fig 1 US-China bilateral goods balance vs World (Census FT900); Fig 2 China current account
  (IMF WEO, level + %GDP); Fig 3 China FX reserves ex-gold (World Bank WDI); Figs 4-5 RMB-misalignment scatter compilations
  under the extended-PPP and macro-balance approaches (literature compilation of four reviews).

### 2.2 Source lineage — each paper's own data

Unlike the GPIM chain, this family is sourced from the papers themselves. The two Sraffa series rest on the **BEA Benchmark
Input-Output accounts** (Use/Make -> A-matrix via the Industry Technology Assumption) plus **BLS** labor compensation for the
skill-adjusted labor vector; XS2001 spans the 71-order 1947-1972 (Ochoa/SIC) cross-sections and the 65-order 1998 (NAICS) Use
table, XS2101 the detailed 1977-2007 benchmarks. XS2201 rests on **IRS SOI Publication 1304** (Table 1.4 AGI bins + Table 1
totals). The Weber-Shaikh five draw on **Census FT900** (XS2301), **IMF WEO** subjects BCA/BCA_NGDPD (XS2302), **World Bank
WDI** `FI.RES.XGLD.CD` (XS2303), and a fixed **four-review literature compilation** — Cline-Williamson (2007), Dunaway-Li
(2005), Cheung-Chinn-Fujii (2010a), Cheung (2012) — for the misalignment scatters (XS2304/XS2305).

### 2.3 Why these measures, from Shaikh's perspective

Each paper chose a measure to make one argument, and the MHRs reconstruct that intent:

- **XS2001 (aggregate ratios, not 403-sector curves).** The Sraffa Stochastic Effect is an *aggregate* claim — that price and
  value aggregates coincide because of the statistical compensation of large numbers — so the right object is the nine
  aggregate ratios across benchmark years, *not* the disaggregated 403-sector price curves (those are a separate
  cross-sectional object, the paper's Figs 1-9, deferred to v1.1). Asking the aggregate question with disaggregated curves
  would be the wrong question.
- **XS2101 (Curvature Index vs the Bienenfeld line).** Shaikh needs a curvature measure that is *comparable across matrix
  orders from 15 to 425*; raw curvature or a second-eigenvalue ratio is not bounded or comparable, and the Bienenfeld linear
  approximation is precisely the endpoint-matching theoretical null the paper is testing against. He needs the full 295-matrix
  spread specifically to test Bródy's *fall-with-size* hypothesis, which a single detailed matrix cannot do.
- **XS2201 (MLE "income temperature", IRS binned data).** `<w>` is the inverse-slope MLE "temperature" of the bottom-97%
  exponential, *not* a raw sample mean — because the data are binned, and because the two-class model's whole point is the
  fitted thermal shape; `f` is the identity `1 - <w>/<r>`, not an independent top-share estimate. IRS SOI binned tabulations
  are preferred over survey micro-data (CPS/PSID) precisely because surveys top-code and thin the Pareto tail the paper needs.
- **XS2301-XS2305 (the estimate *range* is the argument).** This is the family's best source story. Weber & Shaikh's thesis
  is that the currency-manipulation explanation of the US-China imbalance *fails* — the misalignment literature reaches **no
  consensus even on the sign**, with estimates spanning **-36% to +50%** (extended PPP) and **-100% to +40%** (macro
  balance). So Figs 4-5 deliberately plot the *whole scatter of conflicting estimates* rather than any single authoritative
  number, and the paper's **note 17** lays down the rule the replication must honor: treat each estimate as a separate point,
  report ranges as min/max endpoints, never average into a consensus. The imbalance is then explained not by currency but by
  *real cost* differences — the headline (unfigured) statistic that US/China manufacturing unit labor costs stood at **7.8:1**
  (Golub et al. 2018), the Absolute Cost Theory mechanism from Ch11. Picking one misalignment estimate, or averaging them,
  would destroy the argument.

### 2.4 Methodological-change exposure

The Sraffa series sit on the **input-output timeline** (`IO_CHANGE_TIMELINE.md`), not the NIPA one. Their exposure is the
**SIC->NAICS wall** (last SIC benchmark 1992, first NAICS 1997; pre-1997 tables "should not be used as a time series") and
the fact that even within NAICS the industry order drifts at every benchmark (1997/2002/2007/2012/2017) — so any extension to
new benchmark years needs NAICS bridging and a per-vintage aggregation rebuild, and the **benchmark capital-flow table was
discontinued after 1997**, structurally blocking XS2001's fixed-capital (Table 2) model past 1998. XS2201 has *no* NIPA/IO
exposure but crosses the **TCJA-2017** and **CARES-2020** AGI-definition breaks, so any 2017+ re-fit must re-estimate, never
splice. The Weber-Shaikh five are Census/IMF/WDI series with **no** NIPA/IO vintage exposure; their analogues are Census
FT900 HS-code revisions, IMF WEO semi-annual vintage revisions (and its forecast tail — §2.5), WDI revisions, and the fact
that the misalignment literature froze around 2012 (the post-2014 IMF EBA methodology is a *distinct* object, not a
continuation).

### 2.5 Replication fidelity — self-consistency, forecast contamination, and honest truncation

All eight v1.0 builds are **verbatim transcriptions or live-API pulls validated by self-consistency** (V03 compares the melt
against the reconstructed CSV / figure anchors, MAE 0.0 for the transcribed series), *not* independent re-reads of the papers.
Three honesty notes are load-bearing:

1. **XS2302 forecast contamination (F-XS-02, HIGH).** The live IMF WEO pull dragged in **forecast years 2025-2031** (levels
   718.6 / 749.3 / 781.7) inside a series whose DPR, `display_name`, and subseries all say **1997-2024**; the registry
   `year_range` silently absorbed to `[1997, 2031]`, and a **2031 forecast is used as a `reference_value`**. Forecasts are
   presented as realized data with no projection flag. This is the one place the family presents a projection as fact, and it
   must be remediated (truncate to the realized window or carry an explicit forecast flag).
2. **XS2304/XS2305 honest 2-point truncation (`publish: false`).** The misalignment scatters were *not* chart-digitized (the
   the no-fabrication rule forbids reading ~30-35 unnamed dots off a figure). v1.0 ships only the **two named endpoints**
   each paper quotes in body text (XS2304: +50% Coudert-Couharde 2007, -36% Cheung 2012; XS2305: +40% Goldstein 2004, -100%
   Bayoumi-Gagnon-Saborowski 2015), flagged `publish: false` with the full scatter deferred to a v1.1 literature-extraction
   pass. Truncating honestly beats fabricating completely.
3. **Minor anchor caveats.** XS2301's registry `year_range=[2002,2018]` is stale after the 2026-06-11 loader rebuild to 2024
   (F-XS-04), and its old `CENSUS_FT900_EXH1` source id now 404s; XS2303's 2013 anchor is 6.7% off purely because the paper
   rounds to "USD 3.6 trillion" against WDI's 3839 (tolerance widened to 10% by design).

### 2.6 Forward risk

The two Sraffa series share the **unbuilt v1.1 BEA-to-Sraffa pipeline** (A-matrix, eigenvalue R, Sraffa price solver,
Bienenfeld linear/quadratic; ~3-5 days) — it is the *entire* extension for both, and it must recompute the CI/Theil
distributions rather than digitize the figures. XS2201's forward work is an independent IRS SOI MLE re-fit for 2017+ (~1-2
days) that must pin the open-ended top-bin convention (Pareto integral vs multiplier) first. The Weber-Shaikh five need: the
XS2302 forecast fix; archiving the four review PDFs against link-rot before the v1.1 scatter extraction (XS2304/XS2305);
and a standing discipline never to modernize onto a *different* object (BEA BoP-basis goods balance for XS2301, IMF EBA for
the misalignment scatters, `FI.RES.TOTL.CD` including gold for XS2303). The stale BLS International Labor Comparisons feed
behind the 7.8:1 ULC statistic (terminated 2014) is why the proposed XS2306 was never built.

---

## Cross-cutting themes

1. **Honesty about the reproduce/transcribe line.** The GPIM chain is bit-exact but transcribed (F-XS-05); the external family
   is self-consistent but not independently re-read. In both cases the MHRs state the limit rather than hide it.
2. **Vintage/forecast discipline is the recurring hazard.** NIPA comprehensive revisions and the T7.11 +1 shift threaten the
   appendix chain; IMF WEO forecasts and NAICS benchmark drift threaten the external family. The standing rule across all 17
   is *recompute on one coherent vintage, never splice, never present a projection as realized.*
3. **The most consequential single artifact is the BEA-1993 depreciation archive.** It gates any genuine GPIM recompute
   (XS004/XS006/XS007/XS009 -> S601-S604) and is the group's top forward-work item.
4. **Publication gate.** D14 = 85 (BELOW_90) blocks external distribution until the chopped unit-label leaks (F-XS-01) and the
   XS2302 forecast contamination (F-XS-02) are remediated; XS2304/XS2305 remain intentionally `publish: false`.

Per-series detail: `Technical/docs/methodology/series/{XS001..XS009,XS2001,XS2101,XS2201,XS2301..XS2305}_MHR.md`.
Machine-readable dossier: `Technical/methodology_review/CHXS_methodology.json`.
