# S706 — Methodological History Report (MHR)

**Series**: S706 · Figure 7.17 — US Industry Incremental Rates of Profit (IROP), 1988–2005 (30 industries + All-Private)
**Chapter**: 7 (Real Competition) · Group `ch07`/`CH07`
**Status**: `book_period_validated` · `content_type: cross_sectional` (registry) / **time_series in substance** (EPR; review M1) · `construction: composite` · `publish: true`
**Author intent reasoned from**: Shaikh, *Capitalism* (2016), ch.7 pp. 299–301, 305; Appendix 7.1 §III (pp. 857–859).
**Sources read**: `Technical/research/S706_research.json`, `Technical/series_registry.json` (S706), `Technical/methodology_review/CH07_review.json` (M1/M3, touchpoint S706), `SalvagedInputs/book_data/Reconstructed/Shaikh_2008_Appendix_B_industries.csv`, the Phase-0 timelines + concordance `_sources/`.

---

## 1. What the series is
S706 is the **incremental** companion of S705: for the same 30 US NAICS industries, IROP = **change in nominal gross profit ÷ lagged nominal gross investment**, 1988–2005 (starts 1988 because of the lag). Definition (page-cited, `S706_research.json`, Appendix 7.1 p. 857): *"since gross investment figures are widely available and are independent of the debatable assumptions needed to estimate capital stocks, the incremental rate of profit is defined as the ratio of the change in nominal gross profits to lagged nominal gross investment."* Why it matters (book p. 300): IROP is *the* measure Shaikh trusts for equalization because it is **capital-stock-free** — "its two components, gross profit and gross investment, are widely available … unlike the laboriously constructed measures of the capital stock." It reads as the turbulent "marginal" return on the newest capital and is the parent of the deviation panel S710 (Fig 7.18).

## 2. Source lineage — the full adjustment chain
- **Primary agency data (BEA, NAICS-native)**: BEA **GDPbyInd_VA_NAICS** for **GOS** (1987–2005), and **BEA Fixed Asset Table 3.7ES** (historical-cost gross investment by industry) as the denominator — the key difference from S705, which uses net stock (3.1ES) + depreciation (3.4ES).
- **Adjustment chain** (same four adjustments as S705, applied to both numerator PG and denominator IG; formula in `S706_research.json`):
  1. **WEQ**: PG = GOS − WEQ (removes self-employed implicit wage).
  2. **OOH removal** from Real Estate (NIPA T7.12 + FA T5.7 residential-investment lines 15–16).
  3. **Normal-inventory investment** additions to IG (NIPA T1BU/T2AUI + Economic Census of Construction Table 3).
  4. **Bank/insurance reserve-investment** additions to IG (Flow of Funds L.109, L.114–117).
  5. Same **31-industry exclusion** → 30 retained.
- **Why IROP is robust**: both PG and IG are invariant to the Capital Consumption Adjustment and require no capital-stock or depreciation estimate — the chapter's central methodological virtue (book p. 300; eqns 7.5–7.7 derive IROP ≈ ΔPG_t / IG_{t−1}).
- **Native units**: rate (decimal), intrinsically volatile (small IG denominators can flip sign). **Aggregate-before-ratio**: yearly IROP_avg = (Σᵢ PGᵢ,t − Σᵢ PGᵢ,t−1) / Σᵢ IGᵢ,t−1 across the 30 industries, NOT an unweighted mean.
- **RSCD transcription vehicle**: Shaikh's **Appendix 7.2 sheet `iropdataUSind`** = `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix7_iropdataUSind.xlsx`; the adjustments + exclusion are **baked in** (review M3). Loader `L01_S706.py` + `_ch7_xlsx_panels.py`, byte-exact.

## 3. Why these sources (Shaikh's perspective) + rejected alternatives
Shaikh's deepest theoretical commitment in Ch7 is that the **incremental** rate — not the average — is what regulating capital actually equalizes, because mobile capital chases the return on *new* investment. He engineers S706 to make that measurable with the least contestable inputs: **gross investment is directly observed** (BEA FA 3.7ES), so IROP sidesteps the "debatable assumptions" of capital-stock estimation that burden S705. He keeps the *same* WEQ/OOH/inventory/reserve cleaning and the *same* 30-industry sample as S705 so that the average-vs-incremental contrast (Figs 7.15/7.16 vs 7.17/7.18) is a controlled comparison on one dataset.
**Rejected alternatives** (`S706_research.json`): raw NIPA GOS without WEQ (rejected — proprietor distortion); net-stock-based marginal returns (rejected — reintroduces the capital-stock assumptions IROP is designed to avoid); splicing across NIPA vintages (rejected — 2013 R&D changes IG levels, §4); no winsorization of post-crisis spikes (Shaikh leaves them raw — the volatility *is* the phenomenon, book p. 300 "turbulent, spiky, and discontinuous").

## 4. Methodological-change exposure — concordance / IO / NIPA
Same **prime-concordance** exposure as S705, with IROP-specific twists:
- **SIC↔NAICS**: NAICS-native from 1987; sample tracked across NAICS 1997→2022 revisions via `_sources/naics/` and the ADR-005 stability table (`Inputs/…/ADR-005_NAICS/data/naics_concordance_master.csv`). The same sector 50–51 / 69–70 aggregation must be preserved.
- **30-vs-31 industry panel**: identical exclusion key `SalvagedInputs/book_data/Reconstructed/Shaikh_2008_Appendix_B_industries.csv` (Shaikh 2008 Table 9.A1); inherited by transcription, not applied in code (review M3).
- **BEA benchmark re-reporting**: `IO_CHANGE_TIMELINE.md` — GOS-by-industry is re-anchored at each benchmark (1997/2002/2007/2012/2017); the **investment side (FA 3.7ES)** is separately re-based, so numerator and denominator can drift independently across vintages.
- **NIPA comprehensive revisions** (`NIPA_CHANGE_TIMELINE.md`): the **2013 R&D/IP capitalization raises gross-investment (IG) levels** directly — a first-order threat to the S706 denominator (worse than for S705, where it hits the stock). The **2018** revision re-reports GDPbyIndustry and shifts T7.11 lines (+1; resolver `NIPA_T711_FISIM_remap.md`); **2023** re-references. Extension past 2005 must exclude post-2013 R&D/IP investment to hold Shaikh's 2008 concept — end-to-end, never spliced.

## 5. Replication fidelity note
Byte-exact transcription of Shaikh's already-adjusted `iropdataUSind` panel (V03 MAE 0.0, tol 1.0%, n=576), not an end-to-end recompute — most faithful available; figure-overlay MATCH (FIGURE_REPRO_ch07). As with S705, registry `components[]`/`construction: composite` describe **Shaikh's** pipeline, not executed RSCD code (review M3); `reference_values` are round-trip-circular (Decision 0002 auditability); registry `content_type: cross_sectional` contradicts the EPR's `time_series` (review M1). The book's headline finding is preserved exactly: in the deviation panel S710, **every one of the 30 industries crosses zero**, min 4 crossings (Fabricated Metals), max 12 (Broadcast) — book p. 305.

## 6. Forward risk
As with S705, high extension exposure — amplified on the **investment denominator** by the 2013 R&D/IP capitalization (IG rises), and by IROP's intrinsic volatility (post-2008 values can exceed |2.0|; CD2 recorded 2009 = −6.93, 2015 = −6.53, 2021 = 6.72). Next BEA benchmark/NAICS re-classification re-orders the sample. Mitigation identical to S705: single-vintage end-to-end re-fetch of GOS + FA 3.7ES + T7.12 + Z.1, re-apply adjustments, re-exclude per Table 9.A1, re-compute aggregate-before-ratio, exclude R&D/IP, stamp the vintage; commit to a default presentation (raw, per Shaikh) for the volatile tail.
