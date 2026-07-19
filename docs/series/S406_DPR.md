# S406 — Automotive Average Cost (Fig 4.21)

**Data Provenance Record (DPR)** — the internal, full-provenance companion to the public Explainer.
**Record type**: Data Provenance Record (source-and-construction detail)
**Series ID**: S406
**Status**: book_period_validated

> **Recovery (2026-05-26):** This curve was previously marked as having no available underlying data. It was recovered by digitizing Shaikh's Figure 4.21 (Average Cost, which reproduces Inman 1995) via native-vector trace of the book PDF (PyMuPDF `get_drawings`), then overlay-checking the digitized points against the printed figure. It is a theoretical curve (the mean of a Monte-Carlo plant simulation); the horizontal axis is annual vehicle output (not calendar years), and the points are ordered by an index number. The validation step reproduces the digitized values, and the project self-audit passes. Reconstructed points: reconstructed book source data. Extraction workbench: Tsoulfidis-Tsaliki extraction worklog (overlays: `inman_S406_native.png`, `inman_S406_overlay.png`). 
**Authored**: 2026-05-18
**Prepared by**: RSCD data-construction pipeline

---

## 1. Definition

**S406** is Shaikh's Figure 4.21 (book p. 162) — Inman's simulated **automotive average (total) cost** (USD per car) vs. annual vehicle production. Reproduces Inman (1995), p. 64, fig. 5.

Decomposes as `ac(Q) = afc(Q) + amc + alc(Q)` with `amc` constant (Inman's assumption) and `alc(Q)` = the S404 curve.

## 2. Why it matters in Chapter 4

Fig 4.21 shows the asymmetric U-shape with the minimum somewhere in shift 3 — Shaikh's key bridge to the theoretical per-worker and per-hour cost curves (companion series S401/S402).

## From the Book

> his actual automotive cost curves reproduced in figure 4.21 are strikingly similar to the theoretical curves previously depicted in figures 4.16 and 4.17.
> -- Shaikh (2016), Chapter 4, p. 161 

Verified verbatim against the project knowledge-base extraction of the source book (`ch04_production_costs.md`).

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher | Native units | Retrieval |
|---|---|---|---|---|
| **S406-A** (the dataset's single data column) | output range 0–~450 thousand vehicles/year | Inman, R. R. (1995), *The Engineering Economist* 41(1), 53–67, fig. 5 | USD per car | **Recovered by figure digitization** of Shaikh's Fig 4.21 (reproducing Inman's fig. 5), overlay-validated against the printed figure |

## 4. Construction

`ac(Q) = afc(Q) + amc + alc(Q)` where `alc` derives from S404. Inman's published figure shows the combined curve only; component breakdowns are textual. The curve was recovered by digitizing Shaikh's Fig 4.21 reproduction (stored in `Inman_1995_S404-407_cost_curves.json`).

## 5. Year coverage

Not applicable.

## 6. Units

USD per car. Y-axis range ~$5,100–$5,500 in fig. 5 — variation in ac is small relative to level because material + overhead dominate.

## 7. Caveats

1. **Digitized from the printed figure (v1.3 recovery, 2026-05-26).** Inman published the simulation only as figures, not as tabulated values. The series values were recovered by native-vector trace of Shaikh's Figure 4.21 (PyMuPDF `get_drawings` from the source-book PDF), overlay-validated against the printed figure, and stored in the shared Inman reconstruction file reconstructed book source data. This was part of the RSCD v1.3 recovery campaign: 7 book-period series including all four Inman curves (S404–S407) were recovered by offline figure digitization. The series is now `book_period_validated`.
2. **Honest digitization provenance.** Digitization from figures is the project's documented last-resort recovery method. The digitized points are overlay-checked against the printed figure and carry a dated recovery note; they are not fabricated, proxied, or guessed.
3. **Citation confirmed.** Robert R. Inman (1995), *The Engineering Economist* 41(1), 53–67, DOI 10.1080/00137919508967475 (Crossref-verified).

## 8. Cross-references

- **Predecessor series**: none (first constructed in this dataset)
- **Cross-series**: S404 (average labor-cost input), S407 (marginal-cost twin of this average-cost curve).

## 9. Validation expectation

The validation step reproduces the digitized curve from the stored reconstruction and confirms the processed data match it (a round-trip check); because the source is a digitized figure rather than a published table, the check verifies faithful reproduction of the digitized points and shape.
