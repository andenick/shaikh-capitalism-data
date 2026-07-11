# S709 — Methodological History Report (MHR)

**Series**: S709 · Figure 7.16 — US Industry ROP Deviations from Average, 1987–2005 (38 small-multiple panels)
**Chapter**: 7 (Real Competition) · Group `ch07`/`CH07`
**Status**: `book_period_validated` · `content_type: cross_sectional` (registry) / **time_series** (EPR; review M1) · `construction: formula` · `publish: true`
**Author intent reasoned from**: Shaikh, *Capitalism* (2016), ch.7 p. 305; Appendix 7.1 §III (pp. 857–859).
**Sources read**: `Technical/research/S709_research.json`, `Technical/series_registry.json` (S709), `Technical/methodology_review/CH07_review.json` (M1/M2/L1, touchpoint S709), `Technical/code/L01_loaders/L01_S709.py`, `SalvagedInputs/book_data/Reconstructed/Shaikh_2008_Appendix_B_industries.csv`.

---

## 1. What the series is
S709 is the **deviation panel that operationalises Shaikh's turbulent-equalization claim for average profit rates**: for each industry, dev_i,t = ROP_i,t − ROP_avg,t (industry rate minus the All-Private aggregate), plotted as 38 small-multiple sub-charts with a zero line. Book definition (page-cited, `S709_research.json`, p. 305): *"This is clearer in figure 7.16, which displays the deviations of individual sectoral profit rates from the average rate of profit. Industries whose profit rates cross the average rate have deviations that change sign … cross the zero line … Of the thirty industries in this sample, eighteen display this tendency, while twelve do not (seven remain persistently above and five persistently below)."* Added by **Decision 0004** to close the Fig 7.16 gap the original 8-series allotment left open.

## 2. Source lineage
- **Parent series**: **S705** (US Industry Average ROP). S709 is a **one-line algebraic transform** of S705's output; it ingests **no new data**.
- **Inherited lineage** (all of S705's): BEA GDPbyInd_VA_NAICS + Fixed Asset Tables 3.1ES/3.4ES/3.7ES/3.8ES + NIPA T7.12 + Flow of Funds L.109/L.114–117, with the **WEQ / OOH / inventory / reserve** adjustments and the **31→30 industry exclusion** all baked into `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix7_ropdataUSind.xlsx`.
- **Transform**: dev_i,t = ROP_i,t − ROP_avg,t, where ROP_avg = Σᵢ(PGᵢ−DEPᵢ)/Σᵢ Kᵢ(−1) (the aggregate-before-ratio All-Private line, book p. 305 "the overall profit rate of all included private industries" ⇒ weighted aggregate, not unweighted mean).
- **Implementation nuance (review M2)**: the registry marks `construction: formula` with `components = [S705_industry_ROP, S705_All-Private_aggregate]`, but `L01_S709.py:21-28` and `_ch7_xlsx_panels.py:86-109` in fact **read Shaikh's pre-computed `_Deviation` columns** from the same xlsx rather than computing industry−aggregate — *more* faithful in practice (reproduces Shaikh's own deviation values exactly), but no V03 check verifies the dev=industry−aggregate identity.
- **Native units**: rate deviation (decimal). **Panel count**: 38 (30 industries + 6 sub-aggregates like Manufacturing / Manufacturing D / Manufacturing ND / Real & Rental — book PDF p. 346) — the 30-vs-38 distinction (review touchpoint S709) is text-says-30, figure-shows-38.

## 3. Why these sources (Shaikh's perspective) + rejected alternatives
Shaikh's argument needs the deviation view because *levels* clustering (Fig 7.15) is visually ambiguous — persistent outliers can hide crossing. Subtracting the All-Private aggregate and drawing a zero line makes **crossing (equalization) directly countable**: an industry that equalizes has a deviation that changes sign. He deliberately uses the **weighted All-Private aggregate** as the baseline (not an unweighted industry mean) so the benchmark is the actual economy-wide regulating rate. He warns (p. 305) that highly-trended deviations (Nonmetallic Minerals, Machinery, Printing, Rentals) make period-average deviations a poor proxy for econometric long-run values — motivating the later econometric tests.
**Rejected alternatives**: computing deviations against an *unweighted* industry mean (rejected — book wording "overall profit rate of all included private industries" ⇒ aggregate); recomputing dev from scratch rather than reading Shaikh's `_Deviation` columns (RSCD chose the pre-computed columns for byte-exact fidelity — review M2).

## 4. Methodological-change exposure (concordance / IO / NIPA)
S709 **inherits S705's exposure one-for-one** — it is the deviation of the same 30-industry NAICS panel:
- **SIC↔NAICS / NAICS-revision**: same NAICS-native 30-industry sample tracked via `_sources/naics/` + the ADR-005 stability table; the 38-panel set (with sub-aggregates) must be mapped consistently across NAICS 1997→2022. See `_timelines/IO_CHANGE_TIMELINE.md`.
- **30-vs-31 industry panel**: same exclusion key `Shaikh_2008_Appendix_B_industries.csv`; the deviation baseline (All-Private) is defined over exactly the 30 retained industries, so a change in the exclusion set *shifts every deviation*.
- **BEA benchmark + NIPA revisions**: any S705 re-run (2013 R&D/IP; 2018 T7.11 +1 / GDPbyInd re-report; 2023 re-reference — `NIPA_CHANGE_TIMELINE.md`) propagates directly; **deviations must be recomputed from the re-run, never spliced across vintages** (`S709_research.json` anti-degradation).
Because it is a difference of two co-vintaged quantities, S709 is slightly *less* sensitive to level re-basing than S705 (a common shift cancels) but *fully* sensitive to any change in the industry sample or the aggregate definition.

## 5. Replication fidelity note
S709 reproduces Shaikh's **pre-computed deviation columns** byte-exact (V03 MAE 0.0, tol 0.5%, n=589) — the *most* faithful route, but it means the registry's `formula` label describes an identity the code does not itself execute or verify (review M2): no loader computes dev = industry − aggregate and no V03 asserts it. `reference_values` are token single-value picks tracing to real data (review L1). Registry `content_type: cross_sectional` again contradicts the EPR's `time_series` (review M1). The book's "18 of 30 cross zero (7 above, 5 below)" finding is verified verbatim against the KB.

## 6. Forward risk
Inherits all S705 forward risk (next BEA benchmark/NAICS re-classification; post-2013 R&D/IP capital-concept trap; Z.1 line drift). Additional derivative-specific risk: if a future S705 extension changes the **industry sample or the All-Private aggregate definition**, every S709 deviation moves — so S709 must always be **regenerated from the same S705 re-run**, and the pre-computed-column shortcut must be re-derived (or the dev=industry−aggregate identity must be recomputed) on the new vintage. Add a V03 identity check (dev == industry − aggregate) to harden it.
