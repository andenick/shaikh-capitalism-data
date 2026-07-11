# US NIPA Comprehensive-Revision Timeline

**Phase-0 canonical reference for the RSCD replication of Shaikh, *Capitalism* (2016).**
Cite this file (and the machine-readable `NIPA_CHANGE_TIMELINE.json` beside it) instead of re-researching NIPA vintage history.

- **Compiled:** 2026-06-30 (RSCD Phase-0 research agent)
- **Web-verified:** yes — every row cites a bea.gov / apps.bea.gov source.
- **Machine-readable twin:** `NIPA_CHANGE_TIMELINE.json`
- **Companion:** `IO_CHANGE_TIMELINE.md` (benchmark input-output accounts + SIC→NAICS).

> BEA counts **16 comprehensive updates** of the National (Economic) Accounts through 2023. This file details the modern set (**1999–2023**) that bear on Shaikh's 2011-vintage construction and any post-book extension. Pre-1999 comprehensive revisions (…1980, 1985, 1991, 1996) are out of RSCD scope.

## Why this matters for RSCD

Shaikh's Appendix 6.7 footnote 1 fixes **all BEA data at the 2011 vintage**. Every comprehensive revision after 2011 (2013, 2018, 2023) reclassifies magnitudes and, in the 2018 case, shifts NIPA table line numbers. Any extension of a Shaikh series past its book period must be re-computed end-to-end on a single coherent vintage — **never spliced across a comprehensive-revision boundary** (CH6 open-question 5, CH7 open-question 5).

## Comprehensive-revision rows

| Date | Revision | Key changes | Series families affected |
|------|----------|-------------|--------------------------|
| **1999-10** (rel. 1999-10-28) | 1999 Comprehensive (11th) | **Software capitalized** as fixed investment (business, government, own-account); full switch to chain-type (Fisher) indexes + updated reference year; government consumption vs. investment split refined | GDP, Private Fixed Investment (equipment & software), Government investment, Fixed Assets, chain-type indexes |
| **2003-12** | 2003 Comprehensive (12th) | Revised **implicitly-priced banking services** (reference-rate/FISIM approach) and property-casualty **insurance services**; own-account software originals for reproduction; new/redesigned tables | Corporate profits (financial vs nonfinancial), PCE financial services, FISIM/imputed interest, GDP by industry |
| **2009-07** (rel. 2009-07-31) | 2009 Comprehensive (13th) | Incorporated the **2002 benchmark I-O accounts**; definition/classification/method/source/presentation changes | GDP by industry, PCE categories, Investment, NIPA–IO integration |
| **2013-07** (rel. 2013-07-31) | 2013 Comprehensive (14th) | **R&D capitalized** as investment; **entertainment/literary/artistic originals capitalized** → new **Intellectual Property Products (IPP)** category; accrual accounting for **defined-benefit pensions**; expanded residential **ownership-transfer costs**; incorporated **2007 benchmark I-O**; FISIM restatement by sector. **≈ +$400B to GDP level.** | GDP, Private Fixed Investment (new IPP = R&D + entertainment), Corporate profits, NOS/CFC, **Fixed Assets / capital-stock levels rise**, Personal income & saving (pensions), FISIM (T7.11 magnitudes) |
| **2018-07** (rel. 2018-07-27) | 2018 Comprehensive (15th) | Incorporated **2012 benchmark I-O**; improved financial-services & nonprofit methods; personal-saving revisions; new presentations. **Inserted a new monetary-interest sub-row in T7.11 → +1 line shift** (see below). | GDP by industry, Personal saving, Financial services (FISIM), Nonprofit institutions, **T7.11 line numbering** |
| **2023-09** (rel. 2023-09-28) | 2023 Comprehensive Update of the National Economic Accounts (16th) | First **harmonized** update: NIPAs + Industry Economic Accounts released concurrently, incorporating the **2017 benchmark supply-use/I-O tables**; reference year → **2017**; 2017-NAICS effects small (no summary/sector reclassifications) | GDP (reference year → 2017), GDP by industry / supply-use, chain-type indexes, NIPA–IEA harmonization |

## Table-renumbering / silent-break events

These are the events that break hard-coded line-number recipes — the RSCD-specific time-bombs.

1. **T7.11 — 2018 +1 line shift.** The 2018 update inserted one new monetary-interest sub-row in the financial-corporate block, shifting every subsequent line number by **+1**. Shaikh's Appendix Table 6.7.11 / XS003 recipe uses **2011-vintage** lines `4, 28, 44, 52, 53, 54, 73, 74, 75, 91`; on a 2018+ vintage these become `4, 29, 45, 53, 54, 55, 74, 75, 76, 92` (line 4 unchanged). Vintages **2011–2017** share the 2011 numbers; **2019–2024** share the 2018 numbers. Resolver: `Technical/docs/methodology/NIPA_T711_FISIM_remap.md` (resolves by BEA `LineDescription` stub label, not line number).
2. **T7.11 — 2013 FISIM magnitude restatement.** Row **order unchanged**; the per-row magnitudes changed. Same captions, different values across the 2013 boundary — do not splice.

## Cross-check against the local KB

- Local `Knowledge_Base/Methodology/METHODOLOGY_CHANGES_2010_2025.md` confirms 2013 (R&D, ≈+$400B), 2018, and 2023, but omits the 1999/2003/2009 rows and gives only "effective July/September" dates. **This timeline supersedes it** by adding exact release dates, the pre-2013 comprehensive revisions, and the T7.11 renumbering detail.
- Local `NIPA_T711_FISIM_remap.md` independently documents the 2013 (no reorder) and 2018 (+1) T7.11 events — reproduced here with no disagreement.

## Sources

- BEA — Information on previous updates of the National and Regional Economic Accounts — https://www.bea.gov/information-previous-updates-nipa-regional-accounts
- BEA — NIPA Handbook (Concepts and Methods) — https://www.bea.gov/resources/methodologies/nipa-handbook
- BEA SCB (Aug 1999) — Preview of the 1999 Comprehensive Revision — https://apps.bea.gov/scb/pdf/national/nipa/1999/0899niw.pdf
- BEA SCB (Nov 1999) — Initial Results of the Comprehensive NIPA Revision — https://apps.bea.gov/scb/pdf/national/NIPA/1999/1199gdp.pdf
- BEA SCB (Mar 2013) — Preview of the 2013 Comprehensive Revision — https://apps.bea.gov/scb/pdf/2013/03%20March/0313_nipa_comprehensive_revision_preview.pdf
- BEA FAQ 1024 — 2013 comprehensive revision definition/presentation changes — https://www.bea.gov/help/faq/1024
- BEA blog (2013-07-23) — R&D and entertainment capitalization — https://www.bea.gov/news/blog/2013-07-23/comprehensive-revisions-nipa-reconsidering-treatment-rd-and-entertainment
- BEA SCB (Apr 2018) — Preview of the 2018 Comprehensive Update — https://apps.bea.gov/scb/issues/2018/04-april/0418-preview-2018-comprehensive-nipa-update.htm
- BEA SCB (Sep 2018) — 2018 NIPA update results — https://apps.bea.gov/scb/issues/2018/09-september/0918-nipa-update.htm
- BEA SCB (Jun 2023) — Preview of the 2023 Comprehensive Update of the NEAs — https://apps.bea.gov/scb/issues/2023/06-june/0623-nea-preview.htm
- BEA — Information on 2023 Comprehensive Updates — https://www.bea.gov/information-updates-national-economic-accounts-2023
