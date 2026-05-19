# S301 — Change in Expenditure on Necessaries Relative to Change in Income, Case I

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S301
**Status**: ingested
**Content type**: `theoretical`
**Construction**: `formula`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave-a-ch3 (Phase 5-8 fanout)
**Related artifacts**:
- Research dossier: `Technical/research/S301_research.json`
- Adequacy: `Technical/docs/chapters/CH3_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S301_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S301`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` -> `SHAIKH_2016_EQ_3_4_3_11`

---

## 1. Definition

**S301** is the marginal expenditure share on the necessary good as a function of nominal income under Case I of Shaikh's two-good consumer model:

> d(p1 * x1) / dy = (1 - c) * d(p1 * x1min)/dy + c

where x1min is the socially-defined minimum level of the necessary good, and x1min(y) rises sub-linearly in income y (Case I). In Shaikh (2016) the series appears as **Figure 3.3** ("Change in Expenditure on Necessaries Relative to Change in Income, Case I"), p. 94.

## 2. Why it matters in Chapter 3

Chapter 3 develops the methodological claim that aggregate empirical patterns (here, Engel's Law) are robustly insensitive to the underlying micro foundations. Figures 3.3-3.5 demonstrate that **Case I** — in which the minimum necessary level x1min(y) itself rises sub-linearly in income — is sufficient to generate the saturation property of the Engel curve for necessaries. S301 isolates the marginal-share component of this construction, which is the analytical object behind the saturation visible in the integrated Engel curve (S303 / Fig 3.5).

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S301-A** | n/a (theoretical) | Shaikh 2016 eqs (3.4)-(3.11), p. 91-93; Figure 3.3 axis bounds p. 94 | dimensionless | analytic regeneration from equations |

The single subseries S301-A is an analytic curve. There is no "data" in the sense of historical observations; the data are the values of d(p1*x1)/dy evaluated on a discrete income grid in the same range as Shaikh's Figure 3.3 (y in [0, 60]).

## 4. Construction

S301 is **formula**-classified. The recipe:

1. Define an income grid: y in [0, 60], 121 points (step 0.5).
2. Choose a calibration for x1min(y) under Case I (sub-linear). The book does not state Shaikh's exact calibration; we use the simplest functional form that matches the printed axis bounds:
   `x1min(y) = alpha * y^beta` with `alpha = 1.0, beta = 0.5` (square-root path, monotone, elasticity 0.5).
3. Choose c = 0.5 (mid-range; consistent with the Table 3.1 calibration for S308/S309 which uses pi=0.50).
4. Evaluate d(p1*x1)/dy = (1 - c) * d(p1*x1min)/dy + c = (1 - 0.5) * 0.5 * y^(-0.5) + 0.5 = 0.5 + 0.25 / sqrt(y) at each y (with p1 = 1, so p1*x1min = x1min).
5. At y=0 the derivative is undefined (square-root singularity); we trim the curve to y in (0, 60] and report the asymptotic value at y=epsilon for completeness.

**Formula**:
```
d(p1*x1)/dy = (1 - c) * d(x1min)/dy + c
            = (1 - 0.5) * 0.5 * y^(-0.5) + 0.5         (with c=0.5, x1min = y^0.5)
            = 0.5 + 0.25 * y^(-0.5)
```

At y=4: 0.5 + 0.25/2 = 0.625. At y=60: 0.5 + 0.25/sqrt(60) approx 0.532. The curve declines monotonically toward c=0.5 — consistent with Fig 3.3's apparent y-range of [0, ~0.8] and the qualitative saturation pattern Shaikh draws.

## 5. Year coverage

- **No year dimension**. The abscissa is a synthetic income grid (model units 0-60).
- The chopped CSV uses `year` as a per-row index column with the value `1` (point sequence number) for the theoretical grid — the `year` field is preserved for pipeline compatibility, but should not be interpreted as a calendar year. Refer to the `x_value` column (added for theoretical series) for the income value.

## 6. Units

- **Output**: marginal expenditure share, dimensionless ratio.
- **x-axis**: income y in model units (0-60).
- Every chopped CSV row carries `units = "marginal_share_dimensionless"`.

## 7. Caveats

1. **Parameter calibration not stated by Shaikh.** The text states only the qualitative property (x1min sub-linear) and the axis ranges. We use square-root x1min(y) and c=0.5 as the simplest analytically-defensible choice consistent with the axis range. This is disclosed here and again in the EPR. The qualitative shape (declining marginal share toward c) is robust to the precise sub-linear form; the level at any given y is not.
2. **No empirical content.** This is a pedagogical curve, not a measurement. There is no Allen & Bowley table behind Fig 3.3 — that is the role of Figs 3.8/3.9 (S306/S307).
3. **Singularity at y=0.** The square-root choice has an infinite derivative at the origin. We trim to y in (0, 60] and report the curve from y=0.5 onward.
4. **No proxy substitution; no synthetic gap-filling.** This series is by definition a closed-form evaluation of a published equation; the only judgement call is calibration, which is disclosed.

## 8. Cross-references

- **CD legacy ID**: none (this series has no predecessor in CD1 or CD2 — it was first ingested in RSCD).
- **Companion analytic series**: S302 (Fig 3.4, share form), S303 (Fig 3.5, integrated Engel curve), all under the same Case I calibration.
- **Empirical counterpart**: S306 / S307 (the same conceptual object measured in 1904 working-class budgets).
- **Book reference**: Shaikh (2016), Ch. 3, p. 91-93 (text), p. 94 (Figure 3.3).
- **Knowledge Base**: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json` -> Fig3.3 (documentation_type="theoretical", is_empirical=false).

## 9. Validation expectation

- **Tolerance**: validator runs in `PASS_THEORETICAL` mode: it checks that (i) the curve is monotonically declining over y in [0.5, 60], (ii) the asymptote at y=60 is within [0.50, 0.55] (i.e., approaching c=0.5), (iii) all output values lie within the printed axis bound [0.0, 0.8].
- **Expected MAE** vs printed figure: not measured numerically. There are no published tabulated points to compare against. The validator returns `status=PASS_THEORETICAL` when shape and bound checks pass.
- **CD2 divergence**: not applicable (no CD2 predecessor).
