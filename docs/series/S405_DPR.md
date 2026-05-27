# S405 — Automotive Marginal Labor Cost (Fig 4.20)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S405
**Status**: book_period_validated

> **Recovery (2026-05-26):** Recovered from data_unavailable by native-resolution vector trace of Shaikh Fig 4.20 Marginal Labor Cost (= Inman 1995) from the book PDF (Robert _PDF_LIBRARY p204-205), overlay-validated vs the figure. content_type=theoretical (Monte-Carlo simulation curve), x=annual vehicle output; chopped keys on point-index per the S308 functional-curve precedent. provenance: digitized. V03 round-trip PASS; pipeline + anu-doctor 0/0. Source: SalvagedInputs/book_data/Reconstructed/Inman_1995_S404-407_cost_curves.json; method: Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md.
**Authored**: 2026-05-18
**Author**: opus-subagent-ch4-fanout
**Related artifacts**: see S404_DPR §0 (analogous block)

---

## 1. Definition

**S405** is Shaikh's Figure 4.20 (book p. 162) — Inman's simulated **automotive marginal labor cost** (USD per additional car) vs. annual vehicle production (thousands). Reproduces Inman (1995), p. 62, fig. 4.

Same simulation as S404, marginalized: `mlc(Q) = d(total_labor_cost)/dQ`.

## 2. Why it matters in Chapter 4

Shaikh quotes Inman directly (book p. 161): "the peak of the highest spike in marginal labor cost is seven and a half times as high as the bottom" — the curve "is decidedly not 'well behaved'." This is the empirical analogue to S402's spiky theoretical mc curve under per-hour wages and confirms the chapter's central revisionist claim about cost-curve shape.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher | Native units | Retrieval |
|---|---|---|---|---|
| **S405-A** | output range 0–~450 thousand vehicles/year | Inman, R. R. (1995), *The Engineering Economist* 41(1), 53–67, fig. 4 | USD marginal cost per additional car | **NOT RETRIEVABLE** (same paywall as S404) |

Citation correction matches S404 (Robert R. Inman; Crossref DOI 10.1080/00137919508967475).

## 4. Construction

`mlc(Q) = d(fixed_labor + variable_labor(Q)) / dQ = d(variable_labor)/dQ`. Computed by Inman (1995) via Monte-Carlo simulation, reported only as fig. 4. No tabulated underlying values published.

## 5. Year coverage

Not applicable (cost-vs-output cross-section).

## 6. Units

USD per additional car vs. annual vehicle production (thousands). Y-axis range ~$0–$1,000 in fig. 4.

## 7. Caveats

Identical to S404 — `data_unavailable`. No figure digitization into pipeline.

## 8. Cross-references

- **Cross-series**: S404 (average labor cost, fig. 3 of same Inman simulation), S407 (overall marginal cost = mlc + marginal material cost).

## 9. Validation expectation

`PASS_DATA_UNAVAILABLE`.
