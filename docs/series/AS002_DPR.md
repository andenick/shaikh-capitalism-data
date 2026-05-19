# AS002 — Wage Equivalent and Corp/Noncorp Split (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** composite
**Status:** ingested  **Year range (book):** 1947-2011

## Definition

Wage Equivalent and Corp/Noncorp Split

## Why It Matters

WEQ2 = (sigma*PropInc - ECprop)/(1+sigma). Source: Appendix Table 6.8.I.2. Used by AS003 / S603. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| AS002-A | I2 | `PropInc` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS002-B | I2 | `ECprop` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS002-C | I2 | `WEQ2` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS002-D | I2 | `WEQ1` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS002-E | I2 | `Pnoncorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS002-F | I2 | `Pcorpnipa` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS002-G | I2 | `s` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Verbatim transcription of Shaikh (2016) Appendix 6.8 columns; extension recipe in EPR re-fetches NIPA / BEA FA / IRS components.

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `AS002_EPR.md`.

## Units

billions_current_usd

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

(none)

## Validation Expectation

`V03_AS002_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
