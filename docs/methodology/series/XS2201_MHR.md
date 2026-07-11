# XS2201 — Methodological History Report (MHR)

**Series**: XS2201 — Econophysics Two-Class Income Distribution Parameters, US 2002–2016 (Shaikh-Jacobo 2020, Table 1)
**Chapter**: 0 (`xs_class: external_study`) · **Group**: external-study family 22 · **Status**: study_complete
**Perspective**: authored *from Shaikh's perspective* — why *he* built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS2201_research.json`; `Technical/docs/series/XS2201_DPR.md` +
`XS2201_EPR.md`; `Technical/docs/external_studies/XS2201_paper_summary.md` + `ES_PHASE_5_8_CLOSURE.md`;
`Technical/methodology_review/CH_XS_review.json`.

Paper of record: Shaikh, A. & Jacobo, J.E. (2020), "Economic Arbitrage and the Econophysics of Income
Inequality", *Review of Behavioral Economics* 7: 1–17, DOI 10.1561/105.00000129 (now Publishers).
Archival PDF: `SalvagedInputs/methodology_library/B_shaikh_post2016/WL-B-Income/` and
`Inputs/Capitalism Data/.../Shaikh Publications/[2020] Shaikh & Jacobo - Economic Arbitrage and the Econophysics of Income Inequality.pdf`
(`XS2201_paper_summary.md` header). This paper is the journal-article extension of **Shaikh (2016) Ch.17**
("The Theory of the Distribution of Personal Income").

---

## 1. What it is

XS2201 is Shaikh-Jacobo's **annual panel of five jointly-fitted parameters** of the econophysics
"two-class" income-distribution model, US tax years **2002–2016** (15 years). It is the transcription
of the paper's **Table 1 (p.5)** — the *only* time-series object in the paper (Figures 1–3 are
2011-only snapshots; `research.json` methodology_notes[5]; `XS2201_paper_summary.md` §4 note). The five
parameters per year (`XS2201_DPR.md` §1; `research.json` components):

- **G′** — Gini coefficient of the **bottom 97%** (dimensionless; expected ≈ 0.5 for a pure
  exponential), via the midpoint Gini method (Brooks, Notre Dame).
- **⟨r⟩** — overall mean AGI per return (thousands USD) = total AGI / total returns.
- **⟨w⟩** — bottom-97% mean, the **"income temperature"** (thousands USD) — *not* a sample mean but the
  inverse slope of an MLE regression (see §3).
- **f** — top-3% income share (dimensionless), a derived identity `f = 1 − ⟨w⟩/⟨r⟩`.
- **α** — top-3% Pareto power-law exponent (dimensionless).

The model is a **two-class distribution**: the bottom ~97% (essentially labor income) follows a
Boltzmann/exponential ("thermal") law; the top ~3% (essentially property income) follows a Pareto power
law ("superthermal"). Shaikh states the framing verbatim (paper p.2, `research.json` book_quotes[0],
`verbatim_check: true`):

> "… the bottom 97-99% of the overall distribution of personal incomes, which is essentially labor
> income, is well approximated by an exponential distribution, while top 1-3%, which is essentially
> property income, is well approximated by a power law."

The labor/property **break point** falls **within the $100,000–$200,000 AGI bin in every year**
2002–2016 (paper p.14, `research.json` book_quotes[3], `verbatim_check: true`): the two sections are
treated as separate populations, each with `C(r)` beginning at 1, and MLE regression is used
throughout. The novel theoretical contribution (paper Section 4 — **not** in the book) replaces the
prior entropy-maximization derivation with a **turbulent-arbitrage drift-diffusion SDE framework**
(CIR/Feller eq.4 → stationary Gamma; log-linear eq.5 → Gamma, preferred for wages; log-log eq.6 →
Lognormal, preferred for property income; `XS2201_paper_summary.md` §5). The SDE framework is
theoretical context, not a datable series — XS2201 is Table 1 only.

## 2. Source lineage

XS2201's *data of record* for v1.0 is the paper's own Table 1, transcribed verbatim to
`SalvagedInputs/book_data/Reconstructed/XS2201_fitted_parameters.csv` (75 chopped rows = 15 years × 5
params; `ES_PHASE_5_8_CLOSURE.md`; `XS2201_DPR.md` §3). This series has **no NIPA and no IO/concordance
touch** — its provenance is IRS administrative tax data (`research.json` primary_source;
`XS2201_paper_summary.md` §7):

- **IRS Statistics of Income (SOI) Division, Publication 1304** (Individual Income Tax Returns —
  Complete Report), Individual Statistical Tables by Size of Adjusted Gross Income:
  - **Table 1.4** ("All Returns: Sources of Income … by Size of Adjusted Gross Income"), **columns
    1–2**: AGI bin endpoints (current USD) + number of returns per bin (count), tax years **2002–2016**.
    These give the bin midpoints `rᵢ` and frequencies `nᵢ` (`research.json` components domain/frequency).
  - **Table 1** ("Selected Income and Tax Items, by Size … of AGI"): **Total AGI** and **total returns**,
    the normalizers for ⟨r⟩. The paper notes Total AGI from Table 1 equals Total AGI-less-deficit in
    Table 1.4 (paper p.14, `research.json` book_quotes[2], `verbatim_check: true`).
- **Brooks (Notre Dame) GiniNotes.pdf** — the midpoint-Gini method reference for G′
  (`https://www3.nd.edu/~wbrooks/GiniNotes.pdf`; a methodology reference, not a data source;
  `research.json` components[G′], methodology_notes[4]).
- **World Inequality Database (WID)** — listed only as a *cross-validation* sanity check on the top-3%
  share `f`, "usable only as a sanity check … not as a substitute" (different concept: national income
  vs AGI; `research.json` extension_candidates[2]).

The verbatim Sources-and-Methods anchor (paper p.14, `research.json` book_quotes[2]): "Adjusted Gross
Income (AGI) bins and number of returns in each bin are from IRS Tables 1.4 for 2002-2016, column 1-2 …
Total AGI is from IRS Table 1 … and ⟨r⟩ = average AGI = total AGI/total returns."

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

- **Why IRS SOI binned data, not survey micro-data (CPS/PSID).** The scientific target is the **top
  tail** — the Pareto/superthermal top 3% and its exponent α. Household surveys (CPS, PSID) top-code
  and thin the upper tail, destroying exactly the region Shaikh needs; administrative tax data does
  not. RSCD records this precisely: "IRS SOI Pub 1304 is the only US administrative micro-data
  binned-tabulation source that supports the Dragulescu-Yakovenko exponential + Pareto MLE jointly.
  Survey-based CPS/PSID sources truncate the Pareto top tail and are not suitable" (`XS2201_EPR.md`
  §6). The cost of that choice — the data arrives **pre-binned**, not as individual records — is
  precisely what forces the regression-based ⟨w⟩ (next point).
- **Why ⟨w⟩ is an MLE-regression "income temperature", not a raw bottom-97% mean.** Because the data is
  binned, "the mean income of the lower section cannot be directly calculated from midpoint data"
  (paper p.14, `research.json` book_quotes[4], `verbatim_check: true`). Shaikh therefore estimates ⟨w⟩
  as the **inverse slope of the MLE regression of `ln C(r)` vs `r`** on the bottom section — i.e. the
  characteristic scale of the fitted exponential, the "income temperature" in the econophysics sense.
  This is a *theory-driven* estimator, not a convenience: the exponential model *is* the hypothesis, so
  its rate parameter is the right summary of the bottom class. A crude bin-midpoint sample mean would
  (a) be biased by the arbitrary top-bin midpoint convention and (b) not correspond to any parameter of
  the two-class model. The Anu no-proxy rule is explicit here: "any extension must replicate this
  regression-based ⟨w⟩, NOT substitute a direct bottom-97% mean from microdata" (`research.json`
  methodology_notes[2]; `XS2201_DPR.md` §7 caveat 1).
- **Why the two-class split at the $100K–$200K break, data-driven per year, not a fixed threshold.**
  The break is found by "successively adding points to the lower section plot `ln C(r)` vs `r` until a
  significant curvature was evident" (paper p.14, book_quotes[3]) — the point where the exponential
  (labor) regime gives way to the power-law (property) regime. Fixing a dollar threshold would impose
  the answer; the data-driven search lets the break move (though empirically it always lands in the
  same bin). Extension years must **re-identify** the break, not reuse a fixed cut (`research.json`
  methodology_notes[1]).
- **Why top share `f` as the identity `1 − ⟨w⟩/⟨r⟩`, not an independent estimate.** Given the
  two-class decomposition, the top share is *definitionally* the residual of total mean income above
  the thermal mean (Banerjee & Yakovenko 2010; paper p.14, book_quotes[4]). Deriving it as an identity
  keeps the accounting internally consistent with ⟨w⟩ and ⟨r⟩ rather than introducing a separate,
  possibly incompatible, top-share number.
- **Why the turbulent-arbitrage SDE derivation over energy-conservation/entropy-maximization.** The
  prior Yakovenko-school derivation rests on a thermodynamic energy-conservation analogy. Shaikh
  replaces it with a **mean-reverting stochastic arbitrage** process (drift toward an equalized mean +
  diffusion), which he regards as the correct *economic* micro-foundation — arbitrage, not physics,
  drives incomes toward class-specific attractors. This is the paper's original contribution (Section
  4) and the reason the framework generalizes the book's Ch.17 treatment (`XS2201_paper_summary.md`
  §§1,5). It is theory, not a data series.
- **Rejected alternative — full-population Gini / Piketty-Saez top shares.** Disambiguated explicitly:
  "G′ is the *bottom-97%* Gini, NOT the full-population Gini (Census/CBO/World Bank report the latter);
  α is the *top-3%* Pareto exponent, NOT the Piketty-Saez top-share statistic; ⟨w⟩ is a
  regression-derived 'income temperature' inverse slope, NOT a sample mean" (`XS2201_EPR.md` §6). Those
  adjacent statistics measure different objects and would not be the two-class parameters.

## 4. Methodological-change exposure — **the central section**

XS2201 has **no NIPA/IO vintage exposure at all** — its source is IRS SOI, not the national accounts,
so the comprehensive-revision timeline and the SIC→NAICS wall that dominate the GPIM appendix chain and
the Sraffa series (XS2001/XS2101) simply do not apply. Its methodological breaks are **tax-law and
tax-table conventions**:

1. **TCJA-2017 AGI-definition break.** The Tax Cuts and Jobs Act (effective tax year 2018) changed what
   enters Adjusted Gross Income (deductions, exemptions, pass-through treatment). Because the entire
   series is keyed on AGI bins, a post-2017 extension crosses a **definitional discontinuity** — the
   AGI of 2018+ is not the AGI of 2002–2016 without a continuity check. RSCD flags this: "Post-TCJA
   (2018+) AGI definition revisions need to be checked for continuity" (`research.json`
   extension_candidates concerns; `XS2201_DPR.md` §7 caveat 4; `XS2201_EPR.md` §6). The paper's own
   window (2002–2016) stops *before* TCJA, so v1.0 is internally clean.
2. **CARES-2020 AGI adjustments.** The CARES Act (tax year 2020) introduced further AGI-relevant
   provisions (e.g. above-the-line adjustments), a second definitional break any 2020+ extension must
   validate (`XS2201_DPR.md` §7 caveat 4; `research.json` open_questions[4]).
3. **Top-bin convention.** IRS Table 1.4's highest bin is **open-ended** ($10M+ in recent years). The
   paper says "bin midpoints" but does not specify the top-bin treatment; since the top bin drives the
   Pareto α, the convention (Pareto-tail integral vs fixed multiplier of the lower bound) materially
   affects the fit. v1.1 must **document** a convention (Pareto integral preferred; `research.json`
   open_questions[2]; `XS2201_DPR.md` §7 caveat 3). This is a *methodology* exposure internal to the
   estimator, not a vintage drift.
4. **Bin-schedule changes across years.** The AGI bin cut-points are revised over time, so the midpoint
   convention "must be applied year-by-year" and the break-point search re-run per year (`research.json`
   extension_candidates concerns; methodology_notes[1]).
5. **IRS SOI release lag.** Pub 1304 tables publish ~2–3 years after the tax year, so as of 2026 the
   latest available year is likely 2022 or 2023 (`XS2201_EPR.md` §1). Not a definitional break, but a
   hard extension-window limit.
6. **Brooks GiniNotes.pdf URL is dead (404).** The paper-cited midpoint-Gini reference is unreachable;
   v1.1 substitutes Cowell (2011) *Measuring Inequality* ch.5 or a Wayback-archived Brooks PDF — "a
   methodology-reference substitution, NOT a data-source proxy" (`XS2201_DPR.md` §7 caveat 5;
   `XS2201_EPR.md` §4).

## 5. Replication fidelity note

RSCD reproduces XS2201 **bit-exact to the paper's Table 1** by verbatim transcription:
`XS2201_fitted_parameters.csv` → chopped (one row per (year, parameter)) → parquet, V03 cell-by-cell
against the CSV. Result: **PASS, MAE 0.0, max %err 0.00%, 75 rows**, tolerance 0.5%
(`ES_PHASE_5_8_CLOSURE.md` table; `XS2201_DPR.md` §9). Honest limits, disclosed:

- **The MLE fit is NOT executed in v1.0.** RSCD ingests Shaikh & Jacobo's *already-fitted* five
  parameters — it does **not** re-run the cumulative-from-above → break-point search → exponential fit
  → power-law fit pipeline. The parameters are the authors' computed outputs, transcribed
  (`XS2201_DPR.md` §4; `XS2201_EPR.md` §2). The full estimator (acquire Pub 1304 Tables 1.4+1 →
  implement MLE for ⟨w⟩ and α → document top-bin convention → re-fit per year) is the **v1.1 deferral**
  (`XS2201_EPR.md` §3; ~1–2 days per `ES_PHASE_5_8_CLOSURE.md`).
- **Self-consistency, not independent re-read.** As with all external-study series, V03 confirms the
  transcription round-trips (melt vs reconstructed CSV) — **not** an independent re-read of the RBE PDF
  and **not** a re-derivation from IRS source. MAE 0.0 = transcription fidelity only (shared-brief §5).
- **Figures 1–3 are 2011 snapshots, not in the series.** The time-series content is Table 1 alone;
  reproducing the figures would need the raw 2011 IRS Table 1.4 bin data, a separate object
  (`research.json` methodology_notes[5]; `XS2201_paper_summary.md` §4 note).
- **⟨w⟩ and f are derived, not directly observed.** Any extension MUST re-fit ⟨w⟩ by regression and
  re-derive `f = 1 − ⟨w⟩/⟨r⟩` — **never growth-rate splice** the fitted parameters (Anu "No Lazy
  Splices on Derived Quantities" rule, because the five parameters are jointly estimated;
  `research.json` methodology_notes[2]; `XS2201_paper_summary.md` §10).
- **No proxies, no synthetic data.** v1.0 is verbatim transcription; the only substitution contemplated
  is the dead Brooks Gini-notes *methodology reference* (§4 item 6), not a data proxy.

## 6. Forward risk

- **2017+ MLE re-fit is the whole extension, and it crosses two AGI-definition breaks.** Extending the
  panel to 2017–2023 requires re-running the paper's exact MLE pipeline per year on later Pub 1304
  vintages **and** validating continuity across **TCJA-2017** and **CARES-2020** (§4). Fitted parameters
  must be re-computed, never spliced (`XS2201_EPR.md` §3; `XS2201_paper_summary.md` §8).
- **Top-bin convention must be pinned before any re-fit.** The open-ended top bin drives α; v1.1 must
  adopt and document a Pareto-tail (or fixed-multiplier) convention or the top-3% parameters are not
  reproducible (`research.json` open_questions[2]).
- **IRS release lag caps the window.** ~2–3-year lag → latest available ~2022/2023 as of 2026
  (`XS2201_EPR.md` §1).
- **BLS is not applicable here.** Unlike the Sraffa series (which lean on BLS labor coefficients),
  XS2201 draws *no* BLS input — its labor/property split is internal to the IRS AGI distribution, so
  BLS program changes carry no forward risk for this series.
- **Dead methodology-reference URL.** Brooks GiniNotes.pdf (404) must be re-sourced (Cowell 2011 ch.5
  or Wayback archive) and archived to `SalvagedInputs/` at extension time (`XS2201_EPR.md` §4;
  `research.json` open_questions[3]).
- **Pre-2002 backfill option.** IRS SOI Table 1.4 exists back to ~1995 in modern format; extending
  *backward* is methodologically straightforward but requires per-year re-fitting and earlier bin
  schedules — a decision, not an obstacle (`research.json` open_questions[1]).
- **Figure-2/3 label ambiguity.** Whether the "Wage Data" / "Property Income Data" labels denote the
  Table-1.4 AGI cut at the break or a separate W-2 tabulation is not explicit in the paper; confirm
  against the authors' spreadsheet if released (`research.json` open_questions[6]).
