# S302 — Expenditure Share of Necessaries, Case I — Methodological History Report (MHR)

**Group:** ch3 (Micro Foundations and Macro Patterns) · **Construction:** formula (analytic) · **Status:** book_period_validated
**Figure:** 3.4 (book p. 94) · **Predecessor:** none · **Publish:** true
**Reasoning stance:** from Shaikh's own perspective.

> Grounding: `Technical/research/S302_research.json`; KB body text + equations
> (`.../Knowledge_Base/HDARP_v3.3_Campaign/Body_Text/ch03_micro_foundations.md`, `.../Equations/ch03_equations.md`);
> `Technical/docs/chapters/CH3_RESEARCH_SUMMARY.md`; `Technical/methodology_review/CH03_review.json`;
> `Technical/docs/series/S302_{DPR,EPR}.md`; `Technical/code/L01_loaders/L01_S302.py`, `_ch3_helpers.py`. No claim invented.

---

## 1. What it is

S302 is the **analytic curve behind Figure 3.4**: the *average* expenditure share on the necessary good,
`p1x1/y`, over the income grid `y ∈ [0.5, 60]` (dimensionless ratio, axis 0–1.2). It is the integral-form
partner of S301's marginal share — the same Case-I shaping structure viewed as a share rather than a slope.
It is **not empirical**. Shaikh's governing identity is eq. (3.11), quoted verbatim
(`research.book_quotes[0]`, p. 93): `p1x1/y = (1 − c)(p1x1min/y) + c`, and its behaviour
(`book_quotes[1]`, role=method): *"the expenditure share on necessities declines as income increases, while
that of luxuries rises."* This declining necessaries share **is Engel's Law** in share form — the pattern the
whole chapter is built to explain from shaping structures rather than optimization.

## 2. Source lineage

Single source: **Shaikh (2016), eq. (3.11), p. 93; Figure 3.4, p. 94.** No external data agency.
`L01_S302.py` evaluates eq. (3.11) with the shared Case-I calibration (`c = 0.5`, `x1min(y) = y^0.5`;
`_ch3_helpers.py`) on a `np.linspace` grid — pure formula, no file/API. `subsource_id = SHAIKH_2016_EQ_3_4_3_11`.

| Input | Source | Role |
|---|---|---|
| `y` (income grid) | author simulation, 0.5–60 model units | abscissa |
| `c` | Shaikh 2016 eq. 3.4, p. 91; `c = 0.5` | parameter |
| `x1min(y)` | Shaikh 2016 p. 93 (sub-linear); `y^0.5` | parameter |

## 3. Why this source — Shaikh's rationale + rejected alternatives

- **Why the share form alongside the marginal form (S301).** Engel's Law is most naturally *stated* as "the
  budget share of necessaries falls with income." S302 draws exactly that object, so the reader sees the law
  itself, not just its slope. S301 (marginal) and S303 (integrated Engel level) are the same Case-I model at
  three levels of aggregation.
- **Why Case I.** Same rationale as S301: `x1min(y)` rising sub-linearly is one of Shaikh's two deliberate
  routes to saturation; Case II (`c(y)` declining, S304/S305) is the sibling, not a competitor.
- **Rejected alternative — a survey cross-section for this panel.** Shaikh reserves *real* budget data for the
  empirical Figs 3.8–3.9 (Allen & Bowley 1904, S306/S307). Fig 3.4 must stay analytic so the deductive and
  empirical legs of the argument remain visibly distinct.
- **Rejected alternative — a stated calibration.** As with S301, the exact `c`/`x1min(y)` values used to render
  the printed curve are **not stated** (`research.open_questions[1]`); only axis bounds (share 0–1.2). The
  one-parameter fit is a replication choice; author rationale for exact parameters is *not located in the corpus*.

## 4. Methodological-change exposure

**None.** No NIPA line, no I-O account, no concordance. A closed-form evaluation of eq. (3.11), fully insulated
from every NIPA comprehensive revision (`NIPA_CHANGE_TIMELINE.md`) and from SIC→NAICS drift. Only exposure is a
re-calibration choice, which is a modelling decision, not a vintage break.

## 5. Replication fidelity

- **Exact by construction** at idx 1/60/119 — expenditure-share form of Case I (`CH03_review.touchpoints` S302,
  audit-exempt linspace).
- **F-CH3-08 (LOW):** registry `n_points = 121` vs 119 emitted rows (cosmetic).
- **F-CH3-05 (MEDIUM):** `x_value` (income) present in parquet, dropped from chopped — figure not plottable vs
  its true x-axis without a registry `domain` join.
- **F-CH3-07 (MEDIUM):** triage reason wrongly says ch03 unextracted; eq. (3.11) verifies verbatim in the KB
  body text — provenance is real and under-sold.

## 6. Forward risk

- **Not extensible** (analytic, no time dimension); nothing to re-fetch or re-vintage.
- **Reconcile n_points and restore x_value** to the chopped so Fig 3.4 is plottable.
- **Repair triage reason / surface the verified eq. (3.11) quote** in the explainer (D14).
- **Exact printed-curve fidelity** would require recovering Shaikh's un-stated calibration by digitizing Fig 3.4.
