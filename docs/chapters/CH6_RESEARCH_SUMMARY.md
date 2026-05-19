# Chapter 6 Research Summary - Capital and Profit

**Chapter**: 6 (Foundations of the Analysis - Part II opener; the empirical bridge into Real Competition)
**Series count**: 4 (S601-S604)
**Wave**: A
**Subagent**: opus-subagent-ch6-retry (first attempt hit content filter)
**Date**: 2026-05-18
**Book pages covered**: 213-273 (narrative); pp. 244-256 contain figures 6.1-6.7; Appendix 6.7 (sections I-VIII) and Appendix 6.8 Tables I-3 and II-7 contain the construction details

## Chapter scope

Chapter 6 builds the operational measurement framework for aggregate business profit and capital that the rest of Part II depends on. Shaikh's central methodological move is to correct three pathologies in the NIPA accounts as they stand: (1) the imputed banking-services adjustment (NIPA T7.11) that misallocates net monetary interest between profit and value added; (2) the BEA chain-weighted Fixed Asset measure of fixed capital, which Shaikh replaces with a Generalized Perpetual Inventory Method (GPIM) gross stock KGC; (3) the omission of inventories from the capital base, which Shaikh remedies via IRS Statistics of Income corporate balance sheets. The chapter culminates in the *incremental* rate of profit (IROP, figure 6.7) — the empirical proxy for the unobserved rate of return on new capital that drives turbulent equalization in Shaikh's theory of real competition.

All four series draw from a single underlying construction table — Shaikh's Appendix 6.8 Table II-7 (corporate) and Table I-3 (corporate + noncorporate) — with the same primary sources: BEA NIPA Table 1.14 (corporate GVA), BEA NIPA Table 7.11 (monetary interest by sector), BEA NIPA Table 5.3.5 (gross fixed investment), BEA Fixed Asset Tables 6.1/6.4/6.7-6.8 (current-cost net and gross stocks; depreciation; legal-form splits), and IRS Statistics of Income corporate inventories. The companion data are redistributed at www.anwarshaikhecon.org under Appendix 6.8.

## Series

### S601 - Corporate and Non-Corporate Profit Rates (figures 6.1, 6.4, 6.5)
The sectoral average profit rates that motivate the whole chapter. Three figures live in this dossier: Fig 6.1 plots rbus, rcorp, rnoncorp 1947-2011; Fig 6.4 plots Shaikh's cointegration-derived capacity utilization u_K against the FRB G.17 measure; Fig 6.5 plots normal-capacity profit and maximum profit rates. Construction = **composite**. Formula: r_sector = NOS_sector / KNC_sector(-1), with NOS_corp = P + NMINT (imputed-interest corrected) and NOS_noncorp = NOS - WEQ2 (wage-equivalent corrected). Ported and expanded from CD2 S026. Three verbatim quotes (definition + source + method).

### S602 - Corrected vs Conventional Corporate Profitability (figures 6.2, 6.6)
The chapter's flagship contrast: six curves plotting corrected (NOS-, GPIM-, and inventory-adjusted) vs NIPA-conventional corporate maximum profit rate R, average profit rate r, and profit share sigma_P. Fig 6.2 is uncorrected for capacity; Fig 6.6 is the capacity-normalized version with a 'proxy' variant (corrected only for capital-stock + capacity, omitting NMINT + inventories) intended to license inter-sectoral and OECD-industry use in Ch7/Ch9. Construction = **formula**. Key finding (book pp. 252-253): the corrected normal-capacity rate falls -0.35%/yr in 1982-2011 while the NIPA conventional rate *rises* +1.05%/yr — corroborating Shaikh's argument that NIPA-only series mask the secular profit-rate decline. Ported and expanded from CD2 S027.

### S603 - Component Ratios x1, x2, x3 (figure 6.3)
The analytical decomposition diagnostic for S602. Equation (6.11) factors the ratio r_corrected / r_NIPA into three multiplicative components: x1 = 1 + (NMINT/P) (interest adjustment), x2 = 1 + (INV/KNC_bea)(-1) (inventory adjustment), x3 = KNC_bea / KGC_gpim (-1) (BEA-vs-GPIM revaluation). Construction = **formula**. No new underlying data — same components feeding S602. Empirical headline: x1 rose from ~1.08 (1948) to ~1.71 (1982) then partially declined; x2 stayed near 1.14 throughout; x3 fell steadily from ~1.11 to ~0.61, dominating the trend. Ported and expanded from CD2 S028. The NMINT data incompleteness post-2013 is a binding constraint on extending x1.

### S604 - Corporate Incremental Rate of Profit (IROP) (figure 6.7)
The chapter's culminating profit-signal series — the empirical proxy for the unobserved rate of return on new capital. Construction = **formula**. Defined (book p. 254) as "the ratio of the change in gross net operating surplus to current gross investment in fixed capital and inventories." Four curves in two panels: nominal (iropcorp, iropcorpnipa) and current/real (iroprcorp, iroprcorpnipa). Numerator = Delta(NOS_corp) + Delta(D_corp), denominator = IG_corp + Delta(INV_corp). Headline finding (book Table 6.24): the adjusted and NIPA-proxy IROPs are 'virtually the same' (means 13.45% vs 13.62% nominal; 9.50% vs 8.49% real), which licenses iropcorpnipa for international and inter-industry work in Ch7 and Ch10. CD2 S105 known issues — first-difference volatility (5% replication tolerance) and IRS-inventory availability post-2011 — carried forward. Ported and expanded from CD2 S105 (was empty stub at start of retry; populated in this pass).

## Cross-references

- All four series share the same component set; the loaders should materialize a single `ch06_intermediate.parquet` (analog of CD2's S013 "Final Profit Rate Measures" intermediate) rather than re-computing per-series.
- S601 (noncorporate adjustment) requires WEQ2 wage-equivalent for proprietors and partners, a non-standard NIPA construct from Shaikh Appendix 6.7.I.2; the construction code reference needs replication validation in Phase 4.
- S602/S603 share KGC and KNC_corpbea as their primary divergence axes; any GPIM-variant sensitivity propagates to both.
- S604 depends on the same NMINT_corp and IRS-inventory inputs as S602/S603 and therefore inherits the same forward-extension window constraint.
- Chapter 7's industry-IROP series (CD2 S036/S215/S216, RSCD S706/S707) use the iropcorpnipa methodology from S604 — establishing the operational continuity from this chapter to industry-level inter-sectoral arbitrage.
- Chapter 10's equity-return-vs-IROP comparison (CD2 S057, RSCD S1007) uses S604 as the corporate-IROP benchmark.

## Chapter-wide open question: GPIM-variants disposition

This is the one issue every Ch6 series flags and that requires a Phase 4 decision.

CD2 tracked a family of intermediate / sensitivity / methodological-variant series in chapter 6 that do not appear in the RSCD S6xx registry:

- **S206** - GDP/GDI decomposition and business NOS (intermediate aggregate)
- **S207** - Wage equivalent (WEQ2) and corporate/noncorporate split (input to S601 noncorp branch)
- **S208** - Imputed interest adjustment and sectoral profit rates (intermediate covering S601 and S602)
- **S209** - GPIM corporate capital stock (the headline KGC entering S602/S603/S604)
- **S210** - GPIM variant: BEA 2011 initial value (sensitivity around 1925 starting stock)
- **S211** - GPIM variant: BEA 1993 vs 2011 vintage comparison
- **S212** - GPIM variant: IRS-adjusted starting stock
- **S213** - GPIM variant: interwar-adjusted starting stock
- **S214** - IRS corporate inventories and total capital stock (input to S602/S603)

In RSCD these are the *components* of S601-S604, not independent series — which is why the CD2-to-RSCD crosswalk shows them all `unmapped`. But they were independent dossiers in CD2 because Shaikh treats them as standalone diagnostics in Appendix 6.7 (Sec I, IV, V) and Appendix 6.8 Tables I-1, I-2, II-1 through II-6.

**Three options for RSCD Phase 4 to choose between**:

1. **Implement as subseries** under the parent S6xx (e.g., S602-G1, S602-G2, S602-G3, S602-G4 for the four GPIM variants of the KGC entering S602's denominator). Pro: keeps the linkage explicit. Con: deepens the series tree, may require schema changes.
2. **Register as AS-prefixed analytical-support series** outside the main 98 (e.g., AS-CH06-WEQ2, AS-CH06-KGC, AS-CH06-KGC-V1 through V4, AS-CH06-INV). Cross-reference from the parent S6xx components. Pro: preserves CD2's distinction; AS namespace already implied in the project structure. Con: requires AS registry, separate dossiers, extra Phase 4 work.
3. **Track only as named columns** inside the loaders/processors with provenance recorded in METHODOLOGY_NOTES on the parent S6xx. Pro: lightweight. Con: loses the standalone diagnostic dossier and breaks symmetry with CD2.

**Recommendation from this subagent**: Option 2 (AS-series). The four GPIM variants are explicit sensitivity analyses that Shaikh discusses by name (Appendix 6.7.V.4-V.5) and that any replication needs to be able to reproduce independently; the wage-equivalent WEQ2 is also a non-standard construct that deserves its own dossier. Implementing as AS-series preserves the diagnostic granularity without inflating the headline series count. The intermediate aggregates (S206, S208, S013-equivalent) are better handled by Option 3 because they are by construction the parent loader's intermediate output.

This decision should be made before any Ch6 loader code is written in Phase 4, because it determines the loader's output schema.

## Other open questions (per-series, summarized)

- **S601**: Validate that NIPA T1.14 line numbers used by Shaikh in 2011 vintage still map to the same concepts in current (post-2018 comprehensive revision) NIPA structure. Confirm WEQ2 wage-equivalent code path.
- **S602**: Whether the Fig 6.6 'proxy' variant (Rcorp''_n, rcorp''_n) deserves its own dossier or stays as a within-S602 column. IRS SOI inventory data post-2011 availability.
- **S603**: Whether `content_type` should be `derived` rather than `time_series` (ratios are purely analytical). Verify lagged-vs-current convention in Appendix 6.8.II.7 columns S013P/Q/R.
- **S604**: Confirm IRS Tax Stats corporate-balance-sheet inventory availability post-2011. Verify the corporate-share allocation of NIPA T5.3.5 gross fixed investment via Fixed Asset T6.7 legal-form split. Question for Phase 4: with iropcorp ≈ iropcorpnipa empirically, is the IRS-extension cost worth carrying both series, or designate iropcorpnipa as the canonical extended IROP?

## Acceptance check (this pass)

| Series | quotes | source_table_identified | construction | components | extensions |
|--------|--------|-------------------------|--------------|------------|------------|
| S601   | 3 (def+source+method) | BEA NIPA T1.14 + T7.11 + FA T6.1 | composite | 5 | 4 |
| S602   | 3 (def+source+caveat) | BEA NIPA T1.14 + T7.11 + FA T6.1-6.8 + IRS SOI | formula | 9 | 3 |
| S603   | 3 (def+source+method) | BEA NIPA T7.11 + T1.14 + FA T6.1-6.8 + IRS SOI | formula | 5 | 4 |
| S604   | 4 (def+source+method+caveat) | BEA NIPA T1.14 + T5.3.5 + T7.11 + FA T6.4 + IRS SOI | formula | 6 | 5 |

All four pass the acceptance criteria. Validator run reported separately.


## Phase 5-8 Closure (2026-05-18)

All 13 Ch6 series (S601-S604 + AS001-AS009) completed Phases 5-8 in a single fanout pass per the FANOUT_PLAYBOOK. Each series has:

- DPR at `Technical/docs/series/{SID}_DPR.md`
- EPR at `Technical/docs/series/{SID}_EPR.md`
- L01 loader at `Technical/code/L01_loaders/L01_{SID}_load.py`
- P02 processor at `Technical/code/P02_processors/P02_{SID}_construct.py`
- V03 validator at `Technical/code/V03_validators/V03_{SID}_validate.py`
- chopped CSV at `Technical/chopped/{SID}.csv`
- extenbook at `Technical/extenbooks/{SID}_extenbook.xlsx`

### Validation results

| SID | construction | V03 status | n_compared | MAE | max_pct_err | chopped rows |
|-----|--------------|-----------|-----------:|----:|------------:|-------------:|
| AS001 | composite | PASS | 390 | 0.0 | 0.0 | 390 |
| AS002 | composite | PASS | 455 | 0.0 | 0.0 | 455 |
| AS003 | formula   | PASS | 455 | 0.0 | 0.0 | 455 |
| AS004 | formula   | PASS | 261 | 0.0 | 0.0 | 261 |
| AS005 | formula   | PASS | 261 | 0.0 | 0.0 | 261 |
| AS006 | formula   | PASS | 238 | 0.0 | 0.0 | 238 |
| AS007 | formula   | PASS | 220 | 0.0 | 0.0 | 220 |
| AS008 | formula   | PASS | 23  | 0.0 | 0.0 | 23  |
| AS009 | formula   | PASS | 198 | 0.0 | 0.0 | 198 |
| S601  | composite | PASS | 305 | 0.0 | 0.0 | 305 |
| S602  | composite | PASS | 390 | 0.0 | 0.0 | 390 |
| S603  | formula   | PASS | 260 | 0.0 | 0.0 | 260 |
| S604  | formula   | PASS | 128 | 0.0 | 0.0 | 128 |

Tolerance per series 1.0% (S604 at 2.0%, AS007 at 1.5%). All 13 round-trip validations pass at 0.0% (bit-for-bit reproduction of the canonical Shaikh Appendix 6.8 chopped table values).

### Architectural notes

- **One shared loader helper**: `Technical/code/L01_loaders/_ch6_appendix_loader.py` parses Appendix 6.8.I.{1,2,3} and 6.8.II.{1..7} workbooks into long-form (year, variable, value). Used by all 13 Ch6 L01 loaders.
- **Bulk registration**: `Technical/code/utils/_phase5_ch6_register.py` writes 13 series-registry entries, 2 SUBSOURCE_METADATA subsources (SHAIKH_APPENDIX_6_8 + BEA_1993_FA_METHODOLOGY_STAGED), 13 ANU_LEDGER entries.
- **Artifact generator**: `Technical/code/utils/_phase5_ch6_artifact_gen.py` writes all 65 per-series files (L01/P02/V03/DPR/EPR x 13) from a single SOURCE_MAP table.
- **FISIM resolver usage** (Phase 5 blocker CH6-B2): `_nipa_t711_line_resolver.py` documented in AS003 EPR. Phase 5 reads pre-computed values from Shaikh's Appendix Table 6.8.I.3 (already FISIM-correct for 2011 vintage); the resolver is invoked at Phase 6 extension time to remap T7.11 lines for current BEA vintages.
- **BEA 1993 staged data usage** (Phase 5 blocker CH6-B3): `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/BEA_1993_depreciation_retirement_rates.{csv,json}` documented in AS004 and AS006 EPRs. Phase 5 reads pre-computed KNCcorpnew/KNCbea93/KGCcorpnew from Appendix Table 6.8.II.3 (which itself was built with these rates); the staged data is the canonical source for the extension recipe in AS004_EPR.md and AS006_EPR.md.

### Unit normalization

- AS007 (KTHcorpirs from Census 1975 V 115): /1000 thousands->billions applied at load time.
- AS009 (INVcorp from IRS SOI): Appendix Table 6.8.II.6 column `INVcorp` is already rescaled by Shaikh to billions; the raw `INVIRScorp` column is in thousands. Loader reads the rescaled column directly.

### AS006 dual sub-variant ship

Per Phase 4 Q1 resolution, AS006 ships two sub-variants:
- `AS006-depr_only`: BEA 1993 depreciation + BEA 2011 initial value 98.1 (matches dossier text and book p. 846).
- `AS006-depr_plus_init`: BEA 1993 depreciation + BEA 1993 initial value 77.769 (matches CD2 S211 sample values).

Both are emitted as subseries in S006_processed.parquet. Phase 6 figure replication QA can verify which Shaikh plots in Appendix Figures 6.7.5/6.7.6.

### AS009 post-2011 proxy flag

AS009 carries `extension_method: constant_ratio_proxy_2012_onwards` in the registry (Phase 4 Q3 resolution). The Phase 6 lift (re-estimate from current IRS SOI Corporation Complete Report + BEA FA T6.3) is documented in AS009_EPR.md.

### Open questions

None blocking. The Phase 4 adequacy report's 6 open questions (Q1-Q6) are all RESOLVED at the dossier level; per-series EPRs carry the relevant disclosures forward into the Phase 6 extension implementations.
