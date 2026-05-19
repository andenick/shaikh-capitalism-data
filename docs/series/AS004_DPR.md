# AS004 — GPIM Corporate Capital Stock (Operational Baseline) (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
**Status:** ingested  **Year range (book):** 1925-2011

## Definition

GPIM Corporate Capital Stock (Operational Baseline)

## Why It Matters

Operational baseline used by S601-S604 (combines BEA 2011 initial + BEA 1993 depreciation + IRS interwar adjustment). Source: Appendix Table 6.8.II.5. Per Decision 0002 + Phase 4 Q6: AS004 is the operational baseline; AS005 is the pure reference. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| AS004-A | II5 | `KNCcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS004-B | II5 | `KGCcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS004-C | II5 | `KNHcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

KNCcorp_baseline = GPIM (eq. 6.57): KNCnew = IGC + (1-dcorpnew)*(pKN/pKN(-1))*KNCnew(-1), with BEA 2011 initial value 98.1 (1925), BEA 1993 depreciation rate dcorpnew (from `BEA_1993_FA_methodology/BEA_1993_depreciation_retirement_rates.csv`), and IRS interwar adjustment via AS008 multiplier for 1925-1947.

## Year Coverage

Book period: 1925-2011. Vintage-stable extension recipe in `AS004_EPR.md`.

## Units

billions_current_usd

## Caveats

* Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.

## Cross-references

(none)

## Validation Expectation

`V03_AS004_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
