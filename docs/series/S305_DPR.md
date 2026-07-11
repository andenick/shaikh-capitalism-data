# S305 -- Engel Curve of Necessaries, Case II

**Data Provenance Record (DPR)**
**Record type**: Data Provenance Record
**Series ID**: S305
**Status**: theoretical_validated
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Prepared by**: RSCD data-construction pipeline
**Related artifacts**:
- Series research notes: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S305`

---

## 1. Definition

**S305** is the Engel curve for the necessary good under Case II (c(y) declining, x1min held constant). Functional form: p1*x1 = (1 - c(y)) * p1*x1min + c(y) * y. In Shaikh (2016) the series appears as **Fig3.7** on p. 95.

## 2. Why it matters in Chapter 3

Figure 3.7 closes the Case II family. Together with S304 it demonstrates that the same saturating Engel shape arises from c(y) declining as from x1min(y) sub-linear (Case I, S303). This is Shaikh's central methodological point in §III.3 — micro-foundational details do not constrain the aggregate empirical pattern.

## From the Book

> This saturation property carries over the relation between total expenditure on necessaries and total income, both of which only differ from their discretionary counterparts by a common minimum expenditure on necessaries.
> -- Shaikh (2016), Chapter 3, p. 93 

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S305-A** (the dataset's single data column) | n/a (theoretical) | Shaikh 2016 eq (3.5) with c->c(y), p. 91/93; Figure 3.7 axis bounds p. 95 | model units of expenditure | analytic regeneration |

## 4. Construction

1. Income grid y in [0, 60], 121 points.
2. Calibration matched to Shaikh's **plotted Figure 3.6** (the c(y) profile he
   actually used to render Fig 3.7): c(y) = 0.80*exp(-0.014*y), giving
   c(10..50) = 0.70, 0.61, 0.53, 0.46, 0.40 — reproducing the read-off Fig 3.6
   curve. x1min = 10.0 (constant), pinned by the Engel-curve start point
   (E = 10 at y = 10, shared with Fig 3.5 Case I) and matching the chapter's
   simulation minimum (eq 3.5, x1min = 10). p1 = 1. These parameters are local
   to this series' data-loading step and do NOT modify the shared `c_case_ii` used by S304.
3. Evaluate p1*x1 = (1 - c(y)) * p1*x1min + c(y) * y.
4. Reproduces Fig 3.7 bounds: E(10) = 10.0, E(50) = 25.9 (book ~10 -> ~26),
   monotone-rising and concave (saturating) across the entire [0, 60] grid
   (peak at the y=60 boundary), well within the printed [0, 30] axis.

**Formula**: `p1*x1 = (1 - c(y)) * p1*x1min + c(y) * y`, c(y) = 0.80*exp(-0.014*y), x1min = 10

### Calibration history
The original calibration (c0=0.7, k=0.05, x1min=5.0) decayed c(y) far too fast
(c crashed to ~0.06 by y=50) and used half the correct x1min, collapsing the
curve into a non-monotone hump that peaked at ~9 near y=25 then declined to ~7.6
— roughly 3x too low and the wrong shape (book Fig 3.7 rises monotonically).
Corrected 2026-05-27 by matching Shaikh's plotted Fig 3.6 c(y) profile.

## 5. Year coverage

- **No year dimension**.

## 6. Units

- **Output**: expenditure on necessaries (model units).

## 7. Caveats

1. Shaikh states the Engel-curve equation (eq 3.5 with c -> c(y), p. 91/93) and
   the qualitative saturation property, but does NOT publish an explicit
   algebraic c(y). The c(y) used here is calibrated to reproduce **Shaikh's own
   plotted Figure 3.6** (the c-curve he used for Fig 3.7), which is directly
   readable (0.70 at y=10 -> 0.40 at y=50). This is reproduction of a published
   figure, not an invented functional form; the exponential family is one of
   several profiles consistent with that read-off (a near-linear decline fits
   equally well). x1min = 10 is determined, not free: both Engel curves
   (Fig 3.5, Fig 3.7) start at E = 10 at y = 10.
2. No empirical content; no proxy; no synthetic fill. Fully deterministic
   (no np.random).

## 8. Cross-references

- **Predecessor series**: none (first constructed in this dataset).
- **Book reference**: Shaikh (2016), Ch. 3, Fig3.7 on p. 95
- **Knowledge Base**: figure-linkage reference -> Fig3.7
- **Source-book text**: Shaikh (2016) Chapter 3, extracted in the project knowledge base (ch03_micro_foundations.md).

## 9. Validation expectation

- **Tolerance**: the validator's theoretical-curve mode (checks the curve's shape and bounds rather than matching tabulated values). Checks: rising/saturating shape; values within [0.0, 30.0].
