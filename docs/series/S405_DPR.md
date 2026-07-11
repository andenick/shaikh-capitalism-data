# S405 — Automotive Marginal Labor Cost (Fig 4.20)

**Data Provenance Record (DPR)** — the internal, full-provenance companion to the public Explainer.
**Record type**: Data Provenance Record (source-and-construction detail)
**Series ID**: S405
**Status**: book_period_validated

> **Recovery (2026-05-26):** This curve was previously marked as having no available underlying data. It was recovered by digitizing Shaikh's Figure 4.20 (Marginal Labor Cost, which reproduces Inman 1995) via native-vector trace of the book PDF (PyMuPDF `get_drawings`), then overlay-checking the digitized points against the printed figure. It is a theoretical curve (the mean of a Monte-Carlo plant simulation); the horizontal axis is annual vehicle output (not calendar years), and the points are ordered by an index number. The validation step reproduces the digitized values, and the project self-audit passes. Reconstructed points: reconstructed book source data. Extraction workbench: Tsoulfidis-Tsaliki extraction worklog (overlays: `inman_S405_native.png`, `inman_S405_overlay.png`). 
**Authored**: 2026-05-18
**Prepared by**: RSCD data-construction pipeline
**Related artifacts**: see the recovery note in S404_DPR (analogous block)

---

## 1. Definition

**S405** is Shaikh's Figure 4.20 (book p. 162) — Inman's simulated **automotive marginal labor cost** (USD per additional car) vs. annual vehicle production (thousands). Reproduces Inman (1995), p. 62, fig. 4.

Same simulation as S404, marginalized: `mlc(Q) = d(total_labor_cost)/dQ`.

## 2. Why it matters in Chapter 4

Shaikh quotes Inman directly (book p. 161): "the peak of the highest spike in marginal labor cost is seven and a half times as high as the bottom" — the curve "is decidedly not 'well behaved'." This is the empirical analogue to the spiky theoretical marginal-cost curve under per-hour wages (companion series S402) and confirms the chapter's central revisionist claim about cost-curve shape.

## From the Book

> Marginal labor cost in figure 4.20 is therefore flat-bottomed, but with much larger spikes at shift beginnings: the peak of the highest spike in marginal labor cost is seven and a half times as high as the bottom (62)! This curve is decidedly not "well behaved" (64).
> -- Shaikh (2016), Chapter 4, p. 161 

Verified verbatim against the project knowledge-base extraction of the source book (`ch04_production_costs.md`).

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher | Native units | Retrieval |
|---|---|---|---|---|
| **S405-A** (the dataset's single data column) | output range 0–~450 thousand vehicles/year | Inman, R. R. (1995), *The Engineering Economist* 41(1), 53–67, fig. 4 | USD marginal cost per additional car | **Recovered by figure digitization** of Shaikh's Fig 4.20 (reproducing Inman's fig. 4), overlay-validated against the printed figure |

Citation correction matches S404 (Robert R. Inman; Crossref DOI 10.1080/00137919508967475).

## 4. Construction

`mlc(Q) = d(fixed_labor + variable_labor(Q)) / dQ = d(variable_labor)/dQ`. Computed by Inman (1995) via Monte-Carlo simulation and reported only as fig. 4 (no tabulated values were published), so the curve was recovered by digitizing Shaikh's Fig 4.20 reproduction (stored in `Inman_1995_S404-407_cost_curves.json`).

## 5. Year coverage

Not applicable (cost-vs-output cross-section).

## 6. Units

USD per additional car vs. annual vehicle production (thousands). Y-axis range ~$0–$1,000 in fig. 4.

## 7. Caveats

Same recovery posture as S404: previously marked as having no available data, now recovered by figure digitization of Shaikh's reproduction and overlay-validated. Digitization from figures is the project's documented last-resort recovery method when exact values cannot be obtained otherwise; this is not a proxy or fabricated series. Citation confirmed as Robert R. Inman (1995).

## 8. Cross-references

- **Predecessor series**: none (first constructed in this dataset)
- **Cross-series**: S404 (average labor cost, fig. 3 of same Inman simulation), S407 (overall marginal cost = mlc + marginal material cost).

## 9. Validation expectation

The validation step reproduces the digitized curve from the stored reconstruction and confirms the processed data match it (a round-trip check); because the source is a digitized figure rather than a published table, the check verifies faithful reproduction of the digitized points and shape.
