# S701 — Figure 7.11 — US Selling Price vs Unit Labor Cost (cross-section), 1923–1950

**Data Provenance Record (DPR)**

**Series ID**: S701
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry → `series.S701`
- Subsource registry: subsource registry → `SALTER_1969_TABLE28_US`

---

## 1. Definition

**S701** is the **cross-sectional industry scatter** that Shaikh re-plots in Fig7.11 from Salter (1969). Each point is one US industry; both axes are the ratio (1950/1923 × 100; selling price and unit labour cost). Period: 1923–1950. The source is **Salter 1969, p. 164, table 28**.

> **ERRATUM — Salter caption transposition.** The book's Fig 7.11/7.12 *captions* transpose the two Salter tables (the Fig 7.11 caption prints "Source: Salter 1969, 197, table 33"). This is a caption erratum. The authoritative mapping comes from the salvaged workbook Row-0 title ("Table 28. Changes in output per man-hour and related quantities for twenty-seven industries, United States, 1923-50 (1923 = 100)") and the book body text listing the two data sets as "(164, table 28; 197, table 33)": **US Fig 7.11 = Table 28, p.164; UK Fig 7.12 = Table 33, p.197.** Corrected 2026-07-02 (campaign DF-2); this reverses the 2026-06-11 reconciliation, which had elevated the erratum captions.

## 2. Why it matters in Chapter 7

Ch7 develops Shaikh's theory of turbulent regulation of industrial profit rates by costs of production. Fig7.11 is a foundational visual demonstration that cross-industry variation in selling-price change is closely tracked by cross-industry variation in unit-labour-cost change — Shaikh calls it a "striking relationship" (book p. 286) — grounding the classical/Marxian claim that prices of production are regulated by costs.

## 3. Sources

| Subseries | Coverage | Publisher / Reference | Native units | Retrieval |
|---|---|---|---|---|
| **S701-A** | 1923–1950 | Salter (1969) **p. 164, table 28** (US 1923-50); via SalvagedInputs Appendix7_SalterULCPriceTable**28**.xlsx (workbook Row-0 title = "Table 28 … United States, 1923-50 (1923 = 100)") | index (1923=100) — encoded per-industry as 1950-vs-1923 ratio | https://www.cambridge.org/core/search?q=Productivity+and+Technical+Change+Salter (Cambridge); local salvaged xlsx |

The adequacy review confirmed the salvaged xlsx is present locally and that the Cambridge core search URL returns HTTP 200 (the original book-detail URL returns HTTP 500 — CMS error, not 404; substitute documented in `CH7_REGISTRY_DELTA.json`).

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
3. **Underlying data is public-domain** US Census of Manufactures + BLS productivity studies (for the US panel, Salter p. 164 table 28) / UK Census of Production + Board of Trade (for the UK panel, Salter p. 197 table 33).
4. **Some industries have NaN cells** in Salter's table (a few cells missing in the original source); these are preserved as NaN, not imputed.

## 8. Cross-references

- **CD legacy ID**: `S030`
- **Book reference**: Shaikh (2016), Ch. 7, pp. 286–287 (Fig7.11); Appendix 7.1 (book p. 856, PDF p. 894).
- **Knowledge Base**: figure-linkage reference → `Fig7.11`.

## 9. Validation expectation

- **Tolerance**: ±0.5% per cell (cross_sectional content_type per playbook).
- **Expected MAE** against the salvaged xlsx: 0.0 (we read the xlsx verbatim).

## Notation (plain-language key)

- **Cross-sectional** — a point-in-time comparison across industries (here one observation per industry over a fixed span), with no annual time axis; this is why no time-extension applies.
- **Subseries (S701-A)** — the single data line within series S701 (one row per industry, carrying the selling-price and unit-labour-cost ratios).
- **Unit labour cost** — labour cost per unit of output.
- **NAICS / SIC07** — modern industry-classification code schemes (US NAICS / UK SIC 2007) that do not map cleanly onto Salter's 1920s–1960s industry categories.
- **BLS / ONS** — US Bureau of Labor Statistics / UK Office for National Statistics.
- **L01 / V03** — the load and validate scripts that build and check the series.
- **CD2** — the predecessor build of this dataset (legacy ID S030).
- **Phase 4 / Phase 5** — Anu pipeline stages: the readiness (adequacy) review / ingestion.
