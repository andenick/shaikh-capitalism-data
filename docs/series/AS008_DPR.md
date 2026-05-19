# AS008 — GPIM Variant - Interwar Adjustment Multiplier (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
**Status:** ingested  **Year range (book):** 1925-1947

## Definition

GPIM Variant - Interwar Adjustment Multiplier

## Why It Matters

Source: Appendix Table 6.8.II.5 column 'Adj. Ratio'. Intrinsically 1925-1947 only — feeds AS007/AS004 historical correction. No extension by construction. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| AS008-A | II5 | `Adj. Ratio` | Shaikh-computed | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

AS008 = IRS index / BEA 2011 historical-cost index, normalized so 1925 = 1.0. Intrinsically 1925-1947 only — feeds AS007/AS004 historical correction.

## Year Coverage

Book period: 1925-1947. Vintage-stable extension recipe in `AS008_EPR.md`.

## Units

dimensionless_ratio_1925eq1

## Caveats

* Intrinsic year range 1925-1947 only; not an extendable series.

## Cross-references

(none)

## Validation Expectation

`V03_AS008_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
