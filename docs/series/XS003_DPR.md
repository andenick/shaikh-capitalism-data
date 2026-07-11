# XS003 — Imputed Interest Adjustment and Sectoral Profit Rates (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
***Status**: book_period_validated
## Definition

Imputed Interest Adjustment and Sectoral Profit Rates

## Why It Matters

A revision-stable resolver maps the National Income and Product Accounts (NIPA) Table 7.11 line numbers, so the construction survives BEA revisions to financial services indirectly measured (FISIM). Source: Appendix Tables 6.8.I.3 and 6.8.II.7. Used by S601, S602, S603, S604.

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

The canonical Shaikh-published values are transcribed from the published Chapter 6 appendix workbook (Shaikh 2016, Appendix 6.8). Upstream agencies are the Bureau of Economic Analysis (BEA) — NIPA and its Fixed Asset accounts (FA) — the IRS Statistics of Income (SOI), the U.S. Census Bureau (Historical Statistics 1975, for IRS book values), and the Federal Reserve Board G.17 industrial-production release (FRB G.17). All public domain.

## Construction

BankNetIntPaid = T7.11((L4+L44+L73)-(L28+L52+L91)); NFNetImpIntPaid = T7.11((L74+L75)-(L53+L54)); BusImpIntAdj = -BankNetIntPaid - NFNetImpIntPaid. Sectoral profit rates: rcorp = Pcorp/KNCcorp(-1); rnoncorp = Pnoncorp/KNCnoncorp(-1); rbus = Pbus/KNCbus(-1). All capital stocks lagged one period. The revision-stable Table 7.11 line ids are resolved by a stub-label resolver rather than by fixed line numbers.

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `XS003_EPR.md`.

## Units

Units are recorded per subseries, because a single series-level unit label would be misleading here. The seven component subseries are labelled -A through -G: XS003-A, XS003-B, XS003-C are dollar adjustments in `billions_current_usd`; XS003-D, XS003-E, XS003-F, XS003-G are profit rates in `decimal_rate`. Rendered as a two-panel chart (dollars / rates), never a single shared axis.

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

(none)

## Validation Expectation

The validation step round-trips the constructed series against the Appendix 6.8 source workbook at a 1.0% tolerance. Two data-sourcing steps needed for this construction are resolved: the FISIM remap in NIPA Table 7.11, and the 1993 BEA depreciation rates.
