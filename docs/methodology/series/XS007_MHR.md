# XS007 — Methodological History Report (MHR)

**Series**: XS007 — GPIM Variant: IRS-Adjusted Corporate Capital Stock (interwar 1925–1947 anchor)
**Chapter**: 6 (Capital and Profit) · **Group**: XS / appendix (`xs_class: appendix`, former CD2 S212)
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS007_research.json`; `Technical/docs/series/XS007_DPR.md` +
`XS007_EPR.md`; `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`;
`Technical/methodology_review/CH_XS_review.json`; Phase-0
`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`;
`Technical/docs/methodology/NIPA_T711_FISIM_remap.md`; `Technical/MIGRATION/crosswalk.csv`.

---

## 1. What it is

XS007 is one of the four deliberate **GPIM counterfactual variants** (XS005–XS008) that isolate the
methodological choices behind Shaikh's corporate capital-stock denominator. Specifically, XS007 is the
**IRS book-value re-anchoring of the interwar 1925–1947 capital path** — the operational "Great
Depression / World War II" correction that the preferred final measure XS004 (KNCcorp) incorporates.
It is the data behind **Appendix Figures 6.7.8 and 6.7.9** (book pp. 849–851) and the columns of
**Appendix Table 6.8.II.4**.

The three published subseries (`XS007_DPR.md` §Sources), all transcribed from
`SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix Table 6.8.II.4):

| Subseries | Variable | Meaning | Note |
|-----------|----------|---------|------|
| XS007-A | `KTHcorpirs` | IRS book-value net capital stock, corporate (Census 1975 Series V115) | **×0.001 unit scale** (thousands → billions) |
| XS007-B | `KNCcorpbeaAdj` | IRS-adjusted BEA current-cost net stock | identity |
| XS007-C | `KNHcorpbeaAdj` | IRS-adjusted BEA historical-cost net stock | identity |

Book definition (Shaikh 2016, Ch6 Appendix 6.7 §V.4, p. 849, quoted verbatim in
`XS007_research.json` book_quotes[0]):
> "The US Historical Statistics of Income (Census 1975, Series V 115, 924–926) contains data on the
> book value of net capital assets of all corporations derived from US Internal Revenue Service (IRS)
> statistics. Net assets as defined there include land, but we can use them to estimate the path of the
> historical net capital stock. Appendix figure 6.7.8 compares the movements of BEA 2011 historical net
> stock to that of IRS book value stock, each indexed to 100 in 1925. … By 1947 the IRS book value index
> has risen by just 20%, whereas the BEA historical capital stock index has risen by 52% (appendix table
> 6.8.II.4). This difference is not surprising, given that the BEA measure is based on the assumption that
> scrapping of fixed capital is entirely independent of economic conditions."

The application rule (Shaikh, p. 849, `book_quotes[1]`, role=source):
> "Since current- and constant-cost capital stocks are based on the same depreciation rates as
> historical stocks, we can adjust all three for the effects of the interwar period by multiplying them by
> the IRS book value index from 1925 to 1947 and reverting to the GPIM calculation in equations (6.5.22)
> and (6.5.23) thereafter."

**Hand-check (the CH6 open-Q3 resolution).** `CH_XS_review.json` hand_checks records XS007 as
*EXACT* after the unit-scale fix: raw IRS `KTHcorpirs` 1925 = **93341.5159** (thousands) → **93.3415**
billions after `/1000`; XS007-B (`KNCcorpbeaAdj`) 1925 = **98.1**; XS007-C (`KNHcorpbeaAdj`) 1925 =
**69.2**. This "resolves CH6 open-question #3" (`CH6_GPIM_SUMMARY.md` Open Questions #3;
`XS007_research.json` open_questions[0]) — the ~1000× scale discrepancy in the CD2 S212 markdown was
simply that the raw IRS Series V115 is in **thousands of dollars**, not billions.

Appendix location: **Appendix 6.7 §V.4, book pp. 849–851** (narrative); the GPIM accumulation it
reverts to lives in **Appendix 6.5 eqs 6.5.22–6.5.23, pp. 807–821**.

## 2. Source lineage

XS007 fuses one historical archival input with the standard BEA-2011 GPIM stack
(`XS007_research.json` primary_source + components; `XS007_DPR.md`; `CH_XS_review.json` touchpoints[XS007]):

- **IRS book value, interwar 1925–1947 — Census 1975 Series V115.** "book value of net capital assets
  of all corporations derived from … (IRS) statistics," compiled in *Historical Statistics of the United
  States, Colonial Times to 1970*, Series V115, pp. 924–926 (public domain; Census Bureau Historical
  Statistics archive). This is the *only* net-capital measure that reflects company balance-sheet
  write-downs during the Depression. It is a **one-time frozen historical compilation** — not a live
  series (`XS007_EPR.md` Method: "Source data (Census 1975 Series V 115) is itself a one-time historical
  compilation").
- **BEA 2011 historical-cost net stock, corporate — BEA FA Table 6.3.** The denominator of the interwar
  index against which the IRS path is compared (`XS007_research.json` components[1]).
- **BEA 2011 current-cost net stock, corporate (`KNCcorpbea`) — BEA FA Table 6.1, line 2.** Rescaled by
  the IRS-anchored historical path to produce XS007-B (`components[2]`).
- **Post-1947 GPIM baseline — XS004 / eqs 6.5.22–6.5.23.** After 1947 the series "reverts to the GPIM
  calculation" (`book_quotes[1]`); the accumulation identity (DPR XS004) is
  `KNCnew = IGC + (1 − dcorpnew)·(pKN/pKN(−1))·KNCnew(−1)`.

All BEA data are pinned at the **2011 vintage** (Appendix 6.7 footnote 1, p. 828 —
`CH6_GPIM_SUMMARY.md` Open Question #5). Upstream agencies: U.S. Census Bureau (Historical Statistics),
IRS SOI, BEA (Fixed Asset Accounts / NIPA) — all public domain (`XS007_DPR.md` §Sources).

**Executable path (honest).** The RSCD loader does *not* re-fetch Census V115 and re-run the multiply;
it reads the finished `KTHcorpirs` / `KNCcorpbeaAdj` / `KNHcorpbeaAdj` columns verbatim from Appendix
Table 6.8.II.4 and applies only the `×0.001` scale to XS007-A (`XS007_DPR.md` §Construction; F-XS-05
below).

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

**Why anchor the interwar to IRS book values at all.** Shaikh's whole quarrel is with how BEA
*constructs* the pre-war capital path. BEA's published net stock is generated by a perpetual-inventory
method with (a) a post-1925 **initial value** and (b) depreciation/retirement that is invariant to the
business cycle. As he puts it (p. 849, `book_quotes[0]`): the BEA figure "is based on the assumption that
scrapping of fixed capital is entirely independent of economic conditions." The Great Depression drove
massive real scrapping and asset impairment that a cycle-blind PIM cannot see — so BEA's smooth
+52%-by-1947 path *overstates* surviving capital, while IRS book values (+20% by 1947) capture the
write-downs directly because firms had to mark down impaired assets on their tax balance sheets
(`XS007_research.json` methodology_notes[2]). Anchoring 1925–1947 to IRS lets Shaikh **recompute the
stock under his preferred, cycle-sensitive assumptions** rather than accept BEA's.

**Why IRS book value specifically (not FRB, not NIPA).** IRS corporate balance sheets are the only
source that (i) span the interwar window from the 1920s, (ii) cover *all* corporations (including
financial), and (iii) embody actual write-downs. NIPA and BEA-FA are model-imputed, not balance-sheet;
the FRB Flow of Funds is post-war and non-financial-only (the same coverage argument Shaikh makes
explicitly for inventories in XS009, book p. 851). Shaikh exploits the analogy that "historical net
stock estimates derived via the PIM are analogous to company book value data on capital stocks"
(`XS008_research.json` book_quotes[0]) — so an IRS book-value index is a *legitimate* re-anchor for a
PIM historical stock.

**Why a counterfactual variant, not a new baseline.** XS007 is one of four variants (XS005–XS008) that
each perturb exactly one GPIM choice — here the **interwar anchor** — holding the others fixed
(`CH6_GPIM_SUMMARY.md` "Sensitivity Variant Summary"; `XS007_research.json` methodology_notes[0]). The
empirical payoff: after adjustment the corporate net current-cost stock "starts out 28% lower in 1947 …
hence grows faster … [and] ends up on more or less the same path as the official measure by 1977"
(p. 849, `book_quotes[2]`). Isolating the interwar effect this way is what lets Shaikh attribute the
1947 gap between his KNCcorp and BEA's to a *combination* of lower initial value + interwar effect
(`XS008_research.json` book_quotes[2], p. 851).

**Rejected alternatives (from Shaikh's own text):**
- *Accept BEA's published net stock as-is.* Declined — it embeds cycle-invariant scrapping that
  mis-states the Depression/WWII path (`book_quotes[0]`).
- *Apply a modern IRS interwar-style correction to 2008/2020 shocks.* Shaikh does **not** do this; the
  correction is scoped strictly to 1925–1947 (`XS007_research.json` open_questions[1] flags it only as a
  possible future research extension).
- *Re-extend the adjustment past 1947.* Rejected by construction — post-1947 the series "reverts to the
  GPIM calculation" (`book_quotes[1]`); the IRS index is a one-time historical correction, not an
  ongoing input (`XS007_research.json` extension_candidates[0] concerns).

## 4. Methodological-change exposure

XS007's own *primary* input (Census V115, 1925–1947) is **frozen history** and cannot re-vintage — its
exposure is entirely *inherited* through the BEA-2011 stack it re-anchors and the post-1947 GPIM
baseline (XS004) it reverts to (`NIPA_CHANGE_TIMELINE.md` "Why this matters for RSCD"):

1. **2011-vintage pin.** All BEA inputs (FA T6.1/T6.3, and the CFC/NOS feeding the post-1947 GPIM) are
   fixed at the 2011 vintage per Appendix 6.7 footnote 1 (p. 828). The IRS-adjusted *ratios* are computed
   against the **2011** BEA historical index; re-pulling BEA FA on a later vintage would move the
   denominator and silently change the multiplier.
2. **2013 comprehensive update (14th, rel. 2013-07-31).** R&D + entertainment originals capitalized →
   new IPP category; "**Fixed Assets / capital-stock levels rise**," NOS/CFC change, and FISIM restated;
   ≈ +$400B GDP (`NIPA_CHANGE_TIMELINE.md` row 2013-07). Any re-pull of BEA FA T6.1/T6.3 past this
   boundary lands on higher capital levels — do not splice across it.
3. **2018 comprehensive update (15th, rel. 2018-07-27).** Inserted one monetary-interest sub-row in
   **T7.11 → +1 line shift** for every line ≥ 28 (`NIPA_CHANGE_TIMELINE.md` "Table-renumbering"; 
   `NIPA_T711_FISIM_remap.md`). XS007 does not read T7.11 directly, but its post-1947 GPIM baseline
   inherits XS003's corrected-profit inputs; the resolver `_nipa_t711_line_resolver.py` remaps by BEA
   `LineDescription` stub label, not line number (`XS007_EPR.md` Failure Mode Table row 4).
4. **2023 comprehensive update (16th, rel. 2023-09-28).** 2017 benchmark I-O; reference year → 2017.
   Same non-splice discipline applies (`NIPA_CHANGE_TIMELINE.md` row 2023-09).

Rule (CH6 open-Q5, `NIPA_CHANGE_TIMELINE.md`): any extension must recompute end-to-end on **one coherent
vintage** — never splice across a comprehensive-revision boundary. Because XS007 is a historical
correction that terminates in 1947, in practice only its post-1947 GPIM tail (via XS004) is vintage-
exposed; the interwar anchor is immutable.

## 5. Replication fidelity note

RSCD reproduces XS007 **EXACT to the Appendix 6.8 workbook** — the `CH_XS_review.json` hand-check reports
1925 `KTHcorpirs` 93341.5159 → 93.3415 (after `/1000`), XS007-B = 98.1, XS007-C = 69.2, and lists XS007
among the series with "V03 mae=0.0" (strengths[0]). `V03_XS007.py` round-trip-validates against the
Appendix 6.8 source workbook at **1.5% tolerance** (`XS007_DPR.md` §Validation Expectation; note the DPR
still cites the legacy name `V03_XS007_validate.py` — cosmetic finding **F-XS-06**). Honest limits,
disclosed:

- **Transcribed, not recomputed (F-XS-05, MEDIUM).** XS007 "declare[s] construction:formula but carr[ies]
  components:[] and no formula field." The executable path is a **pass-through transcription** of Shaikh's
  Appendix Table 6.8.II.4 (L01 loads the finished `KTHcorpirs`/`KNCcorpbeaAdj`/`KNHcorpbeaAdj` columns; P02
  is schema-only). The GPIM re-anchoring formula (multiply BEA paths by the IRS index 1925→1947, revert to
  6.5.22–6.5.23) lives only in **DPR prose + CH6 summary + the deferred v1.1 EPR extension recipe**
  (`CH_XS_review.json` findings F-XS-05; `XS007_EPR.md` Method + Anti-Degradation Compliance). Fidelity is
  "melt fidelity," not an independent end-to-end recompute.
- **Unit-scale correctness confirmed.** The only non-identity transform in the loader is XS007-A `×0.001`;
  the hand-check verifies it produces the book-consistent 93.3415 (`XS007_research.json`
  phase5_recovered_inputs.unit_normalization_required; `XS007_DPR.md` §Caveats).
- **Units-artifact risk (F-XS-01 / D14, HIGH — group-level).** The chopped-CSV units column for the
  appendix XS group still leaks the banned string `mixed_billions_usd_and_decimal_rates` and mislabels
  dimensionless/rate subseries as `billions_current_usd` (`CH_XS_review.json` findings F-XS-01, gates
  D14). XS007's own subseries are genuine billions, but the group-wide fix must reach the chopped artifact
  before external distribution (D14 = BELOW_90_BLOCKS_EXTERNAL).
- **CD2 divergence pre-disclosed.** CD2 S212 raw values are ~1000× larger (thousands vs billions); the
  loader normalizes via scale = 1/1000 (`XS007_EPR.md` CD2 Divergence Pre-Disclosure).

## 6. Forward risk

- **GPIM end-to-end recompute needs the BEA-1993 archive.** A true (non-transcribed) rebuild of the
  post-1947 tail that XS007 reverts to requires the BEA-1993 finite-life depreciation/retirement rates
  staged at `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/`
  (`XS007_research.json` phase5_recovered_inputs.bea_1993_rates_dir; `XS007_EPR.md` Failure Mode Table
  row 5 — "freeze depreciation rate inputs at 2011-vintage projection"). This is the deferred v1.1 EPR
  recipe.
- **The interwar anchor itself is not a forward risk.** Census 1975 Series V115 is a closed 1925–1947
  historical compilation; there is nothing to re-fetch or re-vintage (`XS007_research.json`
  extension_candidates[0] concerns; `XS007_EPR.md` classification = `not_applicable_historical_correction`).
- **BEA re-vintaging on the post-1947 tail.** Any extension past 2011 must re-pull BEA FA on a single
  coherent vintage and re-run — never splice across 2013/2018/2023 (`NIPA_CHANGE_TIMELINE.md`).
- **Optional research extension (Shaikh does not do it).** Post-1990 IRS SOI corporate balance sheets
  could support a modern interwar-style correction for the 2008 or 2020 shocks; flagged as a possible
  Phase-5 extension only, not part of the book replication (`XS007_research.json` open_questions[1]).
