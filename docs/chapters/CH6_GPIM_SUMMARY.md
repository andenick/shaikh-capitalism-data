# Chapter 6 — GPIM Construction Internals (AS001-AS009)

**Status**: Phase 3 draft, 2026-05-18
**Author**: opus-subagent-as-ch6
**Scope**: 9 analytical-support series documenting Shaikh (2016, ch. 6) profit-rate construction pipeline
**Decision reference**: `Technical/docs/decisions/0002_ch6_gpim_variants_disposition.md`

## What This Chapter Documents

Shaikh's Chapter 6 ("Capital and Profit") concludes with empirical measurement of the US corporate profit rate. The pipeline is non-trivial: NIPA aggregates must be decomposed, corrected for sectoral asymmetries (corporate vs noncorporate), purged of imputed banking flows, and matched against a Generalized Perpetual Inventory Method (GPIM) capital-stock measure that is itself sensitive to four methodological choices (initial value, depreciation rate, interwar adjustment, inventories).

CD2 carried these as nine separate series S206-S214. RSCD's Phase 2 algorithm marked them unmapped because none link to a Ch6 figure directly — they are construction internals, not plotted series. Decision 0002 rehomes them as AS001-AS009, preserving analytical granularity for replication.

All nine dossiers cite Appendix 6.7 ("Empirical Methods and Sources", book pp. 828-855) as the primary source narrative, plus Appendix 6.5 ("Measurement of the Capital Stock", pp. 807-821) for the GPIM accumulation equations (6.5.21-6.5.23).

## Per-Series Summary

| AS ID | CD2 | Name | What it produces | Primary source |
|---|---|---|---|---|
| AS001 | S206 | GDP/GDI Decomposition and Business NOS | Business-sector NOS = Aggregate NOS - HH - NPISH - GOV - GovEnterprise | NIPA T1.7.5, T1.10, T7.12 |
| AS002 | S207 | Wage Equivalent and Corp/Noncorp Split | WEQ2 = (sigma*PropInc - ECprop)/(1+sigma); split of proprietor income into wage equivalent and noncorporate profit | NIPA T1.13, T1.14, T6.2/T6.3, T6.7 |
| AS003 | S208 | Imputed Interest Adjustment and Sectoral Profit Rates | BusImpIntAdj from T7.11 line recipes; final rbus, rcorp, rnoncorp | NIPA T7.11, T7.12; BEA FA T6.1 |
| AS004 | S209 | GPIM Corporate Capital Stock | KNCcorp baseline (preferred): BEA 1993 depreciation + BEA 2011 initial value + interwar adjustment | BEA FA T6.1, T6.4, T6.7, T6.8 + BEA 1993 archive |
| AS005 | S210 | GPIM Variant — BEA 2011 Initial Value | Reference variant: pure GPIM with BEA 2011 init value and BEA 2011 depreciation | BEA FA T6.1 line 1, year 1925 = 98.1 |
| AS006 | S211 | GPIM Variant — BEA 1993 vs 2011 | Sensitivity: BEA 1993 finite-life depreciation in place of BEA 2011 infinite-life geometric | BEA 1993 SCB Table A.13 |
| AS007 | S212 | GPIM Variant — IRS Adjusted | Sensitivity: IRS book-value anchoring 1925-1947 (Great Depression/WWII correction) | Census 1975 Series V 115 (IRS via Historical Statistics) |
| AS008 | S213 | GPIM Variant — Interwar Adjusted | Atomic input: the multiplier ratio IRS/BEA used in AS007 | Derived from AS007 inputs |
| AS009 | S214 | IRS Corporate Inventories and Total Capital Stock | KTCcorp = KGCcorp + INVcorp (corrected total capital stock denominator) | IRS SOI Corporation Source Book + BEA FA T6.3 |

## Pipeline (data-flow diagram)

```
       NIPA T1.7.5/T1.10        NIPA T1.13/T1.14          NIPA T7.11/T7.12
              |                         |                         |
              v                         v                         v
       +-------------+         +----------------+         +----------------+
       |   AS001     |         |    AS002       |         |   AS003 inputs |
       | GDP/GDI dec |-------->| WEQ2 + split   |-------->| imputed interest|
       | Business NOS|         | PropInc -> WEQ2|         | adjustment      |
       +-------------+         +----------------+         +----------------+
                                                                  |
                                                                  v
                                                          +----------------+
                                                          |     AS003      |
                                                          | sectoral profit|
                                                          | rates rbus,    |
                                                          | rcorp, rnoncorp|
                                                          +----------------+
                                                                  |
                                                                  | + capital
                                                                  | denominator
                                                                  v
   BEA FA T6.1 (2011 init)    BEA 1993 Table A.13       Census V 115 (IRS)
        |                            |                          |
        v                            v                          v
   +-----------+               +-----------+              +-------------+
   |   AS005   |               |   AS006   |              |    AS008    |
   | reference |               | depr-rate |              | interwar    |
   | (BEA 2011)|               | variant   |              | multiplier  |
   +-----------+               +-----------+              +------+------+
                                                                 |
                                                                 v
                                                          +-------------+
                                                          |    AS007    |
                                                          | IRS-adjusted|
                                                          | KNHcorp     |
                                                          +------+------+
                                                                 |
              +-------- combined adjustments --------+           |
              v                                      v           v
                              +------------------------+
                              |      AS004 (preferred) |
                              | GPIM KNCcorp / KGCcorp |
                              +-----------+------------+
                                          |
                                          v
                                +------------------+         IRS SOI inventories
                                |    AS009         |<----------------------------+
                                | KTCcorp = KGCcorp|
                                | + INVcorp        |
                                +--------+---------+
                                         |
                                         v
                              [feeds S601-S604 Ch6 final profit rates]
```

## How AS001-AS009 feed S601-S604

Per Decision 0002, each S601-S604 dossier's `components` field is expected to reference AS series transitively. Suggested mapping (to be confirmed in Phase 4):

| S6xx (final profit-rate series) | Direct AS dependencies | Notes |
|---|---|---|
| S601 (corrected corporate profit rate) | AS003 (corrected Pcorp) / AS009 (KTCcorp denominator) | Equation 6.10: r = (P + NMINT)/(KGC_{-1} + INV_{-1}) |
| S602 (business-sector profit rate) | AS003 (rbus); AS001 (business NOS) / AS004 (KNCbus) | Per Appendix Table 6.7.4 worked example |
| S603 (noncorporate profit rate) | AS002 (Pnoncorp via WEQ2); AS003 (rnoncorp) | Tracks rcorp closely per p. 833 |
| S604 (NIPA vs corrected comparison) | AS003 + AS004 + AS009 vs official NIPA/BEA | Figures 6.2, 6.6 |

Validation reference: Appendix Table 6.7.4 (book p. 832) gives 2009 sectoral profit rates as rbus=7.7%, rcorp=7.5%, moncorp=8.1% — any S6xx implementation should reproduce these within rounding when run on 2011-vintage BEA data.

## Sensitivity Variant Summary (AS005-AS008)

The four GPIM variants are NOT alternative baselines — they are deliberate counterfactuals that each isolate ONE methodological choice. Per Appendix 6.7 Section V.5 (book p. 851), the PREFERRED final measure (AS004) combines:
- **Initial value** = BEA 2011 (98.1 bill$ in 1925) — this is AS005's anchor
- **Depreciation rates** = BEA 1993 (finite-life) — this is AS006's perturbation
- **Interwar 1925-1947** = IRS book-value adjustment — this is AS007's perturbation (or AS008's ratio applied to BEA paths)
- **Inventories** = IRS SOI scaled to NIPA — this is AS009

AS005 is the "what if we just trusted BEA 2011 entirely" baseline; AS004 is the "what Shaikh actually uses" corrected measure. Comparing AS005 vs AS004 quantifies the cumulative effect of the three corrections.

## Open Questions for Phase 4

1. **AS004 vs AS005 baseline confusion**: CD2 markdown for S210 (AS005) describes it as the reference "BEA 2011 initial value" variant, but its sample values (1925=98.1) coincide with the BEA 2011 starting point. AS004 (S209) presents itself as the preferred final measure. Phase 4 should confirm S6xx series cite AS004 as operational and reserve AS005 for sensitivity reporting.
2. **AS006 initial-value vs depreciation-variant**: CD2's S211 sample values (1925=77.769) match the BEA 1993 *initial* value (77.7), suggesting CD2 may have conflated AS006's depreciation-rate variant with an initial-value variant. Per book text p. 846, AS006 should hold the BEA 2011 initial value and only change depreciation rates. Flag for Phase 4 reconciliation.
3. **AS007 unit scale**: CD2 S212 values (1925=93,341.52) appear to be in thousands of dollars (raw IRS), not billions. Unit normalization required before any downstream use.
4. **AS009 post-2011 proxy**: Constant 2011 inventory-to-fixed-capital ratio is a documented expedient. Decide in Phase 4 whether to (a) keep with explicit visualization break, (b) re-estimate from current IRS SOI inventory data (which exists, though net capital stock no longer does), or (c) substitute FRB Z.1 nonfinancial corporate inventories.
5. **Vintage drift**: Footnote 1 of Appendix 6.7 (p. 828) states all BEA data are from 2011-vintage tables. Comprehensive revisions in 2013 and 2018 reclassified R&D and entertainment originals as fixed investment, changing CFC, NOS, and capital stock levels. Any extension must explicitly document vintage drift; do not silently splice.
6. **BEA 1993 archive recovery**: AS004 and AS006 require BEA 1993 depreciation/retirement rates that are no longer in current BEA iTable. Either recover from BEA SCB 1993 archive or anchor to Shaikh's posted spreadsheet (`SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68II3.xlsx`).
7. **FISIM methodology revisions**: NIPA Table 7.11 line numbering used in AS003's recipe (lines 4, 28, 44, 52, 53, 54, 73, 74, 75, 91) is 2011-vintage. Current vintage requires re-mapping by stub label.

## Validator Status

Run `python Technical/code/utils/_phase3_research_validator.py` — see `Technical/Build/PHASE3_VALIDATION_REPORT.json` for current pass/fail by series.
