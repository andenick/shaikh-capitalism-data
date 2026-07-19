# S204 — Methodological History Report (MHR)

**Series**: S204 — Ayres Business Cycle Index, 1831–1866 (Shaikh 2016, Figure 2.4A)
**Chapter**: 2 — "Turbulent Trends and Hidden Structures"
**Content type**: `time_series` (monthly) · **Construction**: `direct` · **Extension status**: `discontinued`
**Authored**: 2026-06-30 · **Author**: methodological-historian sub-agent (RSCD Phase-0)
**Scope note**: S204/S205/S206 are ONE data source (the Ayres 1939 monthly cyclical-component index) cut into three plotted windows — this MHR is one of three near-identical historical-only reports; cross-refs to `S205_MHR.md`, `S206_MHR.md`.

---

## 1. What the series is

A monthly index of the **cyclical component of US business activity**, windowed to **1831–1866**, plotted by Shaikh as **Figure 2.4A** ("Business Cycles, 1831–1866"). It is the first of three panels (2.4A–C) that together display ~108 years (1831–1939) of pre-NBER business-cycle fluctuations.

Book definition (verbatim, book p.57): *"Figures 2.4A–C are monthly indicators of the cyclical component of business activity, compiled by the Cleveland Trust Company (Ayres 1939, table 9, appendix A, col. 1)."* (`Inputs/Capitalism Data/…/Body_Text/ch02_turbulent_trends.md` lines 58–61; `research/S204_research.json` book_quotes p.57.)

The panel serves three of Shaikh's Chapter-2 theses (book pp.57–59): the **recurrence** of booms and busts "in never ending sequence"; the **association of wars with upturns** (this panel marks the Mexican War and the US Civil War 1861–1864); and the recurrence of **"Great Depressions"** — this panel carries the **1840s** Great Depression marker (KB fig caption `ch02_fig_2.4A.md`; body text lines 76–107). Y-axis is percentage deviation from trend, −60 to +60.

The three panels are ONE windowed series: same source, differing only in plotted year range (`research/S205_research.json` methodology_notes; registry `S204.subseries.S204-A`).

## 2. Source lineage

- **Single source, no splice, no reindex.** One source feeds this series; there is no second vintage to splice and no rebasing step. Construction is `direct` pass-through of the windowed monthly column (registry `S204.construction_steps`: load → extract → verify → output).
- **Coverage for THIS cut**: 1831–1866 (~432 monthly observations, ~12 obs/yr).
- **Native units**: percent deviation from trend (cyclical component), `units: percent_deviation_from_trend` (registry).
- **Agency / table id**: Cleveland Trust Company (Leonard P. Ayres), *Ayres (1939), table 9, appendix A, col. 1* — `subsource_id: AYRES_1939_T9_APP_A` (registry `S204-A`).
- **Publication**: Ayres, L. P. (1939). *Turning Points in Business Cycles.* New York: Macmillan. Public domain (pre-1964 US publication).
- **Access route**: HathiTrust Digital Library, Record `001141928` (`research/S204_research.json` primary_source.url; registry adequacy notes Record reachable HTTP 200 in the 2026-05-18 scan). This is the out-of-print 1939 volume's access path.
- **RSCD retrieval**: salvaged chopped table (`SalvagedInputs/…/Appendix2_Ayres.xlsx` → `ch02/Appendix2_Ayres.csv`, per DPR §4 and registry `predecessor_artifacts.cd2_source_file`).

## 3. Why this source, from the author's perspective

**Concept.** Shaikh needs a single, internally consistent, *long monthly* record of the cyclical component of business activity — deviation of output around its growth trend — reaching back before the Civil War, to demonstrate that turbulent fluctuation is endemic and recurrent across the whole capitalist epoch, not a modern artifact (book pp.56–59). A monthly composite reaching to 1831 lets him show booms/busts, war-upturn/peace-downturn, and recurrent Great Depressions on one continuous axis; discrete peak/trough chronologies cannot render the *shape* of the fluctuation the way this index does.

**Why the Ayres / Cleveland Trust composite.**
- **Long monthly reach + single consistent compiler.** The Ayres table gives one continuously constructed monthly series from 1831, from a single compiler (Cleveland Trust Co.), i.e. exactly the "long view … best available data" Shaikh wants — consistent with his stated US-centric meta-rationale (verbatim, book p.56): the US is *"the preeminent advanced country and … generally has the best available data"* (body text lines 6–9).
- **Provenance was a personal referral, not a systematic search.** Footnote 1 (book p.57, verbatim): *"I am grateful to Professor Ravi Batra for having pointed me to this rich data source."* (body text line 61; KB fig caption `ch02_fig_2.4A.md` note). This is a real, citable provenance point: the choice of Ayres over other historical activity indices originated in Batra's referral, not a comparative-evaluation exercise.

**Alternatives and why they are not used here.** The corpus holds the two closest modern/historical analogues but no evidence Shaikh evaluated-and-rejected them:
- **NBER Macrohistory Database** (`SalvagedInputs/methodology_library/D_data_methodology/WL-D-NBERMH-001__NBER-MacroHistory.html`) and NBER reference-cycle chronology — the standard modern successor concept. The research dossier flags NBER macrohistory (m12003 etc.) as *"a related but not equivalent series; do NOT splice"* (`research/S204_research.json` extension_candidates; DPR §7 caveat 1). NBER reference-cycle *dates* give turning points, not a continuous monthly deviation-from-trend index — a different object from what Fig 2.4 plots.
- **Census Historical Statistics of the US** (`…/D_data_methodology/WL-D-HSUS-*`) — another historical-activity route, present in corpus, not used for this figure.
- **Cleveland Trust "American Business Activity since 1790"** — the sister Cleveland Trust long index; not the col.-1 cyclical component Shaikh cites.

**Author rationale for *rejecting* NBER reference-cycle dates specifically: not located in corpus.** The affirmative rationale (recurrence / wars / Great-Depressions demonstration requiring a continuous monthly composite, book pp.57–59; Batra referral, book p.57 fn1) IS grounded above; the *comparative* rejection of NBER dates is inferable from concept but is not stated by Shaikh in the located material.

## 4. Methodological-change exposure

**Essentially none.** As a **frozen 1939 historical compilation** with no live upstream agency, S204 is INSULATED from the vintage-restatement machinery that governs Shaikh's modern series:

- **NIPA comprehensive revisions — NOT APPLICABLE.** `NIPA_CHANGE_TIMELINE.md` covers BEA comprehensive updates 1999–2023 (software/R&D capitalization, FISIM restatement, T7.11 line shifts). S204 is a **pre-NIPA, 1831–1866 monthly composite** compiled in 1939; no NIPA table, line number, or reference-year rebasing touches it. No touchpoint.
- **Benchmark I-O — NOT APPLICABLE.** `IO_CHANGE_TIMELINE.md` (BEA benchmark I-O 1947–2017, SIC→NAICS) is irrelevant to a monthly aggregate-activity index that has no industry dimension. No touchpoint.
- **Concordances — NOT APPLICABLE.** No SIC/NAICS, sector, or country-code mapping is involved.

The only residual "change" risk is **transcription fidelity of the printed 1939 table** — i.e. whether the digitized col.-1 values match the Macmillan/Cleveland Trust print. There is no upstream re-basing or re-classification that can move the numbers.

## 5. Replication fidelity note

RSCD reproduces S204 by **byte-faithful transcription** of the windowed Ayres col.-1 monthly values (registry `construction_steps`: `_ayres_processor` pass-through; DPR §4 "Read Ayres (1939) monthly values … filter to 1831–1866"). V03 round-trips the chopped output against the salvaged book truth; registry `validation.reference_values` anchors `{1831: 5.4, 1849: 0.1, 1866: 1.6}` at tolerance 0.01 (DPR §9 expects MAE < 0.5%).

**No extension by design.** `extension_status: discontinued`; the EPR (`S204_EPR.md` §2) records "N/A. Historical-only series," with explicit no-proxy / no-synthetic disclosures. This is a pre-NBER composite indicator **with no clean modern successor**; RSCD does not fabricate a continuation and does not splice NBER macrohistory onto it (DPR §7).

**Honest limits.** (a) Ayres reconstructed the monthly cyclical component from a small number of annual series interpolated to monthly (DPR §7 caveat 2) — a property of the 1939 source, not of RSCD's transcription. (b) The general Chapter-2 finding F-03 (no per-series `DECOMPOSITION.md` project-wide; construction folded into DPR §4 + registry) applies here but is not S204-specific (`methodology_review/CH02_review.json` F-03). No HIGH/MED review finding targets S204.

## 6. Forward risk

**Data-vintage risk: essentially zero** — a frozen 1939 compilation cannot be restated by any live agency. The only residual risks are:
1. **Source-transcription fidelity** — that the digitized col.-1 values faithfully match the printed Ayres (1939) table 9, appendix A.
2. **Access to the out-of-print 1939 volume** — reliance on HathiTrust Record `001141928` (and, for the companion digitized data, the uncertain 2026 status of anwarshaikhecon.org Appendix 2.2 — open question in `research/S204_research.json`).

No forward extension is possible or intended.
