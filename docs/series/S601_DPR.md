# S601 — Corporate and Non-Corporate Profit Rates (Data Provenance Record)

**Chapter:** Ch6  **Content type:** time_series  **Construction:** composite
**Status:** ingested  **Year range (book):** 1947-2011

## Definition

Corporate and Non-Corporate Profit Rates

## Why It Matters

Fig 6.1/6.4/6.5 source. Anti-degradation: extensions re-fetch NIPA T1.14/T7.11/FA T6.1 components and re-compute formula end-to-end; never splice rcorp result. Source: Appendix Tables 6.8.I.3 + 6.8.II.7. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| S601-A | I3 | `rcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S601-B | I3 | `rnoncorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S601-C | I3 | `rbus` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S601-D | II7 | `uK` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S601-E | II7 | `uFRB` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Three sectoral profit-rate series + capacity-utilization u_K / u_FRB. rcorp = (P + NMINT) / (KGC(-1) + INV(-1)) re-using AS003, AS004, AS009. Re-computed end-to-end from components; no splice on the published rate.

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `S601_EPR.md`.

## Units

decimal_rate

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

`AS003`, `AS004`, `AS009`

## Validation Expectation

`V03_S601_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
