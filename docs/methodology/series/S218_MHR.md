# S218 — Methodological History Report (MHR)

**Series**: S218 — GDP per Capita Richest Four and Poorest Four Countries (Maddison), 1600–2000
**Chapter**: 2 (Turbulent Trends and Hidden Structures), §VIII Convergence and Divergence on a World Scale · **Group**: ch2 / CH02
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every author-intent claim traces to a cited path, or is marked "not located in corpus."

Grounding: `Technical/series_registry.json` → `series.S218`; `Technical/research/S218_research.json`
(carries the verbatim "Qutar" typo quote + exclusion rule); `Technical/docs/series/S218_DPR.md` + `S218_EPR.md`;
`Technical/methodology_review/CH02_review.json`; KB
`Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/Figures/ch02/ch02_fig_2.16.md`
and `ch02_fig_2.17.md`, `.../Body_Text/ch02_turbulent_trends.md`; grounding corpus
`SalvagedInputs/methodology_library/D_data_methodology/WL-D-Maddison-*__Maddison-Project`,
`WL-D-PWT-*`, `WL-D-WDI-*`, `WL-D-GGDC-*`; sibling `Technical/docs/methodology/series/S217_MHR.md`.

---

## 1. What the series is

S218 is Shaikh's **country-level global-inequality exhibit**: at each decennial benchmark it averages the
GDP per capita of the **four richest** and the **four poorest** countries in the world (with an explicit
exclusion rule), plus their **ratio**. It feeds **BOTH Figure 2.16** ("GDP per Capita Richest Four and
Poorest Four Countries", book p.71) **and Figure 2.17** ("Ratio of the GDP per Capita of the Richest Four
to the Poorest Four Countries", book p.72) — Fig 2.17 is simply the ratio of the two means from Fig 2.16
(`S218_research.json` methodology_notes; `S218_DPR.md` §1). The constructed averages are also tabulated as a
book cross-check in **Appendix Table 2.1.1 (book p.766)** — "Richest 4 Average / Poorest 4 Average GDP per
capita" for 1600, 1700, 1820, then every 20 years to 2000 (`S218_research.json` primary_source.table_or_series_id;
body p.829 "see appendix 2.1, table 1").

Book definition (Shaikh 2016, Ch2 p.70, quoted verbatim in `S218_research.json`):
> "Figure 2.16 therefore displays the GDPs per capita of the richest and poorest four countries in the world
> in 1600, 1700, 1820, and every decade thereafter (appendix 2.1 Data Sources and Methods). A notable feature
> is the large drop of the poor-country GDP per capita in the postwar period, and again during the neoliberal
> era (after 1980). Figure 2.17 tracks the corresponding rich-to-poor ratio, which stands at 2.8 in 1600, 3.4
> in 1700, 3.8 in 1820, 7.1 in 1900, and 64.2 in 2000."

Three subseries (`S218_DPR.md` §3): S218-A RICHEST 4 (with Shaikh exclusions), S218-B POOREST 4, S218-C the
computed RATIO; ~63 chopped rows. The exhibit is *sharper* than the regional Fig 2.15/S217 precisely because
country-level ranking strips out the internal-averaging that masks divergence (body pp.785–787; KB
`ch02_fig_2.16.md` "Significance") — the ratio climbs **2.8 (1600) → 64.2 (2000)** versus the regional
2.2 → 18.5.

## 2. Source lineage

One source panel, plus a Shaikh-defined **re-rank / average / exclusion** construction
(`S218_DPR.md` §3–§4; `S218_research.json` primary_source, components, formula):

- **Maddison (2003) country-level GDP-per-capita panel**, "Per Capita GDP: PIB par habitant, **1990
  International Geary–Khamis dollars**" (`S218_research.json` primary_source; same source as S217 —
  `S217_MHR.md` §2). Coverage 1600–2000, decennial after 1820.
- **Construction (formula).** For each decade: rank all countries by GDP/cap, take the mean of the **top 4**
  and the mean of the **bottom 4**, and form the ratio: `richest4_avg[t] = mean(top 4, excluding
  Kuwait/Qatar/Venezuela); poorest4_avg[t] = mean(bottom 4); ratio[t] = richest4_avg / poorest4_avg`
  (`S218_research.json` formula; `S218_DPR.md` §4).
- **Shaikh's exclusion rule (verbatim — typo preserved).** Book source note p.765
  (`S218_research.json` book_quotes, `verbatim_check: true`):
  > "Derived from Maddison (2003, http://www.ggdc.net/maddison/maddison-project/home.htm, Per Capita GDP:
  > PIB par habitant, 1990 International Geary–Khamis dollars). Kuwait, Qutar, and so on were removed from the
  > top four when they show up in 1950, because their inclusion dramatically overstates the average. Venezuela
  > shows up in the top four in 1980, but was removed on grounds of symmetry with Kuwait, even though its
  > effect is small. And regions such as "16 Asians" were used when there was no data on the individual
  > countries."

  The original Appendix 2.1 prints **"Qutar"** for "Qatar"; this MHR **preserves the typo verbatim** per the
  no-paraphrase rule (`S218_research.json` open_questions: "Note typo in original Appendix 2.1: 'Qutar' should
  be 'Qatar' (book p.765) — preserved verbatim in quote").
- **Regional-aggregate fallback.** Where no individual-country datum exists, Shaikh substitutes Maddison
  regional aggregates (e.g. "16 Asians", "15 Latin American") — used mainly in the earlier/poorest-tail years
  (`S218_research.json` components period [1600,1900]; `S218_DPR.md` §1).
- **Retrieval in RSCD.** RSCD reads the pre-computed RICHEST 4 / POOREST 4 / RATIO rows from the salvaged
  chopped table (`S218_DPR.md` §4). Grounding corpus / successor: Maddison Project materials at
  `SalvagedInputs/methodology_library/D_data_methodology/WL-D-Maddison-*`; successor = MPD 2023
  (Bolt & van Zanden 2024; `S218_research.json` primary_source.replaced_by).

## 3. Why these sources, author's perspective

- **Why Maddison (2003).** Same rationale as S217: it is the only source giving a **consistent, multi-century,
  cross-country per-capita GDP panel in one common Geary–Khamis standard** — the "monumental work" (book p.70,
  verbatim in body; `S217_MHR.md` §3). A country-level richest/poorest ranking back to 1600 is possible *only*
  because Maddison reconstructs individual-country levels in a comparable unit.
- **Why the country-level richest-4 / poorest-4 cut at all.** The book states the motive: the regional ratio
  (Fig 2.15) "understates the true divergence between rich and poor nations because Asia includes Japan, South
  Korea, and various oil-rich countries, while Africa includes South Africa, Egypt, and others" — so Shaikh
  goes to the country level "therefore" to get a cleaner measure of the actual extremes (body pp.785–787,
  verbatim; KB `ch02_fig_2.16.md` "Significance").
- **Why the exclusion rule (the most distinctive design choice).** Shaikh excludes Kuwait/**Qutar**/Venezuela
  from the *top four* because their oil-rents make them **outliers whose inclusion "dramatically overstates the
  average"** — i.e. they are rich for resource-rent reasons, not for the capitalist-development reasons the
  exhibit is meant to track. Venezuela (top-4 in 1980) is removed "on grounds of symmetry with Kuwait, even
  though its effect is small" — an explicit, documented, symmetric adjustment rather than a silent one (book
  p.765, verbatim above; `S218_DPR.md` §1). This is a *substantive theoretical filter*, not data cleaning:
  the point is the structural rich/poor gap generated by capitalist development, which oil-rent principalities
  would distort.
- **Rejected alternatives — PWT, WDI, GGDC.** As with S217, the corpus stages these
  (`WL-D-PWT-*`, `WL-D-WDI-*`, `WL-D-GGDC-*`) but each is disqualified for a 1600-origin ranking by coverage
  (PWT/WDI begin only mid-20th century). **Shaikh gives no explicit written rejection** of them; the
  coverage-based disqualification is inferred, and the *explicit* author rationale is **not located in corpus.**

## 4. Methodological-change exposure

Same **base-year + reaggregation concordance dependency** as S217, plus an **exclusion-rule re-application**
burden that makes S218's extension strictly harder (`S218_research.json` extension_candidates.concerns;
`S218_DPR.md` §7; `S218_EPR.md` §2):

1. **Base-year discontinuity: 1990 GK → 2011 PPP.** Maddison (2003) is in 1990 GK$; MPD 2023 is in 2011 PPP.
   For the **level** series (S218-A/B) this requires a rebase; for the **ratio** (S218-C) it is
   **base-year-invariant** — numerator and denominator scale together, so the ratio should be unaffected by
   the base change (`S218_DPR.md` §7 caveat 2; `S218_research.json` extension_candidates.concerns).
2. **No lazy splice — the ranking must be recomputed from the country panel.** Because membership of the
   top-4/bottom-4 changes with every data revision, an extension cannot splice the *averages*; it must re-rank
   the full MPD 2023 country panel each decade and re-average (`S218_research.json`
   extension_candidates.concerns; anu-framework no-lazy-splice rule).
3. **Exclusion-rule re-application.** Shaikh's Kuwait/Qatar/Venezuela exclusions must be re-applied to the
   modern panel, and the modern panel may require **additional** exclusions (e.g. Macao, Luxembourg) on the
   same oil-rent/city-state outlier logic — a non-mechanical judgment that must be documented in the EPR
   (`S218_DPR.md` §7 caveat 3; `S218_EPR.md` §2; `S218_research.json` open_questions).
4. **No US-vintage exposure.** Like S217, this is a foreign/multilateral-PPP series; the NIPA/BEA-I–O change
   timelines apply only by analogy (the same never-splice-across-a-revision discipline;
   `NIPA_CHANGE_TIMELINE.md`).

## 5. Replication fidelity note

RSCD reproduces S218 by reading the pre-computed RICHEST 4 / POOREST 4 / RATIO rows from the salvaged chopped
table and unpivoting to long form; validation on the `formula` playbook, **±1.0% tolerance**, expected MAE
< 0.5% (`S218_DPR.md` §4, §9). The book's own **Appendix Table 2.1.1 (p.766)** lists the actual top-4/bottom-4
country identities by year and the constructed averages — "an invaluable cross-check" against the chopped
series (`S218_research.json` methodology_notes, primary_source). Honest limits, disclosed:

- **Exclusion-rule construction documented, not re-derived.** RSCD ships Shaikh's *result* (the
  already-excluded averages) faithfully; it does not itself re-rank a raw country panel for the book period —
  the exclusion logic is documented in `S218_DPR.md` §4 and the verbatim source note, not re-executed
  (`S218_EPR.md` §2).
- **"Qutar" typo preserved verbatim** wherever the source note is quoted (this MHR §2–§3), per the
  no-paraphrase rule (`S218_research.json` open_questions).
- **MPD-2023 re-application deferred.** `year_range_book = [1600, 2000]` ships; `extension_status: deferred`
  because re-ranking + re-excluding on MPD 2023 is a non-trivial manual task (`S218_DPR.md` §5;
  `S218_EPR.md` §2, §7). No synthetic/interpolated values (`S218_EPR.md` §4).
- **No per-series DECOMPOSITION.md** (project-wide F-03): construction lives in `S218_DPR.md` §4 + registry
  `formula`/`components` (`CH02_review.json` finding F-03, MED). CD2 had no dedicated S018 dossier — S017
  covered all three figures jointly; this is a fresh dossier (`S218_research.json` open_questions).

## 6. Forward risk

- **Exclusion-rule membership shifts in the modern panel.** The top-4/bottom-4 identities change with each MPD
  revision, and the outlier set to exclude is not fixed — Macao and Luxembourg (city-state / financial-hub
  outliers) are candidate additions on Shaikh's own logic, but adding them is a *judgment* that alters the
  published averages without any transcription error (`S218_DPR.md` §7 caveat 3; `S218_EPR.md` §2).
- **Levels break, the ratio survives.** Any future re-base (2011 PPP → next reference year) breaks the level
  series S218-A/B but leaves the ratio S218-C invariant — so the most robust extendable object is Fig 2.17's
  ratio, not the Fig 2.16 levels (`S218_DPR.md` §7 caveat 2).
- **Companion-site fragility + re-region.** As with S217, Shaikh's Appendix 2.1/2.2 tables on
  `anwarshaikhecon.org` have uncertain 2026 availability, and MPD region/country reclassification can move the
  ranking; the salvaged chopped table + Appendix Table 2.1.1 (p.766) are the durable book-period anchors
  (`CH02_review.json` finding F-08 context; `S218_research.json` primary_source).
