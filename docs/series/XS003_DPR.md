# XS003 — Imputed Interest Adjustment and Sectoral Profit Rates (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
***Status**: book_period_validated
## Definition

Imputed Interest Adjustment and Sectoral Profit Rates

## Why It Matters

FISIM-revision-stable T7.11 line resolver used (see _nipa_t711_line_resolver.py). Source: Appendix Tables 6.8.I.3 + 6.8.II.7. Used by S601, S602, S603, S604. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| XS003-A | I3 | `BankNetIntPaid` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS003-B | I3 | `NFNetImpIntPaid` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS003-C | I3 | `BusImpIntAdj` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS003-D | I3 | `rbus` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS003-E | I3 | `rcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS003-F | I3 | `rnoncorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS003-G | I3 | `rnoncorp1` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

BankNetIntPaid = T7.11((L4+L44+L73)-(L28+L52+L91)); NFNetImpIntPaid = T7.11((L74+L75)-(L53+L54)); BusImpIntAdj = -BankNetIntPaid - NFNetImpIntPaid. Sectoral profit rates: rcorp = Pcorp/KNCcorp(-1); rnoncorp = Pnoncorp/KNCnoncorp(-1); rbus = Pbus/KNCbus(-1). All capital stocks lagged one period. FISIM-revision-stable line ids resolved via `_nipa_t711_line_resolver.py`.

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `XS003_EPR.md`.

## Units

Per-subseries (the banned `mixed_*` series-level string is removed via the triage patch). XS003-A, XS003-B, XS003-C are dollar adjustments in `billions_current_usd`; XS003-D, XS003-E, XS003-F, XS003-G are profit rates in `decimal_rate`. Rendered as a two-panel chart (dollars / rates), never a single shared axis.

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

(none)

## Validation Expectation

`V03_XS003_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
