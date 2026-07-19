# XS008 — Methodological History Report (MHR)

**Series**: XS008 — GPIM Interwar Adjustment Multiplier (the IRS/BEA ratio, 1925=1.0)
**Chapter**: 6 (Capital and Profit) · **Group**: XS / appendix (`xs_class: appendix`, former CD2 S213)
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS008_research.json`; `Technical/docs/series/XS008_DPR.md` +
`XS008_EPR.md`; `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`;
`Technical/methodology_review/CH_XS_review.json`; Phase-0
`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`; `Technical/MIGRATION/crosswalk.csv`.

---

## 1. What it is

XS008 is the **atomic derived input** underneath XS007: the **interwar adjustment multiplier** itself —
the dimensionless, time-varying ratio of the IRS book-value index to the BEA historical-cost index over
**1925–1947**, normalized to **1.0 in 1925**. Where XS007 is the *applied product* (the adjusted
capital-stock levels), XS008 is the *multiplier series* that gets applied. It is the raw content of
**Appendix Table 6.8.II.5, column "Adj. Ratio"** and the substrate of **Appendix Figures 6.7.8/6.7.9**
(book pp. 849–851).

Single published subseries (`XS008_DPR.md` §Sources; transcribed from
`SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx`):

| Subseries | Variable | Meaning | Note |
|-----------|----------|---------|------|
| XS008-A | `Adj. Ratio` | IRS index / BEA 2011 historical-cost index, 1925=1.0 | Shaikh-computed; **dimensionless** |

Units: `dimensionless_ratio_1925eq1` (`XS008_DPR.md` §Units). Sample values from the CD2 S213 markdown
confirm it is a ratio near 1.0, **not** a capital-stock level: 1925 = 1.0000, 1927 = 1.1243,
1929 = 1.2475, 1933 = 1.1245 (`XS008_research.json` methodology_notes[0]).

Book rationale for the whole interwar experiment (Shaikh 2016, Appendix 6.7 §V.4, p. 849, quoted
verbatim, `XS008_research.json` book_quotes[0]):
> "Current BEA methodology assumes infinite service lives, which is why the earlier BEA methodology based
> on (point estimates of) actual useful lives is preferable. But both methodologies suffer from the fact
> that they assume that depletion rates are invariant to economic conditions. In this section, we examine
> the consequences of allowing for changes in depletion rates due to the cataclysmic events of the Great
> Depression and World War II. Here, we make use of the fact that historical net stock estimates derived
> via the PIM are analogous to company book value data on capital stocks."

The application rule (p. 849, `book_quotes[1]`, role=source):
> "Since current- and constant-cost capital stocks are based on the same depreciation rates as historical
> stocks, we can adjust all three for the effects of the interwar period by multiplying them by the IRS
> book value index from 1925 to 1947 and reverting to the GPIM calculation in equations (6.5.22) and
> (6.5.23) thereafter."

XS008 *is* "the IRS book value index from 1925 to 1947" expressed as a BEA-relative multiplier.

## 2. Source lineage

XS008 is a pure two-input ratio (`XS008_research.json` primary_source + components;
`CH_XS_review.json` touchpoints[XS008], kind = "BEA-FA/IRS"):

- **Numerator — IRS book-value index, 1925–1947.** Census 1975 Series V115, pp. 924–926 (the same
  historical archival input as XS007; `XS008_research.json` components[0]).
- **Denominator — BEA historical-cost index, corporate, 1925–1947.** BEA FA Table 6.3 (corporate
  historical cost), **2011 vintage** (`components[1]`).
- **The ratio itself (XS008-A).** `interwar_multiplier_t = IRS_index_t / BEA_historical_index_t`,
  normalized to 1.0 at 1925 (`XS008_research.json` formula; `components[2]`).

Downstream context (not inputs, but where XS008 is consumed): the multiplier is applied inside XS007
and, combined with the **BEA-1993 depreciation rates** (BEA 1993 SCB Table A.13, shared with XS006) and
the **BEA-2011 initial value** (XS005's anchor), produces the preferred KNCcorp = **XS004**
(`XS008_research.json` methodology_notes[3]; `CH6_GPIM_SUMMARY.md` "Sensitivity Variant Summary").

All BEA data pinned at the **2011 vintage** (Appendix 6.7 footnote 1, p. 828). Upstream agencies: IRS
SOI / U.S. Census Bureau (Historical Statistics) for the numerator, BEA (Fixed Asset Accounts) for the
denominator — all public domain (`XS008_DPR.md` §Sources).

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

**Why isolate the multiplier as its own series.** Shaikh (and RSCD after him) separates the *adjustment*
from the *adjusted product* so the magnitude, sign, and timing of the interwar correction can be
inspected and verified independently of the capital-stock path it modifies
(`XS008_research.json` methodology_notes[1]): "XS008 is the ATOMIC INPUT (the adjustment ratio time
series 1925–1947); XS007 is the APPLIED PRODUCT … Separating them allows the user to inspect the
magnitude of the interwar correction independently … and to verify the correction is applied with the
correct sign and timing." This is the same analytic-granularity logic Decision 0002 used to rehome the
whole GPIM chain as separate XS series rather than fold them into S601–S604.

**Why a ratio to BEA historical cost (1925=1.0).** Shaikh needs a *multiplicative* correction he can
apply uniformly to all three BEA stock concepts (historical, current, constant cost), which share the
same depreciation rates (`book_quotes[1]`). Expressing the IRS anchor as a BEA-relative index anchored to
1.0 in 1925 makes it a clean multiplier: multiply the BEA path by XS008 over 1925→1947, then hand back to
the GPIM. A level series (XS007) could not be reused across the three cost concepts without re-deriving
each; the ratio can.

**The empirical shape and why he trusts it.** The multiplier *rises* above 1.0 in 1927–1929 (IRS book
value grew faster than BEA's PIM-imputed historical stock pre-Depression — possibly asset revaluations or
definitional differences), then *declines* toward 1.0 as the Depression forces corporate write-downs that
bring IRS into line with BEA's smoother path (`XS008_research.json` methodology_notes[2]). By 1947 the
cumulative effect is IRS +20% vs BEA +52% from 1925 (p. 849). The whole point is that BEA's PIM assumes
"depletion rates are invariant to economic conditions" (`book_quotes[0]`); the multiplier *is* the
cycle-sensitivity BEA omits.

**Rejected alternatives (from Shaikh's own construction):**
- *Fold the correction into XS007 and never expose the ratio.* Declined — separating it is what allows
  independent sign/timing verification (`methodology_notes[1]`).
- *Extend the multiplier past 1947.* Rejected **by construction**: after 1947 the GPIM takes over and the
  ratio is 1.0 by definition (`XS008_research.json` open_questions[0]; extension_candidates[0]
  splice_strategy = "none"). XS008 is "intrinsically a 1925–1947 historical correction series; there is
  nothing to extend post-1947" (`XS008_DPR.md` §Caveats).
- *Apply BEA's own interwar path.* Rejected for the same reason as XS007 — BEA's cycle-invariant scrapping
  mis-states the Depression/WWII stock (`book_quotes[0]`).

## 4. Methodological-change exposure

XS008 is a **closed 1925–1947 historical object**; its numerator (Census V115) is frozen and its
denominator (BEA FA T6.3) is pinned at the 2011 vintage — so it carries no live-extension exposure. The
relevant vintage risk is entirely on the *denominator* and on the downstream XS004 that consumes it
(`NIPA_CHANGE_TIMELINE.md` "Why this matters for RSCD"):

1. **2011-vintage pin (Appendix 6.7 fn 1, p. 828).** The BEA historical-cost index in the denominator is
   the **2011** BEA FA T6.3 path. Re-pulling BEA FA on any later vintage would move the denominator and
   silently re-scale the multiplier — even though the numerator (IRS) is fixed.
2. **2013 comprehensive update (14th).** "Fixed Assets / capital-stock levels rise" from R&D/IPP
   capitalization (`NIPA_CHANGE_TIMELINE.md` row 2013-07). A re-vintaged BEA historical index would sit at
   a different level, distorting the 1925=1.0 normalization if naively recomputed.
3. **2018 comprehensive update (15th).** T7.11 +1 line shift (`NIPA_CHANGE_TIMELINE.md`
   "Table-renumbering"). XS008 does not read T7.11, but the XS004 baseline it feeds inherits XS003's
   FISIM-corrected profit inputs via `_nipa_t711_line_resolver.py` (stub-label remap, not line number).
4. **2023 comprehensive update (16th).** 2017 benchmark; reference year → 2017. Non-splice discipline.

Rule (CH6 open-Q5): recompute end-to-end on **one coherent vintage**, never splice across a
comprehensive-revision boundary (`NIPA_CHANGE_TIMELINE.md`). Because XS008 terminates in 1947 and its
numerator is immutable, in practice it is one of the least vintage-exposed series in the group — the risk
is confined to correctly re-vintaging the BEA denominator *if* the multiplier is ever recomputed rather
than transcribed.

## 5. Replication fidelity note

RSCD reproduces XS008 by the read-the-truth-column pattern: it transcribes the `Adj. Ratio` column of
Appendix Table 6.8.II.5 verbatim. `V03_XS008.py` round-trip-validates against the Appendix 6.8 source
workbook at **1.0% tolerance** (`XS008_DPR.md` §Validation Expectation; DPR cites the legacy name
`V03_XS008_validate.py` — cosmetic **F-XS-06**). Honest limits, disclosed:

- **Transcribed, not recomputed (F-XS-05, MEDIUM).** XS008 "declare[s] construction:formula but carr[ies]
  components:[] and no formula field." The executable path is a pass-through transcription of the workbook
  (L01 loads the finished `Adj. Ratio` column; P02 is schema-only). The ratio formula
  (`IRS_index / BEA_historical_index`, 1925=1.0) lives only in DPR prose + CH6 summary + the deferred v1.1
  EPR recipe (`CH_XS_review.json` findings F-XS-05; `XS008_EPR.md` Method + Anti-Degradation). Fidelity is
  melt fidelity against the identical workbook, not an independent recompute of the ratio from Census V115
  and BEA FA T6.3.
- **Dimensionless-units labeling risk (F-XS-01 / D14, HIGH — group-level).** XS008 is exactly the kind of
  **dimensionless/rate subseries** the group finding warns about: the review lists "XS005-C ratio, XS006
  depreciation rate" as mislabeled `billions_current_usd` in the chopped artifact
  (`CH_XS_review.json` findings F-XS-01; gate D14). XS008-A is `dimensionless_ratio_1925eq1` in the
  registry/DPR, but the honest MHR must flag that any single-series unit-string hardcode in the appendix
  L01 loaders would mislabel this ratio — the D14 gate (BELOW_90_BLOCKS_EXTERNAL) is precisely about this
  class of leak reaching the public chopped CSV.
- **CD2 parity.** CD2 S213 sample values (1925=1.0000 … 1943=1.0470) are near 1.0, confirming the series
  is a ratio not a level; round-trip parity expected within tolerance (`XS008_EPR.md` CD2 Divergence
  Pre-Disclosure; `XS008_research.json` open_questions[1] — confirm the series runs to 1947 where the ratio
  re-anchors to GPIM).
- **1927–1929 >1.0 values flagged for source-validation.** The pre-Depression multiplier >1.0 is
  anomalous (IRS grew faster than BEA imputed); flagged for Phase-4 scrutiny, not a fidelity failure
  (`XS008_research.json` open_questions[2]).

## 6. Forward risk

- **No forward extension by design.** XS008 is intrinsically 1925–1947; `extension_candidates`
  splice_strategy = "none", classification = `not_applicable_historical_correction` (`XS008_EPR.md`;
  `XS008_research.json` extension_candidates[0]). There is nothing to re-fetch — the numerator is a closed
  Census compilation and the multiplier is 1.0 after 1947 by construction. The *downstream effect* is
  carried forward only through XS004 (the preferred KNCcorp), never through XS008 itself.
- **Recompute (not transcription) would need the BEA-1993 archive + coherent BEA vintage.** If the v1.1
  EPR recipe ever recomputes the multiplier and its XS004 consumer end-to-end, it must (a) re-derive the
  BEA historical-cost denominator on a single coherent vintage (`NIPA_CHANGE_TIMELINE.md`) and (b) draw
  the BEA-1993 depreciation/retirement rates staged at
  `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/` for the XS004 tail (shared with
  XS006; `XS008_research.json` components[3]; `XS008_EPR.md` Failure Mode Table row 5).
- **Units remediation before external release.** The dimensionless-ratio labeling leak (F-XS-01) must be
  fixed in the chopped artifact before XS008 is publicly distributed (D14 gate;
  `CH_XS_review.json` gates D14).
