# S407 — Automotive Marginal Cost (Fig 4.22)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S407
**Status**: book_period_validated

> **Recovery (2026-05-26):** Recovered from data_unavailable by native-resolution vector trace of Shaikh Fig 4.22 Marginal Cost (= Inman 1995) from the book PDF (Robert _PDF_LIBRARY p204-205), overlay-validated vs the figure. content_type=theoretical (Monte-Carlo simulation curve), x=annual vehicle output; chopped keys on point-index per the S308 functional-curve precedent. provenance: digitized. V03 round-trip PASS; pipeline + anu-doctor 0/0. Source: SalvagedInputs/book_data/Reconstructed/Inman_1995_S404-407_cost_curves.json; method: Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md.
**Authored**: 2026-05-18
**Author**: opus-subagent-ch4-fanout

---

## 1. Definition

**S407** is Shaikh's Figure 4.22 (book p. 163) — Inman's simulated **automotive overall marginal cost** (USD per additional car) vs. annual vehicle production. Reproduces Inman (1995), p. 64, fig. 6.

`mc(Q) = marginal_material_cost(Q) + mlc(Q)`, where the first term equals the (constant) average material cost and the second is the S405 curve.

## 2. Why it matters in Chapter 4

This is Shaikh's culminating empirical exhibit for the chapter's central argument against `p = mc`. Per p. 161: "The rule p = mc would then select a very large number of points if p happened to run along the flat bottom of the curve; would select multiple points, including engineering capacity, if p was between this lower limit and the tops of various spikes; and would select only engineering capacity if p was higher still." The flat-bottom-with-spikes shape — empirically observed in Inman's simulation — destroys the unique-output interpretation of `p = mc`.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher | Native units | Retrieval |
|---|---|---|---|---|
| **S407-A** | output range 0–~450 thousand vehicles/year | Inman, R. R. (1995), *The Engineering Economist* 41(1), 53–67, fig. 6 | USD per additional car | **NOT RETRIEVABLE** (paywall) |

## 4. Construction

`mc(Q) = c_material + mlc(Q)` (constant material cost). `mlc` from S405. Inman fig. 6 shows the combined curve.

## 5. Year coverage

Not applicable.

## 6. Units

USD per additional car. Y-axis range ~$0–$8,000 in fig. 6 — material-cost flat bottom dominates, with modest labor-cost spikes at shift changes.

## 7. Caveats

Identical to S404 — `data_unavailable`. No figure digitization.

## 8. Cross-references

- **Cross-series**: S405 (mlc input), S406 (ac twin), S402 (theoretical analogue under per-hour wages).

## 9. Validation expectation

`PASS_DATA_UNAVAILABLE`.
