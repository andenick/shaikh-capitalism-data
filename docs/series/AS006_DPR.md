# AS006 — GPIM Variant - BEA 1993 Depreciation Rates (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
**Status:** ingested  **Year range (book):** 1925-2011

## Definition

GPIM Variant - BEA 1993 Depreciation Rates

## Why It Matters

Per Phase 4 Q1: two sub-variants shipped. depr_only matches dossier text; depr_plus_init matches CD2 sample values. Source: Appendix Table 6.8.II.3. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| AS006-depr_only | II3 | `KNCcorpnew` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS006-depr_plus_init | II3 | `KNCbea93` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| AS006-dcorpnew | II3 | `dcorpnew` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Two sub-variants per Phase 4 Q1:
* `AS006-depr_only`: GPIM rule (eq. 6.57) with BEA 1993 depreciation rate + BEA 2011 initial value 98.1.
* `AS006-depr_plus_init`: GPIM rule with BEA 1993 depreciation rate + BEA 1993 initial value 77.769.

## Year Coverage

Book period: 1925-2011. Vintage-stable extension recipe in `AS006_EPR.md`.

## Units

billions_current_usd

## Caveats

* Two sub-variants shipped per Phase 4 Q1 — see CD2 Divergence in EPR.

## Cross-references

(none)

## Validation Expectation

`V03_AS006_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
