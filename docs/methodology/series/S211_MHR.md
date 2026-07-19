# S211 — US & UK Wholesale Price Indexes, 1780–1940 — Methodological History Report (MHR)

**Group:** ch2 (Turbulent Trends and Hidden Structures) · **Construction:** composite (windowed view of S210) · **Status:** book_period_validated
**Figure:** 2.9 · **Predecessor:** CD S011 (no CD2 id; reproduced via the S210/CD2 S023 lineage windowed to 1940) · **Publish:** true · **Book period:** 1780–1940 (registry/chopped: 1790–1940) · **Extension:** none by design
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S211_research.json`), the DPR (`Technical/docs/series/S211_DPR.md`; there is no EPR —
> the series has no extension), the registry (`Technical/series_registry.json` → `series.S211`), the book KB
> (Body_Text `ch02_turbulent_trends.md`, Figure `ch02_fig_2.9.md`), the CH2 review
> (`Technical/methodology_review/CH02_review.json`), and the Phase-0 NIPA timeline
> (`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`). Where a rationale is not present in the
> corpus it is marked **"author rationale not located in corpus."** For full source detail see the sibling
> **`S210_MHR.md`** — S211 inherits S210's lineage exactly.

---

## 1. What the series is

S211 is the **US and UK wholesale price indexes, 1780–1940**, on the same **1930 = 100** log basis, plotted as
**Figure 2.9** (KB `Figures/ch02/ch02_fig_2.9.md`, book p. 64). It is **not a new construction** — it is the
**pre-1940 window of S210 / Figure 2.8**, truncated by analytical design. Shaikh states the rationale directly
(book p. 62, `S211_research.json` book_quotes[0], role=definition): "When placed on the same scale as in figure
2.8, the long swings in prices prior to the 1940s are dwarfed by the subsequent secular increases. It is
therefore useful to separate out the two episodes, as in figure 2.9. Then … for more than a
century-and-a-half from 1780 to 1940, price movement displays distinct long swings with no overall trend."
**The truncation *is* the analytical purpose:** compressing the y-axis to 50–300 (vs. 10–10,000 in Fig 2.8)
makes the pre-war long waves legible — the wave-like character that "underpins the notion of 'long waves'
(to which we will return in chapter 5)" (KB `ch02_fig_2.9.md`). This ties Ch2 forward to Ch5/App 5.3, the same
shared WPI/gold dossier that S210 cross-references.

Final units: **Index, 1930 = 100** (log scale), annual (`S211_DPR.md` §6).

## 2. Source lineage

**S211 inherits S210's lineage exactly, windowed to the pre-1940 gold-standard era** (`S211_research.json`
methodology_notes; `S211_DPR.md` §3–4). The truncation drops S210's forward extensions entirely, so only the
Jastram historical segments (plus the two pre-1940 gap-fills) remain in scope:

| Subseries | Coverage | Source / id | Native units | Operation |
|---|---|---|---|---|
| **S211-B (UK)** | 1780–1940 | **Jastram (1977) Golden Constant, Table 2**; **1939–1940 filled via NBER macrohistory `m04053`** growth rates | Index 1930=100 | native basis + growth-rate gap-fill |
| **S211-A (US)** | 1780–1940 | **Jastram (1977) Golden Constant, Table 7** (1800–1940); **1780–1799 interpolated via MeasuringWorth US CPI** rescaled by the 1800 WPI/CPI ratio | Index 1930=100 | native basis + interpolated backfill |

**No BLS WPS/WPU or ONS PLLU extension applies** — those are post-1976/post-1977 extenders and fall entirely
outside the 1940 window. Because the window ends at 1940, S211 also never reaches the WPI→PPI rename boundary
(§4). **Registry/chopped note:** the chopped CSV begins at **1790** (not 1780); a 2026-05-19 reconciliation
(`series_registry.json` reconciliation_notes) attributes this to the MeasuringWorth US WPI source beginning at
1790, so the registry `year_range` is `[1790, 1940]` while the book/figure caption reads 1780. This is a
source-reality alignment, documented, not a data gap.

## 3. Why these sources — author's perspective

The source *concept* is identical to S210 (long-wave price behavior; Jastram's multi-century, gold-anchored
tables; UK added for reach). The one rationale unique to S211 is **why truncate at 1940**: Shaikh does it to
**visually rescue the pre-war long waves** that Fig 2.8's full-span log scale crushes, and to isolate the
gold-standard / pre-Bretton-Woods regime where prices are stationary-with-swings — the empirical hook for the
long-wave argument he develops in Ch5 (book p. 62, KB `ch02_fig_2.9.md` "Purpose"). Extending S211 past 1940
would **defeat its purpose** (`S211_research.json` extension_candidates[0].concerns; `S211_DPR.md` §7). Why
Jastram over alternative historical price houses (HSUS, NBER, JST) remains **author rationale not located in
corpus** — same as S210.

## 4. Methodological-change exposure

- **Essentially none.** Because the series ends at **1940**, it never touches the **BLS WPI→PPI rename /
  WPS→WPU renumber** (post-1974/1978) that exposes S210 and S212 — the entire span sits inside Jastram's frozen
  historical tables plus two pre-1940 growth-rate gap-fills.
- **NIPA / IO timelines DO NOT apply.** As with the whole family, S211 is BLS-style wholesale prices from
  Jastram's compilation and NBER macrohistory — **no NIPA and no benchmark I-O content whatsoever.** The BEA
  comprehensive-revision events in `NIPA_CHANGE_TIMELINE.md` do not touch this series. Stated explicitly.
- **ONS revisions:** not applicable — the ONS `PLLU` extender is post-1977 and out of window.
- **Underlying vintage risk** is limited to the MeasuringWorth CPI used for the 1780/1790–1799 US backfill (a
  stable historical compilation) and the NBER m04053 1939–1940 fill.

## 5. Replication fidelity note

- **Truth basis:** book-period values reproduced from the same Jastram-based construction as S210, windowed to
  1940; `S211_DPR.md` §3 records "salvaged via CD2 S022" (the pre-1940 counterpart in the CD2 tree). Registry
  `reference_values`: 1790 = 74.404, 1865 = 146.6, 1940 = 90.8 (`series_registry.json` validation).
- **No extension, by design** — `extension_status: not_applicable_windowed`; there is intentionally no EPR.
  For any post-1940 need, use S210 (`S211_DPR.md` §7).
- **Honest limit:** the 1780 vs 1790 start discrepancy is a documented source-reality reconciliation, not a
  missing-data defect.

## 6. Forward risk

- **Essentially frozen.** S211 is a **windowed historical view** with no live extender; its inputs (Jastram
  tables, NBER m04053, MeasuringWorth CPI backfill) are all fixed historical compilations. There is no PPI
  re-basing, ONS-discontinuation, or gold-source-update exposure because none of those feeds enter the pre-1940
  window. The only conceivable revision would be a corrected transcription of Jastram's tables or the CD2/chopped
  truth — a validation event, not a source-vintage event.
