# S406 — Automotive Average Cost (Fig 4.21)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S406
**Status**: book_period_validated

> **Recovery (2026-05-26):** Recovered from data_unavailable by native-resolution vector trace of Shaikh Fig 4.21 Average Cost (= Inman 1995) from the book PDF (Robert _PDF_LIBRARY p204-205), overlay-validated vs the figure. content_type=theoretical (Monte-Carlo simulation curve), x=annual vehicle output; chopped keys on point-index per the S308 functional-curve precedent. provenance: digitized. V03 round-trip PASS; pipeline + anu-doctor 0/0. Source: SalvagedInputs/book_data/Reconstructed/Inman_1995_S404-407_cost_curves.json; method: Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md.
**Authored**: 2026-05-18
**Author**: opus-subagent-ch4-fanout

---

## 1. Definition

**S406** is Shaikh's Figure 4.21 (book p. 162) — Inman's simulated **automotive average (total) cost** (USD per car) vs. annual vehicle production. Reproduces Inman (1995), p. 64, fig. 5.

Decomposes as `ac(Q) = afc(Q) + amc + alc(Q)` with `amc` constant (Inman's assumption) and `alc(Q)` = the S404 curve.

## 2. Why it matters in Chapter 4

Fig 4.21 shows the asymmetric U-shape with the minimum somewhere in shift 3 — Shaikh's key bridge to the theoretical curves of S401/S402. Per p. 161: "Inman's empirical results were anticipated in the theoretical discussion in section V because his actual automotive cost curves reproduced in figure 4.21 are strikingly similar to the theoretical curves previously depicted in figures 4.16 and 4.17."

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher | Native units | Retrieval |
|---|---|---|---|---|
| **S406-A** | output range 0–~450 thousand vehicles/year | Inman, R. R. (1995), *The Engineering Economist* 41(1), 53–67, fig. 5 | USD per car | **NOT RETRIEVABLE** (paywall) |

## 4. Construction

`ac(Q) = afc(Q) + amc + alc(Q)` where `alc` derives from S404. Inman's published figure shows the combined curve only; component breakdowns are textual.

## 5. Year coverage

Not applicable.

## 6. Units

USD per car. Y-axis range ~$5,100–$5,500 in fig. 5 — variation in ac is small relative to level because material + overhead dominate.

## 7. Caveats

Identical to S404. Same paywall, same `data_unavailable` posture, no figure digitization.

## 8. Cross-references

- **Cross-series**: S404 (alc input), S407 (mc twin of this ac).

## 9. Validation expectation

`PASS_DATA_UNAVAILABLE`.
