# S206 — Methodological History Report (MHR)

**Series**: S206 — Ayres Business Cycle Index, 1903–1939 (Shaikh 2016, Figure 2.4C)
**Chapter**: 2 — "Turbulent Trends and Hidden Structures"
**Content type**: `time_series` (monthly) · **Construction**: `direct` · **Extension status**: `discontinued`
**Authored**: 2026-06-30 · **Author**: methodological-historian sub-agent (RSCD Phase-0)
**Scope note**: S204/S205/S206 are ONE data source (the Ayres 1939 monthly cyclical-component index) cut into three plotted windows — this MHR is one of three near-identical historical-only reports; cross-refs to `S204_MHR.md`, `S205_MHR.md`.

---

## 1. What the series is

A monthly index of the **cyclical component of US business activity**, windowed to **1903–1939**, plotted by Shaikh as **Figure 2.4C** ("Business Cycles, 1903–1939"). It is the third and last of three panels (2.4A–C) that together display ~108 years (1831–1939) of pre-NBER business-cycle fluctuations; the window ends at 1939, the Ayres source's publication year.

Book definition (verbatim, book p.57): *"Figures 2.4A–C are monthly indicators of the cyclical component of business activity, compiled by the Cleveland Trust Company (Ayres 1939, table 9, appendix A, col. 1)."* (`Inputs/Capitalism Data/…/Body_Text/ch02_turbulent_trends.md` lines 58–61; `research/S206_research.json` book_quotes p.57.)

The panel is where Shaikh's two headline Chapter-2 associations land most dramatically (body text lines 100–107; KB fig caption `ch02_fig_2.4C.md`): the **war–upturn / peace–downturn** association (this panel marks **World War I**, ~1914–1918, with an upturn and its end with a downturn), and the recurrence of **"Great Depressions"** — this panel carries the **1930s** Great Depression (1929–1939), "the most striking element of all," shown as the deepest plunge in the whole 108-year record. Y-axis is percentage deviation from trend, −60 to +60.

The three panels are ONE windowed series: same source, differing only in plotted year range (`research/S206_research.json` methodology_notes; registry `S206.subseries.S206-A`).

## 2. Source lineage

- **Single source, no splice, no reindex.** One source feeds this series; no second vintage to splice, no rebasing. Construction is `direct` pass-through of the windowed monthly column (registry `S206.construction_steps`: load → extract → verify → output).
- **Coverage for THIS cut**: 1903–1939 (~439 monthly observations, ~12 obs/yr).
- **Native units**: percent deviation from trend (cyclical component), `units: percent_deviation_from_trend` (registry).
- **Agency / table id**: Cleveland Trust Company (Leonard P. Ayres), *Ayres (1939), table 9, appendix A, col. 1* — `subsource_id: AYRES_1939_T9_APP_A` (registry `S206-A`).
- **Publication**: Ayres, L. P. (1939). *Turning Points in Business Cycles.* New York: Macmillan. Public domain (pre-1964 US publication). The series ends in 1939 because that is where the source volume itself ends (DPR §7 caveat 2: "Last subperiod of Ayres index; ends 1939 (book publication year)").
- **Access route**: HathiTrust Digital Library, Record `001141928` (`research/S206_research.json` primary_source.url; registry adequacy notes Record live HTTP 200 in the 2026-05-18 scan — this cut carries the highest adequacy score, 95).
- **RSCD retrieval**: salvaged chopped table (the windowed slice of the same `Appendix2_Ayres` source used by S204/S205). Like S205, S206 has **no dedicated CD2 dossier** — `predecessor_ids.cd2_id: null`; split from CD-era S006 (registry `predecessor_ids`, `predecessor_artifacts.cd2_source_file: null`).

## 3. Why this source, from the author's perspective

**Concept.** Shaikh needs a single, internally consistent, *long monthly* record of the cyclical component of business activity to show that turbulent fluctuation is endemic and recurrent across the whole capitalist epoch (book pp.56–59). The 1903–1939 window is the payoff panel: it renders the **1930s Great Depression** — the third and deepest of the recurrent Great Depressions — and the **WWI war-upturn**, the two patterns Shaikh most wants the reader to see (body text lines 100–107). A continuous monthly deviation-from-trend index is what makes the *depth* and *shape* of the 1930s plunge legible against earlier cycles.

**Why the Ayres / Cleveland Trust composite.**
- **Long monthly reach + single consistent compiler.** One continuously constructed monthly series from a single compiler (Cleveland Trust Co.), consistent through 1939, lets Shaikh compare the 1930s trough directly against the 1840s and 1870s on one axis — the "long view … best available data" he wants, consistent with his US-centric meta-rationale (verbatim, book p.56): the US is *"the preeminent advanced country and … generally has the best available data"* (body text lines 6–9).
- **Provenance was a personal referral, not a systematic search.** Footnote 1 (book p.57, verbatim): *"I am grateful to Professor Ravi Batra for having pointed me to this rich data source."* (body text line 61). The choice of Ayres over other historical activity indices originated in Batra's referral, not a comparative-evaluation exercise — a real, citable provenance point.

**Alternatives and why they are not used here.** The corpus holds the closest analogues but no evidence Shaikh evaluated-and-rejected them:
- **NBER Macrohistory Database** (`SalvagedInputs/methodology_library/D_data_methodology/WL-D-NBERMH-001__NBER-MacroHistory.html`) and NBER reference-cycle chronology — the standard successor concept; and NBER's own reference-cycle dates would cover the 1929–1939 contraction. Research dossier: NBER macrohistory is *"a related but not equivalent series; do NOT splice"* (`research/S206_research.json` → "See S204"; DPR §7). NBER reference-cycle *dates* give turning points, not the continuous monthly deviation-from-trend index Fig 2.4 plots.
- **Census Historical Statistics of the US** (`…/D_data_methodology/WL-D-HSUS-*`) — another historical-activity route present in corpus, not used for this figure.
- **Cleveland Trust "American Business Activity since 1790"** — the sister Cleveland Trust long index; not the col.-1 cyclical component Shaikh cites.

**Author rationale for *rejecting* NBER reference-cycle dates specifically: not located in corpus.** The affirmative rationale (recurrence / wars / Great-Depressions demonstration requiring a continuous monthly composite, book pp.57–59; Batra referral, book p.57 fn1) IS grounded above; the *comparative* rejection of NBER dates is inferable from concept but is not stated by Shaikh in the located material.

## 4. Methodological-change exposure

**Essentially none.** As a **frozen 1939 historical compilation** with no live upstream agency, S206 is INSULATED from vintage-restatement:

- **NIPA comprehensive revisions — NOT APPLICABLE.** `NIPA_CHANGE_TIMELINE.md` covers BEA comprehensive updates 1999–2023; S206 is a **pre-NIPA, 1903–1939 monthly composite** compiled in 1939 (it ends before the modern NIPAs even began). No NIPA table, line number, or reference-year rebasing touches it. No touchpoint.
- **Benchmark I-O — NOT APPLICABLE.** `IO_CHANGE_TIMELINE.md` (BEA benchmark I-O 1947–2017, SIC→NAICS) is irrelevant to a monthly aggregate-activity index with no industry dimension. No touchpoint.
- **Concordances — NOT APPLICABLE.** No SIC/NAICS, sector, or country-code mapping involved.

The only residual "change" risk is **transcription fidelity of the printed 1939 table**. There is no upstream re-basing or re-classification that can move the numbers.

## 5. Replication fidelity note

RSCD reproduces S206 by **byte-faithful transcription** of the windowed Ayres col.-1 monthly values (registry `construction_steps`: `_ayres_processor` pass-through; DPR §4 "Same monthly Ayres source as S204/S205, windowed to 1903–1939"). V03 round-trips the chopped output against the salvaged book truth; registry `validation.reference_values` anchors `{1903: -11.0, 1921: -21.7, 1939: -24.9}` at tolerance 0.01 (DPR §9 expects MAE < 0.5%) — the deep negative anchors at 1921 and 1939 reflect the post-WWI downturn and the 1930s Depression trough.

**No extension by design.** `extension_status: discontinued`; the EPR records the series as historical-only with no proxies and no synthetic values (parallel to `S204_EPR.md`). This is a pre-NBER composite indicator **with no clean modern successor**; RSCD does not fabricate a continuation and does not splice NBER macrohistory onto it (DPR §7).

**Honest limits.** (a) Ayres reconstructed the monthly cyclical component from a small number of annual series interpolated to monthly (DPR §7, inherited from S204) — a property of the 1939 source, not of RSCD's transcription. (b) General Chapter-2 finding F-03 (no per-series `DECOMPOSITION.md` project-wide) applies but is not S206-specific (`methodology_review/CH02_review.json` F-03). No HIGH/MED review finding targets S206.

## 6. Forward risk

**Data-vintage risk: essentially zero** — a frozen 1939 compilation cannot be restated by any live agency. Residual risks:
1. **Source-transcription fidelity** — that the digitized col.-1 values faithfully match the printed Ayres (1939) table 9, appendix A.
2. **Access to the out-of-print 1939 volume** — reliance on HathiTrust Record `001141928` (and the uncertain 2026 status of anwarshaikhecon.org Appendix 2.2 for the companion digitized data).

No forward extension is possible or intended.
