# XS005 — Methodological History Report (MHR)

**Series**: XS005 — GPIM Variant, BEA-2011 Reference (Pure GPIM Regenerator): KNCcorp' / KNCcorpbea / ratio
**Chapter**: 6 (Capital and Profit) · **Group**: XS · **xs_class**: appendix · **CD2 predecessor**: S210
**Perspective**: authored *from Shaikh's perspective* — why he builds a pure BEA-mechanical regenerator.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS005_research.json`; `Technical/docs/series/XS005_DPR.md` +
`XS005_EPR.md`; `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`;
`Technical/methodology_review/CH_XS_review.json`; Phase-0
`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md` (+ `IO_CHANGE_TIMELINE.md`).

---

## 1. What it is

XS005 is Shaikh's **"what if we just trusted BEA 2011 entirely" counterfactual** — the pure GPIM
*regenerator*. It runs the identical GPIM accumulation machine as XS004, but with **no** methodological
corrections: it keeps the **BEA-2011 initial value (98.1 in 1925)** *and* the **BEA-2011 (infinite-life
geometric) depreciation rate**, and applies **no interwar adjustment** (`XS005_DPR.md` §Construction;
`XS005_research.json` methodology_notes[0]). Its purpose is not to be a profit denominator but to
**prove the GPIM machine reproduces BEA's own published net stock** before any variant perturbs it.

Three transcribed subseries from **Appendix Table 6.8.II.1** (`XS005_DPR.md` §Sources):
- **XS005-A `KNCcorp'`** — the GPIM-regenerated corporate net current-cost stock;
- **XS005-B `KNCcorpbea`** — the official BEA-published corporate net current-cost stock (the target);
- **XS005-C `KNCcorp'ratio`** — the GPIM/BEA ratio (Shaikh-computed, ≈ 1.0), the accuracy diagnostic.

The regenerator's validation headline (`XS005_research.json` methodology_notes[3]; `XS005_DPR.md`
§Why It Matters): **99.5–99.6% match** between GPIM-generated `KNCcorp'` and official `KNCcorpbea`
(Appendix Table 6.7.12, book p. 844; the RSCD DPR cites Appendix Table 6.8.II.1). Same GPIM current-cost
rule as XS004 (`XS005_research.json` formula):
> `KC_t = IG_t + (1 − z_t)·(pK'_t/pK'_{t−1})·KC_{t−1}`, with `KC_{1925} = 98.1`.

Book period **1925–2011** (`XS005_DPR.md` §Year Coverage). XS005 is a **sensitivity variant — NOT used by
S601–S604** (`XS005_DPR.md` §Why It Matters; `XS005_research.json` methodology_notes[4]).

## 2. Source lineage

Single-agency, single-vintage (`XS005_research.json` primary_source; `CH_XS_review.json` touchpoints XS005
— kind **NIPA/BEA-FA**, note "BEA FA T6.1 (2011 init value 98.1); pure-GPIM regenerator validating BEA 2011
net stock (~99.6%)"):

- **BEA Fixed Asset Accounts, 2011 vintage.** Initial value from **FA Table 6.1, line 1, year 1925 = 98.1**
  (Current-Cost Net Stock of Private Fixed Assets, corporate); gross investment `IG` from **FA T6.7**;
  chain price index `pK'` from **FA T6.4 / T6.1** implicit deflator; the target `KNCcorpbea` is the BEA
  published corporate net-stock line itself (`XS005_research.json` components).
- **BEA-2011 implicit depreciation rate `z`** — taken directly from the BEA-2011 vintage FA tables, i.e.
  the infinite-life geometric rate BEA itself uses. XS005 deliberately **does not** substitute the BEA-1993
  rates (that is XS006's job).
- **The GPIM machinery** is inherited from XS004 (`XS005_research.json` components: "Baseline GPIM
  machinery — source: XS004").

Appendix Table 6.7.13 (book **p. 845**, `XS005_research.json` book_quotes[1]) records the three candidate
1925 values — **BEA 2011 = 98.1 (100%)**, BEA 1993 = 77.7 (79%), SCB 1985 = 67.1 (68%); XS005 uses 98.1.
Published values transcribed verbatim from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx`.
All BEA data at the 2011 vintage (Appendix 6.7 fn 1, book p. 828).

## 3. Why these sources, from Shaikh's perspective + rejected alternatives — **the central rationale**

XS005 answers a **methodological-trust question**, not an empirical-measurement one. Before Shaikh is
entitled to *reject* BEA's published stock (as he does in XS004 via BEA-1993 depreciation + the interwar
anchor), he must first show his regeneration engine is faithful when fed BEA's own assumptions. That is
XS005's entire reason to exist:

1. **Validate the GPIM machine.** `XS005_research.json` methodology_notes[3]: "XS005 is mechanically the
   simplest variant — it is the GPIM regenerator applied with no adjustments, used to verify the 99.6%
   accuracy match against official BEA KNCcorpbea (Appendix Table 6.7.12, p. 844)." If the pure regenerator
   did *not* reproduce BEA to ~99.6%, every downstream variant would be suspect. XS005 is the control.

2. **Establish the convergence property that licenses XS004's initial-value choice.** Shaikh (book
   **p. 845**, `XS005_research.json` book_quotes[2]): "But since all starting points end up on the same path
   in the long run, the lower initial values must grow faster to catch up with the common long-run path …
   This property turns out to have major consequences for the path of the postwar capital stock when we
   adjust for the effects of the Great Depression." Quantified (methodology_notes[1]): the 31% initial
   BEA-1993-vs-2011 gap in 1925 is down to **10% by 1947** and all variants are **within 2% by 1969**
   (Appendix Figure 6.7.4, p. 846). This is *why* XS004 can safely anchor on the highest-quality 98.1
   initial value — the choice is nearly washed out by the postwar period.

3. **It is the fixed reference axis of the four-variant counterfactual design.** `XS005_research.json`
   methodology_notes[0]: "XS005 holds the BEA 2011 initial value (98.1 bill$) fixed, providing the reference
   path … The difference between XS005 and XS006/XS007/XS008 isolates the effect of each perturbation."
   `CH6_GPIM_SUMMARY.md` (Sensitivity Variant Summary) frames it bluntly: "XS005 is the 'what if we just
   trusted BEA 2011 entirely' baseline; XS004 is the 'what Shaikh actually uses' corrected measure.
   Comparing XS005 vs XS004 quantifies the cumulative effect of the three corrections." Each of XS006 (dep.
   rate), XS007/XS008 (interwar), and XS004 (all combined) is measured **against XS005**.

**Rejected alternatives** (from Shaikh's perspective):
- **Using XS005 as the operational profit denominator** — rejected. It embodies exactly the two BEA
  choices Shaikh disputes: infinite-life geometric depreciation and an unsmoothed interwar path. It
  "cedes to BEA's infinite-life geometric assumption" (`XS005_research.json` open_questions[1]) and is
  therefore reserved for reference only; S601–S604 use XS004.
- **Perturbing the initial value as if it mattered much** — the convergence result shows the initial value
  is "largely cosmetic for post-1970 analysis (differences <2% by 1969)"; the substantive lever is the
  depreciation rate (`XS005_research.json` open_questions[1]). So XS005 fixes the initial value and lets
  XS006 carry the real methodological weight.

## 4. Methodological-change exposure

Same NIPA/BEA-vintage exposure as the rest of the GPIM chain, plus one XS005-specific wrinkle — its
validation target *moves with the vintage*:

- **2011-vintage freeze** (Appendix 6.7 fn 1, book p. 828). XS005 both reads BEA-2011 inputs **and**
  validates against the BEA-2011 published `KNCcorpbea`. A re-pull would change *both* sides.
- **2013 Comprehensive (14th).** R&D/entertainment capitalized → IPP; ≈ +$400B GDP; **Fixed-Asset /
  capital-stock levels rise**, NOS/CFC change (`NIPA_CHANGE_TIMELINE.md`). Because XS005's target
  `KNCcorpbea` is itself a BEA capital-stock level, the 99.6% match is a **vintage-specific** result — it
  need not hold if XS005 were regenerated on a 2013+ vintage against a 2013+ target.
- **2018 Comprehensive (15th)** — 2012-benchmark I-O, financial-services methods, T7.11 +1 line shift
  (`NIPA_CHANGE_TIMELINE.md`; bites XS003, not XS005 directly). **2023 (16th)** — reference year → 2017.
- **Anti-splice discipline** (`XS005_DPR.md` §Caveats; `XS005_EPR.md` §Anti-Degradation Compliance): never
  splice across a comprehensive-revision boundary. No IO-benchmark/concordance exposure of its own
  (`IO_CHANGE_TIMELINE.md` governs the Sraffa series, not the GPIM stock).

## 5. Replication fidelity note

- **Bit-exact melt at 1.0% tolerance.** `V03_XS005.py` round-trips the chopped KNCcorp'/KNCcorpbea/ratio
  columns against Appendix Table 6.8.II.1 (`XS005_DPR.md` §Validation Expectation). The group hand-check
  record is `mae = 0.0` fidelity to the Shaikh workbook (`CH_XS_review.json` strengths[0]).
- **Formula-declared-but-transcribed (finding F-XS-05, MEDIUM).** As with all XS003–XS009, XS005 declares
  `construction: formula` but ships `components:[]` and no executable formula field; the runtime path is
  **`L01_XS005.py` loading Shaikh's finished columns + `P02_XS005.py` schema-only pass-through**. The GPIM
  rule and the 99.6% validation live in DPR prose + `CH6_GPIM_SUMMARY.md` + the **deferred v1.1 EPR**
  recompute (`XS005_EPR.md` §Method; `CH_XS_review.json` F-XS-05). So V03 confirms *melt fidelity to
  Shaikh's numbers*, not an independent re-run of the GPIM against BEA components.
- **Units defect on the ratio subseries (finding F-XS-01, HIGH).** The pure-GPIM/BEA ratio **XS005-C
  (= 1.0)** is **dimensionless** but the chopped artifact mislabels it `billions_current_usd` — the
  single-string L01 unit hardcode again. Must move to per-subseries units before external distribution
  (`CH_XS_review.json` F-XS-01, D14 gate; evidence "chopped/XS005.csv XS005-C rows").
- **Stale validator name (F-XS-06, LOW).** DPRs cite legacy `V03_..._validate.py`; actual is `V03_XS005.py`.

## 6. Forward risk

- **Vintage-moving validation target.** The 99.6% GPIM-vs-BEA match is a **2011-vintage** fact; any
  re-derivation must regenerate XS005 and re-fetch `KNCcorpbea` on the *same* vintage or the diagnostic is
  meaningless (`NIPA_CHANGE_TIMELINE.md`; §4).
- **Extension is "mostly cosmetic."** `XS005_research.json` extension_candidates[0].concerns: post-2011 the
  1925 initial value is long since washed out, so an extended XS005 "exists primarily to maintain parallel
  structure with XS006–XS008 variants for sensitivity reporting." The substantive post-2011 questions
  (depreciation rate, IPP inclusion) belong to XS006/XS004, not here (`XS005_research.json`
  open_questions[1]).
- **Shared BEA-1993 archive dependency (indirect).** XS005 itself needs no BEA-1993 rates, but its role as
  the *reference axis* is only meaningful alongside XS006/XS004, whose recompute depends on the recovered
  `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/` archive (see XS004/XS006 MHRs).
- **Baseline-confusion guard.** Keep XS005 documented as the *reference*, not the operational baseline;
  confirm S601–S604 cite XS004 (`XS005_research.json` open_questions[0]; `CH6_GPIM_SUMMARY.md`
  open-question 1). Optional: track Appendix Figure 6.7.4's three lines (KNCcorpbea, KNCcorp1', KNCcorp2')
  as explicit subseries (`XS005_research.json` open_questions[2]).
