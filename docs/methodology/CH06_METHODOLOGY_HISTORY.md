# Chapter 6 — Capital and Profit: Methodology History (the capital-measurement narrative)

**Group:** ch6 · **Primary series:** S601, S602, S603, S604 (+ GPIM internals XS001–XS009, sibling dossiers)
**Book pages:** 213–273 (narrative); Figs 6.1–6.7 at pp. 244–256; construction in Appendix 6.5 (capital stock,
pp. 807–821), Appendix 6.7 ("Empirical Methods and Sources", pp. 828–855), Appendix 6.8 Tables I-3 & II-7.
**Author:** RSCD Phase-2 methodological-historian agent · **Date:** 2026-06-30
**Companion per-series reports:** `Technical/docs/methodology/series/S60{1,2,3,4}_MHR.md`
**Machine twin:** `Technical/methodology_review/CH06_methodology.json`

> Every claim below is anchored to a citable path (research JSONs, chapter summaries, `CH06_review.json`,
> `NIPA_CHANGE_TIMELINE.md`, `NIPA_T711_FISIM_remap.md`). Nothing is invented. Read-only report.

---

## 1. The chapter's methodological project

Chapter 6 is the empirical bridge into Part II (Real Competition). Its single thesis is that **the NIPA/BEA accounts
as published do not measure the classical rate of profit**, and Shaikh corrects three specific pathologies rather
than adopting the published series (`CH6_RESEARCH_SUMMARY.md` "Chapter scope"):

1. **The FISIM / imputed-interest pathology (NIPA T7.11).** NIPA treats banks as producing imputed "banking
   services", misallocating net monetary interest between profit and value added. Shaikh reverses it so
   `NOS = P + NMINT`, restoring the classical/business surplus (p. 246).
2. **The capital-measurement pathology (BEA chain-weighted fixed assets).** BEA's quality-adjusted, chain-weighted
   net stock departs from the perpetual-inventory rule and distorts the output-capital trend (p. 244). Shaikh
   replaces it with his own **Generalized Perpetual Inventory Method (GPIM)** gross current-cost stock `KGC`
   (Appendix 6.5 accumulation eqs 6.5.21–6.5.23; Appendix 6.7.V).
3. **The inventory-omission pathology.** Fixed-asset tables omit inventories from the capital base; Shaikh adds IRS
   Statistics of Income corporate inventories, so total capital `KTC = KGC + INV` (p. 248, eq. 6.10).

The operational profit-rate concept that results is **`r ≡ NOS/KTC(-1) = (P + NMINT)/(KGC(-1) + INV(-1))`**
(eq. 6.10, p. 248) — corrected numerator (classical surplus), corrected total-capital denominator, lagged, at
current cost so the rate is real by construction.

## 2. The four primary series as one pipeline

All four S6xx draw on a **single underlying construction table** — Appendix 6.8 Table II-7 (corporate) and Table I-3
(corporate + noncorporate) — with the same primary sources (`CH6_RESEARCH_SUMMARY.md`):

| Series | Concept | Figures | Table cols | What it adds |
|---|---|---|---|---|
| **S601** | sectoral average profit rates `rcorp`, `rnoncorp`, `rbus` + capacity `uK`/`uFRB` | 6.1, 6.4, 6.5 | I-3 (S208AW/AX), II-7 | motivates the chapter: corrected sectors nearly coincide → corporate rate as proxy |
| **S602** | corrected vs NIPA corporate `R`, `r`, `σ_P` (6 curves) | 6.2, 6.6 | II-7 (S013I/J/N/O …) | the flagship contrast; corrected max rate falls where NIPA rises |
| **S603** | decomposition ratios `x1`, `x2`, `x3` | 6.3 | II-7 (S013P/Q/R) | attributes the corrected/NIPA wedge; **x3 (GPIM) dominates the trend** |
| **S604** | corporate IROP (nominal + real) | 6.7 | II-7 (S013AO/AP …) | proxy for return on new capital; adjusted ≈ NIPA proxy (Table 6.24) |

The GPIM construction internals — business-sector NOS, WEQ2 wage-equivalent, the imputed-interest adjustment, the
GPIM `KGC`/`KNC` and its four sensitivity variants, and IRS inventories — are the **XS appendix series XS001–XS009**
(Decision 0002, `CH6_GPIM_SUMMARY.md`), authored as sibling dossiers. In RSCD they are the *components* of S601–S604,
not independent plotted series; `series_registry.json` records `S60x.components ⊇ {XS003, XS004, XS009}`.

## 3. Why the GPIM over BEA's published net capital stock (the central rationale)

This is the intellectual core of the chapter and the reason S602/S603 exist. From Shaikh's perspective:

- BEA's fixed-asset stock is **chain-weighted and quality-adjusted**, which violates the simple perpetual-inventory
  accumulation and produces a capital series whose trend is not comparable across time (p. 244). The chain
  aggregation embeds relative-price and hedonic adjustments that a *value* measure of advanced capital should not
  carry.
- Shaikh's **GPIM** instead accumulates BEA current-cost **gross investment flows** under transparent, fixed
  assumptions — a 1925 initial value, a depreciation schedule, and an interwar book-value correction — to yield a
  **gross** current-cost stock `KGC` (Appendix 6.5). "Generalized" because the initial value, depreciation rates,
  and interwar treatment are each a deliberate, separately-documented choice, not a black box.
- The empirical payoff appears as **x3 = KNC_bea/KGC falling from ~1.11 to ~0.61** (S603, p. 249): the GPIM stock
  rises steadily relative to BEA's, and S603 shows this capital-stock revaluation — **not** the interest or inventory
  corrections — is what *dominates the downward trend* in the corrected-vs-NIPA profit-rate ratio. That is the
  quantitative evidence for the chapter's headline claim that **NIPA-only profit series mask the secular decline**:
  the corrected normal-capacity rate falls −0.35%/yr in 1982–2011 while the NIPA rate *rises* +1.05%/yr
  (`CH6_RESEARCH_SUMMARY.md` S602).
- The **initial-1925 value matters ~28%** to the level of `KGC` (p. 247, App. 6.7.V.4), which is why Shaikh runs four
  explicit GPIM variants (XS005–XS008) rather than a single stock: BEA-2011 initial value, BEA-1993 finite-life
  depreciation, IRS interwar adjustment, and their combination. The **preferred** measure (XS004) = BEA-2011 initial
  value + BEA-1993 depreciation + IRS interwar adjustment (`CH6_GPIM_SUMMARY.md` §"Sensitivity Variant Summary").

Alongside the capital correction, Shaikh's **numerator** choice (`NOS = P + NMINT`, the FISIM reversal) and
**denominator** choice (total capital `KTC = KGC + INV`, including IRS inventories) complete the profit-rate concept.
He keeps the **corporate** sector as the workhorse because it needs only the easy imputed-interest fix (no WEQ2), and
because after correction the corporate and noncorporate rates nearly coincide (S601, Fig 6.1).

**See also:** `PRODUCTION_BOUNDARY_ACROSS_CLASSIFICATION_ERAS.md` — this Ch6 NIPA institutional-sector boundary (business NOS) is one of three era-specific production-boundary implementations in RSCD (Ch6 NIPA-sector / Ch7 NAICS exclusion key / Ch9 whole-economy), stated there as one fact and never to be harmonized.

## 4. Methodological-change exposure — the NIPA vintage-drift risk (the key chapter-wide hazard)

Shaikh's **Appendix 6.7 footnote 1 fixes all BEA data at the 2011 vintage** (`NIPA_CHANGE_TIMELINE.md` §"Why this
matters"; `CH6_GPIM_SUMMARY.md` OQ5). Every comprehensive revision after 2011 re-defines the concepts the chapter
rests on. The chapter-wide rule is: **never splice across a comprehensive-revision boundary; re-compute end-to-end on
one coherent vintage** (CH6 open-question 5).

- **2013 Comprehensive Update (14th) — the deepest exposure.** R&D and entertainment/literary/artistic originals were
  **capitalized** as fixed investment (new Intellectual Property Products category, ≈ +$400B GDP), **raising CFC,
  NOS, and fixed-asset/capital-stock levels**, and FISIM was restated by sector (`NIPA_CHANGE_TIMELINE.md` 2013 row).
  Because the GPIM *accumulates the entire history of BEA gross investment*, re-capitalized IPP flows change `KGC` at
  **every** year — so a post-2013 GPIM is a *different capital concept*, and the KGC-vs-KNC gap that S602/S603 exist
  to display would be silently corrupted by a splice. Row order in T7.11 unchanged, magnitudes changed.
- **2018 Comprehensive Update (15th) — the T7.11 renumbering time-bomb.** A new monetary-interest sub-row was
  inserted in the financial-corporate block of **T7.11 → +1 line shift** for every line ≥ 28. Shaikh's 2011-vintage
  imputed-interest recipe (Appendix Table 6.7.11, p. 842) uses lines `4, 28, 44, 52, 53, 54, 73, 74, 75, 91`; on a
  2018+ vintage these become `4, 29, 45, 53, 54, 55, 74, 75, 76, 92` (line 4 unchanged). This directly hits
  `NMINT` → S601/S602 `NOS`, S603 `x1`, S604 adjusted numerator. The remap is resolved **by BEA `LineDescription`
  stub label, not line number**, in `Technical/docs/methodology/NIPA_T711_FISIM_remap.md`
  (`_nipa_t711_line_resolver.py`); vintages 2011–2017 share 2011 numbers, 2019–2024 share 2018 numbers.
- **2023 Comprehensive Update (16th).** Reference year → 2017, 2017 benchmark supply-use/I-O; smaller effect but
  shifts chain-index levels underlying the FA tables.
- **Series-specific fragility.** S604's **first-difference** construction is the most fragile: adjacent vintages give
  different `Δ` at the seam, so even a small level revision spikes the IROP at a join. S603's **x1** and S602/S604's
  **adjusted** measures are additionally bounded by chronic `NMINT_corp` incompleteness in recent T7.11 vintages —
  freeze at the last complete year, never forward-fill.

Because all four chopped series end at 2011, this drift handling is **staged but untested** (`CH06_review.json` L4):
the FISIM stub-label resolver and the BEA-1993 depreciation staging exist and are documented, but no extension has
exercised them.

## 5. Replication fidelity — what is faithful, and the honest limits

From `CH06_review.json` (integration score **91.6%, COMPLETE**; D13 data-authenticity **PASS 100**):

- **Bit-exact to the book.** All 21 shipped Ch6 subseries reproduce Appendix 6.8 (Tables I-3 / II-7) at
  **0.0000% max pct error**; no synthetic, spliced, or fabricated values; no `np.random`. S604 additionally matches
  **Table 6.24 exactly** (the one genuine non-circular book anchor in the chapter). Figures 6.1–6.7: 6 MATCH /
  1 MINOR_DEV (Fig 6.6 axis-scope) / 0 MISMATCH.
- **Transcription of finished columns, not a live GPIM recompute** (CH06_review M5). Every S6xx `L01`/`P02` reads
  Shaikh's *pre-computed* Appendix 6.8 columns
  (`SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68{I3,II7}.xlsx`) and transcribes them; the
  profit-rate and IROP formulas are **not executed in code** for the book period. This is faithful and verbatim
  (anti-lazy-splice satisfied) but means the construction is reproduced, not recomputed.
- **The XS→S6xx linkage is declarative prose only, not machine-wired** (CH06_review M1, verdict
  `declarative_prose_only_not_machine_wired`). Registry `S60x.components=[XS003,XS004,XS009]` but `L01_S60x.py` calls
  `_ch6_appendix_loader.load_variables('I3'/'II7', col)` directly and `P02_S60x.py` is pass-through — **no XS output
  parquet is consumed by any S6xx script**. Harmless in the book period (both trace to the same Appendix 6.8), but
  the **GPIM→profit-rate chain is non-executable** as wired. This persists after the AS→XS migration.
- **`reference_values` are circular** (CH06_review M3): V03 round-trips the same XLSX the chopped is built from; only
  S604's Table 6.24 is an independent anchor.
- **Known defects.** S604 ships only **2 of 4** Fig 6.7 curves (H1, HIGH — real-rate panel missing) while
  `publish:true`; S602 carries the **banned mixed-units string** `decimal_rate_and_share` (M4); S601 series-level
  units mislabel the capacity subseries (M4). D14 outward-facing = 88, BELOW_THRESHOLD, from these units issues.

## 6. Forward risk (chapter-wide)

- **The next NIPA benchmark will re-define capital again.** The 2013→2018→2023 sequence shows each comprehensive
  update can re-scope CFC, NOS, investment, and the capital stock. No historical Ch6 value is vintage-stable;
  extension of any S6xx must re-fetch and re-run the whole construction on a single coherent vintage.
- **BEA-1993 depreciation-rate archive recovery is the gating prerequisite for a *true* GPIM recompute.** The
  preferred GPIM (XS004) needs BEA 1993 finite-life depreciation/retirement rates that are no longer in the BEA
  iTable. They are staged at
  `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/BEA_1993_depreciation_retirement_rates.{csv,json}`
  and recoverable from the KB source
  `Inputs/Capitalism Data/Technical/Knowledge_Base/1993_DoC_Fixed_Reproducible_Tangible_Wealth/` (BEA 1993 *Fixed
  Reproducible Tangible Wealth*). Until XS004 is **wired into the S6xx loaders** (M1), any extension uses BEA-published
  stock — i.e. reproduces the *conventional* measure, not Shaikh's corrected one.
- **T7.11 FISIM resolver is untested at extension** (L4): the stub-label remap must be exercised on a live post-2018
  fetch before `NMINT`-dependent measures (S601/S602 corrected, S603 x1, S604 adjusted) can be extended; the chronic
  `NMINT_corp` incompleteness bounds those windows regardless.
- **IROP proxy is the extension path.** Given `iropcorp ≈ iropcorpnipa` (Table 6.24) and the NMINT/IRS constraints,
  `iropcorpnipa` (needs no NMINT, no IRS inventories) is the operationally extendible IROP — Shaikh's own argument
  (p. 256) — and the same NIPA-proxy logic carries into Ch7 (S706/S707) and Ch10 (S1007).
- **Close S604's H1 coverage gap** (add the two real-rate columns from the existing II-7 workbook) before S604 is
  published, or reconcile the `publish` flag with the CLAUDE.md `publish:false` intent (M6).
