# XS008 — GPIM Variant - Interwar Adjustment Multiplier (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
***Status**: book_period_validated
## Definition

Generalized Perpetual Inventory Method (GPIM) variant, the interwar adjustment multiplier.

## Why It Matters

Source: Shaikh (2016), Appendix Table 6.8.II.5, column 'Adj. Ratio'. Intrinsically 1925-1947 only — it feeds the XS007/XS004 historical correction. No extension by construction.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| XS008-A | II5 | `Adj. Ratio` | Shaikh-computed | identity |

The `-A` suffix labels the single sub-variant of this series. The canonical Shaikh-published values are transcribed from the published Chapter 6 appendix workbook (Shaikh 2016, Appendix 6.8). Upstream agencies are the Bureau of Economic Analysis (BEA) — its National Income and Product Accounts (NIPA) and Fixed Asset accounts (FA) — the IRS Statistics of Income (SOI), the U.S. Census Bureau Historical Statistics 1975 (IRS book values), and the Federal Reserve Board G.17 release. All public domain.

## Construction

XS008 = IRS index / BEA 2011 historical-cost index, normalized so 1925 = 1.0. Intrinsically 1925-1947 only — feeds XS007/XS004 historical correction.

## Year Coverage

Book period: 1925-1947. See the companion Extension Provenance Record for details.

## Units

dimensionless_ratio_1925eq1

## Caveats

* Intrinsic year range 1925-1947 only; not an extendable series.

## Cross-references

(none)

## Validation Expectation

The series round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Two construction dependencies are resolved: the remapping of the NIPA Table 7.11 financial services indirectly measured (FISIM) lines, and the BEA 1993 depreciation rates.
