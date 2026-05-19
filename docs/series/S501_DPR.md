# S501 — US and UK Wholesale Price Indexes, 1790-1940

**Data Provenance Record (DPR)** · **Phase**: 5 (Ingestion) · **Series ID**: S501
**Status**: ingested · **Authored**: 2026-05-18 · **Author**: opus-fanout-wave3-ch5
**Related**: `Technical/research/S501_research.json`, `Technical/docs/chapters/CH5_ADEQUACY_REPORT.json`, `Technical/docs/series/S501_EPR.md`, registry → `series.S501`.

---

## 1. Definition

**S501** is the annual US and UK Wholesale Price Indexes (1930=100) restricted to the chronological slice **1790-1940**, used by Shaikh as **Figure 5.3** to illustrate the absence of a long-run trend in nominal price levels under metallic-money regimes.

## 2. Why it matters

Ch5 separates the relative-price problem from the general-price-level problem. Fig 5.3 documents the empirical regularity that, prior to the 1939/40 fiat-money transition, US and UK price levels were *stationary in level* over 150 years of capitalist development. S501 is the empirical anchor for that claim.

## 3. Sources (per subseries)

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S501-A** | 1790-1940 | Jastram (1977, table 7) — US WPI, spliced 1977-onward via BLS PPI but truncated to 1940 here | Index 1930=100 | Local: `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix5_DATALRprices.xlsx`, column `USWPI` |
| **S501-B** | 1790-1940 | Jastram (1977, table 2) — UK WPI, with 1939-1945 NBER macrohistory fill (here truncated 1790-1940 so only 1939, 1940 are wartime-affected) | Index 1930=100 | Same XLSX, column `UKWPI` |

Per Phase 4 (CH5_ADEQUACY): anwarshaikhecon.org DNS does not resolve; local `Appendix5_DATALRprices.xlsx` is canonical. Web citation: `https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/`.

## 4. Construction

S501 is **direct** (chronological slice). The underlying composite construction lives in S502; S501 is exactly the 1790-1940 window of S502's two country columns.

```
S501-A[year] = S502_USWPI[year]   for year in [1790, 1940]
S501-B[year] = S502_UKWPI[year]   for year in [1790, 1940]
```

No reindex, no splice in the loader — values come directly from Shaikh's published 1930=100 columns.

## 5. Year coverage

- Book period: 1790-1940, annual; 151 obs per country (302 total).
- Extension: not applicable (this is a fixed chronological slice for Fig 5.3; the full-range continuation lives in S502).

## 6. Units

Index, 1930 = 100. Both subseries carry `units = "index_1930=100"` in the registry, parquet, and chopped CSV.

## 7. Caveats

1. **UK 1939-1940 wartime gold/price interpolation.** Jastram's UK WPI for 1939-1945 was interpolated by Shaikh using NBER macrohistory `m04053`. Only 1939 and 1940 fall inside S501's window; both are flagged as `proxy_flag=wartime_interpolated_NBER_m04053` in the loader output.
2. **Pre-1800 US interpolation.** Jastram's US WPI table starts at 1800. Shaikh extends 1790-1799 by rescaling the US CPI by the 1800 WPI/CPI ratio (Appendix 2.1 cross-reference). These 10 years are flagged `proxy_flag=pre1800_uswpi_via_uscpi`.
3. **Replication-source identity.** S501 reads the same underlying `Appendix5_DATALRprices.xlsx` column as S502; the loader produces identical values up to 1940. This is enforced by sharing the workbook read.
4. **No proxy substitution.** Both UK and US WPI columns are the Jastram (1977) values as Shaikh published them; the BLS PPI / NBER macrohistory fills are inside the book period, not extensions.

## 8. Cross-references

- CD/CD2 legacy ID: `S022`.
- Book reference: Shaikh (2016), Ch5 p.188; Appendix 5.2 pp.788-789.
- Sibling series: S502 (full-range version 1790-2010); S503/S504 (UK/US WPI-in-gold).

## 9. Validation expectation

- Tolerance: **±1.0%** per year (time_series).
- Truth source: `Appendix5_DATALRprices.xlsx` columns `USWPI` and `UKWPI`.
- Expected MAE: 0.0% (the loader reads the truth column directly; the validator compares the processed parquet to the same column).
