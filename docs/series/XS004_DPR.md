# XS004 — GPIM Corporate Capital Stock (Operational Baseline) (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
***Status**: book_period_validated
## Definition

GPIM Corporate Capital Stock (Operational Baseline)

## Why It Matters

Operational baseline used by S601-S604 (combines the BEA 2011 initial value, the BEA 1993 depreciation rates, and the IRS interwar adjustment). Source: Appendix Table 6.8.II.5. This series is the operational baseline used throughout Chapter 6; its companion series XS005 is the pure Generalized Perpetual Inventory Method (GPIM) reference.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| XS004-A | II5 | `KNCcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS004-B | II5 | `KGCcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS004-C | II5 | `KNHcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from the published Chapter 6 appendix workbook (Shaikh 2016, Appendix 6.8). Upstream agencies are the Bureau of Economic Analysis (BEA) — its National Income and Product Accounts (NIPA) and Fixed Asset accounts (FA) — the IRS Statistics of Income (SOI), the U.S. Census Bureau (Historical Statistics 1975, for IRS book values), and the Federal Reserve Board G.17 industrial-production release (FRB G.17). All public domain.

## Construction

KNCcorp_baseline = GPIM (eq. 6.57): KNCnew = IGC + (1-dcorpnew)*(pKN/pKN(-1))*KNCnew(-1), with BEA 2011 initial value 98.1 (1925), BEA 1993 depreciation rate dcorpnew (from the staged 1993 BEA depreciation/retirement rates), and IRS interwar adjustment via the XS008 multiplier for 1925-1947.

## Year Coverage

Book period: 1925-2011. Vintage-stable extension recipe in `XS004_EPR.md`.

## Units

billions_current_usd

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

(none)

## Validation Expectation

The validation step round-trips the constructed series against the Appendix 6.8 source workbook at a 1.0% tolerance. Two data-sourcing steps needed for this construction are resolved: the remap of financial services indirectly measured (FISIM) in NIPA Table 7.11, and the 1993 BEA depreciation rates.
