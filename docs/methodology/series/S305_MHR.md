# S305 — Engel Curve of Necessaries, Case II — Methodological History Report (MHR)

**Group:** ch3 (Micro Foundations and Macro Patterns) · **Construction:** formula (analytic) · **Status:** book_period_validated
**Figure:** 3.7 (book p. 95) · **Predecessor:** none · **Publish:** true
**Reasoning stance:** from Shaikh's own perspective.

> Grounding: `Technical/research/S305_research.json`; KB body text (eq. 3.5 p. 91, saturation p. 93);
> `CH3_RESEARCH_SUMMARY.md`; `CH03_review.json` (F-CH3-01, F-CH3-11); `S305_{DPR,EPR}.md`;
> `L01_S305.py` (2026-05-27 recalibration, detailed docstring), `_ch3_helpers.py`. No claim invented.

---

## 1. What it is

S305 is the **analytic curve behind Figure 3.7**: the *level* Engel curve for necessaries under Case II —
expenditure on necessaries `p1x1` (0–30 model units) vs income `y ∈ [0, 60]`. It is the integrated result of
feeding S304's declining `c(y)` through Shaikh's Engel equation, and the Case-II counterpart of S303. Not
empirical. Shaikh's saturation statement (`research.book_quotes[0]`, p. 93): with `c` declining, the
discretionary relationship "gets flatter", and *"this saturation property carries over the relation between
total expenditure on necessaries and total income."* The underlying identity is eq. (3.5)
(`book_quotes[1]`, p. 91): `x1 = (1 − c)x1min + c(y/p1)`.

## 2. Source lineage

Single source: **Shaikh (2016), eq. (3.5), p. 91; discussion p. 93; Figure 3.7, p. 95.** No external agency.
`L01_S305.py` evaluates `p1x1 = (1 − c(y))·p1·x1min + c(y)·y` with `p1 = 1`, `x1min = 10`, and the
book-matched `c(y) = 0.80·exp(−0.014·y)` on a `np.linspace` grid — pure formula. `subsource_id =
SHAIKH_2016_EQ_3_4_3_11`.

**Calibration history (2026-05-27).** `c(y)` is the same book-read-off profile as S304 (0.70@y10→0.40@y50).
`x1min = 10` is **pinned by the book**: both Case-I (Fig 3.5) and Case-II (Fig 3.7) Engel curves start at `E = 10`
at `y = 10`, and 10 is the chapter's simulation minimum (`L01_S305.py` docstring). The earlier calibration
(`c0=0.7, k=0.05, x1min=5`) decayed too fast and collapsed the curve into a non-monotone hump ~3× too low; it
was **rejected** for contradicting Shaikh's own Figs 3.6/3.7. These parameters are local to S305 (they do not
touch the shared Case-II helper used—formerly—by S304).

| Input | Source | Role |
|---|---|---|
| `y` (income grid) | author simulation, 0–60 model units | abscissa |
| `c(y) = 0.80·exp(−0.014·y)` | read off printed Fig 3.6 (2026-05-27) | parameter |
| `x1min = 10`, `p1 = 1` | pinned by Fig 3.5/3.7 start point + simulation minimum | parameters |
| `p1x1` (necessaries expenditure) | eq. (3.5) with `c → c(y)` | output |

## 3. Why this source — Shaikh's rationale + rejected alternatives

- **Why the Case-II Engel level.** S305 is the payoff of Case II: it shows that a declining `c(y)` alone (fixed
  `x1min`) produces the same saturating Engel curve as Case I's rising-`x1min(y)` (S303). Two mechanisms, one
  aggregate shape — Shaikh's central "robust insensitivity" claim, now for consumer theory.
- **Why `x1min = 10`, not a free parameter.** Shaikh's *own figures* fix the start point (`E = 10 at y = 10`)
  and his simulation section uses `x1min = 10`; the build pins to that rather than inventing a value — a
  book-disciplined choice.
- **Rejected alternative — the fast-decay/`x1min=5` calibration.** Explicitly rejected for producing a
  non-monotone curve ~3× too low, inconsistent with Fig 3.7 (`L01_S305.py` docstring). This is the largest
  single "why-not" in ch3.
- **Rejected alternative — a stated algebraic `c(y)`.** Not printed in the text; author rationale for the exact
  formula is *not located in the corpus* — only Shaikh's plotted Fig 3.6 and the Fig 3.7 bounds constrain it.

## 4. Methodological-change exposure

**None.** No NIPA line, no I-O account, no concordance. Analytic evaluation of a book equation; fully insulated
from every NIPA comprehensive revision and SIC→NAICS break (`NIPA_CHANGE_TIMELINE.md`). The only "change" is the
internal 2026-05-27 recalibration.

## 5. Replication fidelity

- **Curve is book-matched** after recalibration: chopped `p1x1 = 2.0 / 20.51 / 27.27` (rising ~10→~26 over
  y=10→50, as Fig 3.7 requires) (`CH03_review.touchpoints` S305).
- **STALE registry reference_values (F-CH3-01, HIGH) — the largest drift in ch3 (~4×).** Registry refs still
  carry the pre-recalibration `1.5 / 8.90 / 6.92`, contradicting the corrected chopped `2.0 / 20.51 / 27.27`.
  **Code correct, refs not regenerated.**
- **Why it passed silently (F-CH3-11, HIGH).** V03 checks shape/bounds only, never `reference_values`; same gap
  as S304.
- **F-CH3-05 / F-CH3-07 (MEDIUM):** x_value dropped from chopped; triage reason wrongly says ch03 unextracted.

## 6. Forward risk

- **Regenerate `S305.validation.reference_values` from the recalibrated loader (F-CH3-01, HIGH, blocking).**
  Highest-priority ch3  refresh given the ~4× stale-ref drift; then reconcile `CH3_RESEARCH_SUMMARY.md`.
- **Add the V03 reference-value check (F-CH3-11)** and reconcile the 0.5%/1% tolerances (F-CH3-13).
- **Not extensible** (analytic); restore x_value + repair triage reason (F-CH3-05/07).
- **Exact printed-curve fidelity** would require Shaikh's un-stated `c(y)` formula (only recoverable by
  digitizing Fig 3.6/3.7).
