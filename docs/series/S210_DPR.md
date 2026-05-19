# S210 -- US and UK Wholesale Price Indexes, 1780-2025 (Fig 2.10, log scale)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S210
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S210_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S210_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S210`

---

## 1. Definition

Annual wholesale price indexes for US (1780-2010) and UK (1780-2010) on log scale, both rebased to 1930 = 100. Composite of Jastram (1977) + BLS PPI + ONS PLLU.

In Shaikh (2016) the series appears as **Figure 2.10** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

Foundation series for the inflation-vs-deflation analysis that pervades the book (Chs 2, 5, 14, 15). The very long span makes the gold-standard / fiat-money price-level break of 1933 starkly visible.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S210-A** | 1780-2010 | Jastram (1977) T7 (US WPI) + BLS PPI extension (WPS->WPU) | Index 1930=100 | salvaged via CD2 S023 |
| **S210-B** | 1780-2010 | Jastram (1977) T2 (UK WPI) + ONS PLLU extension | Index 1930=100 | salvaged via CD2 S023 |
| **S210-C** | 2011-2025 | FRED WPU00000000 (PPI All Commodities, US extension) | Index 1982=100 | FRED API |

## 4. Construction

`composite` construction.

1. No Appendix 2 chopped table for WPI; CD2 S023 (which itself replicates Jastram + extensions) used as canonical book replica per decision 0005.
2. Phase 4 substitution: BLS WPS00000000 frozen 1974 -> use WPU00000000 for post-1974 US extension.
3. Phase 4 URL update: NBER macrohistory -> https://www.nber.org/research/data/nber-macrohistory-database.
4. Extension currently US-only via FRED; UK extension via ONS PLLU deferred (transient 502 on specific page).

## 5. Year coverage

- **Book period**: 1780-2010
- **Extension period**: 2011-2025

## 6. Units

Index, 1930 = 100 (log scale on figure)

## 7. Caveats

1. Canonical source not in chopped store; CD2 replica used (decision 0005).
2. UK extension incomplete (ONS PLLU specific URL transient 502); document in EPR.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.10
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
