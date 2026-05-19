# S710 — Figure 7.18 — US Industry IROP Deviations from Average, 1988–2005 (derivative of S706)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S710
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch7-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S710_research.json`
- Adequacy: `Technical/docs/chapters/CH7_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S710_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S710`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `SHAIKH_2008_APPENDIX_7_2_IROP`

---

## 1. Definition

**S710** is the **per-industry deviation** of the S706 profit rate from the All-Private cross-industry aggregate, year by year. Period: 1988–2005. Appears as Fig7.18 in Shaikh (2016).

## 2. Why it matters in Chapter 7

This is the **operationalization** of Shaikh's turbulent-equalization claim: industries whose profit-rate deviations cross zero are equalizing; those that stay persistently above or below are not. Per book p. 305: of the 30 industries in S706's sample, **18 cross zero** in the ROP deviations (S709) but **all 30 cross zero** in the IROP deviations (S710) — the central asymmetry that motivates the chapter's regulating-capital framework.

## 3. Sources

| Subseries | Coverage | Source | Units |
|---|---|---|---|
| **S710-A** | 1988–2005 | Derived from S706 | rate deviation (decimal; industry IROP minus All-Private aggregate IROP) |

The values are read directly from the `*_Deviation` / `*_Dev` columns of Shaikh's Appendix 7.2 xlsx (byte-exact). Construction is a one-line algebraic transform of S706's level columns.

## 4. Construction

`formula`:
```
dev_i,t = ROP_i,t − ROP_avg,t       (for S709, derived from S705)
dev_i,t = IROP_i,t − IROP_avg,t     (for S710, derived from S706)
```
where `ROP_avg` / `IROP_avg` = the **aggregate-before-ratio All-Private** baseline (per book p. 305: "defined by the overall profit rate of all included private industries"). For Phase 5 we read the `*_Deviation` columns directly from Shaikh's xlsx.

## 5. Year coverage

- **Book period**: 1988–2005
- **Extension period**: same as book period (Phase 5); follows S706 for any future extension.

## 6. Units

rate deviation (decimal; industry IROP minus All-Private aggregate IROP).

## 7. Caveats

1. **Pure algebraic derivative of S706.** Any S706 re-run automatically re-derives this series; no separate ingestion.
2. **38-panel small-multiple** in the book includes 6 sub-aggregates (Manufacturing, Manufacturing D, Manufacturing ND, Real & Rental, plus 2 others) on top of the 32 named industry columns. Phase 9 visualization should mirror the book's panel layout.
3. **All-Private baseline** in the xlsx is the aggregate ROP/IROP across the 30 retained industries (not the 32-column count which includes 2 sub-aggregates already).

## 8. Cross-references

- **Parent series**: S706
- **CD2 legacy ID**: `S037`
- **Book reference**: Shaikh (2016), Ch. 7, p. 305, Fig7.18.

## 9. Validation expectation

- **Tolerance**: ±0.5% per cell (derived content_type per playbook).
- **Expected MAE** against the xlsx `*_Deviation` columns: 0.0 (verbatim read).
