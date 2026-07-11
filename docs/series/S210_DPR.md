# S210 -- US and UK Wholesale Price Indexes, 1780-2026 (Fig 2.8, log scale)

**Data Provenance Record (DPR)**

**Series ID**: S210
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S210`

---

## 1. Definition

Annual wholesale price indexes for US (1780-2010) and UK (1780-2010) on log scale, both rebased to 1930 = 100. Composite of Jastram (1977) + BLS PPI + ONS PLLU.

In Shaikh (2016) the series appears as **Figure 2.8** in Chapter 2 ("Turbulent Trends and Hidden Structures").

## 2. Why it matters in Chapter 2

Foundation series for the inflation-vs-deflation analysis that pervades the book (Chs 2, 5, 14, 15). The very long span makes the gold-standard / fiat-money price-level break of 1933 starkly visible.

## 3. Sources (per subseries)

The shipped chopped carries **two subseries (A = US, B = UK)**; the forward extensions are **folded into A and B** (there is no separate lettered extension subseries):

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S210-A** | 1780-2026 | Jastram (1977) T7 (US WPI) + BLS PPI extension (WPS->WPU) — `JASTRAM_1977_T7_PLUS_BLS_PPI_EXT` | Index 1930=100 | salvaged via CD2 S023; BLS PPI growth-rate splice onto the 1930=100 basis |
| **S210-B** | 1780-2022 | Jastram (1977) T2 (UK WPI) + **ONS PLLU** extension — `JASTRAM_1977_T2_PLUS_ONS_PLLU` | Index 1930=100 | salvaged via CD2 S023; ONS PLLU (Price Index of UK Output of Mfg Goods) growth-rate splice onto the 1930=100 basis |

**S210-C folded into S210-A (SWEEP-ch02-04).** An earlier draft declared a separate `S210-C` for the US FRED (`WPU00000000`) extension to 2025; the shipped chopped instead **folds the US extension into S210-A** (carried to 2026 under the `JASTRAM_1977_T7_PLUS_BLS_PPI_EXT` source_id), so no standalone S210-C ships. (Corrected 2026-07-02, campaign DF-2.)

## 4. Construction

`composite` construction.

1. No Appendix 2 chopped table for WPI; CD2 S023 (which itself replicates Jastram + extensions) used as canonical book replica per decision 0005.
2. Phase 4 substitution: BLS WPS00000000 frozen 1974 -> use WPU00000000 for post-1974 US extension.
3. Phase 4 URL update: NBER macrohistory -> https://www.nber.org/research/data/nber-macrohistory-database.
4. **Both country extensions ship (ONS-502 deferral resolved).** The shipped chopped extends S210-A (US) to **2026** via the BLS PPI splice and S210-B (UK) to **2022** via the **ONS PLLU** growth-rate splice — both folded into their book subseries. The earlier "UK extension deferred (transient 502)" limitation no longer applies to what ships. (Note: the L01_S210 / P02_S210 *code* still reflect the older path — US-only extension emitted as a separate S210-C via FRED and a "UK requires ONS PLLU, US-only continuation" diagnostic — which diverges from the shipped chopped. Flagged for the code owner; DF-2 does not touch code this wave.)

## 5. Year coverage

- **Book period**: 1780-2010
- **Extension period (shipped)**: US (S210-A) 2011-2026; UK (S210-B) 2011-2022

## 6. Units

Index, 1930 = 100 (log scale on figure)

## 7. Caveats

1. Canonical source not in chopped store; CD2 replica used (decision 0005).
2. UK extension shipped to 2022 via ONS PLLU (the earlier transient-502 deferral is resolved in what ships). The UK line ends at 2022 vs the US line at 2026 simply because ONS PLLU's last available annual observation is 2022; this is a data-availability boundary, not a deferral.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.8
- Knowledge Base: figure-linkage reference
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
