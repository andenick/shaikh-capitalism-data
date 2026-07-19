# S201 — US Industrial Production Index — Methodological History Report (MHR)

**Group:** ch2 (Turbulent Trends and Hidden Structures) · **Construction:** composite · **Status:** book_period_validated
**Figure:** 2.1 · **Predecessor:** CD/CD2 S001 · **Publish:** true · **Book period:** 1860–2010 · **Extension:** 2011–2025
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S201_research.json`), the DPR/EPR (`Technical/docs/series/S201_{DPR,EPR}.md`),
> the book KB (Body_Text `ch02_turbulent_trends.md`, Figure `ch02_fig_2.1.md`), the CH2 review
> (`Technical/methodology_review/CH02_review.json`), and the Phase-0 NIPA timeline
> (`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`). Where a rationale is not present in
> the corpus it is marked **"author rationale not located in corpus."**

---

## 1. What the series is

S201 is the annual **US Industrial Production Index, 1860–2010**, plotted on a **log scale** as **Figure 2.1**,
the opening figure of Chapter 2 ("Turbulent Trends and Hidden Structures"). It is the first leg of Shaikh's
"growth trio" (Figs 2.1–2.3: industrial production, real investment, real GNP/GDP per capita), the "distant
view" whose slope-as-growth-rate reading makes the "system's apparently inexorable tendency toward growth …
immediately evident" (book p. 56, KB `Body_Text/ch02_turbulent_trends.md` lines 12–22; also
`S201_research.json` book_quotes[0], role=definition, page 56). The KB figure caption
(`Figures/ch02/ch02_fig_2.1.md`) confirms the log y-axis (1→1,000), the 1860–2010 x-axis, and Shaikh's four
"main observations" — growth is evident, growth rates are not constant, output grows faster in earlier epochs,
and growth is always turbulent.

The authoritative source line is **Appendix 2.1 "Data Sources and Methods" (book p. 763)**, transcribed
verbatim in `S201_research.json` book_quotes[1] (role=source, verbatim_check=true):

> "Figure 2.1 US Industrial Production Index, 1860–2010. All Industries, 1860–1959 (1913 = 100) are from the
> BEA (1966, table A15), and 1919–2010 (2007 = 100) from the Board of Governors of the Federal Reserve System
> at http://www.federalreserve.gov/. The two series were rebased to 1958 = 100 and spliced at 1919."

Final units: **Index, 1958 = 100** (`S201_DPR.md` §6). The concept is real industrial output (manufacturing +
mining + electric & gas utilities) at annual frequency.

## 2. Source lineage

Every subseries, its coverage, native units, agency/table id, and the exact splice/reindex chain
(`S201_DPR.md` §3–4, `S201_EPR.md` §3):

| Subseries | Coverage | Agency / table | Native units | Retrieval |
|---|---|---|---|---|
| **S201-A** | 1860–1918 (loaded 1860–1959) | **BEA, *Long Term Economic Growth, 1860–1965* (1966), Table A15 / Series A173** | Index 1913=100 | Salvaged chopped `Appendix2_IndustrialProduction.xlsx` col `IndProdHS_BEA` |
| **S201-B** | 1919–2010 | **Federal Reserve Board (FRB), Statistical Release G.17, Industrial Production — All Industries** | Index 2007=100 (as retrieved ~2011) | Salvaged chopped col `IndProd_FRB` |
| **S201-C** | 2011–2025 | **FRED `INDPRO`** (St. Louis Fed republication of FRB G.17) | Index 2017=100 | Live FRED API, annual = mean of monthly |

**Exact chain (per Appendix 2.1 p. 763 + `S201_DPR.md` §4):**

```
BEA LTEG 1966 Table A15/A173 [1860–1959, native 1913=100]
    → rebase ×(100 / BEA_A173[1958] ≈ 100/457.0 = 0.21882)  → IndProdHS1_BEA
FRB G.17 [1919–2010, native 2007=100]
    → rebase ×(100 / FRB_G17[1958] ≈ 100/20.22705 = 4.94388) → IndProd1_FRB
SPLICE at 1919: use BEA-rebased for 1860–1918, FRB-rebased for 1919–2010
    (at 1919 the two disagree: BEA 24.77 vs FRB 24.31 — Shaikh takes the FRB value, no average)
    → both on 1958=100
FRED INDPRO [2011–2025, native 2017=100]
    → reindex ×(S201_book[2010] / FRED_INDPRO[2010]) at 2010 overlap → 1958=100 → append
```

The CH2 review hand-check confirms the numeric spine: **"1860=1.637; 1919 splice uses FRB 24.31 (not BEA
24.77); 2010=445.274 match workbook `IndProd_Final`"** (`CH02_review.json` hand_checks → S201, verdict PASS).
Agency source-methodology grounding: FRB G.17 documentation `SalvagedInputs/methodology_library/D_data_methodology/WL-D-G17-00{1..5}__FRB-G17.html`;
the pre-FRB historical index provenance traces to Census/NBER historical statistics
(`WL-D-HSUS-*__Census-HSUS`, `WL-D-NBERMH-*__NBER-MacroHistory`), which are the lineage feeding BEA's 1966 LTEG compilation.

## 3. Why these sources, from the author's perspective

**The concept Shaikh measures.** A single real-output index running continuously back to the antebellum period
— the cleanest available proxy for the "long view" of capitalist growth. Per `S201_DPR.md` §2, "the industrial
production index, more than GDP, is the cleanest available real-output series running back to the antebellum
period; it is therefore the natural choice for Shaikh's opening figure." Shaikh's own meta-rationale for the
US focus is stated at book p. 56 (KB `Body_Text/ch02_turbulent_trends.md` lines 6–9, verbatim):

> "In what follows, I will often use the United States as the primary illustration because it is the preeminent
> advanced country and because it generally has the best available data."

**Why BEA LTEG (1966) for the historical splice.** It is the standard compiled long-run US industrial-production
series to 1860, native 1913=100 (Appendix 2.1 p. 763). Shaikh does not narrate his choice among historical IP
indices in the extracted corpus — he simply names BEA (1966, table A15). Explicit rejection rationale for
alternative early indices (e.g. **Miron–Romer**, **Frickey**, the **Census/NBER** IP indices) is **not located in
corpus** — Appendix 2.1 lists only the chosen source, and neither `S201_research.json` nor the KB body text
discusses rejected historical indices.

**Why FRB G.17 for the modern half.** It is the continuously-published, definitive US industrial-production
release (Federal Reserve, monthly since 1919), the natural continuation series through 2010 (Appendix 2.1;
`S201_research.json` methodology_notes[1] — "CD2 dossier (S001) confirmed both components: BEA (1966, table A15,
p. 185) for 1860–1959 and FRB G-17 for 1919–2010"). Choosing FRB over the BEA value *at the 1919 splice year*
is a deliberate, documented act (Shaikh uses FRB 24.31, not BEA 24.77) — the modern authority governs the
overlap (`S201_DPR.md` §4 step 5, §7 caveat 1).

**Why FRED INDPRO for the extension, and why it is not a proxy.** FRED INDPRO **is** the FRB G.17 series
redistributed by the St. Louis Fed under a public-domain license — same agency, same release, same concept.
The registry records `proxy: false` (`S201_DPR.md` §7 caveat 5; `S201_EPR.md` §5). This is documented explicitly
so a future reviewer does not misflag S201-C as a substitution. Author rationale for extension continuity is in
`S201_research.json` methodology_notes[2] ("Extension uses FRED INDPRO, which is the contemporary continuation
of the FRB G.17 series; same agency, same concept").

## 4. Methodological-change exposure

S201 is **index-based, not NIPA-magnitude-based**, so the NIPA comprehensive-revision restatements
(1999/2003/2009/2013/2018/2023 in `NIPA_CHANGE_TIMELINE.md`) do **not** move its levels the way they move S202/S203
— industrial production is a Fed production index, not a BEA product-side aggregate. The live exposure is
**index re-basing**, not benchmark restatement:

- **FRB/FRED base-year drift (the real risk).** FRED rebases INDPRO on a ~5-year cadence — **2007 → 2012 → 2017**
  base (`S201_DPR.md` §7 caveat 3). Re-basing changes the *level* of raw FRED values but preserves *ratios*, so an
  overlap-anchor reindex always recovers the 1958=100 series. Mitigation: **reindex on every load, never cache
  rebased values across runs** (`S201_EPR.md` §3.1, §4). A stale cached level spliced across a rebasing boundary
  would break the series — the analogue, for an index, of the NIPA "never splice across a comprehensive-revision
  boundary" rule (`NIPA_CHANGE_TIMELINE.md` §"Why this matters").
- **Annual-aggregation method.** FRB G.17 is monthly; the book uses the arithmetic mean of 12 months. FRED's
  `frequency=a, aggregation_method=avg` reproduces this exactly (`S201_DPR.md` §7 caveat 4).
- **No I-O / concordance dependency.** S201 has no input-output touchpoint and no SIC→NAICS concordance
  dependency (unlike S202's fixed-asset lineage or S214's STAN crosswalk); the FRB index absorbs industry
  reclassification internally.

**Concordance dependency:** none. **I-O dependency:** none. **NIPA dependency:** none at the level; only the
FRED base-year rebasing must be neutralized at every load.

## 5. Replication fidelity note

- **RSCD reproduces Shaikh's exact recipe from his exact source columns.** Rather than re-digitizing BEA (1966)
  from microfilm (out of print, `S201_DPR.md` §7 caveat 2), the 1860–1918 segment reads the salvaged chopped
  column `IndProdHS_BEA` — Shaikh's own retrieved values — and the 1919–2010 segment reads `IndProd_FRB`;
  both are rebased and spliced in code exactly as Appendix 2.1 specifies. Expected MAE < 0.1% vs the book chopped
  `IndProd_Final` column (`S201_DPR.md` §9); the CH2 hand-check ties out at 1860, 1919, and 2010.
- **Known splice discontinuity (~1.9%) at 1919** — the BEA-rebased and FRB-rebased 1919 values disagree by
  ~0.46 index points (24.77 vs 24.31). This is not smoothed: Shaikh (and RSCD) take the FRB value, so a small
  level step at the join is a *faithful* feature, not a defect (`S201_DPR.md` §7 caveat 1).
- **CD2 divergence is intentional.** CD2's S001 reindexed FRB G.17 off FRED's 2017 base rather than Shaikh's
  own FRB-1958 anchor, yielding 2010 ≈ 453.7 vs the book's 445.3 (~1.9% high). S201 reproduces the *book's*
  recipe, so a ~1.9% divergence from CD2 in 1919–2010 is expected and acceptable (`S201_EPR.md` §9,
  `S201_DPR.md` §8/§9).
- **No proxy, no synthetic fill.** FRED NaN (e.g. current-year annual not yet finalized) propagates as NaN;
  no interpolation/carry-forward (`S201_EPR.md` §6). If `FRED_API_KEY` is absent the series publishes 1860–2010
  only, stamped `extension_status: api_key_missing` (`S201_EPR.md` §7).
- **No CH2-review findings against S201.** The HIGH/MED findings F-01/F-04 are S203-specific; F-02 is S214;
  S201's hand-check is a clean PASS.

## 6. Forward risk

- **Next FRED/FRB re-basing (2017 → 2022 base, expected ~2027).** The extension only stays correct because
  the loader reindexes at the live overlap on every run. If a future refactor caches the rebased 2017-base
  values and splices them onto the 1958-base book series without re-anchoring, the post-2010 segment jumps by
  the base-ratio. Guard: keep the overlap-anchor reindex mandatory; never persist rebased levels
  (`S201_EPR.md` §3.1/§4).
- **FRB methodology revisions to G.17 weights/coverage.** Periodic FRB revisions to industrial-production
  weights restate recent history; because the extension re-fetches the whole post-book segment and re-anchors,
  a weight revision is absorbed — but a *level* comparison against a previously published extension vintage will
  differ. Freeze at last complete annual observation; do not forward-fill (`S201_EPR.md` §6/§7).
- **BEA (1966) LTEG non-recoverability.** The 1860–1918 historical segment can never be re-verified against a
  live source (out of print). The salvaged chopped column is the sole authority; loss of that column would make
  the antebellum segment unreproducible. It is preserved in `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_IndustrialProduction.xlsx`.
- **Discontinuation:** none foreseen — FRB G.17 continues monthly and FRED republishes without latency
  (`S201_DPR.md` §7 caveat 6). Should G.17 ever be discontinued the EPR documents the replacement path.
