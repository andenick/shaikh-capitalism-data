# XS005 — GPIM Variant - BEA 2011 Reference (Pure GPIM Regenerator) (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
***Status**: book_period_validated
## Definition

GPIM Variant - BEA 2011 Reference (Pure GPIM Regenerator)

## Why It Matters

Pure reference regenerator; verifies 99.6% accuracy of the Generalized Perpetual Inventory Method (GPIM) rule (Appendix Table 6.8.II.1). Sensitivity variant — NOT used by S601-S604.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| XS005-A | II1 | `KNCcorp'` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS005-B | II1 | `KNCcorpbea` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS005-C | II1 | `KNCcorp'ratio` | Shaikh-computed | identity |

The canonical Shaikh-published values are transcribed from the published Chapter 6 appendix workbook (Shaikh 2016, Appendix 6.8). Upstream agencies are the Bureau of Economic Analysis (BEA) — its National Income and Product Accounts (NIPA) and Fixed Asset accounts (FA) — the IRS Statistics of Income (SOI), the U.S. Census Bureau (Historical Statistics 1975, for IRS book values), and the Federal Reserve Board G.17 industrial-production release (FRB G.17). All public domain.

## Construction

Pure-reference GPIM regenerator with BEA 2011 initial value AND BEA 2011 (infinite-life geometric) depreciation rate. Verifies 99.6% accuracy vs. official BEA KNCcorpbea per Appendix Table 6.8.II.1.

## Year Coverage

Book period: 1925-2011. Vintage-stable extension recipe in `XS005_EPR.md`.

## Units

billions_current_usd

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

(none)

## Validation Expectation

The validation step round-trips the constructed series against the Appendix 6.8 source workbook at a 1.0% tolerance. Two data-sourcing steps needed for this construction are resolved: the remap of financial services indirectly measured (FISIM) in NIPA Table 7.11, and the 1993 BEA depreciation rates.
