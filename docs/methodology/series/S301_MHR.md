# S301 — Change in Expenditure Relative to Change in Income, Case I — Methodological History Report (MHR)

**Group:** ch3 (Micro Foundations and Macro Patterns) · **Construction:** formula (analytic) · **Status:** book_period_validated
**Figure:** 3.3 (book p. 94) · **Predecessor:** none (no CD/CD2 row) · **Publish:** true
**Reasoning stance:** from Shaikh's own perspective — why *he* drew this curve this way.

> Grounding note: every author-intent claim is anchored to a citable path — the research JSON
> (`Technical/research/S301_research.json`), the KB body text + equations
> (`Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/Body_Text/ch03_micro_foundations.md`,
> `.../Equations/ch03_equations.md`), the chapter summary (`Technical/docs/chapters/CH3_RESEARCH_SUMMARY.md`),
> the review (`Technical/methodology_review/CH03_review.json`), the DPR/EPR
> (`Technical/docs/series/S301_{DPR,EPR}.md`), and the loader (`Technical/code/L01_loaders/L01_S301.py`,
> `_ch3_helpers.py`). No claim is invented.

---

## 1. What it is

S301 is the **analytic curve behind Figure 3.3**: the marginal expenditure share on the necessary good,
`d(p1x1)/dy`, plotted against income `y` over the model grid `y ∈ [0, 60]` (dimensionless share, axis 0–0.8).
It is **not empirical** — it is a deterministic evaluation of one of Shaikh's fundamental consumer-choice
equations. Shaikh's own caption group (`research.book_quotes[0]`, role=definition, p. 93):
*"Figures 3.3–3.5 display the results of the case in which x1min rises more slowly than income…"* Figure 3.3
is the *marginal* member of the Case-I triple (3.3 marginal share → 3.4 average share → 3.5 integrated Engel
curve). Its purpose in the chapter's argument is to show **Engel-curve saturation** arising purely from a
shaping structure (a socially-defined necessary minimum that grows sub-linearly in income), with no appeal to
hyper-rational optimization (`CH3_RESEARCH_SUMMARY.md` "Chapter scope").

## 2. Source lineage

Single source: **Shaikh (2016), equation family (3.4)–(3.11), pp. 91–93; Figure 3.3, p. 94** — no external
data agency. The governing equation is quoted verbatim in the KB body text (p. 93) and in
`research.book_quotes[1]` (role=method): the slope of the Engel curve is
`d(p1x1)/dy = (1 − c) · d(p1x1min)/dy + c`. The loader `L01_S301.py` evaluates the closed form
`0.5 + 0.25/√y` (Case-I calibration `c = 0.5`, `x1min(y) = y^0.5` from `_ch3_helpers.py`) on a
`np.linspace` grid — a pure formula evaluation, no file read, no API. `subsource_id = SHAIKH_2016_EQ_3_4_3_11`.

| Input | Source | Role |
|---|---|---|
| `y` (income grid) | author simulation, arbitrary model units, 0–60 | abscissa |
| `c` (discretionary propensity) | Shaikh 2016 eq. 3.4, p. 91; here `c = 0.5` | parameter |
| `x1min(y)` (necessary minimum) | Shaikh 2016 p. 93 (sub-linear in y); here `y^0.5` | parameter |

## 3. Why this source — Shaikh's rationale + rejected alternatives

- **Why an analytic curve, not data.** The chapter's whole thesis is that aggregate patterns are *robustly
  insensitive* to micro foundations. Shaikh first shows the pattern is *implied by the equations* (Figs 3.3–3.7),
  then that it appears in *real data* (Figs 3.8–3.9, S306/S307), then that it survives *four different
  simulated micro-worlds* (Figs 3.10–3.11, S308/S309). S301 is the first, deductive, leg — so it must be a
  formula plot, not a sample.
- **Why Case I (x1min rises sub-linearly), the rejected sibling being Case II.** Shaikh deliberately presents
  **two independent routes to saturation**: Case I (`x1min(y)` grows slower than income, Figs 3.3–3.5) and
  Case II (`c` declines with income, Figs 3.6–3.7 = S304/S305). S301 is the Case-I marginal share. Neither
  case is "wrong"; showing both is the point — saturation is over-determined.
- **Rejected alternative — a specific published calibration.** Shaikh gives only the *qualitative* form and the
  figure's axis bounds; he never prints the exact `x1min(y)` path or the level of `c`
  (`research.open_questions[1]`; `CH3_RESEARCH_SUMMARY.md` "Key caveats"). The build therefore chose the
  simplest one-parameter family matching the printed bounds (`x1min = y^0.5`, `c = 0.5`). This is an author-of-
  the-replication choice, not Shaikh's stated calibration; **the qualitative shape is robust, the level at any
  specific y is not** (`S301_DPR.md` §7). Author rationale for the exact parameters is *not located in the
  corpus* — only the axis ranges are.

## 4. Methodological-change exposure

**None.** S301 touches **no NIPA table, no benchmark I-O account, and no cross-provider concordance.** It is a
closed-form evaluation of book equations, so it is completely insulated from the NIPA comprehensive-revision
time-bombs catalogued in `NIPA_CHANGE_TIMELINE.md` (2013 IPP, 2018 T7.11 line shift, 2023 rebasing) and from
SIC→NAICS breaks. The only "vintage" risk is intellectual: if a future reader recalibrates `x1min(y)`, the
curve's levels move — but that is a modelling choice, not a data-vintage break.

## 5. Replication fidelity

- **Exact by construction.** V03 reproduces the documented formula `0.5 + 0.25/√y` cell-for-cell at
  idx 1/60/119 (`CH03_review.touchpoints` S301: content_type theoretical, linspace, audit-exempt). No external
  ground truth exists to diverge from.
- **Row-count nit (F-CH3-08, LOW).** Registry `domain.n_points = 121` but the loader/chopped emit **119 rows**
  (grid `[1, 60]`) — cosmetic, does not affect values.
- **x_value dropped from chopped (F-CH3-05, MEDIUM).** The natural abscissa (income `y`) is written to parquet
  but not to the published chopped CSV; DPR §5 points readers at an `x_value` column absent from the chopped,
  so Fig 3.3 cannot be plotted against its true x-axis without a registry `domain` join.
- **Provenance under-sold (F-CH3-07, MEDIUM).** The registry triage reason claims ch03 was "not HDARP-extracted,
  quotes unverifiable" — this is **false**: the ch03 body text, equations, and Table 3.1 are all extracted in the
  KB, and the S301 method quote verifies verbatim against the KB body text (p. 93). Citable provenance exists
  and should be surfaced.

## 6. Forward risk

- **Not extensible.** Analytic curve, no time dimension — mark not-extensible; there is nothing to re-fetch or
  re-vintage. Any "update" is a re-calibration decision, not a data refresh.
- **Reconcile n_points 121→119** (F-CH3-08) and **restore the x_value abscissa to the chopped** (F-CH3-05) so
  the figure is plottable and the registry domain matches the emitted grid.
- **Repair the triage reason** to cite the verified KB quote (F-CH3-07); the "From-the-book" explainer should
  carry the verbatim p. 93 slope equation rather than omit it (D14, `CH03_review.gates.D14`).
- **If exact fidelity to Shaikh's printed curve is ever required**, the missing calibration (`x1min(y)` path,
  level of `c`) would have to be recovered by digitizing Fig 3.3 — currently author rationale for the exact
  parameters is not in the corpus.
