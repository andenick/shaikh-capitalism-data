# S303 -- Engel Curve of Necessaries, Case I

**Data Provenance Record (DPR)**
**Record type**: Data Provenance Record
**Series ID**: S303
**Status**: theoretical_validated
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Prepared by**: RSCD data-construction pipeline
**Related artifacts**:
- Series research notes: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S303`

---

## 1. Definition

**S303** is the integrated Engel curve for the necessary good as a function of nominal income, under Case I (x1min(y) sub-linear in y). Functional form: p1*x1 = (1 - c) * p1*x1min(y) + c*y. In Shaikh (2016) the series appears as **Fig3.5** on p. 94.

## 2. Why it matters in Chapter 3

Figure 3.5 is the visual payoff of the Case I analytic family: the Engel curve for necessaries that exhibits saturation, the empirically-observed pattern Allen & Bowley documented in 1904 (S307/Fig 3.9). It is the integrated counterpart of S301's marginal-share curve.

## From the Book

> people buy proportionately less of necessary goods, and hence proportionately more of other (luxury) goods, as their income increases [...] This is known as Engel's Law of consumer demand.
> -- Shaikh (2016), Chapter 3, p. 92 

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S303-A** (the dataset's single data column) | n/a (theoretical) | Shaikh 2016 eq (3.5), p. 91; Figure 3.5 axis bounds p. 94 | model units of expenditure | analytic regeneration from equation |

## 4. Construction

1. Income grid y in [0, 60], 121 points.
2. Calibration: x1min(y) = y^0.5, c = 0.5, p1 = 1 (Case I, shared with S301/S302).
3. Evaluate p1*x1 = (1 - c)*x1min(y) + c*y = 0.5*y^0.5 + 0.5*y.
4. At y=0 the curve is at 0; at y=60 the curve is 0.5*sqrt(60) + 30 ~ 33.87 (within the printed [0,40] axis).

**Formula**: `p1*x1 = (1 - c) * p1*x1min(y) + c*y`

## 5. Year coverage

- **No year dimension**. y in [0, 60].

## 6. Units

- **Output**: expenditure on necessaries (model units).

## 7. Caveats

1. Same calibration as S301/S302. The integrated curve passes through the origin.
2. Curvature is mild because c=0.5 dominates at high y; the linear-in-y term (c*y = 0.5*y) is the main contributor to the curve at y > 4.
3. No empirical content; no proxy; no synthetic fill.

## 8. Cross-references

- **Predecessor series**: none (first constructed in this dataset).
- **Book reference**: Shaikh (2016), Ch. 3, Fig3.5 on p. 94
- **Knowledge Base**: figure-linkage reference -> Fig3.5
- **Source-book text**: Shaikh (2016) Chapter 3, extracted in the project knowledge base (ch03_micro_foundations.md).

## 9. Validation expectation

- **Tolerance**: the validator's theoretical-curve mode (checks the curve's shape and bounds rather than matching tabulated values). Checks: monotone rising (saturating shape is concave), all values within [0.0, 40.0].
