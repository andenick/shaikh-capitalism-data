# XS004 — Methodological History Report (MHR)

**Series**: XS004 — GPIM Corporate Capital Stock (Operational Baseline): KNCcorp / KGCcorp / KNHcorp
**Chapter**: 6 (Capital and Profit) · **Group**: XS · **xs_class**: appendix · **CD2 predecessor**: S209
**Perspective**: authored *from Shaikh's perspective* — why he built the corporate capital denominator this way.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS004_research.json`; `Technical/docs/series/XS004_DPR.md` +
`XS004_EPR.md`; `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`;
`Technical/methodology_review/CH_XS_review.json`; Phase-0
`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md` (+ `IO_CHANGE_TIMELINE.md`);
`Technical/docs/methodology/NIPA_T711_FISIM_remap.md`;
`SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/`.

---

## 1. What it is

XS004 is Shaikh's **preferred, operational corporate capital-stock denominator** — the object that sits
under the "corrected" corporate profit rate of Chapter 6. It ships three current/historical-cost stock
columns transcribed verbatim from **Appendix Table 6.8.II.5** (`XS004_DPR.md` §Sources):

- **XS004-A `KNCcorp`** — corporate **net** current-cost fixed capital stock (the profit-rate denominator);
- **XS004-B `KGCcorp`** — corporate **gross** current-cost fixed capital stock;
- **XS004-C `KNHcorp`** — corporate **net historical-cost** fixed capital stock.

It is *not* a plotted book series; it is a construction internal (Decision 0002, `CH6_GPIM_SUMMARY.md`
lines 11-13) that feeds the final Chapter-6 profit-rate series **S601–S604** as the capital denominator
(`CH6_GPIM_SUMMARY.md` "How XS001–XS009 feed S601–S604"; `XS004_research.json` methodology_notes[4]).

The construction is the **Generalized Perpetual Inventory Method (GPIM)**. The book's own accumulation
rules (Shaikh 2016, Appendix 6.5 §V.3, **p. 820**, quoted verbatim in `XS004_research.json`
book_quotes[0]):

> "With this, we can express the Generalized PIM (GPIM) accumulation rules for aggregate historical,
> current, and constant cost stocks previously stated in equations (6.5.17) and (6.5.18) as … KNH = INH +
> KNH(-1) where INH = IGC − DEPH, DEPH = historical cost depreciation … KCt = IGt + (1 − zt)
> (pK't/pK'(t−1)) KC(t−1) … KRt = (pIt'/pKt') IGRt + (1 − zt) KR(t−1) = IGt/pKt' + (1 − zt) KR(t−1)."

In the RSCD DPR this is compressed to the current-cost net-stock line (`XS004_DPR.md` §Construction; the
DPR labels it "eq. 6.57" — a cross-doc numbering inconsistency flagged as cosmetic finding F-XS-08):

> `KNCnew = IGC + (1 − dcorpnew)·(pKN/pKN(−1))·KNCnew(−1)`

with **BEA-2011 initial value 98.1 (1925)**, **BEA-1993 finite-life depreciation rate `dcorpnew`**, and the
**IRS interwar multiplier (XS008) applied 1925–1947**. Because that interwar anchor pulls the 1925 starting
point down, XS004's published 1925 `KNCcorp` is **77.77**, not 98.1 (see §5 hand-check).

**Hand-check (bit-exact):** `CH_XS_review.json` hand_checks[0] — chopped KNCcorp/KGCcorp/KNHcorp vs book
Table 6.8.II.5 is **EXACT to 14 significant figures** (1925 `KNCcorp` = 77.77; 1926 = 81.25391618497109);
V03 `mae = 0.0`, `max_pct_err = 0.0`, `n = 261`. Book period **1925–2011** (`XS004_DPR.md` §Year Coverage).

## 2. Source lineage

Two data eras, one iterated stock (`XS004_research.json` primary_source; `CH_XS_review.json`
touchpoints XS004 — kind **NIPA/BEA-FA**):

- **BEA Fixed Asset Accounts (2011 vintage), corporate legal-form line.** The GPIM's flow and price inputs
  come from four Fixed Asset tables (`XS004_research.json` components; `CH_XS_review.json` XS004 note "BEA
  Fixed Asset T6.1/T6.4/T6.7/T6.8 + NIPA CFC"):
  - **FA T6.1** — Current-Cost Net Stock of Private Fixed Assets by Industry Group and Legal Form
    (corporate line 1) → the **1925 initial value 98.1** and the level benchmark;
  - **FA T6.4** — Chain-Type Quantity Indexes → the real/chain deflators `pK'`, `pI'`;
  - **FA T6.7** — Investment (corporate) → gross investment `IG`/`IGC`/`IGR`;
  - **FA T6.8** — Current-Cost Depreciation → the depreciation flow cross-check.
  Plus **NIPA CFC** (consumption of fixed capital) as the depreciation counterpart.
- **BEA 1993-vintage depreciation/retirement rates** (pre-1997 finite-life methodology). These are *not*
  in current BEA iTable. RSCD recovered them (Phase-5 Blocker B3) from Shaikh's own posted
  **Appendix Table 6.8.II.3** (`Appendix6_Table68II3.xlsx`, MD5 `9cdbdf5628837e07856b92925c89599a`) and
  staged them machine-readable at
  `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/BEA_1993_depreciation_retirement_rates.csv`
  (`XS004_research.json` phase5_recovered_inputs; review_history[2]). Variables used: **`dcorpnew`**
  (depreciation rate 1926–2011) and **`rho_corpnew`** (retirement rate 1926–2011); **1990–2011 values are
  Shaikh's own linear projections** from the BEA-1993 raw 1925–1989 series.
- **IRS book values via Census Historical Statistics 1975 (Series V115)** — the interwar (Great
  Depression/WWII) anchor for 1925–1947, entering XS004 through the **XS008** multiplier ratio
  (`XS004_research.json` methodology_notes[3]; `CH_XS_review.json` XS008 note).

The published stock columns themselves are transcribed verbatim from Shaikh's posted Appendix-6.8 workbook
`SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (`XS004_DPR.md` §Sources). Appendix
6.7 footnote 1 (book p. 828) fixes **all** BEA inputs at the **2011 vintage**.

## 3. Why these sources, from Shaikh's perspective + rejected alternatives — **the central rationale**

Shaikh does **not** accept BEA's published corporate net stock as his profit denominator. He rebuilds it
with the GPIM. Four intertwined reasons, all traceable to Appendix 6.7:

1. **He needs a *recomputable* stock, and post-1997 BEA aggregates are not.** The defining measurement
   problem (`XS004_research.json` methodology_notes[0]): "post-1997 BEA capital stocks are chain-weighted
   aggregates that do not obey the simple PIM rule, making it impossible to construct alternate measures by
   varying depreciation, retirement, or initial-value assumptions." Shaikh derives a chain-weighted
   accumulation rule (eqs 6.5.22–6.5.23, book p. 821) that *does* apply to aggregates, so he can
   **regenerate** the stock under his own assumptions instead of accepting BEA's black-box aggregation.

2. **He rejects BEA's post-1997 infinite-life depreciation on classical grounds.** The 1997 BEA switch
   assumes "assets are never scrapped." Shaikh (book **p. 845**, `XS006_research.json` book_quotes[0]):
   "Prior to 1997, the BEA assumed that different types of individual assets had different types of useful
   lives. This was superior to the current BEA assumption that assets are never scrapped." So he swaps in the
   **BEA-1993 finite-life** depreciation/retirement rates (`dcorpnew`, `rho_corpnew`) — the object isolated
   by XS006 — as the depreciation channel of XS004.

3. **He rejects BEA's smooth interwar capital path.** BEA's methodology assumes "depletion rates … invariant
   to economic conditions" (book p. 845), which mis-states the Depression/WWII collapse and recovery of the
   capital stock. Shaikh (book **p. 851**, `XS004_research.json` book_quotes[2]): "The estimated capital
   stocks are then adjusted in the previously described manner to allow for the effects of the Great
   Depression and World War II." That adjustment is the **IRS book-value index (XS007/XS008)** applied
   1925–1947 — which is why XS004's 1925 value is 77.77, below BEA's 98.1.

4. **He keeps BEA's 2011 initial value even while rejecting its depreciation.** Book **p. 851**
   (`XS004_research.json` book_quotes[2]): "The depletion (depreciation and retirement) rates are taken from
   BEA 1993. So too are the initial values for each type of stock, because these are typically estimated on
   the basis of assumed depletion rates." Appendix Table 6.7.13 (book **p. 845**, `XS004_research.json`
   book_quotes[1]) lists the three candidate 1925 values — **BEA 2011 = 98.1 (100%)**, BEA 1993 = 77.7 (79%),
   SCB 1985 = 67.1 (68%) — and XS004 anchors on the BEA-2011 98.1. He can afford to, because the initial
   value washes out ("Only one-third of any initial difference in 1925 remains in 1947", book p. 845; the
   convergence property that XS005 isolates).

**XS004 = the sum of these three deliberate corrections.** `CH6_GPIM_SUMMARY.md` (Sensitivity Variant
Summary, p. 851 ref) states it exactly: the preferred XS004 combines **initial value = BEA 2011 (XS005's
anchor)** + **depreciation = BEA 1993 finite-life (XS006's perturbation)** + **interwar = IRS book-value
(XS007/XS008's perturbation)**. The four variants XS005–XS008 are **not competing baselines** — each is a
counterfactual that isolates exactly **one** of XS004's construction choices, so the reader can price each
correction:

| Variant | Isolates | Holds fixed |
|---|---|---|
| **XS005** | initial-value choice (BEA-2011 98.1) | BEA-2011 depreciation, no interwar adj. |
| **XS006** | depreciation choice (BEA-1993 finite-life) | BEA-2011 init 98.1, no interwar adj. |
| **XS007/XS008** | interwar anchor (IRS book value 1925–47) | — |
| **XS004** | *all three combined* (operational) | feeds S601–S604 |

**Rejected alternatives** (from Shaikh's perspective):
- **BEA's published corporate net stock KNCcorpbea** — rejected as the denominator because it is
  chain-aggregated (non-recomputable), uses infinite-life depreciation, and smooths the interwar. It is
  retained only as a *validation target* (XS005 matches it to ~99.6% to prove the GPIM machine is sound
  before perturbing it — `XS004_research.json` methodology_notes[1], Appendix Table 6.7.12, p. 844).
- **The SCB-1985 (67.1) or BEA-1993 (77.7) 1925 initial value** as the anchor — rejected because the
  initial value is nearly irrelevant to the postwar path (convergence, book p. 845); the *depreciation* and
  *interwar* choices carry the substance, so the highest-quality (BEA-2011) initial value is used.
- **Splicing BEA's post-2011 revised levels onto the book series** — forbidden (see §4).

## 4. Methodological-change exposure

XS004's inputs are the part of the GPIM most exposed to NIPA/BEA vintage drift, because comprehensive
revisions move *capital-stock levels* directly (`NIPA_CHANGE_TIMELINE.md` "Why this matters for RSCD"):

- **2011-vintage freeze.** Appendix 6.7 footnote 1 (book p. 828) pins every BEA input at the **2011
  vintage**. XS004 must be read on that vintage; any re-pull lands on reclassified magnitudes.
- **2013 Comprehensive (14th, rel. 2013-07-31).** R&D + entertainment/literary/artistic originals
  capitalized → new **IPP** category; ≈ **+$400B** GDP; explicitly **"Fixed Assets / capital-stock levels
  rise"** and NOS/CFC change (`NIPA_CHANGE_TIMELINE.md` comprehensive-revision table). This directly
  re-levels FA T6.1/T6.4/T6.7/T6.8 and the corporate stock XS004 reads. Shaikh's 2011 definition **excludes**
  IPP, so a post-2013 extension must decide explicitly whether to add R&D/entertainment originals or match
  the 2011 exclusion (`XS004_research.json` open_questions[1]; extension_candidates[0].concerns).
- **2018 Comprehensive (15th).** 2012-benchmark I-O + financial-services methods; the **T7.11 +1 line
  shift** (`NIPA_CHANGE_TIMELINE.md` "Table-renumbering" §1) — this bites XS003's FISIM recipe, not XS004
  directly, but XS004's sibling in the same pipeline shares the vintage, so a coherent extension must move
  the whole chain together (`NIPA_T711_FISIM_remap.md`).
- **2023 Comprehensive (16th).** Reference year → 2017; 2017-benchmark supply-use.
- **Hard rule:** never splice XS004 across a comprehensive-revision boundary; recompute end-to-end on one
  coherent vintage (`NIPA_CHANGE_TIMELINE.md`; `CH6_GPIM_SUMMARY.md` open-question 5; `XS004_DPR.md`
  §Caveats). No IO-benchmark/concordance exposure of its own (that is the Sraffa XS2001/XS2101 series;
  `IO_CHANGE_TIMELINE.md`).

## 5. Replication fidelity note

RSCD reproduces XS004 **bit-exact to Appendix Table 6.8.II.5** — but by **transcription, not
recomputation**, and the honesty of that distinction is the load-bearing caveat:

- **Bit-exact melt.** V03 round-trips the chopped columns against the Appendix-6.8 workbook at 1.0%
  tolerance; observed **`mae = 0.0`, `max_pct_err = 0.0`, `n = 261`, EXACT to 14 sig figs** (1925
  `KNCcorp = 77.77`, 1926 `= 81.25391618497109`) (`CH_XS_review.json` hand_checks[0], strengths[0]).
- **Formula-declared-but-transcribed (finding F-XS-05, MEDIUM).** XS004 declares `construction: formula`
  and its DPR/research carry the full GPIM equation, **but the registry `components:[]` is empty and there is
  no executable `formula` field** (`CH_XS_review.json` F-XS-05). The real executable path is a **pass-through
  transcription** of Shaikh's finished workbook: **`L01_XS004.py` loads the finished KNCcorp/KGCcorp/KNHcorp
  columns; `P02_XS004.py` is a schema-only pass-through**; the GPIM formula lives only in DPR prose +
  `CH6_GPIM_SUMMARY.md` + the **deferred v1.1 EPR** extension recipe (`XS004_EPR.md` §Method/Anti-Degradation
  Compliance). So "V03 mae 0.0" confirms **melt fidelity against Shaikh's own numbers**, not an independent
  end-to-end re-derivation of the GPIM from BEA components. Honest, and disclosed.
- **Units label defect (finding F-XS-01, HIGH).** `L01_XS004.py:49` hardcodes a single series-level unit
  string `"billions_current_usd"`; that is correct for KNCcorp/KGCcorp/KNHcorp (all billion-dollar stocks),
  but the same hardcode pattern mislabels dimensionless/rate subseries elsewhere in the group (XS005-C ratio,
  XS006 depreciation rate) — must be per-subseries before external distribution (`CH_XS_review.json`
  F-XS-01, D14 gate).
- **Stale validator name (F-XS-06, LOW).** `XS004_DPR.md:44` cites `V03_XS004_validate.py`; the actual
  post-Decision-0004 name is `V03_XS004.py`.

## 6. Forward risk

- **BEA-1993 archive is the recompute bottleneck.** A genuine end-to-end GPIM recompute (the v1.1 EPR)
  needs the BEA-1993 finite-life depreciation/retirement rates, which are **not in current BEA iTable**.
  RSCD's only source is Shaikh's posted `Appendix6_Table68II3.xlsx`, staged at
  `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/` (`XS004_research.json`
  phase5_recovered_inputs; open_questions[0]). Because **1990–2011 `dcorpnew`/`rho_corpnew` are Shaikh's own
  linear projections**, and 2012+ has no BEA-1993 basis at all, the EPR recipe **freezes the rate inputs at
  the 2011-vintage projection** (`XS004_EPR.md` §Method step 4, Failure Mode Table; README provenance).
- **IPP reclassification breaks the definition on extension.** Post-2011 R&D/entertainment capitalization
  changes what "corporate fixed capital" *means*; an extension must take an explicit stance (match Shaikh's
  IPP-exclusive 2011 definition, or build an IPP-inclusive parallel) rather than silently absorbing the new
  category (`XS004_research.json` open_questions[1]; extension_candidates[0].concerns).
- **Never splice.** Post-2011 BEA levels (2013 +$400B re-level, 2018/2023 revisions) must not be
  growth-spliced onto the book series; re-fetch and re-run on one vintage (`XS004_EPR.md`
  §Anti-Degradation Compliance; `NIPA_CHANGE_TIMELINE.md`).
- **Downstream confirmation.** Confirm S601–S604 cite XS004 (not XS005) as the operational denominator and
  reserve the variants for sensitivity reporting (`XS004_research.json` open_questions[2];
  `CH6_GPIM_SUMMARY.md` open-question 1).
