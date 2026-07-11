# XS001 — GDP/GDI Decomposition and Business NOS (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** composite
***Status**: book_period_validated
## Definition

GDP/GDI Decomposition and Business NOS

## Why It Matters

Business net operating surplus (NOS) = Aggregate NOS − households (HH) − non-profit institutions serving households (NPISH) − general government (GenGov) − government enterprises (GovEnterp). Source: Appendix Table 6.8.I.1. Used by XS003 and S602.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| XS001-A | I1 | `NOSbusnipa` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS001-B | I1 | `Aggregate NOSnipa` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS001-C | I1 | `NOShh` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS001-D | I1 | `NOSnpish` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS001-E | I1 | `NOSgengov` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS001-F | I1 | `NOSgoventerp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from the published Chapter 6 appendix workbook (Shaikh 2016, Appendix 6.8). Upstream agencies are the Bureau of Economic Analysis (BEA) — its National Income and Product Accounts (NIPA) and Fixed Asset accounts (FA) — the IRS Statistics of Income (SOI), the U.S. Census Bureau (Historical Statistics 1975, for IRS book values), and the Federal Reserve Board G.17 industrial-production release (FRB G.17). All public domain.

## Construction

Verbatim transcription of Shaikh (2016) Appendix 6.8 columns; extension recipe in EPR re-fetches NIPA / BEA FA / IRS components.

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `XS001_EPR.md`.

## Units

billions_current_usd

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

(none)

## Validation Expectation

The validation step round-trips the constructed series against the Appendix 6.8 source workbook at a 1.0% tolerance. Two data-sourcing steps needed for this construction are resolved: the remap of financial services indirectly measured (FISIM) in NIPA Table 7.11, and the 1993 BEA depreciation rates.
