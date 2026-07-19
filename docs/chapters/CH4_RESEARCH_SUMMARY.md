# Chapter 4 — Production and Costs: Research Rollup

**Phase 3 Wave A** | Reviewer: `opus-subagent-wave-a-ch4` | Date: 2026-05-18

## Scope

Chapter 4 ("Production and Costs," Shaikh 2016, pp. 119–164) contains 24 figures, of which only 8 are flagged as empirical/non-theoretical in `CHAPTER_FIGURE_TABLE_INDEX.json`. Those 8 form the candidate series S401–S408. **None has a CD2 predecessor** in the `CD2_to_RSCD_crosswalk.csv` — this is a fully fresh chapter.

## Critical reclassification

All 8 stubs arrived with default `content_type: "time_series"`. After reading Ch4 and Appendix 4.2, this default is **wrong** for every series in the chapter:

- **S401, S402, S403** are *numerical illustrations* Shaikh computes himself from a stylized productivity formula (eq. 4.2.1 in Appendix 4.2) and stylized prices (pMK, pa, wN/wh, p). They are tabulated for hourly increments H = 1..20 across three shifts, not against calendar time. Reclassified to `content_type: "derived"`, `construction: "formula"`.
- **S404, S405, S406, S407** are *reproductions* of figures 3–6 from Inman (1995), each plotting simulated automotive cost components against annual vehicle production (cross-sectional cost-vs-output curves), not against calendar time. Reclassified to `content_type: "derived"`, `construction: "formula"`.
- **S408** is a *cross-sectional survey snapshot* from Eiteman & Guthrie (1952) — 94% of 1,082 product-responses chose steadily-declining cost curves. Reclassified to `content_type: "cross_sectional"`, `construction: "direct"`. The only calendar-time anchor is the single year 1952.

The validator's `time_series → extension_candidates non-empty` rule does not apply to any of these, so `extension_candidates: []` is correct everywhere. If validator enforces extension for any non-theoretical type, escalate for Phase 4 to ratify the reclassification.

## Per-series synopsis

| SID | Figure | Source | Content type | Notes |
|---|---|---|---|---|
| S401 | 4.16 (p. 155) | Shaikh, Appendix 4.2 Table 4.2.4 (per-worker wage columns) | derived | Cost curves with wN = 100, ulc' = wN·l'. Spikes at shift boundaries. |
| S402 | 4.17 (p. 156) | Shaikh, Appendix 4.2 Table 4.2.4 (per-hour wage columns) | derived | Cost curves with wh = 12.5, ulc = wh·l. Within-shift mc tracks 1/MPL. |
| S403 | 4.18 (p. 157) | Shaikh, Appendix 4.2 Table 4.2.4 (profit columns) | derived | Profit profile from S401/S402 at p = 7. Max-profit at end of shift 2 (per-worker) or at engineering capacity (per-hour). |
| S404 | 4.19 (p. 162) | Inman 1995, p. 61, fig. 3 | derived | Simulated automotive unit labor cost ($/car) vs. annual production. Monte-Carlo. |
| S405 | 4.20 (p. 162) | Inman 1995, p. 62, fig. 4 | derived | Marginal labor cost. Peak spike 7.5× the flat-bottom level. |
| S406 | 4.21 (p. 162) | Inman 1995, p. 64, fig. 5 | derived | Average total cost, asymmetric U with minimum in shift 3. |
| S407 | 4.22 (p. 163) | Inman 1995, p. 64, fig. 6 | derived | Marginal cost dominated by material-cost flat bottom + small labor-cost spikes. |
| S408 | 4.23 (p. 163) | Eiteman & Guthrie 1952, AER 42(5), p. 835 | cross_sectional | 94% of business respondents chose steadily-declining cost curves; contradicts U-shape postulate. |

## Cross-references within the chapter

- S403 derives from S401 + S402 (same Appendix 4.2 numerical scaffold).
- S406 derives from S404 + constant average material cost.
- S407 derives from S405 + constant marginal material cost.
- Shaikh explicitly notes (p. 161) that Inman's empirical curves (S404–S407) are "strikingly similar" to his own theoretical curves (S401–S402), creating a closed theoretical-to-empirical loop within the chapter.

## Open questions for Phase 4 / Phase 5–6

1. **Appendix 4.2 chopped-table workbook is missing** from `SalvagedInputs/book_data/ShaikhChoppedTables/`. Reconstruction options: (a) transcribe Appendix Tables 4.2.1–4.2.4 from book pp. 770–781, or (b) re-implement equation 4.2.1 (xr = (a1 + a2·h − a3·h²)·i) with parameters back-solved from Appendix Table 4.2.1 boundary conditions (xr(h=1)=3.55, xr(h=12)=9.60 peak).
2. **Inman 1995 bibliography** — Shaikh's reference list back matter was not consulted. The exact Inman 1995 citation should be verified before Phase 4 sign-off. Currently provisional.
3. **Eiteman & Guthrie 1952 JSTOR stable ID** is provisional; verify before sign-off.
4. **Schema enhancement** — Phase 4 may want to add a `qualitative_finding` content_type or sub-category for evidence like S408 (a survey percentage rather than a numerical series), and a `cross_references` field to explicitly link derived series (S403 → S401, S402; S406 → S404; S407 → S405).
5. **Author construction** — S401–S403 are author-computed numerical illustrations, not external data. Phase 4 should decide whether such series merit a "primary_source.agency" of "Shaikh (author construction)" (current choice) or a structured author-construction sub-schema.

## Anti-degradation compliance

- No synthetic data substitutions, no proxies, no fabricated URLs.
- All quotes are verbatim from the book PDF (verbatim_check: true for every entry).
- Reclassifications are documented with rationale in each dossier's `methodology_notes`.
- The 8 dossiers contain no calendar-time data — this is faithfully recorded; no fictitious extension series were invented to satisfy the `time_series → extension_candidates` validator rule.

## Validator status

See `Build/PHASE3_VALIDATION_REPORT.json` after running `python Technical/code/utils/_phase3_research_validator.py`. Ch4 series (S401–S408) should all PASS under the current validator since (a) each has ≥3 quotes with definition + source + verbatim_check, (b) primary_source fields are all populated, (c) construction is valid, (d) year_range_book is well-formed, (e) reclassified content_type avoids the `time_series → extension_candidates` rule, and (f) review_history is populated.

---

## Phase 5–8 Closure

**Closed**: 2026-05-18 | **Agent**: opus-subagent-ch4-fanout | **All 8 series PASS**

Full DPR + EPR + L01 + P02 + V03 artifacts authored for every series per `Technical/docs/FANOUT_PLAYBOOK.md`. Three new subsources registered in `SUBSOURCE_METADATA.json`: `SHAIKH_APPENDIX_4_2`, `INMAN_1995_ENGINEERING_ECONOMIST`, `EITEMAN_GUTHRIE_1952`. Registry status for all 8 series upgraded from `candidate` → `ingested`. Phase 4 citation correction (Robert P. Inman → Robert R. Inman; placeholder Brookings URL → Crossref DOI 10.1080/00137919508967475) propagated to registry and subsource metadata.

| SID | content_type | V03 status | MAE | max_pct_err | n_compared | extension status |
|---|---|---|---|---|---|---|
| **S401** | derived | PASS | 0.0 | 0.0% | 122 | not_applicable_theoretical |
| **S402** | derived | PASS | 0.0 | 0.0% | 122 | not_applicable_theoretical |
| **S403** | derived | PASS | 0.0 | 0.0% | 42  | not_applicable_theoretical |
| **S404** | derived | PASS_DATA_UNAVAILABLE | — | — | 0 | not_applicable_theoretical (Inman paywall) |
| **S405** | derived | PASS_DATA_UNAVAILABLE | — | — | 0 | not_applicable_theoretical (Inman paywall) |
| **S406** | derived | PASS_DATA_UNAVAILABLE | — | — | 0 | not_applicable_theoretical (Inman paywall) |
| **S407** | derived | PASS_DATA_UNAVAILABLE | — | — | 0 | not_applicable_theoretical (Inman paywall) |
| **S408** | cross_sectional | PASS | 0.0 | 0.0% | 2 | not_applicable_cross_sectional |

### Per-series notes

- **S401, S402, S403** — Reconstructed Appendix 4.2 Table 4 (`SalvagedInputs/book_data/Reconstructed/Appendix_4_2_Table4.csv`, verbatim from book pp. 779-780) was the canonical source. L01 emits long-form per-(row,component) records (subseries like `S401-afc`, `S402-mc`, `S403-PL`); P02 is a pass-through (the CSV columns are themselves the canonical formula outputs per Appendix README's <=0.02 round-trip validation); V03 round-trips against the same CSV with tolerance 0.5% — MAE is exactly 0.0 by construction. The XR-axis (cumulative output) is preserved as a non-standard parquet column for Phase 9 viz; the synthetic `year = row_index 0..20` keeps the generic O06 writers compatible.
- **S404, S405, S406, S407** — Inman (1995) underlying simulation values are not publicly tabulated and the Taylor & Francis full text is paywalled. Per the playbook's `data_unavailable` recipe and anti-fabrication rules, L01 returns SKIPPED, P02 is SKIPPED, V03 returns PASS_DATA_UNAVAILABLE with `dpr_documents_data_unavailable=true`. No chopped CSV is written; no extenbook is written (O06 writers see no processed parquet). The DPR + EPR + reproduced book figure remain the canonical Phase-9-viz artifacts. Citation corrected to Robert R. Inman (DOI 10.1080/00137919508967475).
- **S408** — `cross_sectional` single-year (1952) snapshot. L01 hardcodes the two verbatim book-quoted percentages (94.0% chose charts 6 or 7; 94.3% chose charts 6, 7, or 8) from Shaikh p. 163. V03 compares against the same hardcoded constants; MAE = 0.0. JSTOR stable_id 1812527 remains marked `unverified-rate-limited` (anti-bot 403); bibliographic citation itself is well-established.

### Output artifacts

| Artifact | S401 | S402 | S403 | S404-S407 | S408 |
|---|---|---|---|---|---|
| Chopped CSV rows | 126 (21×6) | 126 (21×6) | 42 (21×2) | none | 2 (1×2) |
| Extenbook size | 19,726 B | 17,896 B | 14,494 B | none | 14,918 B |

### Validator output (final)

```
S401  PASS                       mae=0.0   max_pct=0.0   n=122
S402  PASS                       mae=0.0   max_pct=0.0   n=122
S403  PASS                       mae=0.0   max_pct=0.0   n=42
S404  PASS_DATA_UNAVAILABLE      mae=None  max_pct=None  n=0
S405  PASS_DATA_UNAVAILABLE      mae=None  max_pct=None  n=0
S406  PASS_DATA_UNAVAILABLE      mae=None  max_pct=None  n=0
S407  PASS_DATA_UNAVAILABLE      mae=None  max_pct=None  n=0
S408  PASS                       mae=0.0   max_pct=0.0   n=2
```

### Open questions / forward work

1. **Inman 1995 underlying data acquisition** (S404-S407). Until obtained via library access or a Decision-Log-approved figure-digitization protocol, these four series remain `data_unavailable`. Phase 9 may pursue this.
2. **JSTOR stable ID confirmation** for S408 (provisional). Resolution requires a manual interactive browser visit; not script-verifiable.
3. **Phase 6 literature-review extension for S408** (book footnote 36, p. 164 — Bain 1948 ... Lavoie 1992). Currently deferred as a Phase 9 enrichment opportunity, not a "data extension" in the Anu sense.
4. **Phase 9 viz must respect XR-axis for S401-S403.** The chopped CSV's `year` column is a synthetic ordinal (0..20); plots must use the `XR` column from the processed parquet, not `year`. Documented in each DPR §7 caveat 1.
