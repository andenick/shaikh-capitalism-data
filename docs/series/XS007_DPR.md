# XS007 — GPIM Variant - IRS Adjusted (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
***Status**: book_period_validated
## Definition

Generalized Perpetual Inventory Method (GPIM) variant, IRS-adjusted.

## Why It Matters

Source: Shaikh (2016), Appendix Table 6.8.II.4 (Great Depression / WWII correction). Unit normalization: the raw IRS Series V 115 values (`KTHcorpirs`) are in thousands of dollars and are divided by 1000 at load time to convert to billions. XS007 has no extension (historical 1925-1947 correction only).

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| XS007-A | II4 | `KTHcorpirs` | BEA NIPA / BEA FA / IRS SOI / Census | x0.001 unit scale |
| XS007-B | II4 | `KNCcorpbeaAdj` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS007-C | II4 | `KNHcorpbeaAdj` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The `-A`, `-B`, and `-C` suffixes label the individual sub-variants of this series. The canonical Shaikh-published values are transcribed from the published Chapter 6 appendix workbook (Shaikh 2016, Appendix 6.8). Upstream agencies are the Bureau of Economic Analysis (BEA) — its National Income and Product Accounts (NIPA) and Fixed Asset accounts (FA) — the IRS Statistics of Income (SOI), the U.S. Census Bureau Historical Statistics 1975 (IRS book values), and the Federal Reserve Board G.17 release. All public domain.

## Construction

KTHcorpirs = IRS book-value index (Census 1975 Series V 115) used to scale BEA 2011 current-cost stock for the Great Depression / WWII window 1925-1947. Raw IRS Series V 115 values are in THOUSANDS OF DOLLARS; loader applies scale factor 1/1000 to convert to billions before downstream use.

## Year Coverage

Book period: 1925-2011. See the companion Extension Provenance Record for the vintage-stable extension recipe.

## Units

billions_current_usd

## Caveats

* Raw IRS Series V 115 in thousands of dollars; loader applies scale=1/1000.

## Cross-references

(none)

## Validation Expectation

The series round-trip-validates against the Appendix 6.8 source workbook at 1.5% tolerance. Two construction dependencies are resolved: the remapping of the NIPA Table 7.11 financial services indirectly measured (FISIM) lines, and the BEA 1993 depreciation rates.
