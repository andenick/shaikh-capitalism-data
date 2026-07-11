# S407 — Automotive Marginal Cost (Fig 4.22)

**Data Provenance Record (DPR)** — the internal, full-provenance companion to the public Explainer.
**Record type**: Data Provenance Record (source-and-construction detail)
**Series ID**: S407
**Status**: book_period_validated

> **Recovery (2026-05-26):** This curve was previously marked as having no available underlying data. It was recovered by digitizing Shaikh's Figure 4.22 (Marginal Cost, which reproduces Inman 1995) via native-vector trace of the book PDF (PyMuPDF `get_drawings`), then overlay-checking the digitized points against the printed figure. It is a theoretical curve (the mean of a Monte-Carlo plant simulation); the horizontal axis is annual vehicle output (not calendar years), and the points are ordered by an index number. The validation step reproduces the digitized values, and the project self-audit passes. Reconstructed points: reconstructed book source data. Extraction workbench: Tsoulfidis-Tsaliki extraction worklog (overlays: `inman_S407_native.png`, `inman_S407_overlay.png`). 
**Authored**: 2026-05-18
**Prepared by**: RSCD data-construction pipeline

---

## 1. Definition

**S407** is Shaikh's Figure 4.22 (book p. 163) — Inman's simulated **automotive overall marginal cost** (USD per additional car) vs. annual vehicle production. Reproduces Inman (1995), p. 64, fig. 6.

`mc(Q) = marginal_material_cost(Q) + mlc(Q)`, where the first term equals the (constant) average material cost and the second is the S405 curve.

## 2. Why it matters in Chapter 4

This is Shaikh's culminating empirical exhibit for the chapter's central argument against the neoclassical `price = marginal cost` rule. Per p. 161: "The rule p = mc would then select a very large number of points if p happened to run along the flat bottom of the curve; would select multiple points, including engineering capacity, if p was between this lower limit and the tops of various spikes; and would select only engineering capacity if p was higher still." The flat-bottom-with-spikes shape — empirically observed in Inman's simulation — destroys the unique-output interpretation of `price = marginal cost`.

## From the Book

> the overall marginal cost curve is essentially flat-bottomed over much of the observed range of output, with modest spikes at each new shift.
> -- Shaikh (2016), Chapter 4, p. 161 

Verified verbatim against the project knowledge-base extraction of the source book (`ch04_production_costs.md`).

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher | Native units | Retrieval |
|---|---|---|---|---|
| **S407-A** (the dataset's single data column) | output range 0–~450 thousand vehicles/year | Inman, R. R. (1995), *The Engineering Economist* 41(1), 53–67, fig. 6 | USD per additional car | **Recovered by figure digitization** of Shaikh's Fig 4.22 (reproducing Inman's fig. 6), overlay-validated against the printed figure |

## 4. Construction

`mc(Q) = c_material + mlc(Q)` (constant material cost). `mlc` from S405. Inman fig. 6 shows the combined curve. The curve was recovered by digitizing Shaikh's Fig 4.22 reproduction (stored in `Inman_1995_S404-407_cost_curves.json`).

## 5. Year coverage

Not applicable.

## 6. Units

USD per additional car. Y-axis range ~$0–$8,000 in fig. 6 — material-cost flat bottom dominates, with modest labor-cost spikes at shift changes.

## 7. Caveats

Same recovery posture as S404: previously marked as having no available data, now recovered by figure digitization of Shaikh's reproduction and overlay-validated. Digitization from figures is the project's documented last-resort recovery method when exact values cannot be obtained otherwise; this is not a proxy or fabricated series. Citation confirmed as Robert R. Inman (1995).

## 8. Cross-references

- **Predecessor series**: none (first constructed in this dataset)
- **Cross-series**: S405 (marginal labour-cost input), S406 (average-cost twin), S402 (theoretical analogue under per-hour wages).

## 9. Validation expectation

The validation step reproduces the digitized curve from the stored reconstruction and confirms the processed data match it (a round-trip check); because the source is a digitized figure rather than a published table, the check verifies faithful reproduction of the digitized points and shape.
