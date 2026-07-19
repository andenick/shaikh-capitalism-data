# XS006 — GPIM Variant - BEA 1993 Depreciation Rates (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
***Status**: book_period_validated
## Definition

Generalized Perpetual Inventory Method (GPIM) variant using the BEA 1993 depreciation rates.

## Why It Matters

Two sub-variants are shipped: `depr_only` matches the appendix text, and `depr_plus_init` matches the sample values from an earlier replication. Source: Shaikh (2016), Appendix Table 6.8.II.3.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| XS006-depr_only | II3 | `KNCcorpnew` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS006-depr_plus_init | II3 | `KNCbea93` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS006-dcorpnew | II3 | `dcorpnew` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The `-depr_only`, `-depr_plus_init`, and `-dcorpnew` suffixes label the individual sub-variants of this series. The canonical Shaikh-published values are transcribed from the published Chapter 6 appendix workbook (Shaikh 2016, Appendix 6.8). Upstream agencies are the Bureau of Economic Analysis (BEA) — its National Income and Product Accounts (NIPA) and Fixed Asset accounts (FA) — the IRS Statistics of Income (SOI), the U.S. Census Bureau Historical Statistics 1975 (IRS book values), and the Federal Reserve Board G.17 release. All public domain.

## Construction

Two sub-variants:
* `XS006-depr_only`: GPIM rule (eq. 6.57) with BEA 1993 depreciation rate + BEA 2011 initial value 98.1.
* `XS006-depr_plus_init`: GPIM rule with BEA 1993 depreciation rate + BEA 1993 initial value 77.769.

## Year Coverage

Book period: 1925-2011. See the companion Extension Provenance Record for the vintage-stable extension recipe.

## Units

billions_current_usd

## Caveats

* Two sub-variants shipped; see the divergence note (versus an earlier replication) in the Extension Provenance Record.

## Cross-references

(none)

## Validation Expectation

The series round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Two construction dependencies are resolved: the remapping of the NIPA Table 7.11 financial services indirectly measured (FISIM) lines, and the BEA 1993 depreciation rates.
