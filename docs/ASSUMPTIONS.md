# Assumptions Register — Shaikh (2016)

Every assumption underpinning the data construction is documented here.
Assumptions are numbered by category:
- **D** = Data (source data properties)
- **M** = Methodological (construction methods)
- **R** = Replication (interpretation of original methodology)

---

## Data Assumptions

### ASM-D01: Chopped CSV accuracy
The Anu Chopped CSVs in `Inputs/ShaikhChopped/` faithfully reproduce the
values from Shaikh's original Excel appendix files in `Inputs/ShaikhChoppedOriginals/`.
**Source**: Manual verification during Phase 0 (Session 1, February 2026).
**Risk**: Transcription errors during CSV conversion could propagate silently.
**Validation**: V01 reference value checks against published figure values.
**Series Affected**: All 113 series.

### ASM-D02: FRED API data vintage consistency
FRED API data cached in `Inputs/API/FRED/` represents the latest available vintage
at download time and is suitable for extending Shaikh's series.
**Source**: FRED documentation confirms data vintages are not retroactively revised
for most series used (INDPRO, UNRATE, CPIAUCSL, etc.).
**Risk**: Major data revisions (e.g., GDP benchmark revisions) could change historical
values. Extension series spliced before a revision may show discontinuities.
**Validation**: V07 extension overlap check compares API data with Shaikh's values
in the overlap period.
**Series Affected**: S001, S002, S003, S007, S009, S067, S076 (all FRED-extended series).

---

## Methodological Assumptions

### ASM-M01: Growth-rate splicing preserves trend
Splicing subseries via growth rates at the splice point preserves the long-run
trend of the combined series without introducing artificial discontinuities.
**Source**: Standard practice in economic data construction; see DEC-002.
**Risk**: If the two segments have genuinely different trend rates at the splice
point (structural break), growth-rate splicing will hide this.
**Validation**: V06 splice quality check flags transitions where the relative
difference exceeds 1%.
**Series Affected**: S001, S002, S007, S009, S076, and other multi-segment series.

### ASM-M02: Annual averaging of monthly data is appropriate
Monthly FRED data converted to annual via simple arithmetic average produces values
comparable to Shaikh's annual data.
**Source**: Standard practice in official statistics; see DEC-003.
**Risk**: For highly seasonal or volatile series, the annual average may differ from
Shaikh's method if he used a different aggregation (e.g., end-of-year, geometric mean).
**Validation**: V07 extension overlap check verifies consistency in the overlap period.
**Series Affected**: All FRED-extended series (7 series).

### ASM-M03: Multi-column final CSVs: extension may reside in non-first column
For series with multiple subseries (S051: profit_rate + prime_rate; S100: debt + income + ratio), the extension may apply to a non-primary column. V07 checks all columns.
**Source**: DEC-022.
**Risk**: Downstream consumers that assume column 0 is the extended series may miss extension data.
**Validation**: V07 now checks all columns. Extenbooks and chopped CSVs always contain full subseries.
**Series Affected**: S051, S100.

---

## Data Assumptions (continued)

### ASM-D03: CES3000000008 represents manufacturing compensation growth
CES3000000008 (Manufacturing Average Hourly Earnings, $/hr) represents the growth pattern of manufacturing production worker compensation, despite being "earnings" (excludes benefits) rather than full "compensation" (includes benefits).
**Source**: BLS CES program. Shaikh's "ec" = compensation/hr; CES measures earnings/hr.
**Risk**: Benefits growth may diverge from earnings growth post-2010. For growth-rate splice, impact is second-order since only growth pattern is borrowed.
**Validation**: Splice discontinuity 0.51σ (acceptable). Compare with COMPRNFB as fallback.
**Series Affected**: S008.

### ASM-D04: FRED DPRIME tracks 3-month T-bill rate
Bank prime rate (DPRIME) grows at similar rates to the 3-month T-bill rate used by Shaikh. The prime-Tbill spread is relatively stable.
**Source**: Federal Reserve. Prime = T-bill + ~3% spread (spread stable post-2000).
**Risk**: During zero-lower-bound periods (2009-2015, 2020-2022), both rates near floor — growth rates become undefined. Growth-rate splice still works because levels match.
**Validation**: S097 grade B+ (0.09σ — very smooth).
**Series Affected**: S051, S097.

### ASM-D05: FRED PI growth tracks Disposable Personal Income growth
Personal Income (PI) growth rate is used as proxy for Disposable Personal Income (DPI) growth in the S100 debt-to-income ratio extension.
**Source**: BEA NIPA. PI includes transfers; DPI = PI - taxes. Difference is small in growth-rate terms.
**Risk**: Tax policy changes could cause PI/DPI divergence. Growth-rate splice limits impact.
**Validation**: S100 extension values are plausible (ratio declining from 1.07 to 0.86, consistent with post-GFC deleveraging).
**Series Affected**: S100.

### ASM-D06: Latest FRED/BEA vintage used for all extensions
All extension data uses the most recent available vintage from FRED/BEA (fetched at pipeline run time).
Growth-rate splices are mathematically immune to base-year revisions. Direct-level series (UNRATE, TB3MS, FODSP) are never revised. Dollar-denominated series (GDP, DPI) show <2% revision between 2016 and 2026 vintages.
**Source**: ALFRED vintage comparison (2016 vs 2026), performed 2026-05-05.
**Risk**: Future benchmark revisions could change historical values. Mitigation: growth-rate method limits impact; ALFRED archival API allows vintage comparison.
**Validation**: Triangulation analysis confirms <0.03pp growth-rate MAE for S001/INDPRO, 0.000% for S009/UNRATE and S023/PPIACO. Only S007/OPHMFG shows material revision (BLS 2022 hours methodology change — documented).
**Series Affected**: All FRED-extended series.

---

## Replication Assumptions

### ASM-R01: Appendix methodology descriptions are complete
Shaikh's appendix Sources & Methods sections (especially Appendix 2.1 and the
chapter-specific appendices) fully and accurately describe the construction
methodology for each series.
**Source**: Shaikh 2016 Appendices, extracted via PDF extraction pipeline into Knowledge Base files.
**Risk**: Undocumented methodology steps (implicit calculations, unpublished
adjustments) could cause replication discrepancies that reference value checks
cannot catch.
**Validation**: V01 reference value checks; manual inspection of discrepancies.
**Series Affected**: All 113 series.

---
