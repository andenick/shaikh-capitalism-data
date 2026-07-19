# S404 — Automotive Unit Labor Cost (Fig 4.19)

**Data Provenance Record (DPR)** — the internal, full-provenance companion to the public Explainer.
**Record type**: Data Provenance Record (source-and-construction detail)
**Series ID**: S404
**Status**: book_period_validated

> **Recovery (2026-05-26):** This curve was previously marked as having no available underlying data. It was recovered by digitizing Shaikh's Figure 4.19 (Automotive Unit Labor Cost, which reproduces Inman 1995) via native-vector trace of the book PDF (PyMuPDF `get_drawings`), then overlay-checking the digitized points against the printed figure. It is a theoretical curve (the mean of a Monte-Carlo simulation of an automotive plant); the horizontal axis is annual vehicle output (not calendar years), and the points are ordered by an index number. The validation step reproduces the digitized values exactly, and the project self-audit passes. Reconstructed points: reconstructed book source data. Extraction workbench: Tsoulfidis-Tsaliki extraction worklog (overlays: `inman_S404_native.png`, `inman_S404_overlay.png`). 
**Authored**: 2026-05-18
**Prepared by**: RSCD data-construction pipeline
**Related artifacts**:
- Series research notes: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry → `series.S404`
- Subsource registry: subsource registry → `INMAN_1995_ENGINEERING_ECONOMIST`

---

## 1. Definition

**S404** is Shaikh's Figure 4.19 (book p. 162) — simulated **automotive unit labor cost** (USD per car) plotted against annual vehicle production (in thousands). The figure is reproduced from Inman (1995), p. 61, fig. 3. Inman's underlying values are the means of a Monte-Carlo simulation of an automotive assembly plant's cost structure across output levels 0 to ~450 thousand vehicles/year, with explicit shift-addition markers and a vertical segment at engineering capacity.

This is a **cost-vs-output curve, not a calendar time series.**

## 2. Why it matters in Chapter 4

Inman's empirical curves (S404–S407) supply the empirical counterpart to Shaikh's theoretical curves (S401–S402). Shaikh's claim on p. 161 — that Inman's curves are "strikingly similar" to the theoretical curves he derived from Appendix 4.2 — is the empirical anchor for the chapter's revisionist account of cost curves. Fig 4.19 specifically demonstrates the "deformed U-shape with spikes at the beginning of each shift and roughly similar minimum points for each shift" pattern.

## From the Book

> Inman (1995) provides one of the most striking illustrations of actual cost curves. [...] The overall result is a deformed U-shape with spikes at the beginning of each shift and roughly similar minimum points for each shift.
> -- Shaikh (2016), Chapter 4, pp. 160-161 

Verified verbatim against the project knowledge-base extraction of the source book (`ch04_production_costs.md`).

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S404-A** (the dataset's single data column) | output range 0–~450 thousand vehicles/year | Inman, R. R. (1995), *The Engineering Economist* 41(1), 53–67 | USD per car vs. annual vehicle production (thousands) | **Recovered by figure digitization** of the curve as reproduced in Shaikh's Figure 4.19 (which reproduces Inman's fig. 3), overlay-validated against the printed figure |

**Citation note**: during citation verification the author was confirmed as Robert R. Inman (not Robert P. Inman, as an earlier draft of the source notes had it). The canonical citation, verified via the Crossref bibliographic service, is:

> Inman, R. R. (1995). "Shape Characteristics of Cost Curves Involving Multiple Shifts in Automotive Assembly Plants." *The Engineering Economist* 41(1), 53–67. DOI: 10.1080/00137919508967475

## 4. Construction

Per Inman (1995), `ulc(Q) = (fixed_labor_cost + variable_labor_cost(Q)) / Q`, where the variable component sums overtime, full-time, under-time, and second/third-shift premia, and the fixed component encodes layoff pay (95% of after-tax pay less $17.50/week). All cost values are means of a Monte-Carlo simulation.

**Inman (1995) published the simulation only as figures 3–6, not as a tabulated series**, and the journal full text is behind a paywall. The curve was therefore recovered by digitizing Shaikh's Figure 4.19 (which reproduces Inman's fig. 3) from the source-book scan; the digitized points are stored at reconstructed book source data and were overlay-validated against the printed figure (see the recovery note at the top of this record).

## 5. Year coverage

Not applicable (cross-sectional cost-vs-output curve, single 1995 simulation).

## 6. Units

USD per car vs. annual vehicle production (thousands). Native to Inman's simulation; not normalized to a base year.

## 7. Caveats

1. **Digitized from the printed figure (v1.3 recovery, 2026-05-26).** Inman published the simulation only as figures, not as tabulated values, and the journal full text is behind a paywall. The series values were therefore recovered by native-vector trace of Shaikh's Figure 4.19 (PyMuPDF `get_drawings`) from the source-book PDF, overlay-validated against the printed figure, and stored as the canonical digitized points at reconstructed book source data. This was part of the RSCD v1.3 recovery campaign: 7 book-period series including all four Inman curves (S404–S407) were recovered by offline figure digitization after being previously marked `data_unavailable`. The recovery flipped all four series to `book_period_validated`. The loader now emits the digitized curve, a machine-readable (chopped) CSV exists, and the validator round-trips the values.
2. **Honest digitization provenance.** Digitization from figures is the project's documented last-resort recovery method when exact values cannot be obtained otherwise. The digitized points are overlay-checked against the printed figure and carry a dated recovery note; they are not fabricated, proxied, or guessed. The provenance is transparently labeled `digitized` in the registry subseries source field and the VALIDATION_REPORT.
3. **Bibliography corrected.** Earlier drafts carried the wrong "Robert P. Inman" and a placeholder link to an unrelated volume. This record and the registry source fields now reflect the verified Robert R. Inman (1995) citation: Inman, R. R. (1995). "Shape Characteristics of Cost Curves Involving Multiple Shifts in Automotive Assembly Plants." *The Engineering Economist* 41(1), 53–67. DOI: 10.1080/00137919508967475 (Crossref-verified).
4. **Journal paywall.** The publisher's page returned an automated anti-bot response (HTTP 403, not an invalid address) during a reachability check; this is why the figure was recovered from Shaikh's reproduction rather than from the original article.

## 8. Cross-references

- **Predecessor series**: none (first constructed in this dataset)
- **Book reference**: Shaikh (2016), Ch. 4, p. 162 (Fig 4.19); narrative pp. 160–161.
- **Cross-series**: S405 (marginal labor cost from same Inman simulation, fig. 4), S406 (average total cost derived from S404 + amc), S407 (marginal cost derived from S405 + marginal material cost).

## 9. Validation expectation

- **Check performed**: the validation step reproduces the digitized curve from the stored reconstruction and confirms the processed data match the digitized points (a round-trip check). Because the source is a digitized figure rather than a published table, the check verifies faithful reproduction of the digitized points and shape rather than computing an error against an independent tabulation.
- **Tolerance**: round-trip exact (the validator reads the same reconstruction the data-loading step consumes).
- **Future refinement**: should Inman's original tabulated values become available (library access, author contact, or a replication study), the digitized reconstruction can be replaced without changing the rest of the pipeline.
