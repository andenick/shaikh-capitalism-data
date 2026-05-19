# Chapter 8 Research Summary - On Perfect and Imperfect Competition

**Chapter**: 8 (On Perfect and Imperfect Competition)
**Series count**: 5 (S801-S805)
**Wave**: B
**Subagent**: opus-subagent-wave-b-ch8
**Date**: 2026-05-18
**Book pages covered**: 371-377 (Section II "Empirical Evidence on Competition and Monopoly", subsections II.3-II.5)
**Appendix**: No formal Appendix 8 exists in the book (the appendix sequence skips from 7.1 directly to 9.1). Underlying numeric data is in `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_*.xlsx`, derived from the chapter narrative and the cited primary studies.

## Chapter scope

Chapter 8 is Shaikh's critical review of the structure-conduct-performance (SCP) / "administered prices" literature. Section II.3 ("Price rigidity and monopoly power") and Section II.5 ("Empirical evidence on profit rates and monopoly power") together display six figures (8.1-8.6) drawn from six external academic studies. Shaikh's argument is unified: every classical concentration-vs-profitability claim, when re-examined with appropriate data and procedures, either disappears, reverses sign, or reflects fixed-cost / entry-barrier effects rather than monopoly power. The chapter contains no original time series construction by Shaikh; all five RSCD Ch8 series are direct reproductions of others' published tables.

## Series

### S801 - Wholesale Prices in Oligopolistic and Competitive Industries, 1965-73 (figure 8.1)
Reproduction of Eichner (1973, Economic Journal, p. 1187) - two monthly/annual wholesale-price-index lines (1957-59=100) for "concentrated" vs. "competitive" industries during 1965-1973, spanning Nixon's wage-price-control Phase I and Phase II. **Construction: direct**. Shaikh uses Eichner's own chart to refute the administered-prices reading: smoother concentrated-industry prices reflect higher entry / fixed costs (Stigler 1963, 70), not monopoly power. Numeric values are NOT in the Appendix8_* chopped tables; they must be re-digitized from Eichner 1973 for full replication. **Stub name corrected** (was misnamed "US Long-Run Interest Rates and Prices" from a stale CD2 S042 Ch10 carryover).

### S802 - Percentage of Prices Increases or No Decreases during Contractions, in Relation to Concentration (figure 8.2)
Three cross-sections of US industries (binned by CR4 midpoint = 20, 50, 80) over three NBER-dated contractions: 1957-07/1958-04, 1960-01/1961-01, 1969-11/1970-11. Source: Weston, Lustgarten and Grottke (1974, AER) as tabulated in Semmler (1984, Competition, Monopoly, and Differential Profit Rates, Table 3.3, p. 95). **Construction: direct**. Numeric data (3x3 grid) digitized in `Appendix8_Semmler19843.3.xlsx`. **Classified as cross_sectional** because each contraction is its own cross-section. Shaikh's argument: the sign of the concentration-price-rigidity coefficient flips across contractions (positive, negative, neutral), contrary to the administered-prices prediction.

### S803 - Rate of Profit on Equity vs. CR8, Bain 42-Industry Sample, 1936-40 (figures 8.3 AND 8.4)
The most-discussed dataset in the chapter. Both panels are from Bain (1951, QJE, "Relation of Profit Rate to Industry Concentration"): figure 8.3 is the scatter of 42 industry-average ROEs vs. CR8 from Bain Table I (pp. 309 & 312); figure 8.4 is the decile-grouped version from Bain Table II (p. 313) using Demsetz (1973b) corrections. **Construction: composite** (two table panels jointly constitute the series; the Demsetz correction is integral). Numeric data digitized in `Appendix8_Bain42IndustryProfit.xlsx` (42 industry scatter) and `Appendix8_Bain42IndustryAggregates.xlsx` + `Appendix8_CorrectedBainData.xlsx` (deciles). Shaikh re-runs the regressions: linear fit R^2 = 0.0781; quadratic R^2 = 0.1896 with critical CR8* = 49.24; corrected grouped data R^2 = 0.033 - all weak, none supporting the Bain hypothesis. **Classified as cross_sectional**; stub name corrected (was "Interest Rates, Prices, and Equity Data" from a stale CD2 S041 Ch10 carryover).

### S804 - Rate of Profit on Assets, Concentrated vs. Unconcentrated Industries, 1939-1957 (figure 8.5)
Reproduction of Stigler (1963, NBER, Capital and Rates of Return in Manufacturing Industries, Table 17, p. 68): six time bins (1939-41, 1942-44, 1945-47, 1948-50, 1951-54, 1955-57) x two industry groups (concentrated, unconcentrated). 12 data points digitized in `Appendix8_StiglerRatesOfProfit.xlsx`. **Construction: direct**. Shaikh emphasizes that mean profit rates on assets are essentially identical across the two groups (7.1% vs. 6.9%) - concentration affects variability, not level. Treated as time_series despite unequal time-bin widths.

### S805 - Rates of Return and Concentration (CR4), 1963 and 1969 (figure 8.6)
Reproduction of Demsetz (1973b, JLE, Table 4, p. 19): six CR4 bins (10-20, 20-30, 30-40, 40-50, 50-60, 60+) x two years (1963, 1969). 12 data points digitized in `Appendix8_DemsetzRatesOfReturn.xlsx`. **Construction: direct**. Shaikh's argument: a weak positive concentration-profit relation in 1963 reverses to a weak negative one in 1969, demonstrating temporal instability - exactly what real competition predicts. **Classified as cross_sectional** (two cross-sections, not a time series).

## Cross-references

- **S803 and S805 share the Demsetz 1973b citation** (Demsetz both corrected Bain's data and supplied new 1963/1969 CR4 data). Loader for both should consume the same Demsetz 1973b source file.
- **S801 (Eichner 1973) and S804 (Stigler 1963)** both support the same Shaikh argument (concentration -> stable prices/profits, not high ones); they could be plotted together in any meta-analysis.
- **Table 8.2 (Mann 1966) and Table 8.3 (Brozen 1971)** appear in the same chapter section but are NOT assigned RSCD series IDs in this wave (they are static tables, not figures); flag for Phase 4 if table-only series IDs are introduced later.
- **Figure 7.3 (chapter 7)** uses similar concentration/profit analytics; cross-chapter linkage at Phase 5 ingestion may be useful.

## Chapter-wide issues / open questions

1. **No formal Appendix 8 in the book** - the appendix sequence jumps from 7.1 to 9.1. The `Appendix8_*.xlsx` files in ShaikhChoppedTables are the de-facto data dictionary for this chapter but are NOT a book appendix. Source-of-record for replication is the originating Bain/Stigler/Demsetz/Semmler/Eichner publication, not Shaikh.
2. **Figure 8.1 (S801) numeric data not digitized** - none of the Appendix8_* spreadsheets contain Eichner 1973 p. 1187. Phase 4 must either digitize it from the journal or obtain Eichner's underlying spreadsheet.
3. **Stub-name mismatches in S801 and S803** - both stubs inherited names from CD2 Ch10 series (S041 "Interest Rates, Prices, and Equity Data" and S042 "US Long-Run Interest Rates and Prices") that are unrelated to Ch8 figures. Names have been corrected; `predecessor_ids.cd2_id` nulled in both (the CD2 dossiers are not genuine predecessors). The crosswalk `MIGRATION/CD2_to_RSCD_crosswalk.csv` should be revisited at Phase 4 to remove the spurious mappings.
4. **No CD2 dossiers exist for any Ch8 series** - the CD2 markdown directory contains only S040-S042 and S047-S049 (Ch9/Ch10 series); none correspond to Bain, Stigler, Demsetz, or Semmler. All five Ch8 dossiers were constructed de novo.
5. **Cross_sectional vs. time_series classification** - S802, S803, S805 reclassified to `cross_sectional` (per stub field they were `time_series`); S801 and S804 remain `time_series`. Phase 4 should confirm that cross_sectional series do not need `extension_candidates`; current dossiers nonetheless supply candidates because each is "extendable" as a repeated cross-section at modern Census/IRS vintages.
6. **Underlying micro data is unavailable** - For all five series, the firm-level data underlying the industry averages (or industry-level lists per CR bin) is not in ShaikhChoppedTables. Any robustness-check extension must consult Bain 1951, Stigler 1963, Demsetz 1973b, Mann 1966, or Weston et al. 1974 directly.
7. **Extension feasibility (Phase 4 decision)** - Modern replication is possible in principle via IRS SOI Corporation Source Book + U.S. Census Bureau Concentration Ratios in Manufacturing, but SIC->NAICS concordance and changing CR4/CR8 definitions make true splicing difficult. Recommend treating Ch8 series as historical illustrations with optional modern parallels rather than as continuously updated series.

## Methodology decisions ported from CD2

- **None ported.** No CD2 dossiers exist for Bain/Stigler/Demsetz/Semmler/Eichner content. Spurious cd2_id values in stubs S801 and S803 (pointing to CD2 Ch10 dossiers) were nulled.

## Rollup paths

- Stubs: `Technical/research/S80[1-5]_research.json` (populated)
- This summary: `Technical/docs/chapters/CH8_RESEARCH_SUMMARY.md`
- Validator: `Technical/code/utils/_phase3_research_validator.py` (run after dossier completion)
- Underlying data: `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_*.xlsx` (6 files; S801 missing)

---

## Phase 5-8 Closure (2026-05-18)

Chapter 8 fanout completed. Pipeline run with default orchestrator (`run.py --series S80x`). Validator outputs captured in `Technical/VALIDATION_REPORT.json`.

| SID  | Status (V03)            | MAE | Tolerance %     | Chopped rows | Notes |
|------|-------------------------|-----|-----------------|--------------|-------|
| S801 | PASS_DATA_UNAVAILABLE   | -   | n/a             | 0 (no CSV)   | Eichner 1973 Fig 8.1 chart-only; resolved as data_unavailable. No parquet / chopped / extenbook generated, by codebase convention. |
| S802 | PASS                    | 0.0 | 0.5 (cross-sec) | 9            | Semmler 1984 Table 3.3, 3 CR4 bins x 3 contractions. |
| S803 | PASS                    | 0.0 | 0.5 (cross-sec) | 104          | Bain 1951 Table I (Fig 8.3) + Table II + Demsetz 1973b corrections (Fig 8.4); three subseries. |
| S804 | PASS                    | 0.0 | 1.0 (time-ser)  | 12           | Stigler 1963 Table 17; 6 bin-labels x 2 series (CONC, UNCONC). |
| S805 | PASS                    | 0.0 | 0.5 (cross-sec) | 12           | Demsetz 1973b Table 4; 6 CR4 bins x 2 years. |

### Artifacts produced

- DPRs / EPRs: `Technical/docs/series/S80[1-5]_{DPR,EPR}.md` (all 5)
- Loaders: `Technical/code/L01_loaders/L01_S80[1-5]_load.py` (S801 is SKIPPED — data_unavailable)
- Processors: `Technical/code/P02_processors/P02_S80[2-5]_construct.py` (S801 has none, by design)
- Validators: `Technical/code/V03_validators/V03_S80[1-5]_validate.py` (all 5)
- Validator helper: `Technical/code/V03_validators/_ch8_validator_lib.py`
- Processed parquets: `Technical/data/processed/S80[2-5].parquet`
- Chopped CSVs: `Technical/chopped/S80[2-5].csv`
- Extenbooks: `Technical/extenbooks/S80[2-5]_extenbook.xlsx`
- Registry/ledger updater: `Technical/code/utils/_ch8_register.py` (idempotent; updates `series_registry.json`, `SUBSOURCE_METADATA.json`, `ANU_LEDGER.json`)

### New SUBSOURCE_METADATA entries

`EICHNER_1973_EJ`, `SEMMLER_1984_TABLE_3_3`, `BAIN_1951_QJE`, `STIGLER_1963_TABLE_17`, `DEMSETZ_1973B_TABLE_4`.

### Minor fix made

- `Technical/code/O06_output/O06_chopped_writer.py` — extended the disambiguator list for `(year, subseries_id)` uniqueness to include the Ch8-specific extra columns: `cr4_midpoint`, `cr4_bin`, `industry`, `census_number`, `axis`, `decile_index`, `cr8_midpoint`. Required so S802/S803/S805 cross-sectional rows (multiple bins per year) pass the duplicate-row guard without rewriting the processors.

### S801 closure notes

S801 stays `data_unavailable` per the playbook (chart-only source; no underlying table; no Appendix8 chopped file; no PDF in workspace). Recovery requires either Eichner 1973 PDF + WebPlotDigitizer or BLS PPI reconstruction approved as a Phase 6 proxy. The series remains registered with `status: data_unavailable`, `data_unavailable_reason: source_only_chart_no_table`, and a ledger entry tagged `5_ingestion_blocked`.
