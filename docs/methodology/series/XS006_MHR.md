# XS006 — Methodological History Report (MHR)

**Series**: XS006 — GPIM Variant, BEA-1993 Finite-Life Depreciation: KNCcorpnew / KNCbea93 / dcorpnew
**Chapter**: 6 (Capital and Profit) · **Group**: XS · **xs_class**: appendix · **CD2 predecessor**: S211
**Perspective**: authored *from Shaikh's perspective* — why he swaps in the pre-1997 depreciation rate.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS006_research.json`; `Technical/docs/series/XS006_DPR.md` +
`XS006_EPR.md`; `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`;
`Technical/methodology_review/CH_XS_review.json`; Phase-0
`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md` (+ `IO_CHANGE_TIMELINE.md`);
`SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/`.

---

## 1. What it is

XS006 is the **depreciation-rate counterfactual** of the GPIM design: it runs the identical GPIM machine as
XS005 but swaps BEA's post-1997 **infinite-life geometric** depreciation for the pre-1997 **BEA-1993
finite-life** depreciation/retirement rates, holding everything else fixed. It isolates **one** of XS004's
three corrections — the depreciation-methodology change — so the reader can price it alone
(`XS006_DPR.md` §Why It Matters; `XS006_research.json` methodology_notes[0]).

RSCD ships **two sub-variants** (Phase-4 Q1 disposition, `XS006_DPR.md` §Construction), transcribed from
**Appendix Table 6.8.II.3**:
- **XS006-depr_only `KNCcorpnew`** — BEA-1993 depreciation rate **+ BEA-2011 initial value 98.1** (the
  *pure* depreciation-rate variant that matches the book text, p. 846);
- **XS006-depr_plus_init `KNCbea93`** — BEA-1993 depreciation rate **+ BEA-1993 initial value 77.769** (the
  variant that reproduces CD2's S211 sample values);
- **XS006-dcorpnew `dcorpnew`** — the BEA-1993 finite-life depreciation-rate series itself (a decimal, ~0.07).

GPIM rule (`XS006_research.json` formula; DPR labels it "eq. 6.57", book eqs 6.5.22–6.5.23 p. 821):
> `KC_t = IG_t + (1 − z_t)·(pK'_t/pK'_{t−1})·KC_{t−1}`, with **`z_t` derived from BEA-1993** (`dcorpnew`,
> `rho_corpnew`) rather than BEA-2011.

Book period **1925–2011** (`XS006_DPR.md` §Year Coverage). Sensitivity variant — not a profit denominator;
XS004 is (`CH6_GPIM_SUMMARY.md`).

**Open-Q2 caution (documented conflation risk).** CD2's S211 sample values (1925 = **77.769**) coincide with
the **BEA-1993 initial value 77.7**, suggesting **CD2 may have conflated** the depreciation-rate variant with
an *initial-value* variant (`XS006_research.json` open_questions[0]; `CH6_GPIM_SUMMARY.md` open-question 2).
Per book **p. 846**, the correct XS006 should hold the **BEA-2011 initial value** and change **only** the
depreciation rate. RSCD's resolution is to ship *both* sub-variants explicitly and flag which is which
rather than silently pick one (`XS006_EPR.md` §CD2 Divergence Pre-Disclosure).

## 2. Source lineage

Cross-vintage: pre-1997 rates + post-1997 flows (`XS006_research.json` primary_source; `CH_XS_review.json`
touchpoints XS006 — kind **NIPA/BEA-FA**, note "BEA 1993 SCB Table A.13 finite-life depreciation vs BEA 2011
infinite-life geometric; depreciation-rate sensitivity"):

- **BEA-1993-vintage depreciation & retirement rates** — the defining input. Sourced to **BEA 1993 Table
  A.13, p. 294** (the Survey of Current Business 1993 vintage), with **Gorman, Musgrave, Silverstein &
  Comins 1985 (SCB 1985)** as the cross-check (`XS006_research.json` primary_source; book_quotes[1]).
  Because these are **not in current BEA iTable**, RSCD recovered them (Phase-5 Blocker B3) from Shaikh's
  posted **Appendix Table 6.8.II.3** (`Appendix6_Table68II3.xlsx`, MD5
  `9cdbdf5628837e07856b92925c89599a`) and staged them at
  `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/BEA_1993_depreciation_retirement_rates.csv`
  (`XS006_research.json` phase5_recovered_inputs; review_history[2]). Variables: **`dcorpnew`** (depreciation
  rate), **`rho_corpnew`** (retirement rate), and **`KNCbea93`[1925] = 77.769** (the BEA-1993 initial value
  for the depr_plus_init sub-variant).
- **Post-1997 BEA investment flows** — gross investment `IG` from **FA T6.7** and price index `pK'` from
  **FA T6.4/T6.1**, 2011 vintage (`XS006_research.json` components). Shaikh takes the 1993-vintage aggregate
  rates "up to 1997, project[s] them into the present, and use[s] them in equations (6.5.22) and (6.5.23)"
  (book **p. 845**, `XS006_research.json` book_quotes[0]).
- **GPIM machinery** inherited from XS004/XS005.

Published stock columns transcribed verbatim from
`SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx`; all BEA inputs at the 2011 vintage
(Appendix 6.7 fn 1, book p. 828).

## 3. Why these sources, from Shaikh's perspective + rejected alternatives — **the central rationale**

XS006 is where Shaikh's **classical objection to the modern BEA depreciation methodology** becomes a
measurable number. His argument, verbatim (book **p. 845**, `XS006_research.json` book_quotes[0]):

> "Prior to 1997, the BEA assumed that different types of individual assets had different types of useful
> lives. This was superior to the current BEA assumption that assets are never scrapped. However, both
> methodologies suffer from the defect that depletion rates are assumed to be invariant to economic
> conditions … We take these earlier aggregate retirement and depreciation rates up to 1997, project them
> into the present, and use them in equations (6.5.22) and (6.5.23)."

So the source choice is **theory-driven**, not convenience-driven:

1. **Finite service lives are the economically correct assumption; infinite lives are not.** The 1997 BEA
   switch to geometric/infinite-life depreciation "assume[s] that assets are never scrapped" — physically
   false. Shaikh (book **p. 846**, `XS006_research.json` book_quotes[1]): "the earlier depreciation rate is
   higher than the present one. This is essentially because the earlier BEA calculations were based on
   finite useful lives for fixed assets, whereas the present BEA ones assume infinite useful lives. Of
   particular note is the fact that the earlier BEA retirement rate is far lower than either of these."
   Empirically (`XS006_research.json` methodology_notes[1]): BEA-1993 depreciation ≈ **6.5–9.5%** vs current
   BEA **5–8%**; BEA-1993 retirement ≈ **2.2–3.7%** (much lower).

2. **The methodology switch materially mis-states the corporate stock, and XS006 quantifies by how much.**
   Book **p. 846** (`XS006_research.json` book_quotes[2]): "the new depreciation rate based on finite
   service lives … The new net stock estimates are generally lower than the current BEA ones, but the
   relative gap diminishes over time as the two converge. On the other hand, the new gross capital stock are
   larger than the modern BEA net stock estimates and grow faster over the postwar period." Net starts
   *below* BEA and converges from below; **gross ends ~68% higher by 2009** (Appendix Figure 6.7.7,
   `XS006_research.json` methodology_notes[1]). This is why XS006 is "one of three corrections (along with
   Great Depression interwar adjustment XS008 and IRS book-value XS007) that produce the 'corrected'
   KNCcorp Shaikh uses in S6xx final profit-rate measures" (`XS006_research.json` methodology_notes[3]).

3. **Isolation-by-design: change depreciation, nothing else.** To make the number attributable purely to the
   depreciation choice, XS006 **holds the BEA-2011 initial value 98.1 fixed** (`XS006_research.json`
   methodology_notes[0]; `CH6_GPIM_SUMMARY.md` Sensitivity Variant Summary — "BEA 1993 finite-life
   depreciation in place of BEA 2011 infinite-life geometric"). It differs from XS005 by **exactly one
   lever** (the depreciation/retirement rate); it differs from XS004 by the *absence* of the IRS interwar
   anchor.

4. **A convergence/divergence theory backs the choice.** The depletion rate `z` determines whether the
   gross-stock path converges to trend. Critical value **`z* = 0.0329`** (= `gK_p/(1+gK_p)` for `gK_p ≈
   0.034`, Appendix 6.7 §V.3, book p. 849, `XS006_research.json` components[2]/methodology_notes[2]).
   BEA-2011 net depreciation (5–8%) lies **above** `z*` (converges); BEA-1993 gross retirement (2.2–3.7%)
   **straddles** `z*`, explaining why the new gross-stock path does not converge to BEA's net-stock path —
   a genuine theoretical result, not an artifact.

**Rejected alternatives** (from Shaikh's perspective):
- **BEA's post-1997 infinite-life geometric depreciation** — rejected as the substantive engine (kept only
  as the XS005 reference); it "materially understates corporate capital stock" (`XS006_research.json`
  methodology_notes[3]).
- **Perturbing the initial value here** — rejected for the *pure* variant: XS006-depr_only holds 98.1 fixed
  so the effect is attributable to depreciation alone (book p. 846). The depr_plus_init sub-variant exists
  only to reproduce/expose CD2's conflated S211 path, not as Shaikh's recommended construction.
- **Discarding the low BEA-1993 retirement rate** — deliberately retained, because its being "far lower"
  is precisely the finding of note (book p. 846) and drives the gross-stock divergence.

## 4. Methodological-change exposure

XS006 is the GPIM series **most exposed to the very 1997 methodology break it is measuring**, plus the
standard post-2011 vintage drift:

- **The 1997 depreciation-methodology break is the object of study, not a hazard** — but it means XS006's
  BEA-1993 rate inputs stop at 1997; Shaikh **projects them "into the present"** assuming the asset mix is
  stable (book p. 845). For IPP-heavy post-2000 capital that assumption is "increasingly violated"
  (`XS006_research.json` extension_candidates[0].concerns).
- **2011-vintage freeze** (Appendix 6.7 fn 1, book p. 828) on the post-1997 investment flows (FA T6.7/T6.4).
- **2013 Comprehensive (14th).** R&D/entertainment → IPP; ≈ +$400B GDP; **Fixed-Asset / capital-stock
  levels rise**, CFC changes (`NIPA_CHANGE_TIMELINE.md`). This re-levels the FA T6.7 investment flows XS006
  reads and, critically, changes the *asset mix* underlying the projected BEA-1993 rates.
- **2018 (15th)** — 2012-benchmark I-O, T7.11 +1 line shift (bites XS003, shared vintage;
  `NIPA_CHANGE_TIMELINE.md` "Table-renumbering" §1). **2023 (16th)** — reference year → 2017.
- **Anti-splice discipline** (`XS006_DPR.md` §Caveats; `XS006_EPR.md` §Anti-Degradation Compliance): never
  splice across a comprehensive-revision boundary; recompute end-to-end on one vintage. No IO-benchmark
  exposure of its own (`IO_CHANGE_TIMELINE.md` governs the Sraffa series).

## 5. Replication fidelity note

- **Bit-exact melt at 1.0% tolerance.** `V03_XS006.py` round-trips the KNCcorpnew/KNCbea93/dcorpnew columns
  against Appendix Table 6.8.II.3 (`XS006_DPR.md` §Validation Expectation). CD2 parity check: S211 sample
  values (1925 = 77.769, 1949 = 155.144, 1973 = 922.601, 1979 = 1976.17) reproduce in the **depr_plus_init**
  sub-variant, confirming the port (`XS006_research.json` methodology_notes[3]).
- **Formula-declared-but-transcribed (finding F-XS-05, MEDIUM).** XS006 declares `construction: formula` but
  ships `components:[]` and no executable formula field; the runtime path is **`L01_XS006.py` loading
  Shaikh's finished columns + `P02_XS006.py` schema-only pass-through**. The GPIM rule, the `z*` theory, and
  the finite-vs-infinite-life argument live in DPR prose + `CH6_GPIM_SUMMARY.md` + the **deferred v1.1 EPR**
  recompute (`XS006_EPR.md` §Method; `CH_XS_review.json` F-XS-05). V03 confirms *melt fidelity to Shaikh's
  numbers*, not an independent end-to-end GPIM re-run with the BEA-1993 rates.
- **Documented sub-variant ambiguity (Open-Q2).** RSCD's honest resolution to the CD2 conflation is to ship
  **both** depr_only (book-text-faithful, init 98.1) and depr_plus_init (CD2-faithful, init 77.769) and tell
  the user to "inspect Appendix Fig 6.7.5 / 6.7.6 to confirm which Shaikh plots" (`XS006_EPR.md` §CD2
  Divergence Pre-Disclosure; `XS006_research.json` open_questions[0]). No silent choice was made.
- **Units defect on the rate subseries (finding F-XS-01, HIGH).** The **`dcorpnew`** depreciation-rate
  subseries (~0.07, dimensionless decimal) is **mislabeled `billions_current_usd`** in the chopped artifact
  — the single-string L01 unit hardcode. Must move to per-subseries units before external distribution
  (`CH_XS_review.json` F-XS-01, evidence "chopped/XS006.csv depreciation-rate rows"; D14 gate).
- **Stale validator name (F-XS-06, LOW).** DPRs cite legacy `V03_..._validate.py`; actual is `V03_XS006.py`.

## 6. Forward risk

- **BEA-1993 archive is the recompute bottleneck — acutely so for XS006.** XS006 *is* the BEA-1993
  depreciation variant, so a genuine recompute is impossible without `dcorpnew`/`rho_corpnew`, which are
  **not in current BEA iTable**. RSCD's only source is Shaikh's posted `Appendix6_Table68II3.xlsx`, staged
  at `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/` (`XS006_research.json`
  phase5_recovered_inputs; open_questions/extension concerns). Recovering the underlying **BEA 1993 Table
  A.13 (p. 294)** from the SCB-1993 archive would give an independent, non-Shaikh source and is the highest-
  value forward step for de-circularizing XS006's validation.
- **Rate projection breaks on IPP-heavy modern capital.** Shaikh's "project them into the present" assumes
  a stable asset mix; post-2000 IPP capitalization violates it, so the EPR **freezes the rate inputs at the
  2011-vintage projection** and any extension must flag this (`XS006_EPR.md` §Method step 4, Failure Mode
  Table; `XS006_research.json` extension_candidates[0].concerns).
- **Order-of-operations documentation for joint use.** When XS006 is combined with XS007 (IRS) and XS008
  (interwar) to build the corrected XS004, the sequence matters (XS006 changes depreciation; XS008 changes
  the 1925–1947 path; XS007 anchors to IRS book value) and must be documented to avoid double-counting
  (`XS006_research.json` open_questions[2]).
- **Never splice** post-2011 BEA levels onto the book series; re-fetch and re-run on one coherent vintage
  (`NIPA_CHANGE_TIMELINE.md`; `XS006_EPR.md` §Anti-Degradation Compliance).
