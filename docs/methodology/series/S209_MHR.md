# S209 — US Unemployment Rate — Methodological History Report (MHR)

**Group:** ch2 (Turbulent Trends and Hidden Structures) · **Construction:** composite · **Status:** book_period_validated
**Figure:** 2.7 · **Predecessor:** CD/CD2 S009 · **Publish:** true · **Book period:** 1890–2010 · **Extension:** 2011–2025
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S209_research.json`), the DPR/EPR (`Technical/docs/series/S209_{DPR,EPR}.md`),
> the registry (`Technical/series_registry.json` → `series.S209`), the book KB (Body_Text
> `ch02_turbulent_trends.md`, Figure `ch02_fig_2.7.md`), the CH2 review
> (`Technical/methodology_review/CH02_review.json`), and the Phase-0 NIPA timeline
> (`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`). Where a rationale is not present in
> the corpus it is marked **"author rationale not located in corpus."**

---

## 1. What the series is

S209 is the annual **US official civilian unemployment rate, 1890–2010**, plotted as **Figure 2.7** (Chapter 2
§III "The Rate of Unemployment"; KB `Figures/ch02/ch02_fig_2.7.md`, book p. 61–62; y-axis 0–30 %). Shaikh's
own gloss: *"Figure 2.7 displays the path of the (official) unemployment rate from 1890 to 2010. It provides a
vivid picture of the enormous impact that Great Depressions have on economic life"* (book p. 60/62,
`S209_research.json` book_quotes[0], role=definition; `Body_Text/ch02_turbulent_trends.md` line 270). The word
Shaikh stresses is **"official"** — this is the headline published rate, not a reconstructed or broadened
measure. He uses it to mark the great crises (the 1873–1893 and 1929–1939 Depressions, the 1970s stagflation,
the 2007+ Global Crisis) and to argue that unemployment is "a key factor regulating the strength of the link
between productivity growth and real wages" — the connective tissue back to Figs 2.5/2.6 (KB `ch02_fig_2.7.md`
Key Insight; book p. 62). Units: **percent of civilian labor force** (`S209_DPR.md` §6; registry `units`).

The authoritative source statement is **Appendix 2.1 (book p. 764)**, transcribed verbatim in
`S209_research.json` book_quotes[1] (role=source, verbatim_check=true):

> "Figure 2.7 US Unemployment Rate, 1890–2010. Civilian unemployment rate 1860–1970 from BEA (1966, Series
> B1-B2), and from 1948 to 2010 from the Economic Report of the President,
> http://www.gpo.gov/fdsys/browse/collection.action?collectionCode=ERP., table b-40."

## 2. Source lineage

A two-piece historical splice extended by one modern series (`S209_DPR.md` §3–4; registry `subseries`,
`construction_steps`).

| Subseries | Coverage | Agency / table id | Native units | Retrieval |
|---|---|---|---|---|
| **S209-A** | 1890–1947 (loaded 1890–1970) | **BEA, *Long Term Economic Growth 1860–1965* (1966), Series B1–B2** (civilian unemployment rate) | Percent | Salvaged chopped (KB `1966_BEA_Long_Term_Economic_Growth`, "CHART 4 data") |
| **S209-B** | 1948–2010 | **Economic Report of the President, Table B-40** (Civilian Unemployment Rate), CEA/GPO | Percent | Salvaged chopped `Appendix2_Unemployment.csv` |
| **S209-C** | 2010/2011–2025 | **FRED `UNRATE`** (BLS Current Population Survey civilian unemployment rate, annual = mean of monthly) | Percent | Live FRED API |

**Exact chain (per Appendix 2.1 p. 764 + `S209_DPR.md` §4; `construction_steps` rescale→splice→extend):**

```
BEA LTEG 1966 Series B1–B2 [1890–1947, percent]
ERP Table B-40 [1948–2010, percent]
    → rebase each to the splice anchor so levels match at the join
SPLICE at 1948: BEA B1–B2 for 1890–1947, ERP B-40 from 1948 onward
FRED UNRATE [2011–2025, percent]
    → append with NO rescale (ERP B-40 and UNRATE are the same BLS/CPS concept, level-equivalent)
```

Both rates are levels in the same units, so the "rebase" here is a level-match at the join, not an index
reindex. Because unemployment sits near 1–2 % in some years, the validator uses an **absolute 0.15pp tolerance**
(not relative), which would otherwise fire false divergences (`S209_DPR.md` §7 caveat 1). Registry
`validation.reference_values` (subseries S209-B, tol 0.01): **1948 = 3.8, 1979 = 5.8, 2010 = 9.6**. The CH2
review **hand-check** independently confirms the spine — **"1890 = 4.0; 1948 ERP splice = 3.8; 2010 = 9.6 match
Unemployment workbook"** (`CH02_review.json` hand_checks → S209, verdict **PASS**). Modern-continuation grounding:
KB `Robin_FRED` `UNRATE.csv` (1948–2025), registry `predecessor_artifacts`.

## 3. Why these sources, from the author's perspective

**The concept Shaikh measures.** The **official** civilian unemployment rate — deliberately the *published*
headline number, so the figure speaks in the terms the public and policymakers use, and so the great crises are
legible at a glance (book p. 62). Shaikh's theoretical stake: unemployment "regulates the strength of the link
between productivity growth and real wages … the higher the unemployment rate, the weaker the strength of labor
vis-à-vis capital" (KB `ch02_fig_2.7.md` Key Insight; book p. 62) — which is *why* it belongs beside Figs
2.5/2.6. His US-data meta-rationale (best available data, book p. 56) applies here too.

**Why BEA LTEG (1966) B1–B2 for the pre-1948 reach.** To carry the "official" rate back to **1890** — before
the modern BLS Current Population Survey existed — Shaikh needs the standard compiled long-run historical series,
which BEA's *Long Term Economic Growth* (1966) provides as Series B1–B2 (Appendix 2.1 p. 764;
`S209_research.json` components[0]). No live source reaches that far back, so the historical estimate is the
only option for the antebellum-through-Depression stretch that carries the figure's whole argument.

**Why ERP Table B-40 for 1948–2010, rather than a single modern BLS series (e.g. FRED UNRATE) for the whole
1948–2010 span.** Appendix 2.1 explicitly cites the **Economic Report of the President, Table B-40** as the
1948–2010 source (`S209_research.json` book_quotes[1]). The ERP is the canonical *government-of-record* annual
compilation of the official rate — the authoritative printed vintage a 2011-era construction would cite — and
it dovetails cleanly with the pre-1948 historical series to give a continuous post-1890 record (`S209_DPR.md`
§2). Using ERP B-40 (rather than pulling UNRATE back to 1948) preserves the *exact printed vintage* Shaikh read,
which is the fidelity target for the book period. An **explicit** in-book argument comparing ERP B-40 against
pulling a single modern BLS/CPS series for the whole span is **not located in corpus** — Appendix 2.1 names ERP
B-40 without narrating the choice.

**Why FRED UNRATE for the extension, and why it is not a proxy.** UNRATE is the **same underlying BLS Current
Population Survey civilian-unemployment-rate concept** as ERP Table B-40 — indeed ERP B-40 *reprints* the BLS
CPS rate. So the extension is a "direct continuation," level-equivalent, requiring no rescale (registry
`S209-C`; `S209_research.json` extension_candidates[0].concerns; `S209_EPR.md` §2/§3 "No proxies used"). Registry
`proxy: false`.

## 4. Methodological-change exposure

- **CPS definitional break at the 1948 splice (the one real caveat).** The pre-1948 BEA LTEG estimates and the
  post-1948 BLS CPS use *slightly different definitions of "unemployed"*; the two-methodology join is the
  documented seam of the series (`S209_DPR.md` §7 caveat 2; `S209_research.json` methodology_notes[1] —
  "pre-1948 LTEG estimates differ in methodology from modern CPS — historical comparability caveat"). The splice
  is level-matched at 1948 and the discontinuity is disclosed, not smoothed.
- **CPS re-benchmarking / population-control revisions (modern exposure).** UNRATE is periodically re-based to
  new decennial population controls and occasional CPS redesigns; these can nudge recent history by small
  amounts. Because the extension appends UNRATE without rescale, a re-benchmark shifts only the appended tail —
  hence the **0.15pp absolute tolerance** guardrail (`S209_DPR.md` §7 caveat 1) is the right instrument, not a
  relative one.
- **NIPA vintage effects: none.** The unemployment rate is a **BLS/CPS labor-force statistic, not a BEA product
  account**, so the NIPA comprehensive revisions (1999/2003/2009/2013/2018/2023 in `NIPA_CHANGE_TIMELINE.md`) do
  **not** touch S209's levels at all — this is the cleanest series in the trio on that axis. The Phase-0
  never-splice-across-a-comprehensive-revision rule is not binding here (no BEA magnitude in the chain).
- **Concordance / I-O dependency:** none. **Source-URL migration:** the ERP archive moved from
  `gpo.gov/fdsys` to `govinfo.gov`; verify the current annual edition still numbers the table B-40
  (`S209_research.json` open_questions; registry adequacy issues_resolved "govinfo ERP collection + FRED UNRATE
  live (HTTP 200)").

## 5. Replication fidelity note

- **RSCD reproduces Shaikh's exact recipe and ties out to hand-checks.** The book period reads the salvaged
  chopped values (BEA LTEG B1–B2 for 1890–1947, ERP B-40 for 1948–2010), level-matched and spliced at 1948
  exactly as Appendix 2.1 specifies. The CH2 review hand-check is a clean **PASS** at all three anchor years
  (1890 = 4.0, 1948 = 3.8, 2010 = 9.6; `CH02_review.json` hand_checks → S209), and these match the registry
  reference values.
- **Splice tolerance is the fidelity instrument.** Validation uses **0.15pp absolute** tolerance (`S209_DPR.md`
  §7 caveat 1), correctly chosen so low-unemployment years do not trigger false relative divergences. Expected
  MAE well within tolerance (`S209_DPR.md` §9).
- **No proxy, no synthetic fill.** Registry `proxy: false`; UNRATE is the same BLS/CPS concept as ERP B-40, so
  the extension is a genuine continuation, not a substitution (`S209_EPR.md` §3). FRED NaN propagates; no
  interpolation (`S209_EPR.md` §4). Missing `FRED_API_KEY` → publish book period only,
  `extension_status: api_key_missing` (`S209_EPR.md` §5/§7).
- **Honest limits.** (a) The **1890–1947 definition differs** from the modern CPS definition — the long reach is
  bought at the cost of a documented methodological seam at 1948. (b) The pre-1948 BEA LTEG segment can never be
  re-verified against a live source (out of print); the salvaged chopped column is the sole authority.
  **No CH2-review finding is against S209** (its hand-check is one of the report's clean PASSes; the HIGH/MED
  findings target S203/S214); only the general **F-03** (construction in DPR §4 + registry, no separate
  DECOMPOSITION.md) applies, which this MHR §2 supplies.

## 6. Forward risk

- **CPS/UNRATE re-benchmark (the standing risk).** Future decennial population-control updates or a CPS
  questionnaire redesign will restate recent UNRATE history slightly. Because the extension appends UNRATE
  unrescaled, re-fetch the whole post-book tail on each run and let the 0.15pp guard absorb small level shifts;
  do not cache a stale annualized UNRATE across a re-benchmark.
- **ERP table-numbering / archive drift.** ERP table numbers are not permanent and the archive has already
  migrated (fdsys → govinfo); a future edition could renumber B-40 or restructure the collection. Resolve the
  modern rate by *series concept* (BLS CPS civilian unemployment rate) rather than by a hard-coded table label
  (`S209_research.json` open_questions) — the same discipline the NIPA T7.11 remap uses for line numbers.
- **Historical-segment non-recoverability.** BEA (1966) LTEG B1–B2 is non-live; loss of the salvaged chopped
  column would make 1890–1947 unreproducible. Preserved under `SalvagedInputs/`.
- **Discontinuation:** none foreseen — BLS CPS continues monthly and FRED republishes UNRATE without latency;
  the 1890–2010 book period is fixed regardless.
