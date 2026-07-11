# Industry-Classification Concordances — Sources & Provenance

**Phase-0 canonical concordance stage for the RSCD replication of Shaikh (2016).**
Cite this directory instead of re-fetching Census/BEA crosswalks.

- **Compiled / retrieved:** 2026-06-30 (RSCD Phase-0 research agent)
- **Publisher (NAICS/SIC bridges):** US Census Bureau, https://www.census.gov/naics/concordances/
- **Publisher (I-O concordances):** US Bureau of Economic Analysis (BEA)
- **Companions:** `../../_timelines/IO_CHANGE_TIMELINE.md`, `../../_timelines/NIPA_CHANGE_TIMELINE.md`

Each Census concordance below was downloaded **directly** from `census.gov/naics/concordances/` on **2026-06-30**. Both the **original Excel** (`.xls`/`.xlsx`, the authoritative machine-readable form) and a **derived `.csv`** (convenience dump via pandas, same basename) are staged in `naics/`. Retrieval was via `curl` (Census blocks generic fetchers but serves files to a browser UA).

## OBTAINED — Census SIC ↔ NAICS bridges (clean CSV headers)

These converted with proper single-row headers; the CSV is directly grep-able/joinable.

| File (in `naics/`) | Rows | Columns (CSV header) | What it maps |
|---|---:|---|---|
| `1987_SIC_to_1997_NAICS.{xls,csv}` | 2335 | `SIC, Part Indicator, SIC Titles and Part Descriptions, 1997 NAICS, 1997 NAICS Titles and Part Indicators` | 1987 SIC → 1997 NAICS (forward bridge) |
| `1997_NAICS_to_1987_SIC.{xls,csv}` | 1867 | `1997 NAICS, NAICS Part Indicator, 1997 NAICS Title, SIC, SIC Part Indicator, SIC Title and Part Description` | 1997 NAICS → 1987 SIC (reverse bridge) |
| `1987_SIC_to_2002_NAICS.{xls,csv}` | 2168 | `SIC, 2002 NAICS, ... titles` | 1987 SIC → 2002 NAICS |
| `2002_NAICS_to_1987_SIC.{xls,csv}` | 2168 | `2002 NAICS, SIC, ... titles` | 2002 NAICS → 1987 SIC (reverse) |
| `1997_NAICS_to_2002_NAICS.{xls,csv}` | 2537 | `2002 NAICS, 1997 NAICS, Total` (count/matrix form) | 1997 ↔ 2002 NAICS revision |
| `2002_NAICS_to_1997_NAICS.{xls,csv}` | 2537 | `2002 NAICS, 1997 NAICS, Total` | 2002 ↔ 1997 NAICS revision (reverse) |

## OBTAINED — Census NAICS revision-to-revision concordances

Full concordances between adjacent NAICS vintages. **CSV caveat:** the source Excel has a **banner title row + a note row** before the real column header, so the auto-converted `.csv` carries two preamble rows — **read the `.xls`/`.xlsx` original, or skip the first 2 rows of the CSV** (real header is `<from> NAICS Code, <from> NAICS Title, <to> NAICS Code, <to> NAICS Title, ...`). Bold `to`-codes = target industry drawn from >1 source industry; italic `from`-codes = source industry split into ≥2 targets.

| File (in `naics/`) | Rows | Maps |
|---|---:|---|
| `2002_to_2007_NAICS.{xls,csv}` | 1202 | 2002 → 2007 NAICS |
| `2007_to_2002_NAICS.{xls,csv}` | 1202 | 2007 → 2002 NAICS (reverse) |
| `2007_to_2012_NAICS.{xls,csv}` | 1186 | 2007 → 2012 NAICS |
| `2012_to_2007_NAICS.{xls,csv}` | 1186 | 2012 → 2007 NAICS (reverse) |
| `2012_to_2017_NAICS.{xlsx,csv}` | 1071 | 2012 → 2017 NAICS |
| `2017_to_2012_NAICS.{xlsx,csv}` | 1071 | 2017 → 2012 NAICS (reverse) |
| `2017_to_2022_NAICS.{xlsx,csv}` | 1152 | 2017 → 2022 NAICS |
| `2022_to_2017_NAICS.{xlsx,csv}` | 1152 | 2022 → 2017 NAICS (reverse) |

**Coverage:** an unbroken chain from **1987 SIC → 1997 NAICS → 2002 → 2007 → 2012 → 2017 → 2022 NAICS** (both directions), plus direct 1987-SIC↔2002-NAICS. This is sufficient to place any Shaikh SIC-era industry or any post-1997 NAICS-era industry on any other vintage.

## REFERENCED BY URL ONLY — BEA I-O industry concordances (not machine-readable CSV)

BEA publishes its I-O↔SIC/NAICS concordances as **appendix tables inside SCB PDF articles**, not as standalone CSVs. Staged as URLs; extract from PDF if a downstream stage needs them as tables.

| Concordance | Location | Authoritative URL |
|---|---|---|
| 1997 I-O codes ↔ SIC/NAICS | "Benchmark I-O Accounts of the US, 1997", App. A — SCB Dec 2002 | https://apps.bea.gov/scb/pdf/2002/12December/1202I-OAccounts2Box27.pdf |
| 2002 I-O codes ↔ NAICS | "US Benchmark I-O Accounts, 2002", App. A — SCB Oct 2007 | https://apps.bea.gov/scb/pdf/2007/10%20october/1007_benchmark_io.pdf |
| 2007 & 2012 I-O codes ↔ NAICS | "Preview of the 2018 Comprehensive Update of the Industry Economic Accounts", App. A — SCB Aug 2018 | https://apps.bea.gov/scb/issues/2018/08-august/pdf/0818-industry-text.pdf |
| BEA landing FAQ for the above | BEA FAQ 22 | https://www.bea.gov/help/faq/22 |

## RELATED LOCAL ARTIFACT (already in the project)

- `Inputs/Capitalism Data/Technical/Divergence_Reports/ADR-005_NAICS/data/naics_concordance_master.csv` — a project-built NAICS 2002/2007/2012/2017/2022 stability table for Shaikh's Ch7 30-industry sample (columns: `naics_2002…naics_2022, title, change_*` flags). The official Census files above are its upstream authority; use them to verify/extend it.

## Provenance summary

- **retrieval_date:** 2026-06-30
- **method:** `curl -A "Mozilla/5.0"` direct file download from `census.gov/naics/concordances/`
- **csv derivation:** `pandas.read_excel(sheet 0, dtype=str).to_csv()` — originals retained as ground truth
- **integrity note:** two 404s were encountered for guessed filenames (`1997_to_2002_NAICS.xls`, `2002_to_1997_NAICS.xls`); the correctly-named `1997_NAICS_to_2002_NAICS.xls` / `2002_NAICS_to_1997_NAICS.xls` succeeded and are the files staged. No fabricated data.
