# S603 — Component Ratios x1, x2, x3 (Data Provenance Record)

**Chapter:** Ch6  **Content type:** time_series  **Construction:** formula
**Status:** ingested  **Year range (book):** 1947-2011

## Definition

Component Ratios x1, x2, x3

## Why It Matters

Fig 6.3 source. x1 freezes when NMINT_corp from T7.11 incomplete (do NOT forward-fill). Source: Appendix Table 6.8.II.7. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| S603-A | II7 | `x1` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S603-B | II7 | `x2` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S603-C | II7 | `x3` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S603-D | II7 | `x3*(x1 / x2)` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Decomposition of rcorp/rcorpnipa = (x1/x2) * x3 per eq. 6.11. x1 = 1 + NMINT/P (imputed-interest factor); x2 = 1 + INV(-1)/KNCbea(-1) (inventory factor); x3 = KNCbea(-1)/KGC(-1) (BEA vs GPIM revaluation). x1 freezes at last complete NMINT year (CD2 known issue, preserved).

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `S603_EPR.md`.

## Units

dimensionless_ratio

## Caveats

* x1 freezes at last complete NMINT_corp year; do NOT forward-fill (CD2 preserved behaviour).

## Cross-references

`AS003`, `AS004`, `AS009`

## Validation Expectation

`V03_S603_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
