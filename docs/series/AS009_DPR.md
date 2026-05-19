# AS009 — IRS Corporate Inventories and Total Capital Stock (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
**Status:** ingested  **Year range (book):** 1946-2011

## Definition

IRS Corporate Inventories and Total Capital Stock

## Why It Matters

Source: Appendix Table 6.8.II.6. UNIT NORMALIZATION: raw IRS SOI INVIRScorp is in thousands of dollars and divided by 1000 at load time. Per Phase 4 Q3: extension_method='constant_ratio_proxy_2012_onwards' flag carried through; Phase 6 lift to re-estimated ratio is recommended but deferred. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| AS009-A | II6 | `INVcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS009-B | II6 | `KGCcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS009-C | II6 | `KTCcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

INVcorp = IRS SOI corporate inventories at current cost. KTCcorp = KGCcorp (from AS004) + INVcorp. Raw IRS SOI inventory line is in THOUSANDS OF DOLLARS in the upstream IRS source; Shaikh's Appendix Table 6.8.II.6 column INVcorp is already in billions of current USD after Shaikh's rescaling. Post-2011 inventory is bounded by IRS reporting; constant-ratio proxy flagged via `extension_method: constant_ratio_proxy_2012_onwards`.

## Year Coverage

Book period: 1946-2011. Vintage-stable extension recipe in `AS009_EPR.md`.

## Units

billions_current_usd

## Caveats

* Raw IRS SOI inventories in thousands of dollars; INVcorp column in Appendix Table 6.8.II.6 is already rescaled to billions.
* Post-2011 inventory uses constant 2011 ratio proxy; flagged via `extension_method`.

## Cross-references

(none)

## Validation Expectation

`V03_AS009_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
