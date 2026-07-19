# Chapter 10 Research Summary - Competition, Finance, and Interest Rates

**Chapter**: 10 (Competition, Finance, and Interest Rates)
**Series count**: 8 (S1001-S1008)
**Wave**: B
**Subagent**: opus-subagent-wave-b-ch10
**Date**: 2026-05-18
**Book pages covered**: 462-474 (figure-bearing pages); 873-874 (Appendix 10.1 Sources and Methods)
**Underlying data**: `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix10_*.xlsx` (4 workbooks: Documentation, Ibbotson, IntroPPrice, USLR)
**Companion online file**: Shaikh's "Appendix 10.2. Data Tables for Chapter 10" available at http://www.anwarshaikhecon.org/

## Chapter scope

Chapter 10 is Shaikh's classical theory of interest, bond yields, equity returns and stock prices. The empirical agenda is to show that (a) bank loan rates and corporate bond yields are equalized to each other and to the price level (Gibson's law), not to a constant real rate (anti-Fisher); (b) equity returns are equalized to the corporate incremental rate of profit, not to a constant discount rate (anti-EMH/Shiller); and (c) the "warranted" stock price computed from the classical model tracks the actual real price far better than Shiller's "rational" price does. The eight RSCD series span 1857-2011 at annual frequency and rely on a tightly-knit set of public primary sources (NBER Macrohistory, Federal Reserve H.15/HS-39, BLS PPI, Jastram 1977 WPI, Shiller annual S&P file, Ibbotson SBBI 2004) plus derivatives of Ch6/Ch7 IROP outputs.

## Series

### S1001 - Bank vs Private Industry IROP, 1988-2005 (figures 10.1, 10.2)
Banking-industry IROP extracted from the Ch7 Appendix 7.2 industry panel and compared to the all-private cross-industry average. **Construction: composite** (extraction + cross-sectional average). Per Appendix 10.1 verbatim: "Incremental rates of profit for banking and for all private industry were previously derived in appendix 7.2." Modern extension via BEA Industry Economic Accounts (GDP-by-industry) is possible but requires re-deriving Shaikh's appendix-7.2 corrected capital stock; banking subsector mapping under NAICS (52 Finance & Insurance vs. narrower 5221 Depository) is an open question.

### S1002 - Interest Rate and Price Level, 1857-2011 (figures 10.3, 10.6)
The chapter's load-bearing long-run macro series. Two components: composite long bond yield (Macaulay railroad bond 1857-1937 + Fed HS-39 Aaa 1936-2010, spliced via 1919-1937 mean ratio + ERP 2012 for 2003-2010), and composite PPI (Jastram 1977 Table 7 1857-1976 + BLS PPI growth-rates 1977-2011). **Construction: composite**. Fig 10.6 plots both on log scale, 1947=base. Fig 10.3 (short rates) is bundled here since the underlying long-yield series is the same; open question for Phase 4 whether to split. Modern extension: FRED `AAA` and `PPIACO` give clean splices.

### S1003 - Relative Price of Finance, 1857-2011 (figures 10.3, 10.7)
i/p ratio, both indexed to 1947=1. **Construction: formula** - pure transformation of S1002 sub-series with no new data ingest. The series visualizes Shaikh's equation (10.8) prediction that real finance cost is regulated by real banking costs and the general rate of profit. Per p.466: "From 1857 to 1927 this ratio is relatively stable even through the Great Depression of 1873-1893..." The post-1980 break is attributed to active monetary policy.

### S1004 - Real Interest Rate HP-filtered, 1857-2011 (figures 10.2, 10.8)
Nominal long bond yield minus PPI inflation, with an HP filter at **lambda=3**. **Construction: formula**. The lambda=3 choice is non-standard (Hodrick-Prescott originally 100 annual; Ravn-Uhlig 2002 suggests 6.25). Shaikh's rhetorical point: even the smoothed trend swings between -4.6% and +10%, refuting Fisher's stability claim. Open question for Phase 4: report alternative lambdas for robustness.

### S1005 - Dividend Yield vs Bond Yield, 1871-2011 (figure 10.9)
Three lines: Shiller S&P dividend yield (D/P), Shiller 10-yr govt bond yield, and the S1002-A composite corporate bond yield. **Construction: composite**. Primary source for dividend and 10-yr govt: Robert Shiller, Yale, http://www.econ.yale.edu/~shiller/data.htm (the "long-term stock, bond, interest rate, and consumption data" file). Modern extension: identical Shiller workbook, continuously updated.

### S1006 - Bond and Equity Returns, 1926-2010 (figure 10.10, Table 10.1)
Ibbotson SBBI 2004 Yearbook Table 2-2: rslarge (large-company stocks), rbcorplt (LT corporate bonds), rbgovlt (LT govt bonds). David Stubbs extended 2004-2010. **Construction: direct** (reproduction of Ibbotson's table). Table 10.1 means: 11.88% / 6.24% / 5.91%. **Licensing flag**: Ibbotson is now a Morningstar commercial product; Damodaran's NYU reconstruction (https://pages.stern.nyu.edu/~adamodar/...) is proposed as an open-license modern extension subject to Phase 4 sign-off.

### S1007 - Equity Rate vs Corporate IROP, 1948-2011 (figure 10.11, Table 10.2)
Current-cost real equity rate of return rreq_t = (dvr_t + delta preq_t) / preq_{t-1} from Shiller deflated by BEA gross investment deflator (NOT CPI), vs. two corporate IROP variants: "adjusted" (NOS + Monetary Interest Paid by Nonfinancial Sector / gross investment in fixed cap + inventories) and "NIPA proxy" (delta gross NIPA profits / gross investment). **Construction: composite**. Means over 1947-2011: 9.83% / 9.50% / 8.49%. Underlying NIPA tables: 1.14 (NOS), 5.2.3/5.6.3 (gross investment), 1.1.9 (deflators).

### S1008 - Actual vs Warranted Stock Price, 1947-2011 (figure 10.13)
Three real-price series in two panels. preq = Shiller nominal P / BEA gross investment deflator. prstarshiller1 = Shiller's P* re-converted from CPI base to BEA-deflator base (per footnote 25, p.473). prweq = classical warranted price from equation (10.31): prweq_t = prweq_{t-1} * (1 + rI_t) - dvr_t, with initial value chosen "so that it has the same mean as the actual stock price over [1948-2011]" (footnote 24). **Construction: composite**. rI is the corporate IROP from S1007. The plot is Shaikh's central anti-EMH visual: the classical warranted price tracks actual price's long swings (1950s-60s boom, 1970s downturn, dot-com bubble) while Shiller's P* is monotone-smooth.

## Cross-references

- **S1002, S1003, S1004 share the same composite long bond yield and PPI** (S1002 sub-series A and B). Loader should compute S1002 once and feed S1003/S1004 from cache.
- **S1005, S1007, S1008 share the Shiller (2014) workbook** and the BEA gross investment deflator. Cache both upstream.
- **S1007 and S1008** share rI (corporate IROP); S1008 depends on S1007's output.
- **S1001 depends on Ch7 Appendix 7.2** (S215 industry IROP panel); cross-chapter dependency.
- **S1008's rational-price comparator (prstarshiller1) requires Shiller P* re-deflation**: a non-trivial step easy to get wrong; flagged in S1008 open questions.

## Chapter-wide issues / open questions

1. **Ibbotson licensing (S1006)**: SBBI is now commercial. Phase 4 should decide whether to use Damodaran's free reconstruction. If RSCD must publish or share the dataset, Ibbotson cannot be redistributed.
2. **HP filter lambda (S1004)**: lambda=3 is Shaikh-specific. Recommend Phase 4 report both lambda=3 and lambda=6.25 (Ravn-Uhlig standard).
3. **NIPA comprehensive revisions (S1001, S1007)**: BEA reclassifies sectors periodically; the "adjusted" NOS series (NOS + Monetary Interest Paid by Nonfinancial Sector) needs careful re-derivation under each revision.
4. **Initial-value convention for warranted price (S1008)**: footnote 24's "same mean over 1948-2011" is a normalization; replication tests must lock this to match Shaikh's DATAintropprice sheet.
5. **Fig 10.3 short-rate panel (S1002)**: currently bundled. Phase 4 may want to split as a separate cross-rate-comparison series (Fed Funds, Discount, 3-mo CD, Munis, Aaa).
6. **NAICS banking subsector (S1001)**: NAICS 52 is broader than Shaikh's banking; NAICS 5221 (Depository credit) is narrower. Phase 4 decision needed.

## CD2 salvage status

All 8 series have CD2 predecessors (S050/S052/S053/S054/S055/S056/S057/S059) with markdown dossiers ported. CD2 validation sample values (e.g., S050 1988=0.169, 1991=-0.037; S052 1857=296.2) are recorded in CD2 markdown and will serve as regression test anchors in Phase 5.

## Validator status

To be confirmed after running `_phase3_research_validator.py`.

---

## Phase 5-8 Closure (2026-05-18)

**Author**: opus-fanout-ch10
**Result**: 8 of 8 series ratified ingested with V03 PASS (MAE = 0 on all book-period comparisons).

### Per-series closure

- **S1001** — Pass-through reproduction of Appendix 7.2 `Banks` and `All Private` columns over 1988-2005. V03 PASS, MAE 0, 36 chopped rows. Extension via BEA NAICS 5221 GDP-by-industry deferred to Phase 6 sensitivity per the adequacy report's open question on Shaikh's corrected-capital-stock convention; loader stamps `extension_status: deferred_to_phase6_sensitivity`. Caveat noted: CD2's S050 spot values diverge from the Appendix 7.2 columns — this is logged informationally; the book's stated primary source is App. 7.2 and we reproduce it verbatim.

- **S1002** — Composite long-yield (Macaulay+Aaa) and PPI (Jastram+BLS) panels over 1857-2011 plus FRED extensions 2012-2026 (AAA + PPIACO reindexed to USWPI[2011] anchor). V03 PASS, MAE 0, 417 chopped rows across 4 subseries. FRED `fredgraph.csv` endpoint is no-key and stable; cache enabled. Open question for the Jastram-to-BLS-PPI 1976/1977 splice point remains documented.

- **S1003** — Relative Price of Finance ratio `(i_t/i_1947)/(p_t/p_1947)` recomputed end-to-end from S1002 components (No-Lazy-Splices rule enforced; ratio is never spliced). V03 PASS, MAE 0, 170 chopped rows.

- **S1004** — Real long bond yield (recomputed) plus HP-filtered trend at two lambdas. **Discovery**: the workbook column labeled `iblongrealHP3` is numerically consistent with **lambda=100**, not lambda=3 (verified by lambda sweep against Shaikh's published values: MAE = 0.0000 at lambda=100; MAE = 0.022 at lambda=3). We pin lambda=100 for book replication (subseries S1004-B); lambda=6.25 (Ravn-Uhlig 2002 annual standard) is emitted alongside as S1004-C sensitivity per Phase 4 ratification. The "HP3" name appears to denote something other than the smoothness parameter Shaikh actually applied. DPR updated with this caveat. V03 PASS, MAE 0, 495 chopped rows.

- **S1005** — Shiller dividend yield, Shiller 10yr govt bond yield, and S1002-A composite corporate yield over 1871-2011, with Shiller `ie_data.xls` and FRED GS10/AAA extensions to current year. Shiller `ie_data.xls` (legacy OLE2 .xls, requires `xlrd`) loads cleanly via new `S00_apis.shiller_annual()`. V03 PASS, MAE 0, 479 chopped rows.

- **S1006** — Ibbotson SBBI 2004 table 2-2 panel (Large Company Stocks, LT Corporate Bonds, LT Government Bonds) over 1926-2010, extended via Damodaran NYU `histretSP.html` for S&P 500 and 10yr T.Bond (verified live 200 OK). Damodaran also publishes a `Baa Corporate Bond` yield column we use as an alternate LT-Corp proxy (S1006-B-ext-damodaran). The FRED `AAA` yield reconstruction is retained as the primary LT-Corp proxy (S1006-B-ext); both are flagged `proxy: true` with Concept Match Justification in the EPR. V03 PASS, MAE 0, 316 chopped rows. New `S00_apis.damodaran_histret()` client added with HTML parse (header=1 on the single table) and percent-string normalization.

- **S1007** — Pass-through of three IntroPPrice derived columns (`rreq`, `iropcorp`, `iropcorpnipa`) over 1948-2011. V03 PASS, MAE 0, 192 chopped rows. Extension deferred to Phase 6 per the adequacy open questions (NIPA vintage pinning + "Monetary Interest Paid by Nonfinancial Sector" exact line lookup).

- **S1008** — `preq` and `prstarshiller1` pass-through plus `prweq` recomputed via eq (10.31) forward iteration. **Discovery**: the book's published `prweq` column hardcodes `adj = 6.75` (verified by `prweq[1947] − preq[1947] = 72.052 − 65.302 = 6.75` exactly). Footnote 24 describes the same-mean calibration that produced the original `adj`; the workbook uses the calibrated value as a fixed parameter. We pin `BOOK_ADJ = 6.75` in P02 to reproduce the published column exactly (and to comply with the Phase 4 "must not re-anchor on extended interval" ruling). V03 PASS, MAE 0, 196 chopped rows. Extension deferred (inherits S1007 vintage deferral).

### Infrastructure additions

- `S00_apis.fred_csv_observations(series_id)` — no-key FRED CSV endpoint per Phase 4 ratification (the `fredgraph.csv` endpoint is reliable and key-free, unlike the rate-limited JSON `/series/<id>` page).
- `S00_apis.shiller_ie_data()` / `shiller_annual()` — fetches `ie_data.xls` (OLE2 legacy via `xlrd`), normalizes the fractional-year date column to monthly, and aggregates to annual mean (Shaikh's DATAintropprice convention).
- `S00_apis.damodaran_histret()` — fetches `histretSP.html`, parses the single big table (header=1), strips `%` and `$` formatting, returns columns `rslarge`, `rbgovlt`, `rbtbills`, `rbcorplt` (Baa).

### Validator output (final)

| SID   | V03 status | MAE | chopped rows | extenbook bytes |
|-------|------------|-----|--------------|------------------|
| S1001 | PASS       | 0   | 36           | 16,582           |
| S1002 | PASS       | 0   | 417          | 32,517           |
| S1003 | PASS       | 0   | 170          | 22,283           |
| S1004 | PASS       | 0   | 495          | 40,592           |
| S1005 | PASS       | 0   | 479          | 34,784           |
| S1006 | PASS       | 0   | 316          | 28,277           |
| S1007 | PASS       | 0   | 192          | 22,909           |
| S1008 | PASS       | 0   | 196          | 24,170           |

### Open questions surfaced during Phase 5

1. **S1004 HP filter convention**: Phase 4 ratified lambda=3 (book replication) but the published column is numerically lambda=100. Recommend updating Phase 4 documentation to note that "HP3" in Shaikh's workbook is a labeling artifact and the operative lambda is 100.
2. **S1008 footnote 24 calibration**: Phase 4 ratified the same-mean rule over [1948, 2011] but the workbook hardcodes `adj = 6.75` (which does not exactly satisfy the mean-equality on the full panel). The pinning is unambiguous for replication; the footnote's claim is a simplification of the original calibration.
3. **S1006 LT Corp Bond proxy**: two alternative open proxies emitted (FRED AAA yield and Damodaran Baa yield). Phase 6 visualization can show both and let the reader assess sensitivity.
4. **CD2 S050 (S1001) divergence**: CD2's reported validation values do not match Appendix 7.2. Recommend Phase 6 cross-check with the CD2 source materials to identify the vintage difference.
