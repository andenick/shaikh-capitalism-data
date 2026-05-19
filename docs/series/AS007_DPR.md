# AS007 — GPIM Variant - IRS Adjusted (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
**Status:** ingested  **Year range (book):** 1925-2011

## Definition

GPIM Variant - IRS Adjusted

## Why It Matters

Source: Appendix Table 6.8.II.4 (Great Depression / WWII correction). UNIT NORMALIZATION: raw IRS Series V 115 (KTHcorpirs) is in thousands of dollars and divided by 1000 at load time to convert to billions. AS007 has no extension (historical 1925-1947 correction only). See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| AS007-A | II4 | `KTHcorpirs` | BEA NIPA / BEA FA / IRS SOI / Census | x0.001 unit scale |
| AS007-B | II4 | `KNCcorpbeaAdj` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS007-C | II4 | `KNHcorpbeaAdj` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

KTHcorpirs = IRS book-value index (Census 1975 Series V 115) used to scale BEA 2011 current-cost stock for the Great Depression / WWII window 1925-1947. Raw IRS Series V 115 values are in THOUSANDS OF DOLLARS; loader applies scale factor 1/1000 to convert to billions before downstream use.

## Year Coverage

Book period: 1925-2011. Vintage-stable extension recipe in `AS007_EPR.md`.

## Units

billions_current_usd

## Caveats

* Raw IRS Series V 115 in thousands of dollars; loader applies scale=1/1000.

## Cross-references

(none)

## Validation Expectation

`V03_AS007_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.5% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
