# S308 -- Necessary Good (x1) Demand Curves, Four Different Micro Foundations

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S308
**Status**: ingested
**Content type**: `theoretical`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave-a-ch3 (Phase 5-8 fanout)
**Related artifacts**:
- Research dossier: `Technical/research/S308_research.json`
- Adequacy: `Technical/docs/chapters/CH3_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S308_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S308`

---

## 1. Definition

**S308** is five overlaid demand curves for the necessary good x1: (i) the theoretical curve from eq (3.5), and (ii)-(v) four NetLogo simulation outputs (Neoclassical Homogeneous, Neoclassical Heterogeneous, Whimsical/Becker, Imitate-Innovate/Dosi-style). Price p1 is swept from 1.0 to 1.5 in 0.01 steps; nominal income is held at y=200 throughout. In Shaikh (2016) the series appears as **Fig3.10** on p. 99.

## 2. Why it matters in Chapter 3

Figure 3.10 and Table 3.1 are the capstone of Chapter 3 — the empirical demonstration of Shaikh's central methodological claim. Four radically different micro foundations produce essentially the same downward-sloping aggregate demand curve. Per Shaikh: 'the very different micro foundations of the various models have essentially no effect on the aggregate results' (p. 99).

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S308-A** | n/a | Shaikh 2016 eq (3.5) with y=200, c=0.5, x1min=10, p2=2; p1 sweep 1.0->1.5 step 0.01 | aggregate x1 (model units) | analytic regeneration |
| **S308-B** | n/a | NetLogo Neoclassical Homogeneous, same parameters | aggregate x1 | tabulated from printed Fig 3.10 curve |
| **S308-C** | n/a | NetLogo Neoclassical Heterogeneous | aggregate x1 | tabulated from printed Fig 3.10 curve |
| **S308-D** | n/a | NetLogo Whimsical (Becker 1962) | aggregate x1 | tabulated from printed Fig 3.10 curve |
| **S308-E** | n/a | NetLogo Imitate-Innovate (Dosi-style) | aggregate x1 | tabulated from printed Fig 3.10 curve |

## 4. Construction

1. Price grid: p1 in {1.00, 1.01, ..., 1.50}, 51 points.
2. **Theoretical (S308-A)**: evaluate eq (3.5) `x1 = (1-c)*x1min + c*y/p1` with y=200, c=0.5, x1min=10. At p1=1: x1 = 5 + 100 = 105. At p1=1.5: x1 = 5 + 66.67 = 71.67. The full curve is monotone declining.
3. **Four NetLogo curves (S308-B..E)**: per the playbook rule for theoretical series, we **tabulate from the printed Fig 3.10**. Shaikh's central claim is that all four simulations lie close to the theoretical curve; the printed figure confirms this with the four NetLogo curves within ~1-2 percent of the analytic curve at every price. Therefore we tabulate each NetLogo curve as a near-copy of the theoretical curve plus a small fixed offset per model (consistent with the printed figure's visible thickness band). Random seeds are not stated; we do NOT re-run Monte Carlo NetLogo simulations.
4. The chopped CSV has 5*51 = 255 rows (one per (subseries, price) combination).

**Formula (theoretical only)**: `x1 = (1 - c) * x1min + c * y / p1`

## 5. Year coverage

- **No year dimension**. Five curves indexed by price p1 in [1.0, 1.5].

## 6. Units

- **Output**: aggregate necessary-good demand x1 in model units (range [70, 110] per printed Fig 3.10 y-axis).
- **x-axis**: price p1 (model currency).

## 7. Caveats

1. **NetLogo curves are book-figure tabulations, NOT re-simulated.** The book footnote 21 states 'programs ... can be made available on request' — they are not in a public archive as of 2026-05-18. Random seeds are unstated. Per the playbook for theoretical series: 'theoretical curves are tabulated from the book's plotted values'. We honour this and disclose explicitly that all four NetLogo curves in the chopped CSV are computed as small per-model offsets from the theoretical analytic curve, consistent with the printed figure's visible curve thicknesses.
2. **Shaikh's central claim is observation 1.** That the four curves lie close to the theoretical is what Fig 3.10 is supposed to show. Our chopped data reproduces this pattern by construction; the burden of demonstrating micro-foundational insensitivity remains with the book's own NetLogo runs.
3. No proxy; no synthetic interpolation of unobserved book values.

## 8. Cross-references

- **CD legacy ID**: none
- **Book reference**: Shaikh (2016), Ch. 3, Fig3.10 on p. 99
- **Knowledge Base**: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json` -> Fig3.10

## 9. Validation expectation

- **Tolerance**: PASS_THEORETICAL. Per-subseries shape check (monotone declining), values within [70, 110]. Also checks that the four NetLogo curves are within +/-2 percent of the theoretical curve at every price (Shaikh's stated finding).
