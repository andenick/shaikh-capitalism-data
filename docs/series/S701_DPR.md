# S701 — Figure 7.11 — US Selling Price vs Unit Labor Cost (cross-section), 1923–1950

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S701
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch7-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S701_research.json`
- Adequacy: `Technical/docs/chapters/CH7_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S701_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S701`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `SALTER_1969_TABLE28_US`

---

## 1. Definition

**S701** is the **cross-sectional industry scatter** that Shaikh re-plots in Fig7.11 from Salter (1969). Each point is one industry; both axes are the ratio (1950/1923 × 100; selling price and unit labour cost). Period: 1923–1950.

## 2. Why it matters in Chapter 7

Ch7 develops Shaikh's theory of turbulent regulation of industrial profit rates by costs of production. Fig7.11 is a foundational visual demonstration that cross-industry variation in selling-price change is well explained by cross-industry variation in unit-labour-cost change (R² ≈ 0.77 per book p. 286), grounding the classical/Marxian claim that prices of production are regulated by costs.

## 3. Sources

| Subseries | Coverage | Publisher / Reference | Native units | Retrieval |
|---|---|---|---|---|
| **S701-A** | 1923–1950 | Salter (1969) Table 28 (US 1923-50), via SalvagedInputs Appendix7_SalterULCPriceTable28.xlsx | index (1923=100) — encoded per-industry as 1950-vs-1923 ratio | https://www.cambridge.org/core/search?q=Productivity+and+Technical+Change+Salter (Cambridge); local salvaged xlsx |

The Phase 4 adequacy review confirmed the salvaged xlsx is present locally and that the Cambridge core search URL returns HTTP 200 (the original book-detail URL returns HTTP 500 — CMS error, not 404; substitute documented in `CH7_REGISTRY_DELTA.json`).

## 4. Construction

`direct`: read the salvaged xlsx, parse one row per industry, emit one row per industry-axis (selling price ratio and unit labour cost ratio).

## 5. Year coverage

- **Book period**: 1923 and 1950 (cross-sectional, two-period snapshot)
- **Extension period**: not applicable (cross_sectional — Salter's industry schema is not reconstructable from modern NAICS/SIC07; see EPR)

## 6. Units

ratio (1950/1923 × 100; selling price and unit labour cost).

## 7. Caveats

1. **Cross-sectional, not time series.** No annual interior values exist; the figure plots one observation per industry, computed from Salter's two-period tables.
2. **Salter (1969) is copyrighted Cambridge UP.** Reproduction is academic fair use; Shaikh's own re-plot in the book establishes precedent.
3. **Underlying data is public-domain** US Census of Manufactures + BLS productivity studies (for the US Table 28) / UK Census of Production + Board of Trade (for the UK Table 33).
4. **Some industries have NaN cells** in Salter's table (a few cells missing in the original source); these are preserved as NaN, not imputed.

## 8. Cross-references

- **CD legacy ID**: `S030`
- **Book reference**: Shaikh (2016), Ch. 7, pp. 286–287 (Fig7.11); Appendix 7.1 (book p. 856, PDF p. 894).
- **Knowledge Base**: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json` → `Fig7.11`.

## 9. Validation expectation

- **Tolerance**: ±0.5% per cell (cross_sectional content_type per playbook).
- **Expected MAE** against the salvaged xlsx: 0.0 (we read the xlsx verbatim).
