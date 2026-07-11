# S208 — US Manufacturing Real Unit Production Labor Cost Index — Methodological History Report (MHR)

**Group:** ch2 (Turbulent Trends and Hidden Structures) · **Construction:** formula · **Status:** book_period_validated
**Figure:** 2.6 · **Predecessor:** CD/CD2 S008 · **Publish:** true · **Book period:** 1889–2010 · **Extension:** 2011–2025
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S208_research.json`), the DPR/EPR (`Technical/docs/series/S208_{DPR,EPR}.md`),
> the registry (`Technical/series_registry.json` → `series.S208`), the book KB (Body_Text
> `ch02_turbulent_trends.md`, Figure `ch02_fig_2.6.md`), the CH2 review
> (`Technical/methodology_review/CH02_review.json`), and the Phase-0 NIPA timeline
> (`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`). Where a rationale is not present in
> the corpus it is marked **"author rationale not located in corpus."**

---

## 1. What the series is

S208 is the annual index plotted as **Figure 2.6, "US Manufacturing Real Unit Production Labor Cost Index,
1889–2010"** (Chapter 2 §II; KB `Figures/ch02/ch02_fig_2.6.md`, book p. 61; y-axis 0–150, Index 1889 = 100).
It is a **derived (formula) series**, not an independently sourced one: **real unit labor cost = the ratio of
real wages to productivity** (book p. 60, `S208_research.json` book_quotes[0], role=definition). Appendix 2.1
states it plainly: *"Figure 2.6 … Derived as the ratio of manufacturing real compensation and productivity in
the previous chart"* (book p. 764, `S208_research.json` book_quotes[1], role=source). In RSCD terms it is
exactly **(S207-B ÷ S207-A) × 100** (`S208_DPR.md` §1).

The concept has a **firm-side** definition that matters for the sources. Book **footnote 3** (p. 60–61,
`ch02_turbulent_trends.md` lines 272–276) distinguishes the *worker-side* real wage of Fig 2.5 (money wage ÷
CPI) from the *firm-side* real wage that underlies Fig 2.6: **"from the point of view of firms, what matters is
the real wage relative to the price of the product. This is the basis for the real unit labor cost measure in
figure 2.6. Note that the real unit labor cost, so defined, is also the share of the nominal wage bill in the
total money value of output."** So S208 is simultaneously (a) real wages ÷ productivity and (b) the **wage
share of the value of output** — the Marxian labor-share / profit-margin driver ("a rise in real unit labor
costs lowers real profit margins," KB `ch02_fig_2.6.md` Importance-for-Business; book p. 60). Shaikh reads its
history as five episodes: 1889–1909 decline, 1909–1929 stability, a 1929–39 Depression anomaly, 1947–63
"Golden Age" stability, and an "extraordinary secular decline" 1963–2010 (KB `ch02_fig_2.6.md` Main
Observations). Final units: **Index, 1889 = 100** (`S208_DPR.md` §6; registry `units`).

## 2. Source lineage — the formula and its component provenance

S208 has **no primary data source of its own** (registry `primary_source: null`; `S208_research.json`
primary_source.agency = "Derived (Shaikh 2016)"). Its provenance *is* the provenance of S207's two legs.

**Formula (registry `formula`; `S208_DPR.md` §4):**

```
RULC_index[t] = ( real_compensation_per_hour[t] / productivity_index[t] ) * 100
```

with components (registry `components`):

| Formula component | Source series | Underlying provenance (see S207 MHR §2) |
|---|---|---|
| Real compensation per hour | **S207-B** | MeasuringWorth nominal comp `ec` ÷ CPI, 1774–2010, rebased 1889=100 |
| Manufacturing productivity index | **S207-A** | BEA LTEG 1966 A173 [1889–1949] spliced at 1950 with BLS ILC Table 1 [1950–2009], rebased 1889=100 |

| Subseries | Coverage | How built | Retrieval |
|---|---|---|---|
| **S208-A** book RULC | 1889–2010 | Read directly from Shaikh's chopped column **`Mfgrealunitlaborcost`** (his own derived ratio) | Salvaged chopped `Appendix2_ManufacturingProductivity.csv` |
| **S208-B** extension | 2011–2025 | **Recompute the formula** from extended S207 components (S207-C productivity + S207-D/-B compensation), rescaled so the 2010 extension value equals the 2010 book value | Formula recompute (no direct series pulled) |

Registry `validation.reference_values` (subseries S208-A, tol 0.01): **1889 = 100.0, 1950 = 117.005337,
2010 = 28.775885** — the deep 2010 trough (≈ 29% of the 1889 level) is the "extraordinary secular decline"
Shaikh describes, and is the V03-certified spine of the book series.

**Exact chain:**

```
BOOK PERIOD (S208-A): read chopped 'Mfgrealunitlaborcost' [1889–2010]  ← Shaikh's own ratio, byte-faithful
EXTENSION (S208-B): for each post-2010 year, recompute
    RULC[t] = (real_comp_ext[t] / productivity_ext[t]) * 100
    using S207's EXTENDED components (OPHMFG productivity, COMPRMS/MW real comp)
    → rescale so RULC_ext[2010] == RULC_book[2010]  (overlap anchor)
    → append
    NEVER splice FRED ULCMFG directly (it is NOMINAL unit labor cost — wrong object)
```

## 3. Why these sources, from the author's perspective

**The concept Shaikh measures.** Real unit labor cost is, for Shaikh, "of paramount importance to business" and
the aggregate driver of profit margins — "a rise in real unit labor costs lowers real profit margins" (book
p. 60; KB `ch02_fig_2.6.md`). Because it equals the wage share of the value of output (fn 3), it is the Marxian
"labor share" tracked over 120 years (`S208_DPR.md` §2). The figure's rhetorical job is to end "that particular
illusion" — born of Golden-Age stability — "that wages automatically rise alongside productivity" (KB
`ch02_fig_2.6.md` Key Insight).

**Why derive it rather than source a ready-made ULC series.** The whole point is *internal consistency* with
Fig 2.5: Shaikh wants the *same* real compensation and *same* productivity that generated the divergence in
Fig 2.5 to be the numerator and denominator of Fig 2.6, so the reader sees the two figures as one argument.
Building RULC as the explicit ratio of his own two series guarantees that; importing an off-the-shelf ULC index
would silently substitute a *different* compensation concept and a *different* deflator. Appendix 2.1's one-line
derivation ("the ratio of manufacturing real compensation and productivity in the previous chart") is the
author's stated rationale (`S208_research.json` book_quotes[1]).

**Why NOT FRED ULCMFG for the extension.** FRED `ULCMFG` is *nominal* unit labor cost (compensation ÷ output),
**not** the deflated real-wage-to-productivity ratio Shaikh computes; splicing it in would be a **silent proxy**
that changes the measured object (`S208_research.json` extension_candidates[0].concerns;
`S208_DPR.md` §7 caveat 1; registry `extension_note`). The Anu Framework **no-lazy-splice rule for derived
quantities** therefore requires the extension to **recompute the formula from extended components** rather than
splice the ratio (registry `adequacy.issues_outstanding`; `S208_research.json` methodology_notes[2];
`S208_EPR.md` §2). This is the single most consequential methodological choice in S208.

**Rejected alternatives beyond ULCMFG.** The research JSON open-question notes that a specific post-2013 BLS
manufacturing real-hourly-compensation series (CD2 cited BLS `PRS30006152`) may be discontinued, which is part
of why the extension leans on the recomputed OPHMFG/COMPRMS components rather than a single modern ULC series
(`S208_research.json` open_questions). An explicit in-book argument weighing these alternatives is **not located
in corpus** — Appendix 2.1 gives only the one-line derivation.

## 4. Methodological-change exposure

- **Compounded parent exposure (the defining risk).** Because S208 is a *ratio of S207's two legs*, it inherits
  **both** parents' vintage exposures at once. The productivity leg carries the **BLS FLS/ILC program SUNSET
  (2013)** → **US-only OPHMFG concept-narrowing** exposure documented in the S207 MHR (§4) and review finding
  **F-09**; the compensation leg carries MeasuringWorth's CPI-splice behavior. A distortion in *either* parent
  propagates into the ratio — and, worse, if the two legs are extended on *different* program bases the ratio
  can drift even when neither level looks individually wrong.
- **NIPA vintage effects (indirect, via productivity).** S208 is index-on-index and not a NIPA magnitude, so the
  comprehensive revisions (1999/2003/2009/**2013**/**2018**/**2023**; `NIPA_CHANGE_TIMELINE.md`) do not restate
  its level directly. The relevant tie is the **2013** revision (R&D+entertainment → IPP, ≈ +$400 B GDP, 2007
  benchmark I-O) coinciding with the BLS FLS sunset at the same 2013 boundary — reinforcing the Phase-0 rule to
  **never splice across a comprehensive-revision boundary** and to keep the extension on Shaikh's **2011 BEA
  vintage** discipline (`NIPA_CHANGE_TIMELINE.md` §"Why this matters").
- **FRED re-basing of the recompute inputs.** Since S208-B is recomputed from OPHMFG and COMPRMS, any FRED
  base-year change to those inputs must be neutralized *before* the ratio is formed; the overlap-anchor rescale
  at 2010 (`S208_DPR.md` §4) and the failure-table overlap walk-back (`S208_EPR.md` §5) handle this.
- **Concordance / I-O dependency:** none direct (the ratio has no crosswalk of its own; it inherits S207's,
  which are also none direct — contrast `CH02_review.json` touchpoints S213/S214).

## 5. Replication fidelity note

- **RSCD reproduces the book ratio byte-faithfully.** The 1889–2010 line is read directly from Shaikh's own
  chopped `Mfgrealunitlaborcost` column (S208-A), so the book period *is* the author's derived series (expected
  MAE < 0.5%; `S208_DPR.md` §9). Reference values 1889/1950/2010 = 100 / 117.01 / 28.78 tie out (§2).
- **No-lazy-splice recompute enforced (the fidelity keystone).** The extension **recomputes the RULC formula
  from S207's extended components** and does **not** splice FRED ULCMFG (nominal). This is stated as a hard
  requirement in the registry (`extension_note`, `adequacy.issues_outstanding`), the DPR (§7 caveat 1), and the
  EPR (§2 Method) — honoring the Anu no-lazy-splice rule for derived quantities. RSCD thereby avoids the silent
  concept-substitution that a direct ULCMFG splice would introduce.
- **No proxy on the formula itself; no synthetic fill.** Registry `proxy: false`; `S208_EPR.md` §3. Any NaN in
  a parent component propagates (no interpolation, `S208_EPR.md` §4). The extension is contingent on S207-C/-D
  being populated (FRED success); if not, the series publishes the book period only.
- **Honest limits.** (a) The extension's fidelity is only as good as its parents — it *inherits* S207's US-only
  productivity concept-narrowing (S207 F-09), so post-2010 RULC is on a slightly different conceptual basis than
  1889–2010. (b) The 1929–39 "anomalous rise" and 1963–2010 secular decline are faithful features of Shaikh's
  own ratio, not artifacts. **No CH2-review finding is specific to S208**; only the general **F-03** (no
  `S2##_DECOMPOSITION.md` project-wide; construction lives in DPR §4 + registry `formula`/`components`) applies,
  and this MHR §2 supplies that decomposition narrative.

## 6. Forward risk

- **Formula-recompute drift (the standing risk).** The extension is only correct if productivity and
  compensation are recomputed on a *consistent, co-anchored* basis each run. If a future maintainer takes the
  documented shortcut and splices FRED ULCMFG (or caches a rescaled ratio across a FRED rebasing), the post-2010
  line silently becomes a nominal-ULC proxy. Guard: keep the recompute-from-components path and the 2010 overlap
  anchor; treat any ULCMFG appearance in the S208 loader as a defect.
- **Inherited sunset risk.** Whatever befalls the S207 productivity extension (OPHMFG revision/re-reference, or
  eventual discontinuation of the BLS Productivity & Costs manufacturing series) flows straight into S208's
  denominator. Re-anchor both parents together; do not extend the ratio past the last year both parents are
  available.
- **Discontinued modern manufacturing PRS series.** The open question about post-2013 BLS manufacturing
  real-hourly-compensation availability (`PRS30006152`) means the compensation leg of the recompute may need a
  documented substitute in future; if so, flag it as a proxy on S207-D and re-derive — never paper over it in
  S208 (`S208_research.json` open_questions).
