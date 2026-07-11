# S602 — Corrected vs Conventional Corporate Profitability (Data Provenance Record)

**Chapter:** Ch6  **Content type:** time_series  **Construction:** composite
***Status**: book_period_validated
## Definition

Corrected vs Conventional Corporate Profitability

## Why It Matters

Source figures: Fig 6.2 / 6.6. The book-period values are transcribed verbatim from Shaikh's published Appendix 6.8 (sub-table II.7). See `CH6_GPIM_SUMMARY.md` for the full Chapter 6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| S602-A | II7 | `Rcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S602-B | II7 | `Rcorpnipa` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S602-C | II7 | `rcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S602-D | II7 | `rcorpnipa` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S602-E | II7 | `Profshcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S602-F | II7 | `Profshcorpnipa` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from book appendix source table*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Six lines plotted in Fig 6.2 / 6.6: corrected vs NIPA (National Income and Product Accounts) maximum rate (Rcorp vs Rcorpnipa), corrected vs NIPA average rate (rcorp vs rcorpnipa), and corrected vs NIPA profit share (Profshcorp vs Profshcorpnipa). Shaikh's eq. 6.10 is applied with the lagged total capital stock KTC[t-1] = KGC[t-1] + INV[t-1]. The linked components XS004 and XS009 (appendix "extra series" holding the GPIM capital-stock and inventory internals used in the denominators) are recorded as **documentary lineage** per Decision 0015 — they disclose the construction chain, not a live computation wired into this package; the book-period values are transcribed verbatim from Appendix 6.8.

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `S602_EPR.md`.

## Units

Units differ by subseries (per-subseries units are authoritative): the four rate lines (Rcorp, Rcorpnipa, rcorp, rcorpnipa) are profit rates expressed as decimals; the two profit-share lines (Profshcorp, Profshcorpnipa) are shares expressed as decimals.

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

`XS003`, `XS004`, `XS009`

## Validation Expectation

`V03_S602` (the validate script) round-trip-checks the built series against the Appendix 6.8 source workbook at 1.0% tolerance. Per the readiness (adequacy) review (`CH6_ADEQUACY_REPORT.json`), the two ingestion blockers B2 (a National Income and Product Accounts table 7.11 FISIM re-mapping, handled by `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.

## Notation (plain-language key)

- **Subseries (S602-A, -B, …)** — the individual data lines that make up series S602; each suffix letter is one curve in the figure.
- **GPIM** — the corrected capital-stock-and-surplus construction Shaikh uses across Chapter 6 (his integrated measure of the profit rate).
- **NIPA / BEA / FA** — US National Income and Product Accounts / Bureau of Economic Analysis / its Fixed Asset accounts.
- **XS004 / XS009** — appendix "extra series" recording GPIM construction internals; here they are documentary lineage (see Construction), not a live computation.
- **L01 / P02 / V03** — the load / process / validate scripts that build and check the series.
- **CD2** — the predecessor build of this dataset, retained for cross-checking.
