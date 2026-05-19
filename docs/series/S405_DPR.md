# S405 — Automotive Marginal Labor Cost (Fig 4.20)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S405
**Status**: ingested (data_unavailable)
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
