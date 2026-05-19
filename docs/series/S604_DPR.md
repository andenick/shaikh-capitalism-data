# S604 — Corporate Incremental Rate of Profit (IROP) (Data Provenance Record)

**Chapter:** Ch6  **Content type:** time_series  **Construction:** formula
**Status:** ingested  **Year range (book):** 1948-2011

## Definition

Corporate Incremental Rate of Profit (IROP)

## Why It Matters

Fig 6.7 source. iropcorpnipa is the canonical extended series post-2011 (iropcorp is bounded by NMINT availability). Source: Appendix Table 6.8.II.7. See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| S604-A | II7 | `iropcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S604-B | II7 | `iropcorpnipa` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Two nominal IROP lines per Fig 6.7 panel 1: iropcorp = Delta(GOS_corp_adj) / (IG_corpbea + Delta(INV_corp)); iropcorpnipa = Delta(GOS_corpnipa) / IG_corpbea. iropcorpnipa is the canonical extended series (no NMINT/INV dependency).

## Year Coverage

Book period: 1948-2011. Vintage-stable extension recipe in `S604_EPR.md`.

## Units

decimal_rate

## Caveats

* iropcorp bounded by NMINT + IRS inventory completeness; iropcorpnipa is canonical for post-2011.

## Cross-references

`AS003`, `AS004`, `AS009`

## Validation Expectation

`V03_S604_validate.py` round-trip-validates against the Appendix 6.8 source workbook at 2.0% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
