# S604 — Corporate Incremental Rate of Profit (IROP) — Methodological History Report (MHR)

**Group:** ch6 (Capital and Profit) · **Construction:** formula · **Status:** book_period_validated
**Figure:** 6.7 · **Predecessor:** CD2 S105 · **Publish:** true
**Reasoning stance:** from Shaikh's own perspective.

> Grounding: `Technical/research/S604_research.json`, `CH6_RESEARCH_SUMMARY.md`, `CH6_GPIM_SUMMARY.md`,
> `Technical/methodology_review/CH06_review.json`, `NIPA_CHANGE_TIMELINE.md`. No invented claims.

---

## 1. What it is (book definition + Appendix 6 table + figure)

S604 is the chapter's **culminating profit-signal series** — the empirical proxy for the *unobserved rate of return
on new capital* that drives Shaikh's turbulent equalization of profit rates. Defined at p. 254 (`book_quotes[0]`,
role=definition): the **incremental rate of return on investment** = *"the ratio of the change in gross net
operating surplus to current gross investment in fixed capital and inventories. The numerator can be calculated by
adding the change in current-cost depreciation to the change in the … imputations-adjusted net operating surplus,
and the denominator by adding the estimated inventory changes to BEA data on fixed capital gross investment."*

**Fig 6.7** has two panels (four curves), Appendix 6.8 **Table II-7**:
- **Nominal panel** (p. 255, `book_quotes[1]`, role=source): `iropcorp` (adjusted) vs `iropcorpnipa` (NIPA proxy).
- **Real / current panel** (p. 256, `book_quotes[2]`, role=method): `iroprcorp` vs `iroprcorpnipa`.

Because a price-level change would move the nominal numerator and the current-cost denominator differently, Shaikh
puts every element in current-currency units, so the "current" IROP is **numerically equivalent to a conventional
real rate** (p. 254, `book_quotes[3]`, role=caveat; Fig 6.7 caption *"Numerically, Current Rates = Real Rates"*).
The critical finding (Table 6.24): the adjusted and NIPA-proxy IROPs are *"virtually the same"* — means 13.45% vs
13.62% nominal, 9.50% vs 8.49% real — which **licenses the simpler NIPA proxy for international and inter-industry
work** (Ch7 §VI.5, Ch10).

## 2. Source lineage (the GPIM chain)

| Component | Source table | Role |
|---|---|---|
| `Δ(NOS_corp)`, `NOS = P + NMINT` | **NIPA T1.14** (P) + **NIPA T7.11** (NMINT) | numerator net part (adjusted) |
| `Δ(D_corp)` current-cost depreciation | **BEA Fixed Asset T6.4** | net→gross conversion in numerator |
| `Δ(P_corpnipa)` | **BEA NIPA T1.14** | numerator (NIPA proxy) |
| `IG_corpbea` gross fixed investment | **NIPA T5.3.5** allocated to corporate via **FA T6.7** legal-form split | denominator (fixed-capital part) |
| `Δ(INV_corp)` inventory change | **IRS SOI** corporate balance sheets, current-cost scaled | denominator increment (adjusted only) |
| current-cost deflator | BEA FA implicit price index | makes real panel a genuine real rate |

Formulas (research JSON): nominal `iropcorp = Δ(GOS_corp_adj)/(IG_corpbea + Δ(INV_corp))` with
`Δ(GOS_corp_adj) = Δ(NOS_corp) + Δ(D_corp)`; NIPA proxy `iropcorpnipa = Δ(GOS_corpnipa)/IG_corpbea`. The real panel
repeats in current terms. Note the **NIPA proxy needs neither NMINT nor IRS inventories** — the operational reason it
extends further. GPIM internals: components draw on **XS003** (adjusted `NOS`), **XS004** (GPIM capital context),
**XS009** (IRS inventories `INV`). Registry `S604.components=[XS003, XS004, XS009]`.

## 3. Why these sources — Shaikh's rationale + rejected alternatives

- **Why the incremental rate over the average rate.** Turbulent equalization operates through the mobility of
  **new** capital, so the arbitrage-relevant signal is the return on *incremental* investment, not on the legacy
  stock (research JSON methodology_notes[0]). Average rates (S601/S602) are too smoothed to be the marginal price
  signal. The true return on new capital is unobservable, so Shaikh explicitly adopts the IROP as its **proxy**
  (p. 254), defending it in Ch7 §VI.5.
- **Why first-differences of gross flows.** The numerator is the change in *gross* operating surplus (net surplus
  plus the change in current-cost depreciation) because new investment is gross; the denominator is *gross* fixed
  investment plus the inventory change — matching numerator and denominator as gross incremental flows (eq. at
  p. 254).
- **Why current/real terms.** So a pure inflation shock does not spuriously move the ratio; current-cost numerator
  and denominator share the price level, making the ratio real by construction (p. 254, footnote 22).
- **Why carry the NIPA proxy `iropcorpnipa` at all — the key result.** Empirically it nearly coincides with the
  fully-adjusted `iropcorp` (Table 6.24), and it needs only easily-available NIPA data (no FISIM reversal, no IRS
  inventories). Shaikh therefore designates it the operationally attractive measure for cross-country and
  inter-industry comparison — *"the NIPA measures are easily estimated across countries and through time"* (p. 256).
  This is the methodological hinge from Ch6 to the industry-IROP work of Ch7 (S706/S707) and the equity-vs-IROP
  comparison of Ch10 (S1007).
- **Rejected alternative — extending the adjusted IROP forward.** Because `NMINT` and IRS inventories are
  incomplete/lagged post-2011, and because first-differences cannot be spliced across vintage seams, Shaikh's own
  logic favors freezing `iropcorp` at the book vintage and extending only `iropcorpnipa` (research JSON
  open_questions[4]).

## 4. Methodological-change exposure — NIPA vintage drift (KEY SECTION)

S604's first-difference construction makes it **uniquely fragile** to vintage drift, on top of the standard 2011-vintage
fixing (App. 6.7 fn 1):

- **First-differences cannot be spliced.** Adjacent vintages produce *different first differences at the seam*
  (research JSON extension_candidates[0].concerns), so even a small comprehensive-revision level shift produces a
  spurious spike in `Δ` at the join. The **2013 IPP capitalization** (R&D + entertainment originals → +$400B GDP,
  raising CFC/NOS/depreciation and gross investment; `NIPA_CHANGE_TIMELINE.md` 2013 row) changes every `Δ(NOS)`,
  `Δ(D)`, and `IG` — the entire numerator and denominator. A post-2013 IROP is a different series.
- **T7.11 +1 line shift (2018)** breaks the `NMINT` recipe feeding the adjusted numerator (lines
  `4,28,44,52,53,54,73,74,75,91` → `4,29,45,…,92`); resolve by stub label
  (`NIPA_T711_FISIM_remap.md` / `_nipa_t711_line_resolver.py`). The **NIPA proxy** `iropcorpnipa` is immune to this,
  since it uses no `NMINT`.
- **T5.3.5 corporate allocation.** Gross investment is total private; the corporate share must be re-derived from
  **FA T6.7** legal-form splits, which move with vintage (~75–80%, vintage-specific; research JSON
  extension_candidates[1]).
- **Binding data window.** The adjusted `iropcorp` is bounded by `NMINT` + IRS-inventory completeness (CD2 S105 known
  issue); `iropcorpnipa` extends through the current BEA vintage — the concrete payoff of Shaikh's proxy argument.

Staged but untested (CH06_review L4): chopped ends 2011; the resolver and BEA-1993 staging have not been exercised on
a live extension.

## 5. Replication fidelity note

- **Genuine non-circular anchor — the strongest in Ch6.** Unlike its siblings, S604 has an external book cross-check:
  `iropcorp`/`iropcorpnipa` reproduce **Table 6.24 EXACTLY** — means 13.45%/13.62%, SD 0.1282/0.1580, CoV
  0.9532/1.1605 (CH06_review `non_circular_book_anchors`). The transcribed subseries also match Appendix 6.8.II.7 at
  **0.0000% max pct error** (n=64). `V03_S604` round-trips at **2.0%** tolerance (wider than the 1.0% Ch6 default,
  reflecting first-difference volatility — CD2 S105's ~5% replication tolerance; research methodology_notes[3]).
- **COVERAGE GAP — ships only 2 of 4 Fig 6.7 curves** (CH06_review **H1, HIGH**). Only the nominal panel
  (`iropcorp`, `iropcorpnipa`) is reconstructed; the **real-rate panel `iroprcorp` (9.50%) and `iroprcorpnipa`
  (8.49%) are NOT built**, though the columns exist in `Appendix6_Table68II7.xlsx`. S604 is `publish:true`, so a
  published headline series reproduces **half its figure**. Cheaply fixable — add the two subseries to the SOURCE_MAP.
  (This is the same gap flagged in project CLAUDE.md "Coverage gaps: … S604 (2 of 4 printed real-rate columns)".)
- **Publish-flag discrepancy** (CH06_review M6): the RSCD CLAUDE.md `publish:false` list excludes S604, yet the
  registry has `S604.publish=true`. **If S604 stays published, H1 is a publication blocker.**
- **Transcription, not live recompute** (CH06_review M5): `P02_S604.py` transcribes Shaikh's II-7 columns; the IROP
  first-difference formula is not executed in code for the book period.
- **XS→S6xx linkage prose-only** (CH06_review M1); **circular `reference_values`** for the transcription (M3), though
  Table 6.24 gives the genuine anchor above.
- Confirm the differencing convention (t vs t−1 vs centered) against the workbook (research open_questions[3]).

## 6. Forward risk

- **Next NIPA benchmark re-defines capital and flows.** Every future comprehensive update that re-levels investment,
  depreciation, or profit changes each `Δ` in the IROP; because differences cannot be spliced, the *only* correct
  extension is an end-to-end recompute on one coherent vintage, and even then the 2011-vintage `iropcorp` and a
  new-vintage `iropcorpnipa` are not on the same footing.
- **Designate `iropcorpnipa` as the canonical extended series.** Given `iropcorp ≈ iropcorpnipa` (Table 6.24) and the
  `NMINT`/IRS-inventory constraints, Shaikh's own logic (p. 256) points to extending only the NIPA proxy and holding
  the adjusted IROP at the book vintage for replication (research open_questions[4]).
- **BEA-1993 depreciation archive recovery** underpins the current-cost `Δ(D_corp)` and the real panel; staged at
  `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/`, KB source
  `1993_DoC_Fixed_Reproducible_Tangible_Wealth`.
- **Close the H1 coverage gap before publication** — reconstruct `iroprcorp`/`iroprcorpnipa` from the existing II-7
  columns so the published S604 reproduces all four Fig 6.7 curves.
