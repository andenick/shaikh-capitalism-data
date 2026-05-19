# S216 -- Normalized Total Prices of Production Profit vs Total Unit Labor Costs, US 1972 (71 Industries)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S216
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S216_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S216_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S216`

---

## 1. Definition

Cross-sectional scatter for 71 industries from BEA 1972 benchmark I-O: x = total vertically-integrated unit labor cost (tv), y = total market prices (tpm) AND total prices of production at observed r (tp(r)). Both axes normalized so industry totals sum to 1.

In Shaikh (2016) the series appears as **Figure 2.16** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

First-pass empirical test of the Sraffian/classical claim that market prices cluster around prices of production. The strong correlation in Fig 2.16 anchors the Real Competition argument in Ch 7.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S216-A** | 1972 | BEA 1972 Use/Make + Shaikh Appendix 9 Sraffian computation (tp(r) normalized) | normalized dollars | salvaged chopped (Appendix9_1972fixed) |
| **S216-B** | 1972 | BEA 1972 Use/Make (tpm normalized) | normalized dollars | salvaged chopped (Appendix9_1972fixed) |

## 4. Construction

`formula` construction.

**Formula**: `Prices of production from Sraffian system at observed r; integrated_ULC = (I - A)^(-1) * l`


1. Read 71-industry tpm, tp(r), tv from Appendix9_1972fixed.xlsx.
2. Normalize each axis so industry totals sum to 1.
3. Emit long-form: one row per (industry, axis-series).

## 5. Year coverage

- **Book period**: 1972-1972
- **Extension period**: N/A

## 6. Units

Normalized dollars (sums of each axis match)

## 7. Caveats

1. Cross-sectional: no temporal extension. Each subsequent BEA benchmark (1977, 1982, ..., 2017) is a separate cross-section.
2. Phase 3 reclassification time_series -> cross_sectional ratified by Phase 4.
3. Tolerance 0.5% per playbook cross_sectional rule.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.16
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 0.5% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
