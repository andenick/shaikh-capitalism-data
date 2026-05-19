# S302 -- Expenditure Share of Necessaries, Case I

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S302
**Status**: ingested
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave-a-ch3 (Phase 5-8 fanout)
**Related artifacts**:
- Research dossier: `Technical/research/S302_research.json`
- Adequacy: `Technical/docs/chapters/CH3_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S302_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S302`

---

## 1. Definition

**S302** is the analytical expenditure-share curve for the necessary good as a function of nominal income under Case I (x1min(y) sub-linear in y). The functional form is eq (3.11): p1*x1/y = (1 - c) * (p1*x1min/y) + c. In Shaikh (2016) the series appears as **Fig3.4** on p. 94.

## 2. Why it matters in Chapter 3

Figure 3.4 is the share-form analog of the marginal-share curve in S301. It demonstrates that the share of expenditure on necessaries declines monotonically with income, the saturation property that produces Engel's Law from the necessary side. Together with S301 and S303, this is Shaikh's analytical proof that Case I (x1min(y) sub-linear) is sufficient for Engel saturation.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S302-A** | n/a (theoretical) | Shaikh 2016 eq (3.11), p. 93; Figure 3.4 axis bounds p. 94 | dimensionless | analytic regeneration from equation |

## 4. Construction

1. Income grid y in [1.0, 60], 119 points.
2. Use the Case I calibration from `_ch3_helpers.py`: x1min(y) = y^0.5, c = 0.5, p1 = 1.
3. Evaluate share = (1 - c) * (x1min/y) + c = 0.5 * y^(-0.5) + 0.5.
4. At y=1 the share is 1.0; it declines monotonically toward c = 0.5 as y -> infinity.

**Formula**: `p1*x1/y = (1 - c) * (p1*x1min/y) + c`

## 5. Year coverage

- **No year dimension**. The abscissa is a synthetic income grid (model units 1-60).

## 6. Units

- **Output**: expenditure share, dimensionless ratio.
- **x-axis**: income y in model units.

## 7. Caveats

1. Parameter calibration (x1min(y), c) not stated by Shaikh; we use the same calibration as S301 for internal consistency across the Case I family (S301/S302/S303). Disclosed here and in EPR.
2. Printed Fig 3.4 has y-axis up to 1.2; with our calibration the share at y=1 is 1.0 (within axis). Shaikh's curve approaches the axis maximum at low y; ours does too.
3. No empirical content. No proxy substitution. No synthetic gap-filling.

## 8. Cross-references

- **CD legacy ID**: none
- **Book reference**: Shaikh (2016), Ch. 3, Fig3.4 on p. 94
- **Knowledge Base**: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json` -> Fig3.4

## 9. Validation expectation

- **Tolerance**: PASS_THEORETICAL mode. Checks: monotone declining, asymptote toward c=0.5 at high y, all values within [0.0, 1.2].
