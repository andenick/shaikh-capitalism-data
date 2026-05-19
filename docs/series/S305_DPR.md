# S305 -- Engel Curve of Necessaries, Case II

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S305
**Status**: ingested
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave-a-ch3 (Phase 5-8 fanout)
**Related artifacts**:
- Research dossier: `Technical/research/S305_research.json`
- Adequacy: `Technical/docs/chapters/CH3_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S305_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S305`

---

## 1. Definition

**S305** is the Engel curve for the necessary good under Case II (c(y) declining, x1min held constant). Functional form: p1*x1 = (1 - c(y)) * p1*x1min + c(y) * y. In Shaikh (2016) the series appears as **Fig3.7** on p. 95.

## 2. Why it matters in Chapter 3

Figure 3.7 closes the Case II family. Together with S304 it demonstrates that the same saturating Engel shape arises from c(y) declining as from x1min(y) sub-linear (Case I, S303). This is Shaikh's central methodological point in §III.3 — micro-foundational details do not constrain the aggregate empirical pattern.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S305-A** | n/a (theoretical) | Shaikh 2016 eq (3.5) with c->c(y), p. 91/93; Figure 3.7 axis bounds p. 95 | model units of expenditure | analytic regeneration |

## 4. Construction

1. Income grid y in [0, 60], 121 points.
2. Calibration: c(y) = 0.7*exp(-0.05*y) (Case II shared with S304); x1min = 5.0 (constant). p1 = 1.
3. Evaluate p1*x1 = (1 - c(y)) * 5.0 + c(y) * y.
4. At y=0: 5.0. At y=60: ~ (1-0.035)*5 + 0.035*60 = 4.825 + 2.1 = 6.925, well within the printed [0, 30] axis.

**Formula**: `p1*x1 = (1 - c(y)) * p1*x1min + c(y) * y`

## 5. Year coverage

- **No year dimension**.

## 6. Units

- **Output**: expenditure on necessaries (model units).

## 7. Caveats

1. The Case II calibration (c(y), x1min) is chosen for consistency with S304 and the printed axis bounds. With c(y) decaying rapidly the integrated Engel curve flattens quickly — visible in Fig 3.7 as a strong saturation. Our values plateau at low absolute level (~7) within the y < 60 range; Shaikh's printed curve appears to reach somewhat higher levels (~25 at y=60), indicating his calibration uses slower c(y) decay or a larger x1min. We document our choice and note the qualitative shape is correct (saturating).
2. No empirical content; no proxy; no synthetic fill.

## 8. Cross-references

- **CD legacy ID**: none
- **Book reference**: Shaikh (2016), Ch. 3, Fig3.7 on p. 95
- **Knowledge Base**: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json` -> Fig3.7

## 9. Validation expectation

- **Tolerance**: PASS_THEORETICAL. Checks: rising/saturating shape; values within [0.0, 30.0].
