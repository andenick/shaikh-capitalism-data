# XS001 — Methodological History Report (MHR)

**Series**: XS001 — GDP/GDI Decomposition and Business Net Operating Surplus (NOS)
**Chapter**: 6 (Capital and Profit) · **Group**: XS / `xs_class: appendix` (GPIM construction internal)
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS001_research.json`; `Technical/docs/series/XS001_DPR.md` +
`XS001_EPR.md`; `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`;
`Technical/methodology_review/CH_XS_review.json`;
`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`;
`Technical/docs/methodology/NIPA_T711_FISIM_remap.md` (downstream XS003 coupling).

---

## 1. What it is

XS001 is the **first step of Shaikh's Chapter-6 corporate-profit-rate pipeline**: a sequential
decomposition of NIPA aggregate domestic Net Operating Surplus (NOS) into its institutional-sector
components, isolating the one Shaikh actually wants — the **business-sector NOS**. It is the
numerator-precursor for every subsequent profit-rate object in the chapter; it plots nothing itself
(the RSCD Phase-2 mapper flagged it "unmapped" precisely because it links to no Ch6 figure — it is a
construction internal, `CH6_GPIM_SUMMARY.md` §"What This Chapter Documents").

Shaikh starts from NIPA's own accounting identity, quoted verbatim in `XS001_research.json`
(book p. 828):

> "In the NIPA definition, NOS = GDP – [SD + compensation of employees within the country + net
> indirect business taxes – economic depreciation, i.e., the depreciation of capital goods valued at
> current cost, called Consumption of Fixed Capital (CFC)]. Notice that this procedure implicitly
> allocates the income side measurement error to the sum of employee compensation and/or net taxes,
> rather than to Net Operating Surplus (NOS)."

The construction is the **Appendix Table 6.7.2 / 6.8.I.1 tableau** (`XS001_research.json` method quote,
book p. 829): Gross Domestic Product (NIPA T1.7.5) − Statistical Discrepancy (T1.7.5) = Gross Domestic
Income (T1.10); less Domestic compensation of employees paid (T1.10), less Taxes on production and
imports less subsidies (T1.10), less Consumption of fixed capital (T1.10) = **Aggregate Domestic Net
Operating Surplus** (T1.10). Shaikh then strips the non-business institutional sectors to land on the
number he wants:

**Business NOS = Aggregate Domestic NOS − NOS_household − NOS_NPISH − NOS_government −
NOS_government_enterprises** (`XS001_research.json` formula; `XS001_DPR.md` §"Why It Matters").

Canonical worked value (Appendix Table 6.7.3, book p. 830, `XS001_research.json` methodology_notes),
**2009**: Business Gross Value Added = 10,189.6; **Business NOS = 2,533.8** — and the corrected business
NOS is "**79% of the corresponding aggregate value**" (verbatim, book p. 830). RSCD hand-check
(`CH_XS_review.json` hand_checks): V03 PASS, mae = 0.0 (n = 390), 1947 reference 63.2 consistent, all
values verbatim to the Appendix 6.8 workbook (`SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx`).

Six chopped subseries (`XS001_DPR.md` Sources table): XS001-A `NOSbusnipa` (the output),
XS001-B `Aggregate NOSnipa`, XS001-C `NOShh`, XS001-D `NOSnpish`, XS001-E `NOSgengov`,
XS001-F `NOSgoventerp`.

Appendix location: **Appendix 6.7 "Empirical Methods and Sources," Section II, book pp. 829–830**
(narrative); Appendix Table 6.8.I.1 (published workbook, transcribed verbatim).

## 2. Source lineage

All components are BEA NIPA, fixed at the **2011 vintage** by Appendix 6.7 footnote 1 (book p. 828):
"All BEA data used in this book comes from tables last downloaded in 2011 and may therefore differ from
more recent tables." (`XS001_research.json` open_questions; `NIPA_CHANGE_TIMELINE.md` §"Why this matters").

Line-level lineage (`XS001_research.json` components; primary_source):

- **GDP** — NIPA **T1.7.5**, line 1 (product side).
- **Statistical discrepancy (SD)** — NIPA **T1.7.5**, line 15 (the product-vs-income wedge).
- **Domestic compensation of employees** — NIPA **T1.10**, line 2.
- **Taxes on production and imports less subsidies** — NIPA **T1.10**, lines 9–10.
- **Consumption of fixed capital (CFC)** — NIPA **T1.10**, line 23.
- **Aggregate domestic NOS** — NIPA **T1.10**, line 11 (the balancing residual).
- **Household-sector NOS subtraction** — NIPA **T7.12** (OOH rental income breakdown), lines 133–140,
  attributed to Ritter (2000) and Mayerhauser & Reinsdorf (2007) (`XS001_research.json` components).
- **NPISH operating surplus** — Mead, McCully & Reinsdorf (2003) method (T7.12-supported).
- **Government enterprise current surplus** — NIPA **T1.10**, line 22.

Review touchpoint (`CH_XS_review.json` touchpoints): kind **NIPA**, "T1.7.5 (GDP), T1.10 (GDI), T7.12;
GDP/GDI decomposition → business NOS; NIPA 2011 vintage (book header)." Upstream agencies per the DPR
Sources table are BEA (NIPA/Fixed-Asset), IRS SOI, U.S. Census Bureau Historical Statistics 1975, and
FRB G.17 — but for XS001 specifically only the NIPA tables above are load-bearing; the wider agency list
is the shared GPIM-chain provenance boilerplate carried on all XS00x DPRs.

Predecessor: **CD2 series S206**, which implemented a 55-base-column tableau covering this decomposition
(`XS001_research.json` methodology_notes; predecessor_ids.cd2_id = "S206").

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

**Why re-derive business NOS by sector rather than take published NIPA operating surplus.** This is the
crux of XS001. Shaikh needs the *classical* profit concept — the surplus generated in production by the
business sector — and NIPA's published operating-surplus aggregates do not deliver it cleanly for three
reasons he acts on here:

1. **NIPA mixes non-business institutional sectors into aggregate NOS.** Published aggregate NOS folds in
   households, NPISH (nonprofits), general government, and government enterprises. Shaikh's classical
   object is the surplus of *capitalist enterprise*, so he subtracts each institutional sector out
   explicitly (`XS001_research.json` methodology_notes: "sequentially decomposes NIPA aggregate domestic
   NOS into household, NPISH, government, government-enterprise, and business components").

2. **The household subtraction is dominated by fictitious owner-occupied housing (OOH).** NIPA imputes a
   rental surplus as if homeowners rent to themselves; Shaikh treats this "as a methodological correction
   rather than a real business activity" (`XS001_research.json` methodology_notes) and removes it via the
   T7.12 lines 133–140 OOH breakdown. Without stripping OOH, the "business" surplus is inflated by an
   activity with no market transaction.

3. **He follows BLS in also excluding government enterprises.** Verbatim (book p. 830): "NIPA defines the
   'business' sector as exclusive of NPISH, HH, and general government, but the Bureau of Labor Statistics
   (BLS) also correctly excludes government enterprises because they are nonprofit (Harper, Moulton,
   Rosenthal, and Wasshausen 2008, 1 and table A.1)." Shaikh adopts the tighter BLS boundary — hence the
   separate `NOSgoventerp` subtraction (T1.10 line 22) that a naive "NIPA business sector" read would miss.

**Why the GDP-side statistical-discrepancy bridge.** Shaikh reaches business NOS as a *residual* of the
product-side identity (GDP − SD → GDI → less EC, less taxes, less CFC). He adopts NIPA's convention of
netting SD on the GDP side, which "implicitly allocates measurement error to wages/taxes rather than NOS"
(`XS001_research.json` methodology_notes; book p. 828). He *flags this as imperfect* — a rejected
alternative would allocate the discrepancy to NOS itself — but accepts it because the classical surplus
should not absorb pure measurement error, and because it keeps his series consistent with the published
NIPA identity.

**Rejected alternative — take BEA's published "net operating surplus, private enterprises" line
directly.** Shaikh declines the shortcut: that line still carries OOH imputed housing surplus and (on the
NIPA boundary) government enterprises, so it is not the classical business surplus. His explicit target is
the **79%-of-aggregate** corrected figure (book p. 830), which only the full institutional-sector
decomposition produces.

**Rejected alternative — allocate the income-side asymmetry to NOS.** Discussed and set aside (book
p. 828): he keeps NIPA's product-side SD convention, flagging rather than "fixing" it, so his numbers
remain reconcilable with the official accounts.

## 4. Methodological-change exposure

XS001 is entirely NIPA-vintage-coupled, and Shaikh froze it at the **2011 vintage** (footnote 1, p. 828).
The exposures on its specific inputs, per `NIPA_CHANGE_TIMELINE.md`:

1. **2013 Comprehensive Revision (14th, rel. 2013-07-31)** — the highest-impact event for XS001's
   internals. R&D and entertainment/literary/artistic originals were **capitalized** as fixed investment
   → the new Intellectual Property Products (IPP) category, **≈ +$400B to the GDP level**, and — directly
   relevant here — **NOS and CFC magnitudes change** and **Fixed-Asset/capital-stock levels rise**
   (`NIPA_CHANGE_TIMELINE.md` comprehensive-revision table). Because XS001 = GDP − SD − EC − taxes − CFC,
   a revision that moves both GDP *and* CFC re-levels the whole residual. There was also a **FISIM
   restatement** touching the household/business boundary that XS003 later reverses. Any XS001 re-pull on
   a 2013+ vintage lands on reclassified GDP/CFC/NOS.

2. **2018 Comprehensive Update (15th, rel. 2018-07-27)** — incorporated the 2012 benchmark I-O, improved
   financial-services and nonprofit methods (the NPISH subtraction path), and personal-saving revisions.
   The famous **T7.11 +1 line shift** is a *downstream XS003* problem, not XS001's — but the 2018 update's
   nonprofit-method change does bear on XS001's NPISH component. (Cite `NIPA_T711_FISIM_remap.md` for the
   line-shift mechanics that hit XS003, and `NIPA_CHANGE_TIMELINE.md` §"Table-renumbering / silent-break
   events" event 1.)

3. **2023 Comprehensive Update (16th, rel. 2023-09-28)** — reference year → 2017, harmonized NIPA+Industry
   accounts on the 2017 benchmark; small NAICS effects. Would re-base any extended XS001 series.

4. **Line-number drift on the OOH subtraction.** XS001 reads NIPA T7.12 lines 133–140 for the household
   OOH subtraction; the EPR concern (`XS001_research.json` extension_candidates) warns "Line numbers may
   shift across vintages; must map by NIPA stub label, not line number" — the same discipline the XS003
   T7.11 resolver enforces mechanically, but for XS001 the OOH/T7.12 mapping is *not yet* wrapped in a
   resolver (forward risk, §6).

**Anti-splice mandate.** `NIPA_CHANGE_TIMELINE.md` §"Why this matters": "Any extension of a Shaikh series
past its book period must be re-computed end-to-end on a single coherent vintage — never spliced across a
comprehensive-revision boundary (CH6 open-question 5)." XS001's EPR encodes exactly this: extension
re-fetches the NIPA components and re-runs the decomposition; it does not append post-2011 published
values to the 2011-vintage book series.

## 5. Replication fidelity note

RSCD reproduces XS001 **bit-exact to Appendix 6.8** by the read-the-truth-column pattern: L01 loads the
finished decomposition columns from `Appendix6_Table68*.xlsx` and V03 round-trips against that same
workbook at **1.0% tolerance** (`XS001_DPR.md` §Validation Expectation), observed **mae = 0.0, n = 390**
(`CH_XS_review.json` hand_checks XS001). The honest limits, disclosed:

- **Transcribed-not-recomputed.** The executable path is a **pass-through transcription** of Shaikh's
  Appendix 6.8 workbook — L01 loads the finished `NOSbusnipa`/aggregate/sector columns; P02 is a
  schema-only pass-through. The end-to-end decomposition (GDP−SD−EC−taxes−CFC, then the four
  institutional-sector subtractions) exists as an executable recipe *only in the deferred v1.1 EPR
  extension path* (`XS001_EPR.md` §Method; and the group finding **F-XS-05**, which observes that the
  formula-type XS series "carry components:[] and no formula field … the executable path is a pass-through
  transcription"). XS001 is nominally `construction: composite`, and its `components` array *is* populated
  in the research JSON — but the runtime L01/P02 still transcribes rather than recomputes.
- **Circular-validation caveat.** V03 confirms *melt fidelity* to the workbook the chopped is derived
  from, not an independent re-derivation from raw 2011-vintage NIPA. The genuine non-circular anchor is the
  book's own printed 2009 figures (Business NOS 2,533.8; the 79%-of-aggregate ratio, p. 830), which the
  research JSON records and the values are consistent with.
- **Units cleanliness.** XS001's six subseries are all dollar levels (`billions_current_usd`), so it does
  **not** suffer the mixed-units leak that hits XS002-G/XS003/XS005-C/XS006 under finding **F-XS-01**;
  XS001 is not named among the mislabeled dimensionless/rate subseries.

## 6. Forward risk

- **OOH/T7.12 stub-label resolver not yet built.** The household subtraction depends on NIPA T7.12 lines
  133–140; unlike XS003's T7.11 recipe (which has `_nipa_t711_line_resolver.py`), XS001's T7.12 OOH mapping
  is narrated ("map by NIPA stub label, not line number", `XS001_research.json`) but not wrapped in code.
  Any 2013/2018/2023-vintage extension must first re-derive the T7.12 OOH line map by caption
  (`XS001_research.json` open_questions: "Extension to 2024 vintage requires retracing OOH and NPISH
  subtractions because NIPA Table 7.12 line numbering may have changed").
- **CFC/NOS re-leveling on any post-2011 pull.** Because the 2013 IPP capitalization moved both GDP and
  CFC, an honest extension cannot compare a 2011-vintage 1947–2011 business-NOS path to a 2013+-vintage
  2012– path without documenting the level break; splicing is forbidden (`NIPA_CHANGE_TIMELINE.md`).
- **Downstream propagation.** XS001 is consumed by XS003 (which adjusts business NOS for imputed interest)
  and validates XS002's corporate/noncorporate split; the open question (`XS001_research.json`) is whether
  S601–S604 reference XS001 *transitively via XS003* rather than directly. A vintage error in XS001
  propagates to every Ch6 profit rate, so the 2011-vintage freeze must be preserved for the book series.
- **BEA API path for extension.** The EPR extension re-fetches via `S00_apis.bea_table` (needs
  `BEA_API_KEY`) and logs `vintage_year`; the failure-mode table (`XS001_EPR.md`) routes vintage drift to
  documented per-year logging, never silent overwrite of the book period.
