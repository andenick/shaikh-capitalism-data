# S404 — Extension Provenance Record

**Series**: S404 — Automotive Unit Labor Cost (Fig 4.19)
**Phase**: 6 (Extension)
**Construction classification**: `derived` / `data_unavailable`
**Extension method**: **not_applicable_theoretical**
**Authored**: 2026-05-18
**Author**: opus-subagent-ch4-fanout

---

## 1. Why this series is NOT extendable

S404 reproduces a single 1995 Monte-Carlo simulation of one automotive plant's cost structure (Inman, *Engineering Economist* 41(1), fig. 3). There is no calendar-year axis to extend; "extension" would require re-running Inman's Monte-Carlo with current data — a research project, not a data pull.

Additionally the underlying simulation values are not publicly tabulated, so even the **book-period** reproduction is `data_unavailable` (see DPR §4 and §7). The data_unavailable status compounds the not-applicable extension status.

## 2. Construction classification

`derived` / `data_unavailable`. Anu lazy-splice prohibition vacuous.

## 3. Method

Not applicable.

## 4. Component re-fetching

Not applicable — paywalled and not previously cached.

## 5. Proxies

**None.** No proxy substitution attempted — per anti-degradation rules, we do not invent a "comparable" study to fill the data hole.

## 6. Synthetic data

**None.** We do not figure-digitize values into the pipeline (see DPR §7 caveat 2). The figure image itself, as reproduced in Shaikh p. 162, is the canonical artifact; Phase 9 viz can include it directly.

## 7. Failure modes & graceful degradation

The `data_unavailable` recipe IS the graceful degradation:
- L01 returns `SKIPPED, reason=data_unavailable`
- P02 returns `SKIPPED`
- V03 returns `PASS_DATA_UNAVAILABLE`
- O06_chopped_writer is no-op (no processed parquet → no chopped CSV)
- O06_extenbook_writer can still build an extenbook with DPR+EPR+Sources sheets only; no Data sheet

## 8. CD2 divergence

Not applicable (no CD2 predecessor).

## 9. Forward roadmap

If Inman 1995 underlying data are obtained, a follow-up Decision Log entry can authorize either (a) loader plumbing from a structured CSV transcription, or (b) authorized WebPlotDigitizer extraction with full provenance disclosure. Until then the series stays `data_unavailable`.
