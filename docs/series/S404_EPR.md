# S404 — Extension Provenance Record

**Series**: S404 — Automotive Unit Labor Cost (Fig 4.19)
**Record type**: Extension Provenance Record
**Construction classification**: `derived` (theoretical Monte-Carlo simulation curve)
**Extension method**: **not_applicable_theoretical**
**Authored**: 2026-05-18
**Author**: RSCD data-construction pipeline

---

## 1. Why this series is NOT extendable

S404 reproduces a 1995 Monte-Carlo simulation of one automotive plant's cost structure. Its horizontal axis is annual vehicle output (in thousands), **not** calendar time, so there is no calendar-year axis to extend forward; a genuine "extension" would require re-running that Monte-Carlo simulation with current data — a research project, not a data pull.

The series values were recovered on 2026-05-26 by figure digitization: the cost curve as reproduced in Shaikh's Chapter 4 (Fig 4.19) — which in turn reproduces Inman (1995), *The Engineering Economist* 41(1):53-67, fig. 3 — was traced, and the digitized points were overlay-validated against the printed figure. The reconstructed points are stored among the project's salvaged reconstructions. (An earlier version of this record described the series as unavailable because Inman's underlying Monte-Carlo values were never published as a table; that description is superseded by the figure-digitization recovery.)

## 2. Construction classification

`derived` — a theoretical Monte-Carlo simulation curve recovered by figure digitization. The lazy-splice prohibition is vacuous because there is no observed time series on either side of a calendar boundary.

## 3. Method

Not applicable.

## 4. Component re-fetching

Not applicable — there is no time series to re-fetch from an agency; the curve is a static simulation result recovered from Shaikh's printed figure.

## 5. Proxies

**None.** No proxy substitution: the values are digitized directly from the figure Shaikh prints (Fig 4.19), not borrowed from some "comparable" study.

## 6. Synthetic data

**None in the prohibited sense.** The values were recovered by digitizing Shaikh's printed figure and overlay-validating the trace against it — a faithful transcription of the source's own published curve, not invented or gap-filled data. The figure image itself, as reproduced in Shaikh p. 162, remains the canonical artifact.

## 7. Failure modes & graceful degradation

Because the values were recovered by figure digitization, the pipeline now runs the normal path rather than the earlier no-data path:
- The data-loading step reads the digitized reconstruction (stored among the project's salvaged reconstructions) instead of skipping.
- The processing step passes the points through.
- The validation step runs in its theoretical-curve mode (`PASS_THEORETICAL` — it checks the curve's shape and bounds against the printed figure rather than matching a public tabulation, since Inman's underlying Monte-Carlo values were never published as a table).
- The chopped-CSV and extenbook writers produce their normal outputs from the reconstructed points.

## 8. Predecessor divergence

Not applicable — no earlier reconstruction of this project (internally called CD/CD2) contained this series.

## 9. Forward roadmap

The series was recovered via authorized figure digitization of Shaikh's printed curve. If Inman's (1995) underlying tabulated data were ever obtained, a follow-up Decision Log entry could authorize loading from a structured CSV transcription, which would supersede the digitized trace with full provenance disclosure.
