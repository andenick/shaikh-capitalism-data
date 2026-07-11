# S304 -- Discretionary Propensity to Consume, Case II

**Data Provenance Record (DPR)**
**Record type**: Data Provenance Record
**Series ID**: S304
**Status**: theoretical_validated
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Prepared by**: RSCD data-construction pipeline
**Related artifacts**:
- Series research notes: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S304`

---

## 1. Definition

**S304** is the discretionary propensity c(y) as a declining function of income under Case II (the alternative path to Engel saturation: c falls with income while x1min is held constant). In Shaikh (2016) the series appears as **Fig3.6** on p. 94.

## 2. Why it matters in Chapter 3

Figure 3.6 sets up Case II by showing the qualitative shape of c(y) — declining monotonically. The resulting Engel curve (S305 / Fig 3.7) then exhibits saturation through a different mechanism than Case I. Together S304+S305 demonstrate that Engel's Law is overdetermined: at least two distinct micro-foundational paths produce the same aggregate pattern.

## From the Book

> The same result obtains if instead c declines with discretionary income. To see this, we rewrite equation (3.4) as (p1x1 - p1x1min) = c (y - p1x1min), which is a linear relationship between discretionary expenditure on necessary goods and discretionary income. Since c is the slope of this curve, as c falls the curve gets flatter.
> -- Shaikh (2016), Chapter 3, p. 93 

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S304-A** (the dataset's single data column) | n/a (theoretical) | Shaikh 2016 eq (3.4) framework, p. 91; Figure 3.6 axis bounds p. 94 | dimensionless | analytic regeneration from chosen c(y) form |

## 4. Construction

1. Income grid y in [0, 60], 121 points.
2. Calibration: c(y) = c0 * exp(-k*y) with c0 = 0.7, k = 0.05. At y=0, c = 0.7; at y=60, c ~ 0.035.
3. Functional form chosen as the simplest monotone-declining curve that hits the axis bounds [0.0, 0.8] of Fig 3.6.

**Formula**: `c(y) = c0 * exp(-k * y)`

## 5. Year coverage

- **No year dimension**.

## 6. Units

- **Output**: discretionary propensity c, dimensionless.

## 7. Caveats

1. Functional form for c(y) is NOT stated in the book. Shaikh shows the qualitative shape (declining), not the exact analytical form. We use exponential decay as the simplest one-parameter family that matches the axis range. Disclosed in EPR.
2. Alternative reasonable forms (linear, power-law) would give similar qualitative behaviour; the validator's shape check is the binding test.
3. No empirical content; no proxy; no synthetic fill.

## 8. Cross-references

- **Predecessor series**: none (first constructed in this dataset).
- **Book reference**: Shaikh (2016), Ch. 3, Fig3.6 on p. 94
- **Knowledge Base**: figure-linkage reference -> Fig3.6
- **Source-book text**: Shaikh (2016) Chapter 3, extracted in the project knowledge base (ch03_micro_foundations.md).

## 9. Validation expectation

- **Tolerance**: the validator's theoretical-curve mode (checks the curve's shape and bounds rather than matching tabulated values). Checks: monotone declining, all values within [0.0, 0.8] (Fig 3.6 axis bounds).
