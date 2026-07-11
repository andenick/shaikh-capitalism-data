# S207 — US Manufacturing Productivity and Production-Worker Real Compensation — Methodological History Report (MHR)

**Group:** ch2 (Turbulent Trends and Hidden Structures) · **Construction:** composite · **Status:** book_period_validated
**Figure:** 2.5 · **Predecessor:** CD/CD2 S007 · **Publish:** true · **Book period:** 1889–2010 · **Extension:** 2011–2025
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S207_research.json`), the DPR/EPR (`Technical/docs/series/S207_{DPR,EPR}.md`),
> the registry (`Technical/series_registry.json` → `series.S207`), the book KB (Body_Text
> `ch02_turbulent_trends.md`, Figure `ch02_fig_2.5.md`), the CH2 review
> (`Technical/methodology_review/CH02_review.json`), and the Phase-0 NIPA timeline
> (`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`). Where a rationale is not present in
> the corpus it is marked **"author rationale not located in corpus."**

---

## 1. What the series is

S207 is the pair of annual indexes plotted as **Figure 2.5, "US Manufacturing Productivity and Production
Worker Real Compensation, 1889–2010"** — the opening figure of Chapter 2 §II ("Productivity, Real Wages, and
Real Unit Labor Costs"), on a **logarithmic scale, 1889 = 100** (KB `Figures/ch02/ch02_fig_2.5.md`; book p. 60).
It co-plots **two** lines:

1. **Manufacturing labor productivity** (output per worker-hour) — "essentially a measure of technical change,
   and its steady long-term rise speaks to the fundamental role of technological progress in capitalist
   development" (book p. 59, `S207_research.json` book_quotes[0], role=definition, verbatim_check=true).
2. **Production-worker real compensation per hour** (CPI-deflated).

Shaikh's purpose is to demonstrate that the two are **not** inevitably tied: real wages "often appear to move
*pari passu* with productivity," producing the "mistaken impression … that the two are inevitably tied
together," but from the early 1980s (Reagan-era "assault on labor," compounded by foreign competition) US
manufacturing real wages stagnate while productivity keeps rising (KB `ch02_fig_2.5.md` Main Observations 3–5;
`Body_Text/ch02_turbulent_trends.md` lines 165–183). The KB body-text source line for the figure reads:
**"Source: U.S. Bureau of Economic Analysis and Measuring Worth.com (1889 = 100)"** (`ch02_turbulent_trends.md`
line 210). Final units: **Index, 1889 = 100** for both lines (`S207_DPR.md` §6; registry `units`,
`triage.reason` — the registry's old "mixed_units" string was corrected, all four subseries are index 1889=100).

The authoritative source statement is **Appendix 2.1 "Data Sources and Methods" (book p. 764)**, transcribed
verbatim in `S207_research.json` book_quotes[1] (role=source, verbatim_check=true):

> "Manufacturing productivity (yr) for 1860–1970 (1958 = 100) from BEA (1966, Series A173) and for 1950–2009
> from BLS International Data, http://www.bls.gov/fls/#productivity, Table 1: Output per Hour in Manufacturing,
> 19 Countries or Areas (2007 = 100). Both series rebased to 1889 = 100 and spliced in 1950 with the earlier
> series rescaled to match in 1950. Production worker real compensation for 1774–2010 based on manufacturing
> production worker nominal compensation (ec) in $/hr and Consumer Price Index (CPI) for 1774–2010 from
> Measuring Worth.com … Real compensation was derived as ec/CPI."

## 2. Source lineage

Two independent constructions are co-plotted; each has its own book-period splice and its own modern
extension (`S207_DPR.md` §3–4; registry `subseries`).

| Subseries | Coverage | Agency / table id | Native units | Retrieval |
|---|---|---|---|---|
| **S207-A** productivity | 1889–2010 | **BEA, *Long Term Economic Growth 1860–1965* (1966), Series A173** [1860–1970] spliced with **BLS International Labor Comparisons / Foreign Labor Statistics, Table 1: Output per Hour in Manufacturing, 19 Countries** [1950–2009] | A173 Index 1958=100; BLS ILC Index 2007=100 | Salvaged chopped `Appendix2_ManufacturingProductivityAndRealWages1889-2010.csv` |
| **S207-B** real compensation | 1889–2010 | **MeasuringWorth** production-worker nominal compensation `ec` ($/hr) ÷ **MeasuringWorth CPI** | ec in $/hr; CPI 1982–84=100 | Salvaged chopped (MW `uswage` + CPI) |
| **S207-C** productivity extension | 2010–2025 | **FRED `OPHMFG`** (Manufacturing Sector: Real Output Per Hour, BLS Productivity & Costs, US-only) | Index 2017=100 | Live FRED API — **proxy=true** |
| **S207-D** compensation extension | 2010–2025 | **FRED `COMPRMS`** (Manufacturing Real Compensation Per Hour) | Index 2017=100 | Live FRED API |

**Exact chain — productivity (S207-A), per Appendix 2.1 p. 764 + `S207_DPR.md` §4:**

```
BEA LTEG 1966 Series A173 [1860–1970, native 1958=100]
    → rebase to 1889=100
BLS ILC/FLS Table 1 "Output per Hour in Mfg, 19 countries" [1950–2009, native 2007=100]
    → rebase to 1889=100
SPLICE at 1950: EARLIER series (BEA A173) rescaled to match BLS at 1950
    → BEA-rebased for 1889–1949, BLS-rebased for 1950–2009, both on 1889=100
FRED OPHMFG [2010–2025, native 2017=100]  ← PROXY (US-only successor to sunset BLS ILC)
    → reindex at 2009/2010 overlap anchor to the book level → append
```

**Exact chain — real compensation (S207-B):**

```
MeasuringWorth production-worker nominal compensation ec [1774–2010, $/hr]
MeasuringWorth CPI [1774–2010, 1982–84=100]
    → real_compensation = ec / CPI   (Appendix 2.1: "Real compensation was derived as ec/CPI")
    → rebase to 1889=100
FRED COMPRMS [2010–2025] → reindex at 2009/2010 overlap anchor → append
```

Registry `validation.reference_values` (subseries S207-B, tol 0.01): **1889 = 100.0, 1950 = 441.668796,
2010 = 831.968618** — V03-certified spot-checks round-tripped against the book XLSX / ShaikhChoppedTables.
Agency source-methodology grounding for the productivity leg:
`SalvagedInputs/methodology_library/D_data_methodology/WL-D-BLS-{002,003,008,009}__BLS-productivity.pdf`
and the BLS program archive `WL-D-BLS-013__BLS-archive.html` (which catalogues "Foreign labor statistics" as a
now-archived BLS category); MeasuringWorth's own method write-ups are cited by Shaikh as "Characteristics of the
Production-Worker Compensation Series" and "What Was the Consumer Price Index Then?" (`S207_research.json`
book_quotes[1]).

## 3. Why these sources, from the author's perspective

**The concept Shaikh measures.** Productivity here is a proxy for **technical change** — the "material foundation
for a potential rise in real wages" (book p. 59; KB `ch02_fig_2.5.md` Key Insight). Real compensation is the
**worker-side** real wage (money wage ÷ CPI), deliberately distinguished from the firm-side real wage that
feeds Fig 2.6 (book fn 3, p. 60–61, `ch02_turbulent_trends.md` lines 272–276). Plotting the two together is
the whole rhetorical point: it lets the reader *see* the post-1980 divergence that "shatters" the stylized-fact
comfort that wages track productivity. Shaikh's meta-rationale for building this on US data is stated at book
p. 56 — the US "is the preeminent advanced country and … generally has the best available data"
(`Body_Text/ch02_turbulent_trends.md`; `appendix_methodology_summary.json` data_limitations[0]).

**Why BEA LTEG (1966) A173 for the historical productivity leg.** It is the standard compiled long-run US
manufacturing output-per-man-hour series reaching back to the nineteenth century (Appendix 2.1 p. 764). Shaikh
names it directly and does not narrate a comparison against alternatives; explicit rejection rationale for
substitutes such as **Kendrick (1961) *Productivity Trends*** (which the registry `predecessor_artifacts` shows
was *available* in the KB, `1961_Kendrick_Productivity_Trends`, coverage 1869–1960) is **not located in corpus** —
Appendix 2.1 lists only BEA (1966, A173). Note the plot begins at **1889, not 1860**, because CD2 flagged BEA
coverage 1860–1889 as sparse (`S207_research.json` methodology_notes[1]).

**Why BLS International Labor Comparisons Table 1 for the modern productivity leg — and why not BLS MFP/KLEMS.**
Shaikh takes the BLS ILC "Output per Hour in Manufacturing (19 Countries)" series for 1950–2009 (Appendix 2.1
p. 764). The concept BLS ILC measures — a *directly comparable, single-deflator manufacturing labor-productivity
index* built expressly for cross-country comparison — is the natural continuation of a labor-productivity
(output-per-hour) index, whereas BLS Multifactor Productivity / KLEMS measure a *different* object
(capital+labor+intermediate joint productivity) and would break the "output per worker hour" definition Shaikh
states on p. 59. That much is inferable from the stated definition; but an **explicit** in-text argument
rejecting BLS MFP or KLEMS is **not located in corpus** (neither `S207_research.json` nor the KB body text
discusses rejected productivity programs).

**Why FRED OPHMFG for the extension, and why it *is* flagged a proxy.** The book's modern productivity source —
the BLS International Labor Comparisons / Foreign Labor Statistics program — **was permanently sunset in 2013**
(budget-driven termination of the international-comparisons program; `S207_research.json`
primary_source.replaced_by, extension_candidates[0].concerns, open_questions; registry
`S207-C.proxy_justification`; `S207_DPR.md` §7 caveat 2). No live successor reproduces the *19-country
comparison*. FRED **OPHMFG** is the closest faithful continuation: it is the **US-only** manufacturing-sector
real-output-per-hour series from the same BLS Productivity & Costs lineage. Extending with it therefore
**narrows the concept from a 19-country international-comparison basis to a US-manufacturing-only basis** — a
genuine change in what the series measures, not a like-for-like continuation. RSCD records this honestly as
`proxy: true` on S207-C with the concept-narrowing justification (registry `S207.proxy`,
`S207-C.proxy_justification`; `S207_EPR.md` §3). *(This is exactly the exposure CH2-review **F-09** asks to be
spelled out; see §4/§5.)*

**Why MeasuringWorth for compensation (no proxy).** The compensation leg's extension (FRED COMPRMS, and MW's own
continuously-updated `ec`/CPI) is the *same source/agency concept* as the book period — "direct continuation"
(`S207_research.json` extension_candidates[1].concerns). No proxy flag on S207-B/S207-D.

## 4. Methodological-change exposure

- **The key exposure — BLS FLS/ILC program SUNSET (2013).** Unlike a data revision, this is a *program
  termination*: the exact 19-country "Output per Hour in Manufacturing" table Shaikh cited stopped being
  produced after 2013 (`S207_research.json` primary_source.replaced_by; `S207_DPR.md` §7 caveat 2). The book URL
  `http://www.bls.gov/fls/#productivity` returns 404 in 2026 (`S207_research.json` open_questions). Any extension
  *must* switch program (to US-only OPHMFG) and thereby accept the concept-narrowing above — there is no way to
  continue the original series on its own terms. This is the single most important methodological fact about
  S207 and the substance of review finding **F-09**.
- **NIPA vintage effects (indirect).** S207 is index-based (output-per-hour and CPI-deflated compensation), not
  a NIPA product-side magnitude, so the comprehensive-revision restatements
  (1999/2003/2009/**2013**/**2018**/**2023**; `NIPA_CHANGE_TIMELINE.md`) do not move its *levels* the way they
  move value/investment series. The one indirect tie is that BLS manufacturing output/hour concepts are
  benchmarked against BEA industry accounts, so the **2013** comprehensive revision (R&D + entertainment → IPP,
  ≈ +$400 B GDP, 2007 benchmark I-O) coincides with — and reinforces the case not to splice across — the same
  2013 boundary at which the FLS program ended. The Phase-0 rule applies: **never splice an extension across a
  comprehensive-revision boundary** (`NIPA_CHANGE_TIMELINE.md` §"Why this matters"); Shaikh fixes BEA data at
  the **2011 vintage**.
- **FRED re-basing.** OPHMFG and COMPRMS are published on a rolling base (2017=100 as retrieved); the loader must
  reindex at the live overlap on every run, never persist rebased levels (`S207_EPR.md` §5 failure table, overlap
  walk-back 2010→2009→2008).
- **Concordance / I-O dependency:** none direct. (Contrast S214's OECD STAN→NAICS crosswalk,
  `CH02_review.json` touchpoints.) MeasuringWorth's CPI splice is internally reconciled by MW.

## 5. Replication fidelity note

- **RSCD reproduces Shaikh's exact recipe from his exact source columns.** The book-period productivity and
  compensation lines are read from the salvaged chopped
  `Appendix2_ManufacturingProductivityAndRealWages1889-2010.csv`/MW columns — Shaikh's own retrieved values —
  rebased to 1889=100 and, for productivity, spliced at 1950 with the earlier series rescaled to match, exactly
  as Appendix 2.1 specifies. Expected MAE < 0.5% vs book truth (`S207_DPR.md` §9); reference values tie out at
  1889/1950/2010 (§2 above).
- **Proxy flag is set and disclosed (F-09 honored).** S207-C carries `proxy: true` with the BLS-FLS-sunset →
  OPHMFG concept-narrowing justification in the registry, the DPR (§7 caveat 2), and the EPR ("No-Proxy
  disclosure" §3). The extension is a *documented US-only successor*, not a silent substitution — this MHR §3–4
  is the fuller write-up F-09 requested.
- **No synthetic fill.** Where FRED returns NaN the NaN propagates; no interpolation/carry-forward
  (`S207_EPR.md` §4). Missing `FRED_API_KEY` → publish book period only, `extension_status: api_key_missing`
  (`S207_EPR.md` §5/§7).
- **Honest limits.** (a) The 1889–1949 productivity segment can never be re-verified against a live source
  (BEA 1966 out of print) — the salvaged column is the sole authority. (b) The productivity extension is
  concept-narrowed (US-only) and so is *not* strictly comparable to the book's 19-country basis; the proxy flag
  encodes this. (c) MeasuringWorth `uscompensation` → `uswage` was a URL rename only, values unchanged
  (`S207_DPR.md` §7 caveat 1; registry adequacy). **No CH2-review HIGH/MED finding is against S207**; the only
  finding, **F-09**, is LOW and is the terseness this document remediates.

## 6. Forward risk

- **Sunset-source continuity (the standing risk).** Because the original BLS ILC program is gone, S207's
  productivity extension is permanently dependent on OPHMFG staying live and on the US-only concept-narrowing
  being tolerated. If OPHMFG is itself revised or rebased (BLS periodically re-references Productivity & Costs),
  re-fetch and re-anchor the whole post-book segment; never splice a cached OPHMFG level onto the book series
  across a BLS reference-year change.
- **Divergence between the two extension legs.** Productivity (OPHMFG, US-only) and compensation (COMPRMS/MW)
  are extended from *different* programs; a BLS manufacturing-sector redefinition that touches output-per-hour
  but not compensation-per-hour (or vice-versa) would distort the post-2010 *gap* that is the figure's whole
  message. Guard: keep both legs on the same anchor year and re-fetch together.
- **Next NIPA/BLS benchmark (post-2023).** A future comprehensive update re-benchmarking manufacturing industry
  output would restate recent OPHMFG history; freeze at the last complete annual observation and do not
  forward-fill (`S207_EPR.md` §6/§7).
- **Non-recoverability of the antebellum/pre-1950 segment.** BEA (1966) LTEG A173 and the original BLS
  19-country table are both non-live; loss of the salvaged chopped column would make 1889–2009 unreproducible.
  Preserved under `SalvagedInputs/`.
