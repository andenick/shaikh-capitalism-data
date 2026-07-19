# XS009 — Methodological History Report (MHR)

**Series**: XS009 — IRS Corporate Inventories and Total Capital Stock (KTCcorp = KGCcorp + INVcorp)
**Chapter**: 6 (Capital and Profit) · **Group**: XS / appendix (`xs_class: appendix`, former CD2 S214)
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS009_research.json`; `Technical/docs/series/XS009_DPR.md` +
`XS009_EPR.md`; `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`;
`Technical/methodology_review/CH_XS_review.json`; Phase-0
`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`; `Technical/MIGRATION/crosswalk.csv`.

---

## 1. What it is

XS009 is the **corrected total-capital-stock denominator** for Shaikh's corporate profit rate — the
final object at the bottom of the GPIM pipeline. It adds **corporate inventories (INVcorp)** to the
adjusted **gross current-cost fixed capital (KGCcorp, from XS004)** to form the total capital stock
**KTCcorp = KGCcorp + INVcorp**. It is the data behind **Appendix Figure 6.7.10** and the columns of
**Appendix Table 6.8.II.6** (book pp. 851–852).

Three published subseries (`XS009_DPR.md` §Sources; transcribed from
`SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx`):

| Subseries | Variable | Meaning | Note |
|-----------|----------|---------|------|
| XS009-A | `INVcorp` | Corporate inventories, current cost, scaled to NIPA | already rescaled to billions in II.6 |
| XS009-B | `KGCcorp` | Adjusted gross current-cost corporate fixed capital | identity (from XS004) |
| XS009-C | `KTCcorp` | Total corporate capital stock = KGCcorp + INVcorp | identity |

Why it exists — the classical profit-rate denominator (`XS009_research.json` methodology_notes[0]):
KTCcorp is the denominator of the **final corrected corporate profit rate**, Ch6 §VIII equation (6.10):
`r = (P + NMINT) / (KGC₋₁ + INV₋₁)` (book p. 248). For Shaikh the profit-rate denominator must be **total
advanced capital = fixed + circulating (inventory) capital**, not fixed capital alone.

The coverage problem, in Shaikh's own words (Appendix 6.7 §VI, p. 851, verbatim,
`XS009_research.json` book_quotes[0]):
> "The remaining step is to estimate corporate inventories so as to add them to the adjusted gross
> current-cost capital stock. NIPA has industry data on private industries (NIPA table 5.8.5), but it is
> not by legal form. The Federal Reserve Board (FRB) Flow of Funds has current cost data on corporate
> inventories and capital stock but only for non-financial corporations."

The IRS bridge (p. 852, `book_quotes[1]`, role=source):
> "However, the IRS publishes corporate balance sheets beginning in 1926 and these contain data on
> inventories, and from 1990 to 2011 also data on net historical capital stock. The IRS data is based on
> samples, so we cannot apply it directly to the NIPA corporate sector. The procedure therefore has two
> steps: first, estimation of the ratio of inventories to historical cost fixed capital for the whole
> period from 1947 to 2011; second, rescale the implicit inventory levels to those of the corrected
> capital stocks in appendix 6.8.II.5 by multiplying the preceding inventory by the ratio of adjusted
> historical to current-cost fixed capital stock."

The linear-time backcast (p. 852, `book_quotes[2]`, role=method):
> "On the first step, the ratio of the IRS net book value stock to the BEA net historical stock in
> 1990–2011 turns out to be essentially a linear function of time, so it was extrapolated back to
> 1949–1989 and then multiplied by the BEA net historical stock to yield an estimate of the corresponding
> IRS book value stock. This is used to construct the IRS ratio of inventories to net book value over the
> whole period from 1947 to 2011 … Multiplying this ratio by the BEA corporate net historical stock
> essentially scales up IRS inventory levels to match NIPA data."

Appendix location: **Appendix 6.7 §VI, book pp. 851–852**; profit-rate equation **6.10, p. 248**.

## 2. Source lineage

XS009 is a **composite** — the only GPIM series whose construction is `composite` rather than `formula`
(`XS009_research.json` construction). Its inputs (`XS009_research.json` components;
`CH_XS_review.json` touchpoints[XS009], kind = "NIPA/BEA-FA/IRS"):

- **IRS corporate inventories (raw) — IRS SOI Corporation Source Book**, inventories line, 1926–present
  (`XS009_research.json` components[0]; primary_source). The only source with inventories for *all*
  corporations including financial.
- **IRS net historical capital stock, 1990–2011 — IRS SOI corporate balance sheets** (net depreciable
  assets at historical cost). Used to fit the IRS/BEA ratio (`components[1]`). *Discontinued after 2011*
  — the crux of the post-2011 proxy problem (§6).
- **BEA corporate net historical-cost stock — BEA FA Table 6.3** (`components[2]`; touchpoint cites
  "BEA FA T6.3").
- **BEA corporate current-cost net stock — BEA FA Table 6.1, line 2** (for the historical→current-cost
  rescale ratio; `components[3]`).
- **Adjusted gross current-cost fixed capital (KGCcorp) — XS004 output** (`components[4]`).
- **IRS/BEA ratio linear-time fit** — OLS on observed 1990–2011 IRS-to-BEA ratios, extrapolated back to
  1947–1989 (`components[5]`; `book_quotes[2]`).

Construction chain (`XS009_research.json` formula; `XS009_DPR.md` §Construction):
**Step 1** IRS_book_t = BEA_KNH_corp_t × irs_to_bea_ratio_t (linear-time fit backcast to 1947).
**Step 2** inv_ratio_t = IRS_inventories_t / IRS_book_t. **Step 3** INVcorp_t = inv_ratio_t ×
BEA_KNH_corp_t (rescale to NIPA-comparable level). **Step 4** KTCcorp_t = KGCcorp_t + INVcorp_t.
Post-2011: INVcorp_t = (INVcorp_2011 / KGCcorp_2011) × KGCcorp_t (**constant-ratio proxy** — see §6).

All BEA data pinned at the **2011 vintage** (Appendix 6.7 fn 1, p. 828). Upstream agencies: IRS SOI, BEA
(Fixed Asset Accounts / NIPA), FRB (referenced as rejected alternative) — public domain (`XS009_DPR.md`
§Sources).

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

**Why total capital must include inventories.** Shaikh's profit rate is the *classical* rate on **total
advanced capital**, which is fixed capital **plus circulating (inventory) capital**. The final corrected
denominator is therefore `KGC₋₁ + INV₋₁` in eq. (6.10) (book p. 248; `XS009_research.json`
methodology_notes[0]). Omitting inventories would understate the capital advanced and overstate the
profit rate. Empirically the effect is on the *level*, not the *trend*: inventories are "roughly stable as
a fraction of fixed capital," so adding them "has only a small effect on value added (less than 2%)" but
"is required for analytical completeness" (`XS009_research.json` methodology_notes[2], citing book
pp. 247–248, eqs 6.11).

**Why IRS SOI inventories specifically — the coverage triangle.** Only IRS reports inventories for **all**
corporations (`book_quotes[1]`). The two obvious alternatives fail on coverage (`book_quotes[0]`;
`XS009_research.json` methodology_notes[1]):
- **NIPA Table 5.8.5** has inventories by *industry* but **not by legal form** — cannot isolate the
  corporate sector.
- **FRB Flow of Funds** has corporate inventories at current cost but **only for non-financial
  corporations** — misses financial corporates.
IRS SOI is the only source that spans all corporations (and back to 1926), so Shaikh anchors on it — at
the cost of its sample-based nature, which forces the two-step rescale-to-NIPA bridge.

**Why the two-step linear-time bridge (rather than direct IRS levels).** "The IRS data is based on
samples, so we cannot apply it directly to the NIPA corporate sector" (`book_quotes[1]`). Shaikh does not
want IRS *levels*; he wants the IRS *inventory-to-capital ratio*, which he then applies to the
NIPA-comparable BEA capital stock. Because IRS net historical capital stock only exists 1990–2011, he
exploits the empirical regularity that the IRS/BEA net-stock ratio is "essentially a linear function of
time" and backcasts it to 1949–1989 to get an IRS book-value stock for the whole 1947–2011 window
(`book_quotes[2]`). This is what lets the inventory ratio be computed over the full period even though
direct IRS capital data is only two decades long.

**Why treat IRS inventories as current-cost without further adjustment.** IRS inventory data mixes FIFO
(historical cost at acquisition) and LIFO (current cost). Shaikh argues that because inventory turnover is
rapid, "even FIFO inventories are valued at fairly recent costs while LIFO ones are at current costs," so
the aggregate is "treated as approximately current-cost without further adjustment" (book p. 852;
`XS009_research.json` methodology_notes[4]).

**Rejected alternatives (from Shaikh's own text):**
- *NIPA T5.8.5 inventories.* Rejected — not by legal form (`book_quotes[0]`).
- *FRB Flow-of-Funds corporate inventories.* Rejected — non-financial only (`book_quotes[0]`). (Flagged
  as a *defensible substitute* for a future post-2011 fix in `XS009_research.json` open_questions[0]c.)
- *Apply IRS sample levels directly to NIPA.* Rejected — sample basis requires the ratio-and-rescale
  bridge (`book_quotes[1]`).

## 4. Methodological-change exposure

XS009 stacks the vintage exposure of both the BEA fixed-capital stack **and** the IRS SOI stream, on the
2011-vintage pin (`NIPA_CHANGE_TIMELINE.md` "Why this matters for RSCD"):

1. **2011-vintage pin (Appendix 6.7 fn 1, p. 828).** BEA FA T6.1/T6.3 (the rescale denominators) and the
   XS004 KGCcorp it adds to are all 2011-vintage.
2. **2013 comprehensive update (14th, rel. 2013-07-31).** R&D + entertainment capitalization →
   "**Fixed Assets / capital-stock levels rise**"; NOS/CFC change (`NIPA_CHANGE_TIMELINE.md` row
   2013-07). Because XS009 rescales IRS inventories by BEA net historical stock, a re-vintaged BEA
   denominator moves the scaled INVcorp level — do not splice across 2013.
3. **2018 comprehensive update (15th, rel. 2018-07-27).** T7.11 +1 line shift
   (`NIPA_CHANGE_TIMELINE.md` "Table-renumbering"; `NIPA_T711_FISIM_remap.md`). XS009 does not read T7.11
   directly, but its KGCcorp input (XS004) inherits XS003's FISIM-corrected profit inputs, remapped by
   `_nipa_t711_line_resolver.py` (stub label, not line number; `XS009_EPR.md` Failure Mode Table row 4).
4. **2023 comprehensive update (16th, rel. 2023-09-28).** 2017 benchmark; reference year → 2017. Same
   non-splice discipline (`NIPA_CHANGE_TIMELINE.md` row 2023-09).
5. **IRS SOI discontinuity (structural, not a NIPA revision).** IRS stopped publishing corporate **net
   historical capital stock** after 2011, breaking Step 1's ratio-fit input for any live extension
   (`XS009_research.json` extension_candidates[0] concerns; open_questions[0]). This is the CH6 open-Q4
   expedient, treated in §6.

Rule (CH6 open-Q5): recompute end-to-end on **one coherent vintage** — never splice across a
comprehensive-revision boundary (`NIPA_CHANGE_TIMELINE.md`).

## 5. Replication fidelity note

RSCD reproduces XS009's book-period columns by the read-the-truth-column pattern: it transcribes
`INVcorp`/`KGCcorp`/`KTCcorp` from Appendix Table 6.8.II.6. `V03_XS009.py` round-trip-validates against
the Appendix 6.8 source workbook at **1.0% tolerance** (`XS009_DPR.md` §Validation Expectation; DPR cites
the legacy name `V03_XS009_validate.py` — cosmetic **F-XS-06**). Honest limits, disclosed:

- **Transcribed, not recomputed (F-XS-05, MEDIUM).** XS009 "declare[s] construction:formula but carr[ies]
  components:[] and no formula field" — actually its research JSON is richer (`construction: composite`
  with a 4-step formula and 6 components), but the **executable path is still a pass-through
  transcription** of Shaikh's Appendix Table 6.8.II.6 (L01 loads the finished INVcorp/KGCcorp/KTCcorp
  columns; P02 is schema-only). The two-step IRS-bridge + linear-time backcast lives only in DPR prose +
  CH6 summary + the **deferred v1.1 EPR extension recipe** (`CH_XS_review.json` findings F-XS-05;
  `XS009_EPR.md` Method steps 1–4 + Anti-Degradation Compliance). Fidelity is melt fidelity, not an
  independent re-estimation of the inventory ratio.
- **Post-2011 constant-ratio proxy (CH6 open-Q4).** For years > 2011 INVcorp is *not* actual IRS data:
  it is `(INVcorp_2011 / KGCcorp_2011) × KGCcorp_t`, a documented **constant-ratio proxy** carried via
  `extension_method: constant_ratio_proxy_2012_onwards` (`XS009_DPR.md` §Why It Matters + §Caveats;
  `XS009_research.json` methodology_notes[3]). This must be flagged in any S6xx profit-rate plot that
  consumes KTCcorp past 2011 (`XS009_research.json` extension_candidates[1] concerns). This is an
  **extension-only** proxy; the book period 1946–2011 carries **no proxies** (`XS009_EPR.md` No-Proxy
  Disclosure; Decision 0002 + Phase-4 Q3).
- **Unit-scale correctness.** Raw IRS SOI inventories are in **thousands of dollars** (CD2 S214
  1946 = 36,965,000-scale, `XS009_research.json` open_questions[2]); the Appendix II.6 `INVcorp` column is
  already rescaled to billions after Shaikh's procedure, so the loader treats it as billions
  (`XS009_DPR.md` §Construction + §Caveats; `XS009_EPR.md` CD2 Divergence Pre-Disclosure notes the same
  ~1000× normalization applies as in XS007).
- **Units-artifact risk (F-XS-01 / D14, HIGH — group-level).** XS009's own subseries are genuine billions,
  but the group-wide chopped-CSV units leak (`mixed_billions_usd_and_decimal_rates` / mislabeled
  dimensionless rows) must be remediated before external distribution (`CH_XS_review.json` findings
  F-XS-01; gate D14 = BELOW_90_BLOCKS_EXTERNAL).

## 6. Forward risk

- **IRS SOI update need + the post-2011 proxy lift.** The single biggest forward risk: IRS discontinued
  **net historical capital stock** after 2011, so the constant-ratio proxy is used for 2012+. The
  recommended Phase-6 lift (deferred) is to **re-estimate the INV/KGC ratio from current IRS SOI data** —
  the *Corporation Complete Report* (https://www.irs.gov/statistics/soi-tax-stats-corporation-complete-report)
  still publishes inventories, just not the net capital stock — using BEA FA T6.3 historical-cost stock as
  the denominator (`XS009_EPR.md` Method step 4; `XS009_research.json` open_questions[0]a/b/c). Alternatives
  flagged: keep the proxy with an explicit visualization break, or substitute FRB Z.1 non-financial
  corporate inventories as a defensible fallback. IRS SOI publication lags 3–4 years, so any live
  extension trails BEA by 2–3 years (`XS009_research.json` extension_candidates[0] concerns).
- **GPIM recompute needs the BEA-1993 archive.** XS009 adds to KGCcorp (XS004), whose finite-life
  depreciation/retirement rates come from BEA 1993 — staged at
  `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/` (`XS009_EPR.md` Failure Mode Table
  row 5; shared with XS004/XS006). An end-to-end (non-transcribed) rebuild of KTCcorp needs this archive
  plus a coherent BEA vintage.
- **BEA re-vintaging.** Any extension past 2011 must re-pull BEA FA T6.1/T6.3 on a single coherent vintage
  and re-run — never splice across 2013/2018/2023 (`NIPA_CHANGE_TIMELINE.md`); a re-vintaged BEA
  denominator moves the rescaled INVcorp.
- **Downstream discontinuity flag.** KTCcorp feeds the final corrected corporate profit rate (likely
  S601, possibly S603 — `XS009_research.json` open_questions[1]); the post-2011 inventory proxy is a
  discontinuity that must be surfaced in any final profit-rate plot using KTCcorp (`extension_candidates[1]`).
