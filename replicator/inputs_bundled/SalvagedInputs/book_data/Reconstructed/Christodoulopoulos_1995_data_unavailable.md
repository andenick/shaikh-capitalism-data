# S703 / S704 underlying data — UNAVAILABLE

**Series affected**
- S703 = Capitalism (2016) Figure 7.13 — World manufacturing average and
  incremental ROP, 8 industries x 8 OECD countries (PPP-aggregated),
  1970-1989
- S704 = Capitalism (2016) Figure 7.14 — US manufacturing average and
  incremental ROP, ~14 sub-industries, 1960-1989

**Source for both figures** (per book Appendix 7.1 II, p. 856 / PDF p. 894):
> Christodoulopoulos, George (1995). "International Competition and
> Industrial Rates of Return." Department of Economics, New School for
> Social Research, New York.

This is an unpublished dissertation / working paper that does not have
a public DOI or canonical URL. It is cited only in Shaikh (2008) and
Shaikh (2016).

## Search results (negative)

- No copy of Christodoulopoulos (1995) anywhere in `D:/Arcanum/Projects/RSCD/Inputs`
  (recursive Grep for "Christodoulopoulos" returns only metadata
  references in Shaikh derivative catalogs — no PDF or data file).
- No copy in `Inputs/Capitalism Data/Technical/data/raw/01_SOURCE_MATERIALS/Web Folders/Shaikh Publications/`
  (this folder contains Shaikh's own publications but not those of his
  doctoral students).
- The underlying source is OECD International Sectoral Database (ISDB)
  1994 vintage, which OECD has discontinued. The successor STAN database
  uses a different industry schema and provides only partial back-coverage.

## What the source PDF (Shaikh 2008) DOES contain

The full text of Shaikh (2008) "Competition and Industrial Rates of
Return" (in *Issues in Finance and Industry*, eds. Arestis & Eatwell)
was extracted to verify whether the underlying world-aggregate or
US-manufacturing time series is published anywhere in Shaikh's own
appendix:

- Shaikh (2008) Appendix 1 (p. 186 / PDF p. 14): describes the OECD ISDB
  variables and the PPP-aggregation methodology, but **does not tabulate
  the underlying series**. It refers the reader back to "Christodoulopoulos
  (1995, app. A)" for the full derivation.
- The Shaikh companion site Appendix 7.2 files locally cached at
  `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix7_*.xlsx`
  contain the 1987-2005 BEA-NAICS construction (which feeds Figures
  7.15-7.18 = S705/S706/S709/S710), **not** the 1960-1989 ISDB
  reconstruction behind Figures 7.13-7.14.

## Why this is `data_unavailable` not `extracted`

Per project constraint:
> No fabricated values. If only a chart exists with no underlying table,
> mark `data_unavailable` (Phase 6 may use WebPlotDigitizer manually).

The series values exist as:
1. Line charts in Shaikh (2008) Figures 9.1-9.4 (book pp. 175-177).
2. Line charts in Capitalism (2016) Figures 7.13-7.14 (book pp. 303-304).

In both cases the underlying numerical panel is not published. The only
paths to recover the time-series values are:
- WebPlotDigitizer of either set of charts (manual, Phase 6).
- Track down Christodoulopoulos (1995) directly (likely via NSSR library
  archive or direct author contact — George Christodoulopoulos's current
  affiliation is not in this workspace).
- Reconstruct from OECD ISDB 1994 raw data — but OECD has discontinued
  this dataset and no cached copy is in `Inputs/`.

## Recommendation for Phase 5 plotting

Same as for Tsoulfidis & Tsaliki: either include the book figures as
images (no underlying data needed) or queue for Phase 6 manual
digitization. The world-aggregate series (S703) is the harder of the
two because the 8-country PPP aggregation cannot be re-derived from
modern OECD STAN without documented methodology drift; if digitization
is done, it should target Shaikh's published chart values directly, not
a reconstruction.
