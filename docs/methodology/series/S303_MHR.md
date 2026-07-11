# S303 — Engel Curve of Necessaries, Case I — Methodological History Report (MHR)

**Group:** ch3 (Micro Foundations and Macro Patterns) · **Construction:** formula (analytic) · **Status:** book_period_validated
**Figure:** 3.5 (book p. 94) · **Predecessor:** none · **Publish:** true
**Reasoning stance:** from Shaikh's own perspective.

> Grounding: `Technical/research/S303_research.json`; KB body text + equations
> (`.../HDARP_v3.3_Campaign/Body_Text/ch03_micro_foundations.md`, `.../Equations/ch03_equations.md`);
> `CH3_RESEARCH_SUMMARY.md`; `CH03_review.json`; `S303_{DPR,EPR}.md`; `L01_S303.py`, `_ch3_helpers.py`. No claim invented.

---

## 1. What it is

S303 is the **analytic curve behind Figure 3.5**: the *level* Engel curve for the necessary good — expenditure
on necessaries `p1x1` (0–40 model units) as a function of income `y ∈ [0, 60]`. It is the **integrated
counterpart of S301** (the marginal share) and the completing member of the Case-I triple. Not empirical.
Shaikh's own text (`research.book_quotes[0]`, p. 93): the constant-`c` Engel curve `p1x1 = (1 − c)p1x1min + cy`
is *linear*, but once `x1min` "rises as real income rises but not as fast as income… the Engel curve for
necessary goods will exhibit saturation" (`book_quotes[1]`, role=method). S303 draws that saturating curve —
the visual payoff of the Case-I argument.

## 2. Source lineage

Single source: **Shaikh (2016), eqs. (3.5)/(3.11), p. 91–93; Figure 3.5, p. 94.** No external agency.
`L01_S303.py` integrates the Case-I model (`c = 0.5`, `x1min(y) = y^0.5`; `_ch3_helpers.py`) on a `np.linspace`
grid — pure formula. `subsource_id = SHAIKH_2016_EQ_3_4_3_11`.

| Input | Source | Role |
|---|---|---|
| `y` (income grid) | author simulation, 0–60 model units | abscissa |
| `p1x1` (necessaries expenditure) | eqs. (3.5)/(3.11), Shaikh 2016 p. 91, 93 | output |
| `c`, `x1min(y)` | `c = 0.5`; `x1min = y^0.5` (sub-linear, Case I) | parameters |

## 3. Why this source — Shaikh's rationale + rejected alternatives

- **Why the integrated Engel level, given S301/S302.** Shaikh presents the same Case-I mechanism as a slope
  (3.3), a share (3.4), and a *level* (3.5) so the reader sees saturation in the form textbooks actually plot —
  expenditure vs income. It is one model, three views, not three findings.
- **Why Case I.** The sub-linear `x1min(y)` route to saturation; Case II (S305) is the sibling route via
  declining `c(y)`. S303 and S305 are visually near-identical Engel curves reached by *different* mechanisms —
  which is precisely Shaikh's over-determination point.
- **Rejected alternative — real budget data.** Empirical Engel curves are Figs 3.8–3.9 (S306/S307, UK 1904);
  Fig 3.5 stays deductive.
- **Rejected alternative — a stated calibration.** Exact `x1min(y)` path not printed (`research.open_questions[1]`);
  only axis bounds (expenditure 0–40). The `y^0.5` path is a replication choice; author rationale for exact
  parameters *not located in the corpus*.

## 4. Methodological-change exposure

**None.** No NIPA line, no I-O account, no concordance. Closed-form evaluation of book equations; fully
insulated from every NIPA comprehensive revision and SIC→NAICS break (`NIPA_CHANGE_TIMELINE.md`). Only exposure
is a re-calibration modelling choice.

## 5. Replication fidelity

- **Exact by construction** at idx 1/61/121 — integrated Engel curve, Case I (`CH03_review.touchpoints` S303,
  audit-exempt linspace). S303 emits **121 rows** (unlike S301/S302's 119), so it is *not* subject to F-CH3-08.
- **F-CH3-05 (MEDIUM):** `x_value` (income) dropped from chopped; DPR §5 directs readers to an absent column —
  figure not plottable vs true x-axis without a registry `domain` join.
- **F-CH3-07 (MEDIUM):** triage reason wrongly says ch03 unextracted; the Engel-saturation quote verifies
  verbatim in the KB — provenance is real.

## 6. Forward risk

- **Not extensible** (analytic, no time dimension).
- **Restore x_value to the chopped** so Fig 3.5 is plottable; **repair triage reason** and surface the verified
  p. 93 quote (D14).
- **Exact printed-curve fidelity** would require recovering the un-stated `x1min(y)` calibration by digitizing
  Fig 3.5.
