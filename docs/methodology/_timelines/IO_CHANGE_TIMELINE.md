# BEA Benchmark Input-Output Accounts Timeline

**Phase-0 canonical reference for the RSCD replication of Shaikh, *Capitalism* (2016), Chapters 6/7/9.**
Cite this file (and `IO_CHANGE_TIMELINE.json` beside it) instead of re-researching BEA I-O history.

- **Compiled:** 2026-06-30 (RSCD Phase-0 research agent)
- **Web-verified:** yes — every row cites a bea.gov / apps.bea.gov source.
- **Companions:** `NIPA_CHANGE_TIMELINE.md`; official concordances staged at `../concordances/_sources/`.

## Cadence & detail

BEA publishes a **benchmark I-O account every 5 years** (years ending in **2 and 7**), keyed to the quinquennial Economic Census. Each benchmark is available at four detail levels: **sector (~15)**, **summary (~71)**, **underlying summary (~138)**, and **detail (~402–405)**. Detail-level estimates exist only for benchmark years.

## Benchmark-year table

| Benchmark | Classification | Detail | Notable change (RSCD-relevant) |
|-----------|----------------|--------|--------------------------------|
| **1947** | 1957 SIC | detail | First BEA benchmark. Shaikh/Ochoa 1947 71-order cross-section. |
| **1958** | 1957 SIC | detail | Shaikh/Ochoa 1958. |
| **1963** | 1957 SIC | detail | Shaikh/Ochoa 1963. |
| **1967** | SIC (current) | ~478 | Shaikh/Ochoa 1967. |
| **1972** | 1972 SIC | ~496 | Shaikh/Ochoa 1972 — **last** of the historical Ochoa 71-order panel Shaikh uses. |
| **1977** | 1977 SIC | ~537 | Not in Shaikh's Ch9 panel (his set jumps 1972 → 1998). |
| **1982** | 1977 SIC | ~537 | SIC-era. |
| **1987** | 1987 SIC | ~498 | Anchors the 1987-SIC side of the Census SIC↔NAICS bridge. |
| **1992** | 1987 SIC | ~498 | **LAST SIC-basis benchmark.** Do not splice to 1997+. |
| **1997** | **1997 NAICS** | ~498 detail / **65-order** summary | **FIRST NAICS benchmark.** Hard break vs. SIC. First to include software as investment. **Also the LAST benchmark capital-flow table** (see below). |
| **2002** | 2002 NAICS | detail/summary | Incorporated into the **2009** NIPA comprehensive revision (SCB Oct 2007). |
| **2007** | 2007 NAICS | detail (~405)/summary (~71)/sector (~15) | **First benchmark fully integrated** with annual industry accounts + NIPAs (supply-use). Incorporated into **2013** NIPA revision. |
| **2012** | 2012 NAICS | detail/summary/sector | Incorporated into **2018** NIPA update. 2007↔2012 I-O concordance in SCB Aug 2018 App. A. |
| **2017** | 2017 NAICS | supply-use (detail/summary/sector) | Incorporated into **2023** harmonized update; 2017-NAICS effects small. **Most recent benchmark** as of 2026-06-30. |

## The SIC → NAICS break (the Ch9 wall)

- **Last SIC benchmark = 1992; first NAICS benchmark = 1997.**
- BEA explicitly states the pre-1997 historical benchmark tables **"should not be used as a time series"** and do not reflect subsequent NIPA comprehensive revisions.
- **RSCD impact:** Shaikh's Ch9 historical panel splices the **Ochoa 1947–1972 71-order (SIC)** cross-sections with the **1998 BEA 65-order (NAICS)** Use table. These classifications are **not conformable**; a single continuous industry panel across the 1972→1998 gap is not reconstructable (CH9 open-question 3). Treat each benchmark cross-section as a frozen exhibit.

## Industry order / detail notes

- **Ochoa 71-order vs BEA 65-order.** Shaikh's 1947–1972 cross-sections use Ochoa (1984)'s **71-industry order** (real estate excluded). His 1998 cross-section uses BEA's **65-order** industry-by-industry Use table (post-redefinition), with the real-estate column corrected for owner-occupied-housing imputations (**NIPA T7.12 lines 133–134**). The two schemes are not directly conformable.
- **NAICS-era order still drifts.** Even within NAICS, the summary/detail row-column order and aggregation are revised at each benchmark, so industry indices are **not stable across benchmark years**.

## Capital-flow benchmark matrix — discontinued after 1997

- The BEA **benchmark capital flow table** (a use-type × using-industry matrix distributing new equipment/software/structures investment across industries) was historically produced for each benchmark year.
- **Last benchmark = 1997**, released in **SCB November 2003** — the seventh in the series, the first on a NAICS basis, and the first to include software.
- **No benchmark capital-flow table exists for 2002 or later** — the benchmark matrix was effectively **discontinued after 1997**. (BEA later explored *annual* capital-flow tables as research; the fixed benchmark asset-by-industry matrix still ends at 1997.)
- **RSCD impact (CH9 open-question 4):** Shaikh's fixed-capital wage-profit model distributes BEA Fixed Asset Tables **3.1ES/3.4ES** across industries using the **1997** capital flow matrix. Any post-1998 fixed-capital replication must **approximate** the asset-by-industry distribution from BEA's detailed Fixed Asset Tables (type × industry) — a structural obstacle to extension.

## Cross-check against the local KB

- Local `CH9_RESEARCH_SUMMARY.md` independently states the six benchmark cross-sections, the Ochoa-71 / BEA-65 split, the NAICS-vs-SIC non-splice, and the post-1997 capital-flow gap — **no disagreement**; this timeline supplies the full benchmark-year classification history and official concordance files behind those claims.
- Local `Divergence_Reports/ADR-005_NAICS/data/naics_concordance_master.csv` already stages NAICS 2002–2022 stability flags for Shaikh's Ch7 30-industry sample; the official Census concordances staged under `../concordances/_sources/` are the upstream authority for that file.

## Sources

- BEA — Historical Benchmark Input-Output Tables — https://www.bea.gov/industry/historical-benchmark-input-output-tables
- BEA — Benchmark Input-Output Data — https://www.bea.gov/industry/benchmark-input-output-data
- BEA — Input-Output Accounts Data — https://www.bea.gov/data/industries/input-output-accounts-data
- BEA — Capital Flow Data — https://www.bea.gov/industry/capital-flow-data
- BEA FAQ 22 — SIC / I-O / NAICS concordance codes — https://www.bea.gov/help/faq/22
- BEA FAQ 18 — 1997 Capital Flow Table — https://www.bea.gov/help/faq/18
- SCB Dec 2002 — Benchmark I-O Accounts of the United States, 1997 — https://apps.bea.gov/scb/pdf/2002/12December/1202I-OAccounts2Box27.pdf
- SCB Oct 2007 — U.S. Benchmark I-O Accounts, 2002 — https://apps.bea.gov/scb/pdf/2007/10%20october/1007_benchmark_io.pdf
- SCB Aug 2018 — Preview of the 2018 Comprehensive Update of the Industry Economic Accounts (2007/2012 I-O concordance, App. A) — https://apps.bea.gov/scb/issues/2018/08-august/pdf/0818-industry-text.pdf
