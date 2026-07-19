# S601 — Corporate and Non-Corporate Profit Rates (Data Provenance Record)

**Chapter:** Ch6  **Content type:** time_series  **Construction:** composite
***Status**: book_period_validated
## Definition

Corporate and Non-Corporate Profit Rates

## Why It Matters

Source figures: Fig 6.1 / 6.4 / 6.5. The shipped book-period values are transcribed verbatim from Shaikh's published Appendix 6.8 (sub-tables I.3 and II.7). The anti-degradation *extension* recipe — re-fetching the underlying US national-accounts components (BEA National Income and Product Accounts tables 1.14 / 7.11 and Fixed Asset table 6.1) and re-computing the formula end-to-end rather than splicing the published rate — is the designed forward method; live re-computation is deferred to the roadmap (Decision 0015) and is not yet wired into this package. See `CH6_GPIM_SUMMARY.md` for the full Chapter 6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| S601-A | I3 | `rcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S601-B | I3 | `rnoncorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S601-C | I3 | `rbus` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S601-D | II7 | `uK` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S601-E | II7 | `uFRB` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from book appendix source table*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Three sectoral profit-rate lines plus two capacity-utilization lines (Shaikh's own estimate u_K and the Federal Reserve's u_FRB). The corporate rate is rcorp = (P + NMINT) / (KGC[t-1] + INV[t-1]) — profit plus net monetary interest (NMINT) over the prior year's capital stock. The linked components XS003 / XS004 / XS009 (appendix "extra series" holding the GPIM capital-stock and surplus internals) are recorded here as **documentary lineage** per Decision 0015: they disclose the construction chain Shaikh followed, not a live computation wired into this package. For the book period the published rate is transcribed verbatim from Appendix 6.8; no splice is performed.

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `S601_EPR.md`.

## Units

decimal_rate

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

`XS003`, `XS004`, `XS009`

## Validation Expectation

`V03_S601` (the validate script) round-trip-checks the built series against the Appendix 6.8 source workbook at 1.0% tolerance. Per the readiness (adequacy) review (`CH6_ADEQUACY_REPORT.json`), the two ingestion blockers B2 (a National Income and Product Accounts table 7.11 FISIM re-mapping, handled by `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.

## Notation (plain-language key)

- **Subseries (S601-A, -B, …)** — the individual data lines that make up series S601; each suffix letter is one curve in the figure.
- **GPIM** — the corrected capital-stock-and-surplus construction Shaikh uses across Chapter 6 (his integrated measure of the profit rate).
- **NMINT** — net monetary interest, added back into profit to form the corrected operating surplus.
- **u_K / u_FRB** — capacity-utilization measures: Shaikh's own estimate (u_K) and the Federal Reserve's published rate (u_FRB).
- **NIPA / BEA / FA** — US National Income and Product Accounts / Bureau of Economic Analysis / its Fixed Asset accounts.
- **XS003 / XS004 / XS009** — appendix "extra series" recording GPIM construction internals; here they are documentary lineage (see Construction), not a live computation.
- **L01 / P02 / V03** — the load / process / validate scripts that build and check the series.
- **CD2** — the predecessor build of this dataset, retained for cross-checking.
