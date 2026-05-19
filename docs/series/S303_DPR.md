# S303 -- Engel Curve of Necessaries, Case I

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S303
**Status**: ingested
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave-a-ch3 (Phase 5-8 fanout)
**Related artifacts**:
- Research dossier: `Technical/research/S303_research.json`
- Adequacy: `Technical/docs/chapters/CH3_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S303_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S303`

---

## 1. Definition

**S303** is the integrated Engel curve for the necessary good as a function of nominal income, under Case I (x1min(y) sub-linear in y). Functional form: p1*x1 = (1 - c) * p1*x1min(y) + c*y. In Shaikh (2016) the series appears as **Fig3.5** on p. 94.

## 2. Why it matters in Chapter 3

Figure 3.5 is the visual payoff of the Case I analytic family: the Engel curve for necessaries that exhibits saturation, the empirically-observed pattern Allen & Bowley documented in 1904 (S307/Fig 3.9). It is the integrated counterpart of S301's marginal-share curve.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S303-A** | n/a (theoretical) | Shaikh 2016 eq (3.5), p. 91; Figure 3.5 axis bounds p. 94 | model units of expenditure | analytic regeneration from equation |

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

- **CD legacy ID**: none
- **Book reference**: Shaikh (2016), Ch. 3, Fig3.5 on p. 94
- **Knowledge Base**: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json` -> Fig3.5

## 9. Validation expectation

- **Tolerance**: PASS_THEORETICAL mode. Checks: monotone rising (saturating shape is concave), all values within [0.0, 40.0].
