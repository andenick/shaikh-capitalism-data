# Chapter 9 - Competition and Inter-Industrial Relative Prices: Research Summary

**Author**: opus-subagent-wave-b-ch9
**Date**: 2026-05-18
**Status**: draft (Wave B)
**Series in scope**: S901, S902, S903 (3 of 17 empirical figures)

## Chapter overview

Chapter 9 ("Competition and Relative Prices", book pp.376-434) is Shaikh's empirical chapter on classical price theory. Its core empirical claim is that prices of production - derived from the standard wage-profit system - are very close to direct prices (prices proportional to integrated labor times), and that market prices in turn cluster around prices of production. Three datasets carry this claim:

1. **The 1947-1998 input-output panel.** Six benchmark years (1947, 1958, 1963, 1967, 1972, 1998), each yielding a single cross-section of 65-71 industries. For 1998 the source is BEA's industry-by-industry Use table (65-order, post-redefinition); for 1947-1972 it is Ochoa (1984)'s 71-order compilation as reused in Shaikh (1998a). Real estate is excluded from the 1947-1972 tables (Ochoa) and the 1998 real estate column is corrected for owner-occupied housing imputations (NIPA 7.12 lines 133-134).
2. **Capital stock & depreciation for the fixed-capital model (1998).** BEA Fixed Asset Tables 3.1ES (current-cost net stock) and 3.4ES (depreciation), distributed across industries using the 1997 benchmark capital flow matrix under the assumption that all asset types in industry j grow at industry j's gross rate g_j.
3. **PWT 7.1 real GDP per worker.** Used as a productivity index to rescale each year's wage-share curve onto a common real-output axis (Appendix 9.2 Sec V, p.869).

Appendix 9.1 (matrix algebra, pp.861-866) and Appendix 9.2 (data and methods, pp.867-870) are the methodological backbone. The companion appendix workbooks at `SalvagedInputs/book_data/ShaikhChoppedTables/` are `Appendix9_1947fixed.xlsx` ... `Appendix9_1998Fixed.xlsx`, `Appendix9_ObservedProfitRates.xlsx`, `Appendix9_PennWorldTables.xlsx`/`Appendix9_PennWorldTables2.xlsx`, `Appendix9_pvdevexample.xlsx`, `Appendix9_ReswitchExamples.xlsx`, `Appendix9_ReswitchingPseudoProductionFunction.xlsx`.

## Per-series notes

### S901 - Market Prices vs Direct Prices, 71 Industries (Fig 9.1, 9.2, 9.16)

Cross-sectional comparison of log-normalized market prices to log-normalized direct prices in each of six benchmark years. Direct prices are d_i = mu * w_i * v_i where mu = TP/TV (sum of market prices over sum of total labor times). Four distance measures are reported per year (Table 9.9): %MAWD (Ochoa 1984), classical delta_c (Shaikh's scale-free analogue, eq. 9.13), CV, Euclidean delta_e. %MAWD and delta_c coincide in the market-vs-direct case because both use the same weighted mu.

Fig 9.16 reuses this dataset but compares market prices to **prices of production** (rather than to direct prices) in the fixed-capital model for 1947, 1972, 1998 - so it is methodologically a hybrid of the S901 data infrastructure and the S902 production-price construction.

Quotes verified verbatim against PDF pp.395-396 and Appendix 9.2 pp.867-868. Note: the PyMuPDF text dump introduces line-break hyphenation artifacts (`re- duces`, `45- degree`, `iTable/ index_industry`) which were normalized in the stored quotes; semantic verbatim is preserved, character-for-character matches against the rendered book.

### S902 - Integrated Output-Capital Ratios and Standard Prices (Fig 9.4-9.7, 9.9-9.11, 9.13-9.15, 9.18)

Two derived objects sharing the same 1998 BEA data:
(a) integrated output-capital ratios VR(r)_j as functions of r/R for each of 65 industries (Fig 9.4, 9.5 circulating; Fig 9.9, 9.11 fixed);
(b) standard prices p(r)_j / v_j as functions of r/R (Fig 9.6, 9.7 circulating; Fig 9.10 fixed).

Both objects are evaluated for r/R in [0, 1] in 1998 only. The multi-year distance summaries (Fig 9.13, 9.14 across years; Fig 9.15 production-vs-direct prices in 1947, 1972, 1998) extend the construction to the historical benchmarks via the same fixed-capital pipeline.

Quotes verified verbatim against PDF pp.406-407 (Sec VII.1) and Appendix 9.2 pp.867-869.

### S903 - Actual Wage-Profit Curves, 1947-1998 (Fig 9.8, 9.12, 9.19; plus shared figures)

Empirical wage-share curve sigma_W(r) = 1 - r/Ra(r) (Appendix 9.1 eq. 9.1.10) for each benchmark year, rescaled by PWT 7.1 real output per worker to make the curves comparable across years (book eq. 9.23). Max profit rates R_t are dominant eigenvalues of KT (Appendix 9.1; Table 9.18 reports: R_1947=1.088, R_1958=0.9734, R_1963=0.8547, R_1967=0.7644, R_1972=0.7033, R_1998=0.7317).

The stub's figure list bundles Fig 9.6, 9.7, 9.13-9.16, 9.18 with S903 because the CD2 progenitor (S049) was a catch-all wage-profit/standard-price/reswitching series. In RSCD the core S903 content is the wage-profit curves themselves (Fig 9.8, 9.12, 9.19); the rest properly belongs to S902 or S901.

Quotes verified verbatim against PDF pp.422-423 (Sec X) and Appendix 9.2 pp.868-869.

## Series count recommendation: KEEP AT 3 (with figure-list cleanup in Phase 4)

The Ch9 weakness flag in the KB coverage inventory was warranted: most Ch9 figures lack `has_axis` metadata so the Phase 2 classifier downgraded them to cross-sectional and consolidated them into a small number of composite series. After reading the chapter directly, I confirm that **three composite series is the right granularity** because the empirical engine is genuinely a single integrated computation:

- one input-output dataset (S901 substrate)
- one solve of the price-of-production eigensystem (S902 product: VR(r) and p(r)/v)
- one application of the wage-share identity (S903 product: w(r) curves)

The 17 "empirical" figures in Ch9 are largely **different views of the same computation** at different (r/R) slices, different model variants (circulating vs fixed), and different historical years. Splitting them into 17 series would multiply the dossier count without adding genuine source-distinct provenance: every figure ultimately traces to either BEA Use/Fixed Asset Tables (1998) + PWT 7.1 (productivity) or to Ochoa (1984)/Shaikh (1998a) historical IO tables (1947-1972).

That said, **the current 3-series partition has overlapping figure lists** (Fig 9.6, 9.7, 9.10, 9.13, 9.14, 9.15, 9.16, 9.18 appear in two or three of S901/S902/S903 each). Phase 4 should adjudicate a cleaner partition. My suggested mapping:

| Figure(s) | Series |
|---|---|
| 9.1, 9.2 | S901 (market vs direct, cross-section + temporal) |
| 9.3 (numerical example), 9.17 (numerical), 9.20-9.22 (theoretical) | not empirical - exclude from S9xx series entirely |
| 9.4, 9.5, 9.9, 9.11 | S902 (VR(r)_j integrated output-capital ratios) |
| 9.6, 9.7, 9.10 | S902 (standard prices p(r)/v) |
| 9.13, 9.14 | S902 (distance measures, standard-price vs labor-time) |
| 9.15 | S902 (production-vs-direct-price scatter, multi-year) |
| 9.16 | S901 (market-vs-production-price scatter, multi-year - data substrate is S901) |
| 9.18 | S902 (production-vs-direct-price time-series ratios) |
| 9.8, 9.12, 9.19 | S903 (wage-profit curves, single-year and 1947-1998 panel) |

This cleanup is **a Phase 4 adequacy task, not Phase 3**. The current 3-series count is correct; only the per-series `figures` arrays need pruning.

**Alternative not recommended (expand to N):** breaking each figure into its own series would create 14 dossiers, all citing the same 3-4 underlying sources (BEA, PWT 7.1, Ochoa 1984/Shaikh 1998a). The marginal informational value is near zero and the cross-references become combinatorial.

**Alternative not recommended (merge into 1):** the three series do have analytically distinct content (a price comparison, an eigensystem decomposition, a wage-share identity); collapsing them would lose the methodological structure that Phase 5 will need when implementing the construction code.

## Cross-references

- All three Ch9 series depend on the same BEA + Ochoa/Shaikh IO substrate. They should all reference Appendix 9.2 in their `methodology_notes`.
- S902 and S903 both depend on the eigenvalue decomposition machinery of Appendix 9.1; the maximum profit rates in Table 9.18 are shared between them.
- S901's market-vs-production-price distances (Fig 9.16, Table 9.14) are an artifact of S902's production-price calculation applied to S901's price data - so S901's open_questions notes the methodological dependency on S902.

## Open questions deferred to Phase 4

1. **Per-series figure-list cleanup** as above.
2. **PWT 7.1 -> PWT 10.01 splice** for any post-1998 wage-profit extension (S903).
3. **NAICS vs SIC industry crosswalk**: the 1947-1972 71-order tables and the 1998 65-order BEA table use different industry classifications and cannot be spliced into a single continuous panel.
4. **Capital-flow benchmark availability post-1997**: BEA stopped publishing the full asset-by-industry benchmark capital flow matrix; any post-1998 fixed-capital w-p curve replication must approximate it from BEA's detailed Fixed Asset Tables (by type x industry).
5. **Verbatim-quote PDF artifacts**: the stored quotes have been normalized to remove PyMuPDF line-break hyphenation and lost-space artifacts (`re-\nduces`, `whencomparingmarketanddirectprices`, etc.) while preserving the rendered book text character-for-character. Any future automated fuzzy-match validator should fold these whitespace normalizations into its comparison.

## Validator status

`python Technical/code/utils/_phase3_research_validator.py` -> S901, S902, S903 all PASS (verified 2026-05-18, full report at `Technical/Build/PHASE3_VALIDATION_REPORT.json`).

---

## Phase 5-8 Closure (2026-05-18, opus-fanout-wave3-ch9)

All three Ch9 series (S901-S903) authored to playbook spec and pass V03 at tolerance 0.5% with MAE 0.0% (read-the-truth-column pattern against the 14 salvaged Appendix9 workbooks). Per Phase 4 ratification, all three are `content_type: cross_sectional` with `extension_status: not_applicable_cross_sectional` (extension = adding benchmark years, deferred).

**Figure-list cleanup applied** per Phase 4 figure_mapping_full_chapter, with registry `figures` fields:
- S901: `["Fig9.1", "Fig9.2", "Fig9.16"]`
- S902: `["Fig9.4", "Fig9.5", "Fig9.6", "Fig9.7", "Fig9.9", "Fig9.10", "Fig9.11", "Fig9.13", "Fig9.14", "Fig9.15", "Fig9.18"]`
- S903: `["Fig9.8", "Fig9.12", "Fig9.19"]` (trimmed from CD2's catch-all 11-figure overflow; Fig 9.6/9.7/9.13/9.14/9.15/9.18 reassigned to S902, Fig 9.16 to S901). Zero overlap remaining; 17 empirical figures fully partitioned across 3 series; non-empirical Fig 9.3/9.17/9.20-9.22 explicitly excluded.

- **S901** (Market prices vs direct prices, cross_sectional composite): 970 chopped rows = 14 subseries (7 benchmarks × {market-norm, direct-norm}). Reads pre-computed `tpm`/`td`/`tv` columns from Appendix9_1947fixed.xlsx through Appendix9_1972fixed.xlsx (71 industries each) plus Appendix9_1998Circ.xlsx + Appendix9_1998Fixed.xlsx (65 industries each), normalizes to unit-length shares. NAICS-vs-SIC industry-classification mismatch documented as a hard limit on continuous panels. %MAWD distance measures computed per benchmark as informational diagnostic. V03 PASS at 0.5%.

- **S902** (Eigensystem standard prices + observed profit rates, cross_sectional composite): 976 chopped rows = 14 standard-price subseries + 7 R_obs scalars. Reads pre-computed `tp(r)` (standard prices) and `tv` (labor-time shares) plus `Appendix9_ObservedProfitRates.xlsx`. R_obs sanity gate confirmed: 1947=0.236, 1958=0.176, 1963=0.21, 1967=0.229, 1972=0.188, 1998=0.1258 — all match within 0.5%. Pre-computed standard-price columns trusted (per playbook static-data treatment); fresh eigenvalue decomposition of KT to verify Table 9.18 R_t values is documented as a downstream scientific-validation concern, not a v1 blocker. V03 PASS at 0.5%.

- **S903** (Wage-profit curves, cross_sectional formula): 1237 chopped rows = 14 curve subseries (wage-share + real-wage for 7 benchmarks) + 7 R_t scalars + 1 R_circ + 6 PWT productivity-index anchors. Reads pre-computed `wshr{YR}`/`wr{YR}` columns from `Appendix9_PennWorldTables2.xlsx`. **PWT 7.1 variable confirmed as `rgdpwok`** (Real GDP per worker, chain-weighted) per `Appendix9_PennWorldTables.xlsx`, disambiguating the truncated "Real" reference in Appendix 9.2 p.869. **R_fixed sanity gate** confirmed: [1.088, 0.9734, 0.8547, 0.7644, 0.7033, 0.7317] match Table 9.18 exactly. PWT 7.1 → PWT 10.01 growth-rate splice strategy documented in EPR §3 with No-Lazy-Splices enforcement (productivity multiplier applies to freshly-derived σW(r), never to a re-scaled wr(r)). V03 PASS at 0.5%.

**Ch9 outcomes**: 3/3 PASS at 0.5% tolerance, MAE 0.0% throughout. All 14 `Appendix9_*.xlsx` files confirmed and integrated. Legacy BEA iTable URL → `https://www.bea.gov/industry/input-output-accounts-data` substitution applied via Phase 4 delta merger; Fixed Asset Tables URL also added for S902/S903. Total chopped rows: 970/976/1237 = 3183. Extenbooks materialized for all three.

Open questions:
1. Fresh eigenvalue solve of KT = K·(I-(A+D))^-1 against Table 9.18 R_t values is the canonical scientific-validation target — deferred to a Phase 9-style replication skill that doesn't block ingestion.
2. OOH (NIPA T7.12 lines 133-134) correction is applied **upstream** by Shaikh in the Appendix9_1998*.xlsx workbooks; v1 reads the corrected values rather than re-applying. A v2 that fetches raw BEA Use Tables would need to re-derive the correction explicitly.
3. Capital flow benchmark matrix gap post-1997 is a structural obstacle to any post-1998 fixed-capital benchmark extension; documented for future v2.
