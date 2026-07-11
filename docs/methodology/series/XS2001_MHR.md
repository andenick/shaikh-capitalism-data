# XS2001 — Methodological History Report (MHR)

**Series**: XS2001 — Sraffa Price/Value Aggregate Ratios, US 1947–1998 (Shaikh 2020, Tables 1–2)
**Chapter**: 0 (`xs_class: external_study`) · **Group**: external-study family 20 · **Status**: study_complete
**Perspective**: authored *from Shaikh's perspective* — why *he* built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS2001_research.json`; `Technical/docs/series/XS2001_DPR.md` +
`XS2001_EPR.md`; `Technical/docs/external_studies/XS2001_paper_summary.md` +
`ES_PHASE_5_8_CLOSURE.md`; Phase-0 `Technical/docs/methodology/_timelines/IO_CHANGE_TIMELINE.md`
(+ `NIPA_CHANGE_TIMELINE.md`); `Technical/methodology_review/CH_XS_review.json`.

Paper of record: Shaikh, A. (2020), "An Empirically Sufficient Form for Sraffa Prices", festschrift
essay in honor of Luigi Pasinetti (Velupillai (ed.), Palgrave Macmillan per the paper's own reference
list p.20); companion to Shaikh, Coronado & Nassif-Pires (2020) EJEEP. Archival PDF of record:
`SalvagedInputs/methodology_library/B_shaikh_post2016/WL-B-Sraffa/` and
`Inputs/Capitalism Data/.../Shaikh Publications/[2020] Shaikh - An Empirically Sufficient Form for Sraffa Prices.pdf`
(`XS2001_EPR.md` §7).

---

## 1. What it is

XS2001 is Shaikh's **aggregate price/value-ratio panel** — the *time-series* half of the 2020
Pasinetti-festschrift essay. For each of six US BEA benchmark I-O years (**1947, 1958, 1963, 1967,
1972, 1998**), under **two** Sraffa-price models (**circulating** capital = Table 1, **fixed** capital =
Table 2), it reports **nine** aggregates as the ratio of a bundle valued at prices of production to the
same bundle valued at direct prices (labor values): observed rate of profit `r_obs`, `r_obs/R`,
constant capital, variable capital, surplus value, value added, rate of surplus value, rate of profit,
and the maximum profit rate `R`. That is the 12-row panel (2 models × 6 years, 9 aggregates each) of
**Tables 1–2, paper p.10** (`XS2001_DPR.md` §1; `research.json` figures[0-1]).

The measure exists to demonstrate **one** empirical claim — the **Sraffa Stochastic Effect (SSE)**:
across the entire observed range of the profit rate, the *aggregate* price and labor-value magnitudes
of a real economy are statistically indistinguishable. Shaikh states it verbatim (paper Section 3, p.4,
quoted in `research.json` book_quotes[2], `verbatim_check: true`):

> "In the circulating capital case, average price-value ratios for various aggregates range between
> 0.95 and 1.03 (Table 1), while in the fixed capital case they range between 0.97 and 1.05 (Table 2).
> As Marx and Sraffa had both understood, there is no effective difference between actual aggregates."

RSCD stores every cell in [0.94, 1.08] (`XS2001_DPR.md` §1) — a slightly wider empirical band than the
0.95–1.05 headline because it includes the profit-rate rows (`r_obs`, `R`) as well as the pure price/
value ratios. One documented in-band anomaly, **preserved as printed, not a transcription error**: the
1998 column of Table 2 has Rate of Profit = 0.98 and Max Rate R = 1.00, the only sub-unit Max Rate in
the panel (`XS2001_DPR.md` §7 caveat 3).

The underlying price system is Sraffa's, in Shaikh's **condensed form** (paper Section 5, p.7,
`research.json` book_quotes[0], `verbatim_check: true`):

> "… a condensed form of Sraffa prices (equation 6) … 6) p(r) = (1 − r/R) v + r p(r) H … 8)
> p(r)^(1) = (1 − r/R) v + r p(R) H … 10) p(r)^(2) = p(r)^(1) + r(p(r)^(1) − p(R)) H"

with `v = l(I−A)⁻¹`, `H = A(I−A)⁻¹`, `R = 1/λ₁(H)` the maximum profit rate, and `p(R)` the dominant
left-eigenvector of `H` (`research.json` formula). Equations 8 (Bienenfeld 1988 linear first iterate)
and 10 (quadratic second iterate — the "empirically sufficient form" of the title) drive the paper's
*other* empirical object, the 2002 403-order sector price curves of **Figures 1–9**, which are
**cross-sectional, 2002-only, and NOT part of XS2001** — they are deferred to v1.1 (`XS2001_DPR.md` §7
caveat 4; EPR §3). XS2001 v1.0 is the scalar-aggregate half only.

## 2. Source lineage

XS2001's *data of record* for v1.0 is Shaikh's own published tables, transcribed verbatim to
`SalvagedInputs/book_data/Reconstructed/XS2001_aggregate_ratios.csv` (108 chopped rows per
`ES_PHASE_5_8_CLOSURE.md`; `XS2001_DPR.md` §3). Behind those tables sits the primary-data lineage
Shaikh built them from (`research.json` primary_source; `XS2001_DPR.md` §3):

- **BEA Benchmark Input-Output Data** (Make/Use tables, detailed industry level), the `A`-matrix and
  value-added source — `nipa_touch` is empty for this series; the touch is **IO**, not NIPA.
  - **1947, 1958, 1963, 1967, 1972 — Ochoa/Shaikh 71-order (SIC-vintage)**, real-estate excluded, the
    same historical panel used for S901/S902 in Ch9. Per the Phase-0 IO timeline these map to the BEA
    benchmark I-O years 1947/1958/1963 (1957 SIC), 1967 (~478-order SIC), and **1972 (1972 SIC, ~496)
    — the last of the Ochoa 71-order panel Shaikh uses** (`IO_CHANGE_TIMELINE.md` benchmark table).
  - **1998 — BEA 65-order (NAICS-vintage)** Use table, the same 65-order object S901 uses, with the
    real-estate/owner-occupied-housing correction applied upstream.
- **BLS** compensation-of-employees + employment, used to build **skill-adjusted sectoral labor
  coefficients** `l` (normalized by the ratio of aggregate compensation to aggregate employment —
  the identical recipe of the companion XS2101, delegated to Shaikh 2012:98; `research.json`
  primary_source.secondary_sources_used[0], components[1]).
- **Shaikh (1998) Appendix 15.2** (1947–1972 physical bundles — intermediate input, workers'
  consumption, surplus product, net output, capital stock) and **Shaikh (2012) Data Appendix** (1998
  bundles); paper footnote 2, p.4 (`research.json` open_questions[5], components[2]). These are the
  essential upstream dependencies for the aggregate *bundles* being valued.
- **Shaikh, Coronado & Nassif-Pires (2020) Appendix I** — construction of the 2002 403-order matrix
  used only for the deferred Figures 1–9 (acknowledged paper p.5 fn 4; `research.json`
  secondary_sources_used[2]).

`concordance_touch`: the SIC↔NAICS bridge families staged under
`Technical/docs/methodology/concordances/_sources/naics/` are the authority that would be *required*
to relate the 71-order (SIC) and 65-order (NAICS) sides — see §4.

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

- **Why aggregate ratios, not the full 403-sector curves, to carry the SSE claim.** The SSE is a
  statement about *aggregates* — that price and value totals coincide "because of statistical
  compensation of large numbers." The natural evidence is therefore the ratio of aggregate bundle
  valuations (constant capital, variable capital, surplus value, value added, and the two derived
  rates), collapsed to **one scalar per (model, year)** at the observed profit rate. The 403-sector
  curves answer a *different* question — the *shape* of each individual `pᵢ(r)/vᵢ` over `r ∈ [0,R]` —
  which is the subject of Figures 1–9 and of the companion XS2101's Curvature Index, not of the SSE.
  RSCD encodes exactly this division: "aggregate price/value ratios are NOT cross-sectional Sraffa
  price curves p(r) — those are XS2101's empirical object. Tables 1–2 collapse the curve to a single
  scalar at r_obs per (model, year)" (`XS2001_EPR.md` §6). Reporting 403 sector curves to prove an
  *aggregate* proposition would be answering the wrong question at 400× the pipeline cost.
- **Why six sparse benchmark years, not an annual or continuous series.** Only **benchmark** I-O years
  carry the detailed Use/Make tables needed to form a clean `(I−A)⁻¹` and integrated labor times;
  detail-level estimates exist *only* for benchmark years (`IO_CHANGE_TIMELINE.md` "Cadence & detail").
  Annual I-O tables are interpolated and lower-detail. Shaikh reports the sparse set his upstream
  bundle appendices (Shaikh 1998/2012) already support, and treats each year as a frozen cross-section.
- **Why two capital models (circulating + fixed) side by side.** The SSE must be shown robust to the
  capital concept. The circulating-capital model (Table 1) assumes wages are not advanced and only
  materials cost is circulating capital (paper Section 5, p.7); the fixed-capital model (Table 2) adds
  the durable capital stock. Presenting both demonstrates the near-unity result is not an artifact of
  one accounting convention.
- **Why skill-adjusted BLS labor coefficients, not raw employment.** Direct prices are proportional to
  vertically-integrated labor time; heterogeneous labor must be reduced to a common standard. Shaikh
  weights employment by compensation (normalized by economy-wide compensation-per-worker) rather than
  head-count so that a skilled hour counts as more abstract labor — the same choice made in the
  companion paper (`research.json` components[1]; paper Appendix 2 quoted in XS2101).
- **Rejected alternative — a continuous 1947→1998 industry time series.** Declined for the same reason
  as S901: the 71-order SIC and 65-order NAICS eras are not conformable and cannot be spliced (§4).
  Shaikh reports the years as a discontinuous panel, never a bridged series.
- **Rejected alternative — nominal-vs-real GDP ratios or Marx-Tonak constant/variable-capital
  aggregates as the SSE measure.** Explicitly ruled out in `XS2001_EPR.md` §6: "No alternative agency
  exists for the industry-level technology matrix needed"; the SSE is a property of the *Sraffa* price
  system solved on the BEA `A`-matrix, so only the eigenvalue/left-eigenvector computation on that
  matrix family measures the intended concept.

## 4. Methodological-change exposure — **the central section**

XS2001 sits on the **SIC→NAICS classification wall**, the same Phase-0 obstacle that governs S901
(`IO_CHANGE_TIMELINE.md`, "The SIC → NAICS break (the Ch9 wall)"):

1. **71-order SIC ↔ 65-order NAICS non-splice.** Last SIC benchmark = **1992**; first NAICS benchmark =
   **1997**. BEA explicitly states the pre-1997 historical benchmark tables **"should not be used as a
   time series."** XS2001's panel jumps **1972 → 1998** directly across this wall. The 1947–1972 Ochoa
   71-order (SIC) cross-sections and the 1998 BEA 65-order (NAICS) Use table are **not conformable**; a
   single continuous industry panel across the gap is not reconstructable. RSCD carries this as an
   explicit caveat — "Matrix-size discontinuity: 71-order for 1947–1972, 65-order for 1998. Documented
   as a column in the chopped CSV" (`XS2001_DPR.md` §7 caveat 2). Because the SSE is an *aggregate*
   scalar per year, the discontinuity is benign for the *stated claim* (each year's near-unity ratio
   stands on its own) — but it forbids treating the six scalars as a bridged industry series.
2. **Even within NAICS, industry order drifts.** The summary/detail row-column order is revised at each
   benchmark (1997/2002/2007/2012/2017), so any v1.1 extension that adds 2002/2007/2012/2017 aggregate
   ratios needs a fresh `A`-matrix build, fresh exclusions, and fresh labor coefficients per benchmark —
   not a splice (`IO_CHANGE_TIMELINE.md` "Industry order / detail notes"; `research.json`
   extension_candidates concerns).
3. **Concordance authority (`concordance_touch`).** The Census SIC↔NAICS bridges required even to
   *attempt* a crosswalk are staged in `concordances/_sources/naics/` (1987 SIC↔1997 NAICS and the
   1997→2002→…→2022 NAICS revision chain); BEA's own I-O↔SIC/NAICS concordances live only as SCB-PDF
   appendix tables (SCB Dec 2002 App. A for 1997 I-O codes; SCB Aug 2018 App. A for the 2007↔2012 I-O
   concordance — `IO_CHANGE_TIMELINE.md` Sources). These document *why the crosswalk is lossy*,
   reinforcing the non-splice discipline.
4. **Capital-flow benchmark discontinuity (fixed-capital model, Table 2).** The BEA benchmark
   capital-flow table — the use-type × industry matrix that distributes fixed investment across
   industries — was **last produced for 1997** (SCB Nov 2003) and **discontinued thereafter**
   (`IO_CHANGE_TIMELINE.md` "Capital-flow benchmark matrix"). Shaikh's fixed-capital model (Table 2)
   needs an asset-by-industry distribution; his 1998 column can lean on the 1997 benchmark capital-flow
   matrix, but **any post-1998 fixed-capital extension must approximate** that distribution from BEA's
   detailed Fixed Asset Tables — a structural obstacle to extending Table 2 that does not afflict the
   circulating-capital Table 1.
5. **NIPA vintage coupling (indirect).** The 1998 side draws BEA value-added and the owner-occupied
   housing correction, which are NIPA-vintage-sensitive. Shaikh fixes BEA data at the **2011 vintage**
   (project convention; `NIPA_CHANGE_TIMELINE.md`). Any re-pull of the 1998 Use table after the 2013,
   2018, or 2023 comprehensive revisions would land on reclassified magnitudes (R&D/software → IPP
   capitalization; ~+$400B GDP; Fixed-Asset levels rise) and must **never be spliced across a
   comprehensive-revision boundary** — the same rule that governs the GPIM appendix chain.

## 5. Replication fidelity note

RSCD reproduces XS2001 **bit-exact to the published Tables 1–2** by verbatim transcription:
`XS2001_aggregate_ratios.csv` → chopped → parquet, with V03 comparing the processed parquet against the
reconstructed CSV cell-by-cell. Result: **PASS, MAE 0.0, max %err 0.00%, 108 rows**, tolerance 0.5%
(`ES_PHASE_5_8_CLOSURE.md` table; `XS2001_DPR.md` §9). Honest limits, disclosed:

- **Self-consistency, not independent re-read.** V03 validates the melt of the reconstructed CSV against
  the reconstructed CSV — it confirms **transcription fidelity**, not an independent re-read of the
  published PDF. MAE 0.0 means "the pipeline did not corrupt the numbers we typed in," not "the numbers
  were re-derived from BEA source." This is the standard external-study caveat (shared-brief §5).
- **The BEA-to-Sraffa pipeline is NOT executed in v1.0.** No `A`-matrix is built, no eigenvalue `R` is
  solved, no Sraffa price is computed. The aggregate ratios are Shaikh's own computed values, ingested.
  The end-to-end recompute (build Use/Make loader → apply paper-Appendix-I exclusions [owner-occupied
  dwellings, scrap, used/secondhand, non-comparable imports, RoW] → construct `A` → compute
  `H = A(I−A)⁻¹` → solve `R` and `p(R)` → compute `p(r)` at `r_obs` → form aggregate ratios) lives only
  in the **deferred v1.1 shared-pipeline recipe** (`XS2001_EPR.md` §3, steps 1–6). This is a multi-day
  engineering effort (3–5 days per `ES_PHASE_5_8_CLOSURE.md` v1.1-deferrals table), shared with XS2101.
- **Figures 1–9 are not in this series.** The 2002 403-order sector price curves and Bienenfeld
  linear/quadratic approximations (the paper's *cross-sectional* object) are explicitly excluded from
  XS2001 v1.0 and deferred to v1.1 (`XS2001_DPR.md` §7 caveat 4; EPR §3 step 6). They must be
  **regenerated** from the 2002 matrix via eqs 6/8/10 — **never chart-digitized** (`research.json`
  open_questions[4]; no-fabrication rule).
- **No proxies, no synthetic data.** v1.0 is verbatim transcription only (`XS2001_EPR.md` §§4–5).

## 6. Forward risk

- **v1.1 pipeline is the whole extension.** Filling the missing BEA benchmark aggregate-ratio years
  (1977, 1982, 1987, 1992, 2002, 2007, 2012, 2017) — which would turn the sparse 6-year panel into a
  near-quinquennial 1947–2017 SSE series — requires standing up the shared `BEA_benchmark_IO_to_Sraffa`
  pipeline and running it on each benchmark matrix (`XS2001_EPR.md` §1, §3; `research.json`
  extension_candidates[3]). Each added benchmark arrives on a *fresh NAICS vintage with revised industry
  order*, so extension is benchmark-**addition**, never a splice.
- **Fixed-capital extension is structurally blocked past 1998.** The discontinued benchmark capital-flow
  table (last = 1997) means the Table-2 (fixed-capital) model cannot be cleanly extended to
  2002/2007/2012/2017 without approximating the asset-by-industry distribution from detailed Fixed
  Asset Tables (§4 item 4). Table 1 (circulating) has no such obstacle.
- **NIPA comprehensive revisions keep moving the 1998 magnitudes.** Any re-pull of the 1998 Use table
  post-2013/2018/2023 lands on reclassified value-added; stay on one coherent vintage
  (`NIPA_CHANGE_TIMELINE.md`).
- **Source-URL / venue fragility.** `anwarshaikhecon.org` was DNS-unreachable at ingestion; the
  URL-of-record is the archival PDF (`XS2001_EPR.md` §7). The festschrift **DOI/volume is not pinned**
  (paper's own reference list cites Velupillai (ed.), Palgrave Macmillan; `research.json`
  open_questions[2]) — a v1.1 metadata task.
- **Upstream-appendix dependency.** Extending Tables 1–2 needs Shaikh (1998) Appendix 15.2 and Shaikh
  (2012) Data Appendix acquired/scanned into the KB if not already present (`research.json`
  open_questions[5]).
