# AS005 — GPIM Variant - BEA 2011 Reference (Pure GPIM Regenerator) (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
**Status:** ingested  **Year range (book):** 1925-2011

## Definition

GPIM Variant - BEA 2011 Reference (Pure GPIM Regenerator)

## Why It Matters

Pure reference regenerator; verifies 99.6% accuracy of the GPIM rule (Appendix Table 6.8.II.1). Sensitivity variant — NOT used by S601-S604. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| AS005-A | II1 | `KNCcorp'` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS005-B | II1 | `KNCcorpbea` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS005-C | II1 | `KNCcorp'ratio` | Shaikh-computed | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Pure-reference GPIM regenerator with BEA 2011 initial value AND BEA 2011 (infinite-life geometric) depreciation rate. Verifies 99.6% accuracy vs. official BEA KNCcorpbea per Appendix Table 6.8.II.1.

## Year Coverage

Book period: 1925-2011. Vintage-stable extension recipe in `AS005_EPR.md`.

## Units

billions_current_usd

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

(none)

## Validation Expectation

`V03_AS005_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
