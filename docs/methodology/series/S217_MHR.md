# S217 — Methodological History Report (MHR)

**Series**: S217 — GDP per Capita of World Regions (Maddison), 1600–2000
**Chapter**: 2 (Turbulent Trends and Hidden Structures), §VIII Convergence and Divergence on a World Scale · **Group**: ch2 / CH02
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every author-intent claim traces to a cited path, or is marked "not located in corpus."

Grounding: `Technical/series_registry.json` → `series.S217`; `Technical/research/S217_research.json`;
`Technical/docs/series/S217_DPR.md` + `S217_EPR.md`; `Technical/methodology_review/CH02_review.json`
(touchpoint `S217/concordance`; hand_check `S217` World 1600=595.13 PASS); KB
`Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/Figures/ch02/ch02_fig_2.15.md`
and `.../Body_Text/ch02_turbulent_trends.md`; grounding corpus
`SalvagedInputs/methodology_library/D_data_methodology/WL-D-Maddison-*__Maddison-Project`,
`WL-D-PWT-*__Penn-World-Table`, `WL-D-WDI-*__WB-WDI`, `WL-D-GGDC-*`.

---

## 1. What the series is

S217 is Shaikh's **long-run cross-country growth exhibit**: real GDP per capita of the **World plus five
major regions** — Western Europe; Western Offshoots (United States, Canada, Australia, New Zealand); Latin
America (incl. Caribbean); Asia (East and West); Africa — from **1600 to the present (~2008)**, in **1990
International Geary–Khamis dollars**, on a **log scale**. It is the data behind **Figure 2.15** ("GDP per
Capita of World Regions 1990, International Geary–Khamis Dollars (Log Scale)", book p.70).

Book definition (Shaikh 2016, Ch2 p.69, quoted verbatim in `S217_research.json`):
> "We end this chapter with a global perspective on long-term economic development, based on data from the
> monumental work of Maddison (2003). Figure 2.15 tracks the trends in real GDP per capita from 1600 to the
> present, in five major regions of the world: Western Europe, Western Offshoots (United States, Canada,
> Australia, and New Zealand), Latin America (including the Caribbean), Asia (both East and West), and Africa."

Construction (`S217_DPR.md` §1, §4): **`direct`** — a byte-faithful port of Maddison's regional aggregates,
unpivoted from a wide chopped table (rows=region, cols=decade) to long form. Six subseries
S217-A…S217-F (World + 5 regions), ~224 chopped rows. Because slopes on the log scale represent growth
rates, the exhibit carries the chapter's closing "two-world" argument: growth in Western Europe / Western
Offshoots against near-three-century stagnation-and-decline in Asia and Africa, with rankings that change
over time (body pp.767–777; KB `ch02_fig_2.15.md` "Main Observations").

**Distinct from S218.** S217 is the **regional-aggregate** figure. Its own rich-to-poor ratio is
**regional** — 2.2 (1600), 2.4 (1700), 2.8 (1820), 6.7 (1900), 18.5 (2000) (body pp.781–782;
`S217_research.json` methodology_notes) — and Shaikh explicitly notes it *understates* true divergence
because Asia bundles Japan/South Korea/oil-rich states and Africa bundles South Africa/Egypt (body
pp.785–787), which is precisely why he then builds the country-level Figs 2.16/2.17 (**S218**). The review
hand-check confirms the lineage: **World 1600 = 595.13 matches the Maddison workbook** (`CH02_review.json`
hand_checks `S217`).

## 2. Source lineage

One provenance era, one source, ported directly (`S217_DPR.md` §3; `S217_research.json` primary_source):

- **Maddison (2003), *The World Economy: Historical Statistics* (OECD Development Centre, Paris).** The
  variable is "Per Capita GDP (PIB par habitant), 1990 International Geary–Khamis dollars"; the regional
  aggregates plotted are Western Europe, Western Offshoots, Latin America, Asia, Africa
  (`S217_research.json` primary_source.table_or_series_id; book source note p.765, verbatim:
  > "Figure 2.15 GDP per Capita of World Regions, 1990, International Geary–Khamis Dollars (Log Scale). …
  > Derived from Maddison (2003, http://www.ggdc.net/maddison/maddison-project/home.htm, Per Capita GDP:
  > PIB par habitant, 1990 International Geary–Khamis dollars)."
- **Native units / frequency:** 1990 GK$ per capita; annual where available, decennial sampling for older
  periods (`S217_research.json` primary_source.frequency; `S217_DPR.md` §7 caveat 2). Coverage 1600–2000
  (book period; figure runs to ~2008).
- **Retrieval in RSCD.** Each of the six regional subseries is read from the salvaged chopped table
  (`S217_DPR.md` §3 subseries table). No formula, no splice, no proxy — a direct transcription of Maddison's
  published regional series (`S217_research.json` construction = `direct`).
- **Grounding corpus / successor.** Maddison Project materials at
  `SalvagedInputs/methodology_library/D_data_methodology/WL-D-Maddison-001…004__Maddison-Project.*` and
  `WL-D-GGDC-*`; the named successor dataset is the **Maddison Project Database 2023** (Bolt & van Zanden
  2024; `S217_research.json` primary_source.replaced_by, extension_candidates).

## 3. Why these sources, author's perspective

- **Why Maddison (2003).** The book states the motive in its own words: it is the **"monumental work"** that
  provides a *consistent multi-century, cross-country GDP-per-capita panel in a single common standard*
  (1990 International Geary–Khamis dollars), which is what makes centuries-long regional slopes comparable on
  one log chart (body p.742, verbatim; `S217_research.json` book_quotes p.69). No other source in the
  grounding corpus offers a coherent 1600→present regional reconstruction in one PPP-anchored unit.
- **Why a common Geary–Khamis standard.** The GK multilateral-PPP dollar is what lets Shaikh read *rates of
  growth* off log slopes and compare regions at a moment (the ratio computation, body pp.781–782); a
  current-exchange-rate or single-country-deflator basis would not be comparable across regions and centuries
  (`S217_DPR.md` §6; KB `ch02_fig_2.15.md` "Key Features").
- **Rejected alternatives — Penn World Table, World Bank WDI, GGDC.** The methodology library stages the
  natural competitors (`WL-D-PWT-*__Penn-World-Table`, `WL-D-WDI-*__WB-WDI`, `WL-D-GGDC-*`), but each is
  disqualified for *this* exhibit by coverage: PWT and WDI begin only in the mid-20th century and cannot
  reach 1600, and GGDC's sectoral databases are not a multi-century per-capita GDP panel. **Shaikh gives no
  explicit written rejection of these alternatives** — the book names only Maddison as "monumental"; the
  coverage-based disqualification is inferred from the corpus, and the *explicit* author rationale for
  rejecting PWT/WDI/GGDC is **not located in corpus.**

## 4. Methodological-change exposure

The key exposure is a **base-year + region-reaggregation concordance dependency** at the successor boundary
(`CH02_review.json` touchpoint `S217/concordance`; `S217_research.json` extension_candidates.concerns;
`S217_DPR.md` §7 caveat 1; `S217_EPR.md` §2–§3):

1. **Base-year discontinuity: 1990 GK → 2011 PPP.** Maddison (2003) is in **1990 International Geary–Khamis
   dollars**; the successor **Maddison Project Database 2023** (Bolt & van Zanden 2024) is in **2011
   International-dollar PPPs**. A splice therefore requires a **rebase**, not a concatenation — the level of
   every observation shifts (`S217_research.json` extension_candidates.units/concerns).
2. **Region reaggregation.** MPD's regional definitions were **revised in 2018 and 2020** (and again in 2023);
   the "Western Offshoots / Latin America / Asia / Africa" aggregates are not guaranteed to be the same
   country sets Maddison (2003) used, so the regional lines are not drop-in comparable across the boundary
   (`S217_research.json` extension_candidates.concerns; `S217_EPR.md` §3).
3. **Table-shape caveat.** The CD2 dossier notes the MPD 2023 country table is wide (206 columns); the
   `time_series` classification here refers to the *regional aggregates*, not the full country-level table
   (`S217_research.json` extension_candidates.concerns).

This exhibit does **not** touch US NIPA or BEA I–O vintages — it is a foreign/multilateral-PPP series — so
the NIPA and IO change timelines apply only by analogy (the same "never splice across a base/definition
revision" discipline; `NIPA_CHANGE_TIMELINE.md` "Why this matters for RSCD"). Extension to MPD 2023 is
therefore **deferred** (`S217_EPR.md` §7).

## 5. Replication fidelity note

RSCD reproduces S217 as a **byte-faithful direct port** of Maddison (2003): the six regional subseries are
melted from the salvaged chopped table with no transformation, and the review's independent hand-check —
**World 1600 = 595.13 matches the Maddison workbook** — confirms the transcription (`CH02_review.json`
hand_checks `S217`, verdict PASS; `S217_DPR.md` §9). Validation on the `direct` playbook: **±1.0% tolerance**,
expected MAE < 0.5% (`S217_DPR.md` §9). Honest limits, disclosed:

- **Book period only; MPD-2023 extension deferred.** `year_range_book = [1600, 2000]` ships;
  `extension_status: deferred` because the 1990 GK → 2011 PPP rebase + region reaggregation is a manual
  Phase-9 splice, not an automated append (`S217_DPR.md` §4–§5; `S217_EPR.md` §2, §7). No synthetic or
  interpolated values are introduced (`S217_EPR.md` §4).
- **KB caption thinness (project-wide).** The authoritative source note (Maddison 2003, PIB par habitant,
  1990 GK$) lives in `S217_research.json` book_quotes (p.765); the KB figure file
  (`ch02_fig_2.15.md`) only points to "appendix 2.1" (`CH02_review.json` finding F-08, LOW).
- **No per-series DECOMPOSITION.md** (project-wide F-03): the direct-port recipe lives in `S217_DPR.md` §4 +
  registry (`CH02_review.json` finding F-03, MED).

## 6. Forward risk

- **MPD revisions re-base and re-region.** Every Maddison Project update (2018, 2020, 2023, and future
  releases) can shift the base year and redraw regional aggregates, breaking a naive continuation of the
  1990-GK regional lines; any extension must be recomputed end-to-end on a single MPD vintage, never spliced
  across a release boundary (`S217_research.json` open_questions; `S217_EPR.md` §2–§3).
- **Companion-site fragility.** Shaikh's own Appendix 2.1 / 2.2 data tables live on
  `anwarshaikhecon.org`; their 2026 availability is uncertain, so the salvaged chopped table is the durable
  anchor for the book-period series (`CH02_review.json` finding F-08 context; `S217_DPR.md` §8).
- **Region-membership drift.** Because the regional aggregates are the object here, any country reclassified
  between Maddison (2003) and a successor (e.g. reassignment within "Western Offshoots" or "Asia") changes the
  line without any error in transcription — a substantive, not clerical, forward risk.
