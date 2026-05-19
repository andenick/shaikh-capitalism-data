# AS003 — Imputed Interest Adjustment and Sectoral Profit Rates (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
**Status:** ingested  **Year range (book):** 1947-2011

## Definition

Imputed Interest Adjustment and Sectoral Profit Rates

## Why It Matters

FISIM-revision-stable T7.11 line resolver used (see _nipa_t711_line_resolver.py). Source: Appendix Tables 6.8.I.3 + 6.8.II.7. Used by S601, S602, S603, S604. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| AS003-A | I3 | `BankMonIntPaid` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS003-B | I3 | `NFNetImpIntPaid` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS003-C | I3 | `BusImpIntAdj` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS003-D | I3 | `rbus` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS003-E | I3 | `rcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS003-F | I3 | `rnoncorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS003-G | I3 | `rnoncorp1` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

BankNetIntPaid = T7.11((L4+L44+L73)-(L28+L52+L91)); NFNetImpIntPaid = T7.11((L74+L75)-(L53+L54)); BusImpIntAdj = -BankNetIntPaid - NFNetImpIntPaid. Sectoral profit rates: rcorp = Pcorp/KNCcorp(-1); rnoncorp = Pnoncorp/KNCnoncorp(-1); rbus = Pbus/KNCbus(-1). All capital stocks lagged one period. FISIM-revision-stable line ids resolved via `_nipa_t711_line_resolver.py`.

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `AS003_EPR.md`.

## Units

mixed_billions_usd_and_decimal_rates

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

(none)

## Validation Expectation

`V03_AS003_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
