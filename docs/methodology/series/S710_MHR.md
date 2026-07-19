# S710 — Methodological History Report (MHR)

**Series**: S710 · Figure 7.18 — US Industry IROP Deviations from Average, 1988–2005 (38 small-multiple panels)
**Chapter**: 7 (Real Competition) · Group `ch07`/`CH07`
**Status**: `book_period_validated` · `content_type: cross_sectional` (registry) / **time_series** (EPR; review M1) · `construction: formula` · `publish: true`
**Author intent reasoned from**: Shaikh, *Capitalism* (2016), ch.7 pp. 300, 305; Appendix 7.1 §III (pp. 857–859).
**Sources read**: `Technical/research/S710_research.json`, `Technical/series_registry.json` (S710), `Technical/methodology_review/CH07_review.json` (M1/M2, touchpoint S710), `Technical/code/L01_loaders/L01_S709.py`/`_ch7_xlsx_panels.py`, `SalvagedInputs/book_data/Reconstructed/Shaikh_2008_Appendix_B_industries.csv`.

---

## 1. What the series is
S710 is the **incremental** deviation panel — **the chapter's single strongest empirical exhibit** for turbulent equalization: dev_i,t = IROP_i,t − IROP_avg,t for the same 30 US industries, 1988–2005, 38 sub-panels with a zero line. Book definition (page-cited, `S710_research.json`, p. 305): *"This is most clear in figure 7.18, which displays the deviations of individual industry incremental profit rates from the overall average. In every single case, individual incremental rates of profit cross back and forth relative to the average incremental rate: the smallest number of such crossing is four (Fabricated Metals), while the largest is twelve (Broadcast). This is a radically different picture from that presented by average rates of profit in the same sample."* Added by **Decision 0004** to close the Fig 7.18 gap.

## 2. Source lineage
- **Parent series**: **S706** (US Industry Incremental ROP). One-line algebraic transform; ingests no new data.
- **Inherited lineage** (all of S706's): BEA GDPbyInd_VA_NAICS (GOS) + **Fixed Asset Table 3.7ES** (historical-cost gross investment) + WEQ/OOH/inventory/reserve adjustments + 31→30 exclusion, all baked into `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix7_iropdataUSind.xlsx`.
- **Transform**: dev_i,t = IROP_i,t − IROP_avg,t, where IROP_avg = (Σᵢ PGᵢ,t − Σᵢ PGᵢ,t−1)/Σᵢ IGᵢ,t−1 (aggregate-before-ratio All-Private incremental line).
- **Implementation nuance (review M2)**: as with S709, the code reads Shaikh's pre-computed `_Dev` columns rather than computing IROP_i − IROP_avg; faithful, but the identity is unverified by V03.
- **Native units**: rate deviation (decimal), inheriting IROP's high-frequency volatility (why the digitized Greek counterpart S708 is lower-confidence). Panel count 38 (30 + sub-aggregates; book PDF p. 348). Starts **1988** (IROP lag).

## 3. Why these sources (Shaikh's perspective) + rejected alternatives
S710 is where Shaikh's theory wins its cleanest test. The **incremental** deviation is the sharper instrument for two reasons he states: IROP is **capital-stock-free** (book p. 300), so the crossing pattern cannot be an artefact of depreciation/stock assumptions; and incremental rates are what mobile capital actually equalizes. The result — **all 30 industries cross zero, repeatedly** — is qualitatively stronger than the average-rate panel (S709: only 18 of 30 cross). He keeps the identical sample, adjustments, and weighted All-Private baseline as S705/S706/S709 so the average-vs-incremental asymmetry is a controlled contrast on one dataset.
**Rejected alternatives**: unweighted-mean baseline (rejected, same as S709); winsorizing/HP-filtering the volatile deviations (Shaikh leaves them raw — the spikiness is the phenomenon, book p. 300); recompute-from-scratch vs Shaikh's `_Dev` columns (RSCD chose pre-computed for fidelity — review M2).

## 4. Methodological-change exposure (concordance / IO / NIPA)
Inherits **S706's exposure one-for-one**:
- **SIC↔NAICS / NAICS-revision**: NAICS-native 30-industry sample tracked via `_sources/naics/` + ADR-005 stability table; 38-panel set mapped across NAICS 1997→2022.
- **30-vs-31 exclusion**: same key `Shaikh_2008_Appendix_B_industries.csv`; the IROP_avg baseline is defined over the 30 retained industries, so any exclusion change moves all deviations.
- **BEA benchmark + NIPA revisions**: the **2013 R&D/IP capitalization hits the investment denominator (IG)** directly (a common shift does *not* fully cancel in a ratio-of-differences), making S710 sensitive to the 2013/2018/2023 boundaries; **recompute from the S706 re-run, never splice** (`S710_research.json` anti-degradation, `NIPA_CHANGE_TIMELINE.md`).

## 5. Replication fidelity note
Reproduces Shaikh's pre-computed `_Dev` columns byte-exact (V03 MAE 0.0, tol 0.5%, n=558) — most faithful; figure-overlay MATCH (FIGURE_REPRO_ch07). Same caveats as S709: registry `formula` names an identity the code does not itself execute/verify (review M2); registry `content_type: cross_sectional` vs EPR `time_series` (review M1). The book's "every single case crosses zero; 4 (Fabricated Metals) to 12 (Broadcast) crossings" is verified verbatim — the headline result of the chapter.

## 6. Forward risk
Inherits S706 forward risk, amplified: IROP-deviation volatility (post-crisis magnitudes can exceed |2.0|) plus the **2013 R&D/IP capitalization directly perturbing the IG denominator**. Next BEA benchmark/NAICS re-classification re-orders the sample. Always regenerate from the same S706 re-run on a single vintage; commit to a raw (per-Shaikh) default presentation; add a V03 identity check (dev == IROP_i − IROP_avg). 38-panel small-multiple layout deferred to Phase 9 viz.
