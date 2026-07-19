# S216 — Methodological History Report (MHR)

**Series**: S216 — Normalized Total Prices of Production Profit versus Total Unit Labor Costs, US 1972 (71 Industries)
**Chapter**: 2 (Turbulent Trends and Hidden Structures), §VII Relative Prices · **Group**: ch2 / CH02
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every author-intent claim traces to a cited path, or is marked "not located in corpus."

Grounding: `Technical/series_registry.json` → `series.S216`; `Technical/research/S216_research.json`;
`Technical/docs/series/S216_DPR.md` + `S216_EPR.md`; `Technical/methodology_review/CH02_review.json`
(touchpoint `S216/io`); Phase-0 `Technical/docs/methodology/_timelines/IO_CHANGE_TIMELINE.md`
(+ `NIPA_CHANGE_TIMELINE.md`); KB `Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/Figures/ch02/ch02_fig_2.14.md`
and `.../Body_Text/ch02_turbulent_trends.md`; sibling `Technical/docs/methodology/series/S901_MHR.md`
(the Ch9 exhibit built on the same 1972 71-order substrate).

---

## 1. What the series is

S216 is Shaikh's **single-year cross-sectional price-comparison scatter**: for each of **71 sectors of the
US input–output table for 1972** it pairs, industry by industry, the **normalized total market price**
(and the normalized total price of production at the observed profit rate) against the **normalized total
vertically-integrated unit labor cost** (the "direct price"). It is the data behind **Figure 2.14** —
"Normalized Total Prices of Production Profit versus Total Unit Labor Costs, US 1972 (Seventy-One
Industries)" (book p.70; `S216_research.json` book_quotes p.764, verbatim).

Book definition (Shaikh 2016, Ch2 p.67, quoted verbatim in `S216_research.json`):
> "Figure 2.14 displays the relation between observed market prices and prices proportional to vertically
> integrated unit labor costs (direct prices), for each of seventy-one sectors of the US input–output table
> for 1972. The vertical axis represents the market value of each sector's total output (i.e., its unit
> market price times its total output), while the horizontal axis represents the corresponding direct money
> value of the same outputs."

Construction (`S216_DPR.md` §1, §4): x = total vertically-integrated unit labor cost `tv`; y = total market
price `tpm` **and** total price of production at observed `r`, `tp(r)`; both axes l1-normalized so the
industry totals sum to 1; a 45° line is drawn for **visual comparison — not a fitted regression**
(body text pp.709–710). One row per (industry, axis-series) in long form.

**Content type — the load-bearing classification decision.** The stub defaulted to `time_series` with
`year_range=[null,null]`; Phase 3 reclassified it to **`cross_sectional`** with `year_range_book=[1972,1972]`,
ratified by Phase 4 (`S216_research.json` methodology_notes, open_questions; `S216_DPR.md` §7 caveat 2;
`CH02_review.json` touchpoint `S216/io`: "content_type correctly cross_sectional (extension suppressed)").
A single benchmark-year I–O scatter cannot be "extended" along the time axis — a 1977/1982/…/2012 scatter
is a *different exhibit*, not a continuation of this one.

**Link to Chapter 9.** Fig 2.14 is the Chapter-2 preview of the Ch9 relative-price apparatus: its source
note reads "Discussed in chapter 9 in relation to figure 9.1. Appendix 9.3 Data Tables for Chapter 9"
(`S216_research.json` book_quotes p.764, verbatim), and the body text points to "chapter 9, tables 9.9 and
9.13" (body p.714; KB `ch02_fig_2.14.md` "Data Source"). The **1972 71-order** column of S216 is the same
substrate that `S901` (Fig 9.1 market-vs-direct) and `S902` (Fig 9.16 market-vs-prices-of-production) scatter
in Chapter 9 (`S901_MHR.md` §1–§2).

## 2. Source lineage

One provenance era feeds one frozen cross-sectional object (`S216_DPR.md` §3; `S216_research.json`
primary_source, components):

- **1972 — BEA benchmark Input–Output (Use + Make tables), aggregated to the Ochoa 71-order.** Agency:
  U.S. Bureau of Economic Analysis, Input–Output Accounts (`S216_research.json` primary_source.agency).
  Per the Phase-0 IO timeline, the 1972 benchmark is on a **1972-SIC basis (~496 detail)** and is the
  **last of the historical Ochoa 71-order panel Shaikh uses** — his Ch9 set jumps 1972 → 1998
  (`IO_CHANGE_TIMELINE.md` benchmark-year table). Native units: normalized dollars (axes scaled to a common
  total); single-year cross-section, 1972 only.
- **Sectoral labor coefficients (employment / output) + Sraffian price computation.** Components:
  BEA 1972 Use table (71-sector), BEA 1972 Make table, and sectoral labor coefficients
  (`S216_research.json` components). Formula (`S216_research.json` formula; `S216_DPR.md` §4): prices of
  production computed from the Sraffian system at the **observed average profit rate**; vertically-integrated
  unit labor cost = `(I − A)⁻¹ · l`.
- **Retrieval in RSCD.** RSCD reads Shaikh's own pre-computed `tpm`, `tp(r)`, `tv` columns from the salvaged
  chopped workbook **`Appendix9_1972fixed.xlsx`** (`SalvagedInputs/book_data/ShaikhChoppedTables/`;
  `S216_DPR.md` §3 subseries S216-A/S216-B) and re-normalizes — the identical read-the-truth-column pattern
  used for `S901` (`S901_MHR.md` §1).

**No splice.** Because S216 is a single benchmark year, there is no temporal join — no overlap anchor, no
rebase, no vintage bridge. Each subsequent BEA benchmark (1977, 1982, …, 2017) would be a *separate*
cross-section requiring its own registry row (`S216_DPR.md` §7 caveat 1; `S216_EPR.md` §2).
Grounding corpus for the BEA I–O program: `SalvagedInputs/methodology_library/D_data_methodology/WL-D-IO-001…009__BEA-IO.*`.

## 3. Why these sources, author's perspective

- **Why the 1972 benchmark I–O, 71-order.** Shaikh needs a *fully articulated inter-industry matrix* to
  form the Leontief inverse `(I − A)⁻¹` and hence vertically-integrated ("direct") prices; only **benchmark**
  I–O years carry the detail/summary tables that support a clean inverse (annual I–O tables are interpolated
  and less detailed — `IO_CHANGE_TIMELINE.md` cadence note; `S901_MHR.md` §3). 1972 is chosen because it is
  the **last conformable year of the Ochoa (1984) 71-order historical panel** Shaikh reuses across his
  price-of-production work (`IO_CHANGE_TIMELINE.md` benchmark-year table; `S901_MHR.md` §3).
- **Why this exhibit at all — the classical "93% theory of price" test.** The choice is theoretically
  motivated, and the book states the motive plainly. Smith "was the first one to make this decomposition"
  and Ricardo argued relative prices are "dominated by the ratio of their vertically integrated unit labor
  costs," with the residual profit-rate influence capped at 7% — the **"93% Theory of Price"** that has
  "long been derided by modern economists on theoretical grounds" (body pp.693–702, verbatim). Fig 2.14 is
  Shaikh's empirical answer: from 1947–1998 the average absolute deviation of market prices from direct
  prices is **15.4%**, and of long-run competitive prices from direct prices **13.2%** — so ~**87%** of the
  inter-industrial structure of competitive prices is accounted for by direct + indirect unit labor costs,
  "not far from Ricardo's estimate" (body pp.710–716, 888–890; KB `ch02_fig_2.14.md` "Empirical Results"/
  "Ricardo's 93% Theory of Price"). The Sraffa/Pasinetti/Kurz–Salvadori vertical-integration lineage is cited
  at body p.682. Deeper grounding: `SalvagedInputs/methodology_library/A_shaikh_pre2016/WL-A-RealComp-*`.
- **Why cross-sectional, not a time series.** The point of Fig 2.14 is *proximity to the 45° identity across
  sectors in a single articulated economy*, not a trend. The 45° line "is not a fitted regression line"
  (body pp.709–710); a time-series framing would misrepresent the claim, and the underlying benchmark years
  are not conformable (see §4). Author rationale for the specific reclassification is RSCD-internal
  (`S216_research.json` methodology_notes), consistent with the book's single-year presentation.
- **Rejected alternative — a continuous multi-benchmark price panel.** Explicitly declined at framework
  level: each BEA benchmark is a separate scatter, "not extendable in the time-series sense"
  (`S216_research.json` extension_candidates.concerns; `S216_DPR.md` §7). This mirrors the Ch9 wall Shaikh
  himself hits — his panel jumps 1972 → 1998 rather than splicing (`S901_MHR.md` §3–§4).

## 4. Methodological-change exposure

S216 sits on the same **SIC → NAICS classification wall** documented in the Phase-0 IO timeline
(`IO_CHANGE_TIMELINE.md`, "The SIC → NAICS break (the Ch9 wall)"):

1. **Benchmark cadence + frozen-exhibit rule.** BEA publishes a benchmark I–O account **every 5 years**
   (years ending 2 and 7), each on its own classification vintage (`IO_CHANGE_TIMELINE.md` cadence). A
   1977/1982/…/2012 scatter is therefore a *new* exhibit, never a continuation of the 1972 one — extension
   in the time dimension is suppressed by design (`CH02_review.json` touchpoint `S216/io`).
2. **SIC → NAICS hard break.** Last SIC benchmark = **1992**; first NAICS benchmark = **1997**. BEA states the
   pre-1997 historical benchmark tables "should not be used as a time series"
   (`IO_CHANGE_TIMELINE.md`). The 1972 71-order (SIC-era) cross-section cannot be spliced to any NAICS-era
   benchmark.
3. **Ochoa-71 vs BEA-65 non-conformability (the Ch9 wall).** Shaikh's historical 71-order (real-estate-
   excluded, Ochoa 1984) and BEA's post-1997 65-order Use table are **not directly conformable**; a single
   continuous industry panel across the 1972 → 1998 gap is not reconstructable
   (`IO_CHANGE_TIMELINE.md` "Industry order / detail notes"; `S901_MHR.md` §4.1). Even *within* NAICS, the
   summary/detail row order is revised at each benchmark, so industry indices are not stable across vintages.
4. **NIPA-vintage coupling (secondary).** Any *re-derivation* of the 1972 prices from raw BEA tables (rather
   than reading Shaikh's frozen `Appendix9_1972fixed.xlsx`) would inherit NIPA comprehensive-revision drift
   (software→IPP capitalization 2013, T7.11 renumbering 2018 — `NIPA_CHANGE_TIMELINE.md`). RSCD avoids this
   entirely by reading the pre-computed columns; the exposure is latent, not active.

## 5. Replication fidelity note

RSCD reproduces S216 by the **read-the-truth-column** pattern: it re-reads Shaikh's pre-computed
`tpm`/`tp(r)`/`tv` columns from `Appendix9_1972fixed.xlsx` and re-normalizes identically (`S216_DPR.md`
§4, §9). Validation is on the `cross_sectional` playbook: **±0.5% tolerance**, expected MAE < 0.5%
(`S216_DPR.md` §7 caveat 3, §9). Honest limits, disclosed:

- **Cross-sectional by design; temporal extension is `not_applicable_cross_sectional`** — not a coverage gap
  but a category fact (`S216_EPR.md` §1, §7; `S216_DPR.md` §5). No proxies and no synthetic/interpolated
  values are introduced (`S216_EPR.md` §3–§4).
- **Melt-fidelity, not independent book confirmation.** As with `S901`, reading and re-normalizing the same
  workbook the chopped is melted from confirms *transcription fidelity*, not an out-of-sample check; the
  genuine non-circular anchors are the Ch9 distance tables 9.9/9.13 (`S216_research.json` book_quotes p.764;
  `S901_MHR.md` §5).
- **KB caption thinness (project-wide).** Ch02 figure captions are thin and the Appendix 2.1 source-methods
  text (book pp.763–766) is not cleanly extracted to the KB (`CH02_review.json` finding F-08, LOW) — the
  authoritative source note lives in `S216_research.json` book_quotes (p.764), not in the KB figure file.
- **No per-series DECOMPOSITION.md** (project-wide F-03): construction lives in `S216_DPR.md` §4 + registry
  `formula`/`components` (`CH02_review.json` finding F-03, MED).

## 6. Forward risk

- **The next benchmark is a new scatter, not continuity.** A 2017 (or forthcoming 2022) benchmark I–O
  cannot be appended to the 1972 cross-section; it requires its own registry row, its own labor-coefficient
  construction, and a fresh Leontief inverse (`S216_EPR.md` §2; `S216_DPR.md` §7).
- **NAICS non-conformability blocks a true panel.** The Ochoa-71 ↔ BEA-65 wall means no continuous
  1947→present industry price panel is reconstructable without a lossy crosswalk; the natural "extension" is
  benchmark-*addition*, never a splice (`IO_CHANGE_TIMELINE.md`; `S901_MHR.md` §6).
- **BEA re-vintaging of the historical tables.** BEA has revised historical benchmark magnitudes over time;
  any future re-pull to validate `Appendix9_1972fixed.xlsx` against a modern iTable reconstruction lands on
  NIPA-revised magnitudes and must stay on a single coherent vintage (`NIPA_CHANGE_TIMELINE.md`;
  `S901_MHR.md` §6).
