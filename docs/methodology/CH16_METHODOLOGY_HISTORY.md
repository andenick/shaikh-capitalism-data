# Chapter 16 — Growth, Profitability, and Recurrent Crises — Methodology History Dossier

**Group:** ch16 · **Series:** S1601–S1606 (6) · **Book pages:** 727–736 (chapter); 898–899 (Appendix 16.1 Sources and Methods)
**Reasoning stance:** from Anwar Shaikh's own perspective — why *he* constructed each series as he did.
**Companion per-series MHRs:** `Technical/docs/methodology/series/S160{1..6}_MHR.md`
**Machine-readable twin:** `Technical/methodology_review/CH16_methodology.json`

> Grounding: every claim is anchored to a citable path — the research JSONs (`Technical/research/S160N_research.json`),
> `Technical/docs/chapters/CH16_RESEARCH_SUMMARY.md`, the review (`Technical/methodology_review/CH16_review.json`),
> the DPRs/EPRs, the S1605 processor (`Technical/replicator/lib/P02_processors/P02_S1605.py`), and the Phase-0
> NIPA/IO timelines (`Technical/docs/methodology/_timelines/`). No claim is invented.

---

## 1. What the chapter builds

Chapter 16 is Shaikh's empirical synthesis of postwar US profitability, the neoliberal turn, and the run-up
to the 2007 global crisis. The six series are four narrative threads (`CH16_RESEARCH_SUMMARY.md`
"Chapter context"):

1. **Long-wave price patterns in gold** (S1601, Fig 16.1) — situate 2007 as "on schedule."
2. **The wage–productivity gap** opened in the Reagan era (S1602, Fig 16.3) — the "great divorce," with a
   counterfactual wage path.
3. **The secular collapse of short-term interest rates** after 1981 (S1603, Fig 16.7) — a *global* policy-rate
   decline.
4. **The resulting profit/leverage boom** — the net corporate profit rate (S1604, Fig 16.8), household
   debt/income (S1605, Fig 16.9), and household debt-service (S1606, Fig 16.10) — that culminated in the
   crisis.

| SID | Fig | What it is | Construction |
|-----|-----|------------|--------------|
| S1601 | 16.1 | US/UK golden-wave price residuals (1930=100) | composite (WPI/gold, cubic de-trend) |
| S1602 | 16.3 | Hourly real wages + productivity + counterfactual | composite (BLS Nonfarm Business) |
| S1603 | 16.7 | US 3-mo T-bill + bespoke OECD weighted rate | composite (Fed H.10 × IMF IFS) |
| S1604 | 16.8 | Net average + net real incremental profit rate | composite (Appx 6.8.II.7 − TB3MS) |
| S1605 | 16.9 | Household debt-to-income ratio | formula (Z.1 D.3 L2 / NIPA T2.1 L27) |
| S1606 | 16.10 | Household debt-service + financial-obligations ratio | direct (Fed DSR/FOR release) |

A defining feature: **all six have strong CD2 predecessors (S093, S095, S098–S101)** ported via the
CD2→RSCD crosswalk, so this chapter is predominantly a **fidelity-validation and modernization-extension**
exercise, not de-novo source discovery (`CH16_RESEARCH_SUMMARY.md` "Chapter context"). Book-period
replication is publication-grade — **all 6 V03 PASS, MAE = 0** — and extension is deferred to Phase 6 by
design (`CH16_review.certification_note`; integration score **91.6, COMPLETE**).

## 2. The source families — heterogeneous, three of six touch NIPA

Unlike ch14 (all eight series on NIPA T1.10), ch16 draws on **six different provider families**, and only
half touch BEA NIPA (`CH16_review.nipa_touchpoints`):

- **S1601** — BLS/NBER WPI + BoE/O'Donoghue UK WPI + London gold (via **Appendix 5.3**). Price/gold, not NIPA.
- **S1602** — **BLS** Major Sector Productivity and Costs (Nonfarm Business, `PRS84006153`/`PRS84006093`). BLS, not NIPA.
- **S1603** — **Fed H.10** trade weights × **IMF IFS** country rates; US 3-mo T-bill (ERP T73 → `TB3MS`). Rate data; marginal NIPA (ERP is CEA/GPO, not a BEA line).
- **S1604** — **Appendix 6.8.II.7** corporate profit rates (BEA NIPA + Fixed Assets + benchmark I-O) **minus** `TB3MS`. **Deep NIPA + indirect I-O touch.**
- **S1605** — Fed **Z.1 D.3 line 2** (→ `HCCSDODNS`) / BEA **NIPA T2.1 line 27** DPI (→ `DPI`). **NIPA denominator.**
- **S1606** — **Fed** Household Debt Service / Financial Obligations release (→ `TDSP`/`FODSP`). Fed direct; not a NIPA-vintage series.

So the NIPA-vintage discipline that dominated ch14 bears on only **S1603 (marginal), S1604 (deep), and
S1605 (denominator)** here — and only **S1604 carries a benchmark-I-O touch** (through its chapter-6
profit-rate chain).

## 3. Why these sources — the chapter's three concept battles

Chapter 16 is unusually rich in *concept-provenance* decisions. Three define it:

### 3.1 The reference-grade WIN — S1605 concept restoration (review POS1)

The chapter's model result is **S1605**. CD2 extended the household debt-to-income ratio with **wrong-concept
proxies on both sides**: **CMDEBT** (households **+ nonprofits**) for the numerator and **PI** (broader
**pre-tax** Personal Income) for the denominator. Shaikh's Appendix is explicit — **Z.1 D.3 line 2**
(households only) over **NIPA T2.1 line 27, *Disposable* PI** (after-tax). RSCD **restores the book spec**:
`HCCSDODNS / DPI`, `proxy: false`, with a `proxy_justification` recording that the swap *corrects* CD2's
proxy rather than adding one (`S1605_DPR.md` §4; `S1605_EPR.md` §5; `CH16_review.POS1`). The restoration ships
with a **documented 1000× dimensional guard**: `HCCSDODNS` is in *millions*, `DPI` in *billions*, so the
loader computes `ratio = hccsdodns / (dpi * 1000.0)` with an inline dimensional comment **and** a sanity
assertion `0.3 ≤ ratio ≤ 1.5` that fails on any unit slip (`P02_S1605.py`; `CH16_review.POS1`). This is the
textbook remediation of the anu-framework Unit-Documentation failure mode. **The MHRs document HCCSDODNS/DPI
as canonical and flag CMDEBT/PI strictly as the rejected CD2 proxy — do not regress.**

### 3.2 The honest FLAG — S1601-E concept narrowing (review H3)

The chapter's one *provenance blemish* is **S1601**'s deferred extension. **S1601-E** splices **ONS K646,
"output of manufactured products" PPI**, onto the book's **all-commodities WPI** with `proxy: false`
(`S1601_DPR.md` §3; `S1601_EPR.md` §§3,5; `CH16_review.H3`). That is a **concept narrowing** —
manufactured-output PPI drops raw materials, fuels, and farm products — mislabelled as a non-proxy. The MHR
flags it honestly and prescribes re-stamping it `proxy: true` with a Concept Match Justification (or
re-sourcing to a UK all-commodities index) **before Phase 6 ships**. The disciplined counter-example is in
the same chapter: **S1603-E** offers OECD MEI as an alternative and correctly stamps it `proxy: true` with an
explicit CMJ on the GDP-PPP-vs-trade-weight basket difference (`S1603_EPR.md` §4). S1601-E should copy
S1603-E.

### 3.3 The bespoke construction — S1603 Ragab OECD weighting

Shaikh's OECD short-rate is **not** an off-the-shelf aggregate: he (crediting **Amr Ragab**) applies **Fed
H.10 broad-index *trade* weights** to **IMF IFS** country rates, because he wants the rate environment
weighted by relevance to US monetary transmission (`S1603_research.book_quotes[1]`, p. 899). The book-fidelity
extension rebuilds that; OECD MEI (GDP-PPP-weighted) is the honest proxy alternative (§3.2). Latest-vintage
H.10 weights are fixed across the panel (Phase 4 ratified) to avoid weight churn.

Other author choices worth recording: **golden-denominated prices** so Kondratieff long waves survive the
post-1933 nominal drift (S1601; Kondratieff 1984); **BLS output-per-hour** productivity for Fig 16.3's
per-hour wage/productivity picture — deliberately *different* from ch14's per-FTE productivity, no conflict
(S1602); the **net** (post-T-bill) profit rate to expose the Stagflation-Crisis simultaneity (S1604); and
**HP filter λ = 100** for annual data, with Ravn–Uhlig λ = 6.25 emitted only as a rejected sensitivity
(S1604; `S1604_DPR.md` §4).

## 4. Methodological-change exposure — the NIPA/I-O calendar for the three exposed series

Shaikh fixes all BEA data at the **~2011 vintage** (Appendix 6.7 fn 1; `NIPA_CHANGE_TIMELINE.md`
§"Why this matters"). The three exposed ch16 series:

- **S1604 (deep NIPA + benchmark I-O).** Its Appendix-6.8.II.7 profit-rate inputs rest on BEA NIPA (corporate
  GVA/profits) + Fixed Assets (capital stock). The **2013 (14th)** update capitalized R&D/entertainment
  (**≈ +$400B GDP**, higher capital stock, CFC/NOS restatement) and incorporated the **2007 benchmark I-O**;
  **2018 (15th)** brought the 2012 benchmark I-O, FISIM method changes, and the **T7.11 +1 line shift**
  (resolver `NIPA_T711_FISIM_remap.md`); **2023 (16th)** re-based to reference year 2017
  (`NIPA_CHANGE_TIMELINE.md`). Because each NIPA update *incorporates a benchmark I-O account*
  (`IO_CHANGE_TIMELINE.md`), S1604 carries an **indirect benchmark-I-O touch** — the only ch16 series that
  does. Plus a structural HP100 endpoint fragility.
- **S1605 (NIPA denominator + Fed Z.1 restructure).** DPI (T2.1 line 27) is restated at each comprehensive
  update (2013 pension accrual; 2018 personal-saving; 2023 rebase). Separately, the **2013 Fed Z.1 → Financial
  Accounts restructure** renumbered D.3 — sidestepped by keying on FRED `HCCSDODNS`.
- **S1603 (marginal).** The US 3-mo T-bill is a Treasury market rate (no methodology change since 1934); the
  ERP citation is a CEA/GPO publication, not a BEA NIPA line. Its real drift knobs are Fed H.10 weight
  revisions, ERP URL rot (gpoaccess → govinfo), and IMF IFS country coverage.

**S1601, S1602, S1606 do not read a NIPA magnitude** — their drift exposure is WPI/PPI revisions + gold
de-peg (S1601), BLS index rebases + deflator regime (S1602), and essentially none (S1606, a stable Fed direct
series). The universal rule inherited from Phase-0: **never splice across a comprehensive-revision boundary;
re-derive end-to-end on one coherent vintage** (`NIPA_CHANGE_TIMELINE.md`).

## 5. Replication fidelity, at a glance

- **Book period is bit-exact for all 6** — V03 MAE = 0.0 (exact pass-through of Appendix 5.3 / 16.2 columns;
  `CH16_RESEARCH_SUMMARY.md` Phase 5–8 closure). **D13 Data-Authenticity gate = PASS (100)**: no
  synthetic/frozen data, non-circular hand-checks EXACT for all six (e.g. S1602 `1947 = 40.2151/45.3276`;
  S1604 `1948 = 0.153564`, counterfactual `2011 = 0.031605`; S1605 internal `734.3/1187.3 = 0.61846`; S1606
  annual means hand-computed from quarterly), source blanks preserved (`CH16_review.gates.D13`).
- **Integration 91.6, COMPLETE** — held below EXEMPLARY by the D10 viz-integration gap (figures reproduced as
  static overlay PNGs only; no app/FPRs/`SUBSERIES_METADATA.json`), two thinner research JSONs (S1605/S1606),
  and the unflagged S1601-E narrowing (`CH16_review.certification_note`; findings **H1, H2, H3**).
- **Honest limits carried forward:** S1601-E concept narrowing (H3, flag before Phase 6); no
  `SUBSERIES_METADATA.json` project-wide → no viz-app integration (H1); no FPRs for the six figures (H2);
  S1602 counterfactual regression + S1604 `rcorpalt` re-derivation deferred to Phase 6; S1606 DSR-vs-FOR
  labelling unresolved (L4).
- **Best practice to preserve:** the S1605 concept restoration + 1000× sanity guard (POS1) — the model for how
  a wrong-concept proxy should be *corrected and guarded*, and the exact discipline S1601-E still needs.

## 6. Per-series index

| SID | Primary concept | NIPA / I-O touch | Key honest note |
|-----|-----------------|------------------|-----------------|
| S1601 | US/UK golden-wave price residuals (1930=100) | none (WPI/gold) | **S1601-E narrows all-commodities WPI → ONS-K646 manufactured PPI with proxy:false (H3)** |
| S1602 | Hourly real wages + productivity + counterfactual | none (BLS) | BLS per-hour productivity (≠ ch14 per-FTE); counterfactual regression deferred; feeds S1604 |
| S1603 | US 3-mo T-bill + bespoke OECD weighted rate | marginal (ERP, not a NIPA line) | Ragab Fed-H.10×IMF-IFS build; OECD-MEI honestly proxy:true+CMJ (model for S1601-E) |
| S1604 | Net avg + net real incremental profit rate | **deep NIPA + indirect benchmark I-O** | HP100 λ=100 (6.25 rejected); endpoint fragility; needs S1602 + RSCD S0608 |
| S1605 | Household debt-to-income ratio | **NIPA T2.1 L27 DPI denominator** | **reference-grade restoration to HCCSDODNS/DPI + 1000× guard (POS1); reject CD2 CMDEBT/PI** |
| S1606 | Household debt-service + financial-obligations ratio | none (Fed direct) | lowest drift; DSR-vs-FOR labelling unresolved (L4); thinnest research JSON (M1) |
