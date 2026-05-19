# S801 — Extension Provenance Record

**Series**: S801 — Wholesale Prices in Oligopolistic and Competitive Industries, 1965-1973 (Eichner Fig 8.1)
**Phase**: 6 (Extension)
**Construction classification**: `data_unavailable`
**Extension method**: not applicable — see §1
**Authored**: 2026-05-18
**Author**: opus-subagent-ch8-fanout
**Related**: `S801_DPR.md`

---

## 1. Classification

`content_type = data_unavailable`. There is no byte-exact underlying dataset to extend. Eichner (1973) p. 1187 publishes Figure 8.1 as a chart only; no underlying table accompanies the chart; Shaikh (2016) reproduces the chart without transcribing values; the Appendix8_* chopped tables do not include this figure (only Figs 8.2-8.6).

## 2. Why no extension is attempted

- The original raw data (Eichner's 1965-1973 wholesale-price indices for his specific concentrated vs. competitive industry partition) is not available in any source accessible to the RSCD workspace.
- The closest modern source (BLS PPI by NAICS industry, partitioned via Census Concentration Ratios) has incompatible industry classifications (SIC 1965-1973 vs. NAICS post-1997), and the set of industries in Eichner's specific high-CR / low-CR partition is itself unrecoverable.
- Any modern reconstruction would therefore be a proxy in the Anu sense, requiring formal Concept Match Justification and Phase 6 human review approval. Per the Anti-Degradation and No-Proxy rules, this is not undertaken in Phase 5.

## 3. Method

N/A.

## 4. No-Proxy disclosure

**None attempted.** BLS PPI is not a proxy for Eichner's chart — it would be a *re-construction* requiring (a) SIC→NAICS concordance, (b) re-application of CR thresholds, and (c) selection of an industry set that mirrors Eichner's (which itself is unrecoverable from the published article). Such a reconstruction would not meet the Anu No-Proxy bar without explicit Phase 6 human review.

## 5. No-Synthetic disclosure

**None.** No interpolation, no digitization (digitization deferred to Phase 9 visualization, where it is appropriately constrained with `provenance: digitized` flagging).

## 6. Failure-mode table

| Failure | Action |
|---|---|
| Loader invoked | Returns `{"status": "SKIPPED", "reason": "data_unavailable"}` — by design, not a failure |
| Processor invoked | Not authored — no `P02_S801_construct.py` |
| Validator invoked | Returns `{"status": "PASS_DATA_UNAVAILABLE"}` |
| Chopped writer invoked | No `Technical/data/processed/S801.parquet` exists; writer silently passes |
| Extenbook writer invoked | No processed parquet → no extenbook by default; manual extenbook (DPR + EPR + Source pages only) may be authored later if needed |

## 7. CD2 divergence pre-disclosure

CD2 had no genuine per-series CSV that matches this exhibit's content. The stub's `cd2_id = S042` was a stale carryover from a Ch10 interest-rate series and has been nulled. The CD2-vs-RSCD comparison is not meaningful here.

## 8. Recovery paths (out-of-scope for Phase 6)

1. **Obtain Eichner 1973 EJ PDF** from JSTOR (DOI 10.2307/2230843; institutional access required — Wayback fallback confirmed HTTP 200) and run WebPlotDigitizer on Figure 8.1 to extract (date, concentrated_index, competitive_index) samples. This would be a **Phase 9 visualization task** with explicit `provenance: digitized` flagging, not a Phase 5 data-ingestion task.
2. **Author contact**: Alfred Eichner died in 1988; his archived working papers may contain the underlying spreadsheet. Out of scope for the current pipeline.
3. **BLS PPI reconstruction**: would be a NEW series (e.g., S801b), classified as a proxy substitution per Anu Framework, requiring Phase 6 formal review and a Concept Match Justification. Out of scope for the current pipeline.
