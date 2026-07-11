# S603 — Component Ratios x1, x2, x3 — Methodological History Report (MHR)

**Group:** ch6 (Capital and Profit) · **Construction:** formula · **Status:** book_period_validated
**Figure:** 6.3 · **Predecessor:** CD2 S028 · **Publish:** true
**Reasoning stance:** from Shaikh's own perspective.

> Grounding: `Technical/research/S603_research.json`, `CH6_RESEARCH_SUMMARY.md`, `CH6_GPIM_SUMMARY.md`,
> `Technical/methodology_review/CH06_review.json`, `NIPA_CHANGE_TIMELINE.md`. No invented claims.

---

## 1. What it is (book definition + Appendix 6 table + figure)

S603 is the **analytical decomposition diagnostic** for S602. Shaikh's identity (6.11), stated verbatim at p. 249
(`book_quotes[0]`, role=definition), factors the ratio of his corrected corporate profit rate to the NIPA rate into
three multiplicative components:

```
r ≡ (P + NMINT)/(KGC(-1) + INV(-1))
  = r_NIPA · ((1 + NMINT/P) / (1 + (INV/KNC_NIPA)(-1))) · (KGC(-1)/KNC_NIPA(-1))
  = r_NIPA · (x1/x2) · x3            (eq. 6.11)
```

- **x1 = 1 + NMINT/P** — the **net monetary interest** (imputed-interest) factor.
- **x2 = 1 + (INV/KNC_NIPA)(-1)** — the **inventory** factor (total vs BEA-only fixed capital base).
- **x3 = KNC_NIPA(-1)/KGC(-1)** — the **capital-stock revaluation** factor (BEA official net stock vs Shaikh's GPIM
  gross stock).

**Fig 6.3** (p. 249, `book_quotes[1]`, role=source) plots x1, x2, x3 and the product `(x1/x2)·x3 = rcorp/rcorpnipa`.
Shaikh's reading: x1 rises then stabilizes (rising debt offset by falling rates); x2 is *"fairly stable"* (~1.14
throughout); **x3 falls steadily** because the GPIM stock rises relative to BEA's — *"so (x1/x2)·x3 … has a downward
trend."* The methodological headline is therefore that **the capital-stock revaluation (x3) dominates the trend**,
while the interest factor (x1) drives the fluctuations. Canonical values: Appendix 6.8 **Table II-7** columns
`S013P` (x1), `S013Q` (x2), `S013R` (x3); ships as subseries x1, x2, x3, and `x3*(x1/x2)` (CH06_review, n=65,
0.0000% error).

## 2. Source lineage (the GPIM chain)

S603 introduces **no new underlying data** — it recombines exactly the components feeding S602 into ratios
(research JSON methodology_notes[0]):

| Ratio | Numerator input | Denominator input | Sources |
|---|---|---|---|
| **x1** | `NMINT_corp` | `P_corp` | **NIPA T7.11** (FISIM) / **NIPA T1.14** |
| **x2** | `INV_corp(-1)` | `KNC_corpbea(-1)` | **IRS SOI** inventories / **BEA FA T6.1** |
| **x3** | `KNC_corpbea(-1)` | `KGC_corp(-1)` | **BEA FA T6.1** / **Shaikh GPIM** (App. 6.7.V.5) |

The GPIM `KGC` entering x3 is the **XS appendix series** chain (XS004 preferred; XS005–XS008 sensitivity variants);
the IRS inventories in x2 are **XS009**; the FISIM `NMINT` in x1 is **XS003**. Registry
`S603.components` reference this chain (prose-only, see §5). Nomenclature to standardize (research
methodology_notes[2]): official BEA = `KNC_corpbea`; Shaikh GPIM = `KGC_corp` (gross), `KNC_corp_gpim` (net).

## 3. Why these sources — Shaikh's rationale + rejected alternatives

- **Why a decomposition series at all.** S603 exists purely to *communicate which correction matters*. Shaikh could
  have left the corrected/NIPA gap unexplained; instead eq. (6.11) is his explicit analytical bridge attributing the
  wedge between `rcorp` and `rcorpnipa` (Fig 6.2) to its three drivers, and Fig 6.3 shows the answer is
  overwhelmingly x3 — the GPIM capital-stock revaluation (methodology_notes[3]). This is the quantitative core of the
  chapter's argument that the *capital measure*, not the profit measure, is where NIPA misleads.
- **Why the GPIM enters x3 (rejecting BEA's stock).** Same rationale as S602: BEA's chain-weighted/quality-adjusted
  net stock departs from the perpetual-inventory rule (p. 244); x3 = KNC_bea/KGC quantifies exactly how far. That x3
  falls from ~1.11 to ~0.61 (methodology_notes[1]) is Shaikh's evidence that the divergence is large and
  monotone — not a rounding artifact.
- **The profit-rate concept behind x1, x2.** x1 encodes the numerator choice `NOS = P + NMINT` (classical surplus,
  not NIPA profit); x2 encodes the denominator choice `KTC = KGC + INV` (total, not fixed, capital). Together they
  are the algebra of Shaikh's `r = P/(K+INV)` concept relative to NIPA's `P/KNC`.
- **Rejected alternative — plotting a sensitivity panel of x3 variants.** The GPIM `KGC` has four CD2/XS variants
  (initial-value, vintage, IRS, interwar). Shaikh's S028 and RSCD's S603 plot **only the headline x3** using the
  preferred GPIM (XS004); the variants are reserved for the XS sensitivity dossiers (research open_questions[0]).
- **Content-type note.** The ratios are analytical, not independent observations; a case exists for
  `content_type: derived` rather than `time_series` (CH06_review L2), but Shaikh plots them as time series and they
  require fresh component data to extend, so `time_series` is retained.

## 4. Methodological-change exposure — NIPA vintage drift (KEY SECTION)

S603 inherits **the union of S602's and S603's own** vintage exposures, because each ratio depends on a
vintage-sensitive input, and Shaikh fixes all at the **2011 vintage** (App. 6.7 fn 1):

- **x1 — the sharpest and most immediate exposure.** x1 = 1 + NMINT/P depends on `NMINT` from **T7.11**, which the
  **2018 update shifted by +1 line** (recipe lines `4,28,44,52,53,54,73,74,75,91` → `4,29,45,…,92`) and the **2013
  update restated in magnitude** without reordering. Any post-2011 x1 computed with hard-coded lines silently reads
  the wrong rows; resolve by stub label via `NIPA_T711_FISIM_remap.md` / `_nipa_t711_line_resolver.py`. Moreover
  `NMINT_corp` is **incomplete for recent years** (research JSON extension_candidates[0].concerns) — so x1 must be
  **frozen at the last complete NMINT year** and treated as undefined thereafter, never forward-filled
  (methodology_notes[4]).
- **x3 — the deep-history exposure.** x3 = KNC_bea/KGC. The **2013 IPP capitalization** raises both the BEA stock
  (`KNC_bea`) and the GPIM-accumulated stock (`KGC`) across the whole investment history, so x3 on a post-2013
  vintage measures a *different capital concept ratio* than Shaikh's 2011-vintage x3. This is why the chapter forbids
  splicing across a comprehensive-revision boundary (`NIPA_CHANGE_TIMELINE.md` §"Why this matters").
- **x2 — inventory-base exposure.** Depends on IRS SOI inventories and BEA FA net stock; both move with vintage and
  IRS reporting changes.

Staged but untested (CH06_review L4): the FISIM resolver and BEA-1993 depreciation staging exist; no extension has
exercised them.

## 5. Replication fidelity note

- **Bit-exact.** x1, x2, x3, and `x3*(x1/x2)` reproduce Appendix 6.8.II.7 at **0.0000% max pct error** (n=65,
  CH06_review). `V03_S603` round-trips at 1.0% tolerance.
- **Transcription, not live recompute** (CH06_review M5). `construction:formula` but `P02_S603.py` transcribes
  Shaikh's pre-computed II-7 columns rather than recomputing the ratios from raw components; verbatim and faithful
  for the book period, recompute deferred to extension.
- **XS→S6xx linkage prose-only** (CH06_review M1): `L01_S603.py` reads Appendix workbook columns directly; XS003/
  XS004/XS009 outputs never consumed — so the "x3 dominates" finding is documented and 0.0000%-faithful but the
  decomposition is not executed against the GPIM outputs.
- **Circular `reference_values`** (CH06_review M3): V03 round-trips the source XLSX. Verify the lagged-vs-current
  denominator convention of columns S013P/Q/R against the workbook (research open_questions[2]).

## 6. Forward risk

- **Next NIPA benchmark re-defines capital.** x3 is literally the ratio of two capital-stock concepts; any future
  benchmark that re-levels investment (as 2013 did) re-levels x3 across all years. x1 is exposed to the next T7.11
  restatement/renumbering. Extension must recompute all three ratios end-to-end on one coherent vintage.
- **x1 freeze is structural, not temporary.** Because `NMINT_corp` is chronically incomplete in recent T7.11
  vintages, the interest factor x1 (and hence the product line `(x1/x2)·x3`) cannot be extended as far as x2/x3;
  document the freeze year and mark post-freeze x1 undefined.
- **BEA-1993 depreciation archive recovery** needed for a genuine x3 recompute (the GPIM `KGC` denominator); staged
  at `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/`, KB source
  `1993_DoC_Fixed_Reproducible_Tangible_Wealth`. Until XS004 is wired, x3 cannot be recomputed — only transcribed.
