# Reconstructed Inputs — Provenance

Files in this directory were reconstructed by direct extraction from primary
source PDFs during Phase 5 blocker remediation (Wave B, 2026-05-18).
Every row is verbatim from a single, citable source page; no values were
imputed, smoothed, or back-cast.

---

## Shaikh_2008_Appendix_B_industries.csv

**31-industry exclusion list used in Shaikh (2008) — the basis for the 30-industry
sample plotted in Capitalism (2016) Figures 7.15-7.18.**

### Source
- Shaikh, Anwar (2008). "Competition and Industrial Rates of Return."
  In Arestis, P. & Eatwell, J. (eds.), *Issues in Finance and Industry: Essays
  in Honour of Ajit Singh*. Palgrave Macmillan, pp. 167-194.
- Local PDF: `Inputs/Capitalism Data/Technical/data/raw/01_SOURCE_MATERIALS/Web Folders/Shaikh Publications/[2008] Shaikh - Competition and Industrial Rates of Return.pdf`
- Verbatim source: **Table 9.A1 "Full list of excluded industries"**, in
  Appendix 2 ("US data, 1987-2005, for Figures 9.5-9.12"), book p. 190 /
  PDF p. 16.

### Method
- PyMuPDF text dump of the local PDF (`fitz`, no OCR needed — the PDF is
  digitally embedded).
- Each row in `Shaikh_2008_Appendix_B_industries.csv` is a verbatim copy of
  one row of Table 9.A1: `industry_no`, `industry_level` (Shaikh's
  cluster column), and `industry_title`.
- `exclusion_ground` and `naics_subgroup` are derived classification columns
  (NOT in the original table) that mirror the textual reasons Shaikh gives
  for exclusion on book pp. 178 and 191 (PDF pp. 10 and 17):
  - `dominated-by-non-profit` — arts, museums, educational services,
    social services
  - `inadequate-WEQ-data-or-dominated-by-non-profit` — legal, medical,
    computer services; finance subsectors with insufficient wage-equivalent
    data
  - `internationally-noncompetitive` — textiles, mining, domestic oil
  - `low-or-negative-profit-rate-period-average` — Shaikh's residual
    "another eighteen industries... below 5 per cent average rate of profit"
    (book p. 191)
  - `non-profit-or-noncompetitive` — agriculture / forestry / fishing
    (both agriculture rows 1-2 fall here)

The `exclusion_ground` column is interpretive: Shaikh's text groups
industries by reason in prose but does not tag each row in Table 9.A1
with its specific ground. The mappings here are best-effort based on the
prose at pp. 178 and 191; verify against the book before using them as
authoritative.

### Verification
- 31 data rows in the CSV (count check).
- Industry numbers preserved exactly as printed in Table 9.A1 (with the
  jumps in numbering that reflect the omitted INCLUDED industries — there
  are NAICS industries numbered 6-9, 11-12, 14, 17-19, 22-28, 32, 36,
  38-41, 43, 45-46, 52, 58-60 that are INCLUDED in Shaikh's 30-industry
  sample and intentionally do not appear here).
- Industry titles are character-perfect copies including Shaikh's
  punctuation and capitalization.

### Use in RSCD
- Series dossiers S705, S706, S709, S710 all depend on this list (used to
  restrict the 61-industry NAICS panel to the 30 that Shaikh retains).
- The construction step is: from the BEA GDPbyInd 61-industry NAICS panel,
  DROP these 31 industries; the remaining 30 are the sample used for
  ROP_avg and IROP_avg aggregates in Figures 7.15-7.18.

---

## Tsoulfidis_Tsaliki_2011_data_unavailable.md

See file for documentation of why S707/S708 underlying time-series data
cannot be extracted from the primary source.

## Christodoulopoulos_1995_data_unavailable.md

See file for documentation of why S703/S704 underlying time-series data
cannot be extracted from any locally available source.
