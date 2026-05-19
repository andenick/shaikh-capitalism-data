# AS001 — GDP/GDI Decomposition and Business NOS (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** composite
**Status:** ingested  **Year range (book):** 1947-2011

## Definition

GDP/GDI Decomposition and Business NOS

## Why It Matters

Business NOS = Aggregate NOS - HH - NPISH - GenGov - GovEnterp. Source: Appendix Table 6.8.I.1. Used by AS003 / S602. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| AS001-A | I1 | `NOSbusnipa` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS001-B | I1 | `Aggregate NOSnipa` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS001-C | I1 | `NOShh` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS001-D | I1 | `NOSnpish` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS001-E | I1 | `NOSgengov` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS001-F | I1 | `NOSgoventerp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Verbatim transcription of Shaikh (2016) Appendix 6.8 columns; extension recipe in EPR re-fetches NIPA / BEA FA / IRS components.

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `AS001_EPR.md`.

## Units

billions_current_usd

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

(none)

## Validation Expectation

`V03_AS001_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
