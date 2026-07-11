# S205 — Methodological History Report (MHR)

**Series**: S205 — Ayres Business Cycle Index, 1867–1902 (Shaikh 2016, Figure 2.4B)
**Chapter**: 2 — "Turbulent Trends and Hidden Structures"
**Content type**: `time_series` (monthly) · **Construction**: `direct` · **Extension status**: `discontinued`
**Authored**: 2026-06-30 · **Author**: methodological-historian sub-agent (RSCD Phase-0)
**Scope note**: S204/S205/S206 are ONE data source (the Ayres 1939 monthly cyclical-component index) cut into three plotted windows — this MHR is one of three near-identical historical-only reports; cross-refs to `S204_MHR.md`, `S206_MHR.md`.

---

## 1. What the series is

A monthly index of the **cyclical component of US business activity**, windowed to **1867–1902**, plotted by Shaikh as **Figure 2.4B** ("Business Cycles, 1867–1902"). It is the second of three panels (2.4A–C) that together display ~108 years (1831–1939) of pre-NBER business-cycle fluctuations.

Book definition (verbatim, book p.57): *"Figures 2.4A–C are monthly indicators of the cyclical component of business activity, compiled by the Cleveland Trust Company (Ayres 1939, table 9, appendix A, col. 1)."* (`Inputs/Capitalism Data/…/Body_Text/ch02_turbulent_trends.md` lines 58–61; `research/S205_research.json` book_quotes p.57.)

The panel serves Shaikh's Chapter-2 theses of **recurrent** boom/bust fluctuation and the recurrence of **"Great Depressions"** — this panel carries the **1870s** Great Depression marker (the Long Depression / "Great Depression of 1873–1893"; KB fig caption `ch02_fig_2.4B.md`; body text lines 110–131; DPR §2 and §7 caveat 2 note the Long Depression 1873–1879 and the Panic of 1893 troughs). Y-axis is percentage deviation from trend, −60 to +60.

The three panels are ONE windowed series: same source, differing only in plotted year range (`research/S205_research.json` methodology_notes: *"Same Ayres source as S204 and S206; differs only in plotted year range"*).

## 2. Source lineage

- **Single source, no splice, no reindex.** One source feeds this series; no second vintage to splice, no rebasing. Construction is `direct` pass-through of the windowed monthly column (registry `S205.construction_steps`: load → extract → verify → output).
- **Coverage for THIS cut**: 1867–1902 (~432 monthly observations, ~12 obs/yr).
- **Native units**: percent deviation from trend (cyclical component), `units: percent_deviation_from_trend` (registry).
- **Agency / table id**: Cleveland Trust Company (Leonard P. Ayres), *Ayres (1939), table 9, appendix A, col. 1* — `subsource_id: AYRES_1939_T9_APP_A` (registry `S205-A`).
- **Publication**: Ayres, L. P. (1939). *Turning Points in Business Cycles.* New York: Macmillan. Public domain (pre-1964 US publication).
- **Access route**: HathiTrust Digital Library, Record `001141928` (`research/S205_research.json` primary_source.url; registry adequacy notes the same Record verified live, with a transient 403 on this particular request).
- **RSCD retrieval**: salvaged chopped table (the windowed slice of the same `Appendix2_Ayres` source used by S204). Note S205 has **no dedicated CD2 dossier** — `predecessor_ids.cd2_id: null`; it was split from the CD-era S005 (registry `predecessor_ids`, `predecessor_artifacts.cd2_source_file: null`).

## 3. Why this source, from the author's perspective

**Concept.** Shaikh needs a single, internally consistent, *long monthly* record of the cyclical component of business activity to show that turbulent fluctuation is endemic and recurrent across the whole capitalist epoch (book pp.56–59). The 1867–1902 window is where the **Long Depression of the 1870s** — one of the three canonical Great Depressions "well known to economic historians" (body text lines 104–106) — appears; that recurrence argument is the panel's whole purpose.

**Why the Ayres / Cleveland Trust composite.**
- **Long monthly reach + single consistent compiler.** One continuously constructed monthly series from a single compiler (Cleveland Trust Co.) gives Shaikh the "long view … best available data" he wants — consistent with his US-centric meta-rationale (verbatim, book p.56): the US is *"the preeminent advanced country and … generally has the best available data"* (body text lines 6–9).
- **Provenance was a personal referral, not a systematic search.** Footnote 1 (book p.57, verbatim): *"I am grateful to Professor Ravi Batra for having pointed me to this rich data source."* (body text line 61). The choice of Ayres over other historical activity indices originated in Batra's referral, not a comparative-evaluation exercise — a real, citable provenance point.

**Alternatives and why they are not used here.** The corpus holds the closest analogues but no evidence Shaikh evaluated-and-rejected them:
- **NBER Macrohistory Database** (`SalvagedInputs/methodology_library/D_data_methodology/WL-D-NBERMH-001__NBER-MacroHistory.html`) and NBER reference-cycle chronology — the standard successor concept. Research dossier: NBER macrohistory is *"a related but not equivalent series; do NOT splice"* (`research/S205_research.json` → "See S204"; DPR §7). NBER reference-cycle *dates* give turning points, not the continuous monthly deviation-from-trend index Fig 2.4 plots.
- **Census Historical Statistics of the US** (`…/D_data_methodology/WL-D-HSUS-*`) — another historical-activity route present in corpus, not used for this figure.
- **Cleveland Trust "American Business Activity since 1790"** — the sister Cleveland Trust long index; not the col.-1 cyclical component Shaikh cites.

**Author rationale for *rejecting* NBER reference-cycle dates specifically: not located in corpus.** The affirmative rationale (recurrence / Great-Depressions demonstration requiring a continuous monthly composite, book pp.57–59; Batra referral, book p.57 fn1) IS grounded above; the *comparative* rejection of NBER dates is inferable from concept but is not stated by Shaikh in the located material.

## 4. Methodological-change exposure

**Essentially none.** As a **frozen 1939 historical compilation** with no live upstream agency, S205 is INSULATED from vintage-restatement:

- **NIPA comprehensive revisions — NOT APPLICABLE.** `NIPA_CHANGE_TIMELINE.md` covers BEA comprehensive updates 1999–2023; S205 is a **pre-NIPA, 1867–1902 monthly composite** compiled in 1939. No NIPA table, line number, or reference-year rebasing touches it. No touchpoint.
- **Benchmark I-O — NOT APPLICABLE.** `IO_CHANGE_TIMELINE.md` (BEA benchmark I-O 1947–2017, SIC→NAICS) is irrelevant to a monthly aggregate-activity index with no industry dimension. No touchpoint.
- **Concordances — NOT APPLICABLE.** No SIC/NAICS, sector, or country-code mapping involved.

The only residual "change" risk is **transcription fidelity of the printed 1939 table**. There is no upstream re-basing or re-classification that can move the numbers.

## 5. Replication fidelity note

RSCD reproduces S205 by **byte-faithful transcription** of the windowed Ayres col.-1 monthly values (registry `construction_steps`: `_ayres_processor` pass-through; DPR §4 "Same monthly Ayres source as S204, windowed to 1867–1902"). V03 round-trips the chopped output against the salvaged book truth; registry `validation.reference_values` anchors `{1867: -2.0, 1885: -3.6, 1902: 4.5}` at tolerance 0.01 (DPR §9 expects MAE < 0.5%).

**No extension by design.** `extension_status: discontinued`; the EPR records the series as historical-only with no proxies and no synthetic values (parallel to `S204_EPR.md`). This is a pre-NBER composite indicator **with no clean modern successor**; RSCD does not fabricate a continuation and does not splice NBER macrohistory onto it (DPR §7).

**Honest limits.** (a) Ayres reconstructed the monthly cyclical component from a small number of annual series interpolated to monthly (DPR §7, inherited from S204) — a property of the 1939 source, not of RSCD's transcription. (b) General Chapter-2 finding F-03 (no per-series `DECOMPOSITION.md` project-wide) applies but is not S205-specific (`methodology_review/CH02_review.json` F-03). No HIGH/MED review finding targets S205.

## 6. Forward risk

**Data-vintage risk: essentially zero** — a frozen 1939 compilation cannot be restated by any live agency. Residual risks:
1. **Source-transcription fidelity** — that the digitized col.-1 values faithfully match the printed Ayres (1939) table 9, appendix A.
2. **Access to the out-of-print 1939 volume** — reliance on HathiTrust Record `001141928` (and the uncertain 2026 status of anwarshaikhecon.org Appendix 2.2 for the companion digitized data).

No forward extension is possible or intended.
