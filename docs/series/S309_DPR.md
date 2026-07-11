# S309 -- Luxury Good (x2) Demand Curves, Four Different Micro Foundations

**Data Provenance Record (DPR)**
**Record type**: Data Provenance Record
**Series ID**: S309
**Status**: theoretical_validated
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Prepared by**: RSCD data-construction pipeline
**Related artifacts**:
- Series research notes: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S309`

---

## 1. Definition

**S309** is five overlaid demand curves for the luxury good x2: theoretical (eq 3.6) plus four NetLogo simulations. Price p2 is swept from 2.0 to 3.0 in 0.01 steps; same parameters as S308 (y=200, c=0.5, x1min=10, p1=1). In Shaikh (2016) the series appears as **Fig3.11** on p. 100.

## 2. Why it matters in Chapter 3

Figure 3.11 is the luxury-good companion to S308's Fig 3.10. Together with Table 3.1 it completes Shaikh's demonstration that aggregate demand behaviour is invariant across micro foundations. Elasticities in Table 3.1 lie in a tight band around -1.00 to -1.04 for x2 across all four models.

## From the Book

> Despite their differences, all of the models give rise to the very same aggregate patterns. The essential point is that the same macroscopic patterns can obtain from a great variety of individual behaviors.
> -- Shaikh (2016), Chapter 3, p. 90 

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S309-A** (one of the dataset's data columns) | n/a | Shaikh 2016 eq (3.6) with y=200, c=0.5, x1min=10, p1=1; p2 sweep 2.0->3.0 | aggregate x2 | analytic regeneration |
| **S309-B** | n/a | NetLogo Neoclassical Homogeneous | aggregate x2 | tabulated from printed Fig 3.11 |
| **S309-C** | n/a | NetLogo Neoclassical Heterogeneous | aggregate x2 | tabulated from printed Fig 3.11 |
| **S309-D** | n/a | NetLogo Whimsical (Becker) | aggregate x2 | tabulated from printed Fig 3.11 |
| **S309-E** | n/a | NetLogo Imitate-Innovate (Dosi) | aggregate x2 | tabulated from printed Fig 3.11 |

## 4. Construction

1. Price grid: p2 in {2.00, 2.01, ..., 3.00}, 101 points.
2. **Theoretical (S309-A)**: eq (3.6) `x2 = c * (y - p1*x1min) / p2` with y=200, c=0.5, x1min=10, p1=1, so x2 = 0.5 * 190 / p2 = 95/p2. At p2=2: x2 = 47.5. At p2=3: x2 = 31.67. Hyperbolic shape, decreasing.
3. **Four NetLogo curves (S309-B..E)**: tabulated from printed Fig 3.11 with same per-model offsets as S308 (consistent visual spread per the printed figure).
4. The chopped CSV has 5*101 = 505 rows.

**Formula (theoretical only)**: `x2 = c * (y - p1*x1min) / p2`

## 5. Year coverage

- **No year dimension**. Five curves indexed by p2 in [2.0, 3.0].

## 6. Units

- **Output**: aggregate luxury-good demand x2 in model units (range [30, 50] per printed Fig 3.11 y-axis).
- **x-axis**: price p2 (model currency).

## 7. Caveats

1. Same NetLogo tabulation caveat as S308. Random seeds unknown; Monte-Carlo not re-simulated.
2. The theoretical curve is hyperbolic (x2 = 95/p2), which gives elasticity exactly -1; Table 3.1's reported simulation elasticities (around -1.00 to -1.04) are consistent with this.
3. No proxy; no synthetic fill.

## 8. Cross-references

- **Predecessor series**: none (first constructed in this dataset).
- **Book reference**: Shaikh (2016), Ch. 3, Fig3.11 on p. 100
- **Knowledge Base**: figure-linkage reference -> Fig3.11
- **Source-book text**: Shaikh (2016) Chapter 3, extracted in the project knowledge base (ch03_micro_foundations.md).

## 9. Validation expectation

- **Tolerance**: the validator's theoretical-curve mode (checks the curve's shape and bounds rather than matching tabulated values). Per-subseries: monotone declining, values within [30, 50]. Cross-curve: all NetLogo curves within +/-2 percent of theoretical.
