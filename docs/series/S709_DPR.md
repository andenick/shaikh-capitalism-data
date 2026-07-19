# S709 — Figure 7.16 — US Industry ROP Deviations from Average, 1987–2005 (derivative of S705)

**Data Provenance Record (DPR)**

**Series ID**: S709
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry → `series.S709`
- Subsource registry: subsource registry → `SHAIKH_2008_APPENDIX_7_2_ROP`

---

## 1. Definition

**S709** is the **per-industry deviation** of the S705 profit rate from the All-Private cross-industry aggregate, year by year. Period: 1987–2005. Appears as Fig7.16 in Shaikh (2016).

## 2. Why it matters in Chapter 7

This is the **operationalization** of Shaikh's turbulent-equalization claim: industries whose profit-rate deviations cross zero are equalizing; those that stay persistently above or below are not.

The book's prose on p. 305 states: "Of the **thirty** industries in this sample, **eighteen** display this tendency, while twelve do not (seven remain persistently above and five persistently below)." Book Appendix B arithmetic (61 original industries minus 31 excluded = **30 retained**) is internally consistent with the prose.

**However, Shaikh's own source data file** `Appendix7_ropdataUSind.xlsx` (the basis for this replicated series) contains **31 industry columns** (plus an 'All Private' aggregate), not 30. When the deviation formula is applied to those 31 columns, the zero-crossing count is **17** (not 18). RSCD faithfully reproduces Shaikh's source xlsx column-for-column, so the shipped S709 carries **31 industries with 17 zero-crossers** — an exact match to Shaikh's own published data file.

This is an **upstream book-prose-vs-data-file discrepancy**, not an RSCD construction defect. The book's prose (and its Appendix B arithmetic) says 30, but Shaikh's own spreadsheet — the primary artifact — has 31. The extra industry cannot be definitively identified without a printed 30-name roster, which the book's chapter 7 prose does not provide. RSCD treats the source xlsx as authoritative. Evidence: internal source record (T1.1 final resolution, 2026-07-17).

The central qualitative claim — that incremental-rate (IROP) deviations cross zero for all industries (S710) while average-rate (ROP) deviations do not (S709) — holds under either count.

## 3. Sources

| Subseries | Coverage | Source | Units |
|---|---|---|---|
| **S709-A** (subseries — one data line within S709) | 1987–2005 | Derived from S705 | rate deviation (decimal; industry ROP minus All-Private aggregate ROP) |

The values are read directly from the `*_Deviation` / `*_Dev` columns of Shaikh's Appendix 7.2 xlsx (byte-exact). Construction is a one-line algebraic transform of S705's level columns.

## 4. Construction

`formula`:
```
dev_i,t = ROP_i,t − ROP_avg,t       (for S709, derived from S705)
dev_i,t = IROP_i,t − IROP_avg,t     (for S710, derived from S706)
```
where `ROP_avg` / `IROP_avg` = the **aggregate-before-ratio All-Private** baseline (per book p. 305: "defined by the overall profit rate of all included private industries"). For Phase 5 we read the `*_Deviation` columns directly from Shaikh's xlsx.

## 5. Year coverage

- **Book period**: 1987–2005
- **Extension period**: same as book period (Phase 5); follows S705 for any future extension.

## 6. Units

rate deviation (decimal; industry ROP minus All-Private aggregate ROP).

## 7. Caveats

1. **Pure algebraic derivative of S705.** Any S705 re-run automatically re-derives this series; no separate ingestion.
2. **38-panel small-multiple** in the book includes 6 sub-aggregates (Manufacturing, Manufacturing D, Manufacturing ND, Real & Rental, plus 2 others) on top of the 32 named industry columns. Phase 9 visualization should mirror the book's panel layout.
3. **31-vs-30 industry count (upstream discrepancy, T1.1 RESOLVED, 2026-07-17).** The book's prose (p. 305) and Appendix B arithmetic say 30 industries / 18 zero-crossers. Shaikh's own source xlsx `Appendix7_ropdataUSind.xlsx` contains 31 industry columns, producing 17 zero-crossers. RSCD faithfully reproduces the source xlsx column-for-column — see §2 for the full explanation and internal source record for the T1.1 adversarial verification. No RSCD data change; the source xlsx is authoritative.

## 8. Cross-references

- **Parent series**: S705
- **CD2 legacy ID** (identifier in CD2, the predecessor build of this dataset): `S035`
- **Book reference**: Shaikh (2016), Ch. 7, p. 305, Fig7.16.

## Notation (plain-language key)

Short forms used above, in plain language (this record is a downloadable external artifact):

- **S### / -A** — series identifiers in this project (e.g. S709); a trailing letter (e.g. S709-A) marks a *subseries* — one data line within that series.
- **DPR / EPR** — Data Provenance Record (this file) / Extension Provenance Record (its companion).
- **Phase N** — Anu Framework pipeline stages: Phase 5 = ingestion, Phase 6 = extension, Phase 9 = visualization.
- **CD2** — the predecessor build of this dataset.
- **ROP** — (average) rate of profit.
- **IROP** — incremental rate of profit: the return on newly added capital (the year-to-year change in profit divided by the new investment that produced it).
- **MAE** — mean absolute error.

## 9. Validation expectation

- **Tolerance**: ±0.5% per cell (derived content_type per playbook).
- **Expected MAE** against the xlsx `*_Deviation` columns: 0.0 (verbatim read).
