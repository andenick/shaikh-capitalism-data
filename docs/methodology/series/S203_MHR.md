# S203 — US Real GDP per Capita (MeasuringWorth) — Methodological History Report (MHR)

**Group:** ch2 (Turbulent Trends and Hidden Structures) · **Construction:** direct · **Status:** book_period_validated
**Figure:** 2.3 · **Predecessor:** CD/CD2 S003 · **Publish:** true · **Book period (plotted):** 1889–2010 · **Extension:** 2011–2025
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.
**Carries CH2-review findings F-01 (HIGH, source corruption — ✅ REMEDIATED 2026-07-01, Decision 0008) and F-04 (MED, naming) — see §5.**

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S203_research.json`), the DPR/EPR (`Technical/docs/series/S203_{DPR,EPR}.md`),
> the book KB (Body_Text `ch02_turbulent_trends.md`, Figure `ch02_fig_2.3.md`), the CH2 review
> (`Technical/methodology_review/CH02_review.json`, findings F-01/F-04 + hand_check), and the Phase-0 NIPA
> timeline. Where a rationale is not present in the corpus it is marked **"author rationale not located in
> corpus."**

---

## 1. What the series is

S203 is annual **US Real GDP per Capita**, plotted **log-scale** as **Figure 2.3** — the third and final leg of
Shaikh's Chapter-2 growth trio. The book figure title is **"US Real GDP per Capita, 1889–2010"** and it plots
**1889–2010** (KB `Figures/ch02/ch02_fig_2.3.md`: log y-axis $1,000→$100,000, ~121 years), even though the text
of the trio at book p. 56 calls it "real GNP per capita" (KB `Body_Text/ch02_turbulent_trends.md` line 13;
`S203_research.json` book_quotes[0], role=definition). It is the per-capita real-output leg of the "distant
view" of 150-year secular growth (`S203_DPR.md` §2).

The authoritative source line is **Appendix 2.1 (book p. 763)**, transcribed verbatim in
`S203_research.json` book_quotes[1] (role=source, verbatim_check=true):

> "Figure 2.3 US Real GDP per Capita, 1889–2010. 1790–2010, from Measuring Worth.com at
> http://measuringworth.com/usgdp/. Their sources and methods are described in their link "Source and
> Techniques Used in the Construction of Annual GDP, 1790 – Present.""

**Caption/coverage discrepancy (documented, not an error to fix here):** Appendix 2.1 says the data run
**1790–2010** but Figure 2.3 *plots* **1889–2010** (`S203_research.json` methodology_notes[1];
`year_range_book = [1889, 2010]`). The chopped file in fact carries values back to 1780
(`Technical/chopped/S203.csv` header rows begin 1780) — i.e. the full MeasuringWorth span is stored, the figure
plots the 1889-on window.

## 2. Source lineage

S203 is a **direct port** (not a splice) of one dataset — MeasuringWorth's `usgdp`:

| Subseries | Coverage | Agency / dataset | Native units | Retrieval |
|---|---|---|---|---|
| **S203-A** | 1780/1889–2010 | **MeasuringWorth (Officer & Williamson), "Annual GDP of the United States, 1790–Present", `usgdp` dataset — Real GDP per Capita variant** | Real (constant 2005) dollars | Salvaged chopped `Appendix2_MeasuringWorthGDP_1889-2010.xlsx` |
| **S203-B** | 2011–2025 | **FRED `A939RX0Q048SBEA`** (Real GDP per Capita, chained 2017$) — automated reindex anchor | Chained 2017$ | FRED API |

**Chain (`S203_DPR.md` §4, `S203_EPR.md` §2):**

```
MeasuringWorth usgdp Real-GDP-per-capita column  [book: 1889–2010, stored 1780–2010, real 2005$]
    → direct read (no in-period splice)
FRED A939RX0Q048SBEA [2011–2025, chained 2017$]  → reindex at 2010 overlap → append
```

MeasuringWorth is a *synthesis* source: it stitches **Kuznets**, **Balke–Gordon**, and **BEA NIPA** estimates
into one continuous 1790–present real-GDP series (`S203_research.json` methodology_notes[2]). Its published
"Sources and Techniques" note is the second-order provenance Shaikh points to (Appendix 2.1). The upstream BEA
NIPA leg is documented in `SalvagedInputs/methodology_library/D_data_methodology/WL-D-NIPA-*__BEA-NIPA.pdf`;
the historical Kuznets/Balke–Gordon reconstruction lineage sits with the historical-statistics corpus
(`WL-D-HSUS-*__Census-HSUS`, `WL-D-HistCap-*`). MeasuringWorth itself has no dedicated methodology-library PDF in
the salvaged corpus — its methodology is the external "Source and Techniques" web note named in Appendix 2.1.

## 3. Why these sources, from the author's perspective

**The concept Shaikh measures.** Long-run real output *per capita* — the living-standard leg of the growth trio,
needing an unbroken series from the 19th century to 2010. MeasuringWorth is the standard scholarly synthesis that
provides exactly this (it is the same source Shaikh uses for the CPI leg elsewhere, `Appendix15_MeasuringWorthCPI.xlsx`,
and jointly with BEA for Fig 2.5, book p. 60 KB body text line 210).

**Why MeasuringWorth rather than a single official series.** No single official US series runs continuously back
to 1790/1889 at annual per-capita real terms; MeasuringWorth is the canonical academic reconstruction that
splices Kuznets → Balke–Gordon → BEA NIPA into one series with a published methodology (Appendix 2.1 explicitly
directs the reader to MeasuringWorth's "Source and Techniques" note). The US-focus meta-rationale (book p. 56,
KB `Body_Text/ch02_turbulent_trends.md` lines 6–9: "the United States … generally has the best available data")
again governs the choice. Shaikh does **not** narrate a comparison against alternative long-run GDP
reconstructions (e.g. **Maddison**, **Johnston–Williamson variants**, **BEA-only back to 1929**) for this figure
— **author rationale for rejecting alternatives is not located in corpus** beyond the Appendix 2.1 naming.
(Maddison *is* used deliberately elsewhere in Ch2 — Figs 2.15–2.17, book pp. 71–72 — for the world-regions view,
which is a different concept; that is not a rejection of Maddison for Fig 2.3, merely a different task.)

**Why the extension continues MeasuringWorth (with FRED as reindex anchor).** The extension is definitionally the
same source/program continued; FRED `A939RX0Q048SBEA` is used only to automate the post-2010 reindex, not to
substitute a different concept (`S203_EPR.md` §2/§3, "No proxies used. All extension sources are the same
agency/program as the original"; `S203_research.json` extension_candidates[0]: "Same source as original; direct
continuation with re-indexing only if dollar base year changes").

## 4. Methodological-change exposure

S203's modern segment ultimately rests on **BEA NIPA** (via MeasuringWorth's BEA leg and via the FRED
`A939RX0…SBEA` extension), so it inherits NIPA comprehensive-revision exposure — but *filtered through
MeasuringWorth's own revision cadence*:

- **BEA NIPA restatements propagate into MeasuringWorth.** When BEA re-benchmarks (2013 R&D/IPP ≈ +$400B; 2018
  2012-benchmark I-O; 2023 reference year → 2017), MeasuringWorth re-splices its modern (BEA) leg accordingly, so
  the level of the recent-decades portion of `usgdp` shifts between MeasuringWorth vintages
  (`NIPA_CHANGE_TIMELINE.md` 2013/2018/2023 rows; `S203_research.json` open_questions: "MeasuringWorth
  occasionally revises historical estimates; document the access date when extending"). The book value is frozen
  at Shaikh's ~2011 pull.
- **FRED extension base-year drift.** `A939RX0Q048SBEA` is chained-2017$; the 2023 revision moved the reference
  year to 2017. As with S201, level drift from re-basing is neutralized by the overlap-anchor reindex at 2010 —
  but the extension segment is on a *post-2013, IPP-inclusive* GDP concept, broader than Shaikh's pre-2013
  2005-dollar MeasuringWorth base. **Do not splice across the 2013 boundary without re-anchoring**
  (`NIPA_CHANGE_TIMELINE.md` §"Why this matters").
- **Unit-base mismatch to manage.** Book series is real **2005 dollars**; FRED extension is chained **2017
  dollars** (`S203_DPR.md` §6, §3 table). The reindex at the 2010 overlap converts the extension onto the book's
  level; the units label must not be silently overwritten.

**I-O touchpoint:** indirect (BEA leg incorporates successive benchmark I-O). **Concordance dependency:** none at
the series level. **NIPA dependency:** indirect but real, on both the modern book leg and the extension.

## 5. Replication fidelity note — ⚠ CARRIES REVIEW FINDINGS F-01 & F-04

**F-01 (HIGH, D13, source corruption — must be remediated before external publish).** The salvaged workbook
column S203 is byte-faithful to — `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_MeasuringWorthGDP_1889-2010.xlsx`
— is **corrupted across the Great Depression**. Real GDP per capita **rises** through 1929–1934, which is
economically impossible (the Depression trough should show a ~25–30% *fall*). Verified directly in
`Technical/chopped/S203.csv`:

| year | value (real 2005$) |
|---|---|
| 1929 | 8,187.56 |
| 1930 | 8,831.99 |
| 1931 | 10,240.48 |
| 1932 | 11,999.11 |
| 1933 | 13,771.49 |
| 1934 | 14,705.52 |

An honest MeasuringWorth series falls sharply 1929→1933. The RSCD chopped was **faithful to a corrupted source
column**, not fabricated — the corruption is upstream in the salvaged workbook. Critically, **V03 was structurally
blind to it**: the validator round-tripped the *same* corrupted XLSX it built the chopped from, so its "MAE 0.0 /
PASS" was meaningless for detecting this defect (`CH02_review.json` F-01 + hand_checks → S203, verdict
`SOURCE_CORRUPT`: "1929-34 real GDP/cap rises through Depression; faithful to corrupted salvaged workbook; V03
PASS meaningless").

**✅ F-01 REMEDIATED 2026-07-01 (Decision 0008 / campaign T1.2, agent C34).** The corrupt span was diagnosed
precisely as **1930–1944** (comparison against the fresh MeasuringWorth vintage: only those years carry the
Depression-rise defect, at 30–107% deviation from the vintage-predicted level; pre-1930 and post-1944 differ from
the current vintage only by ordinary re-estimation drift). Fix, implemented in the pipeline
(`P02_S203._correct_depression()`), never by hand-editing and never touching the salvaged workbook:

- Fresh re-pull of MeasuringWorth `usgdp` Real GDP per capita (2026 vintage, year-2017 dollars), retrieved
  2026-07-01 via the site's `export.php` CSV endpoint; raw committed at
  `Technical/data/raw/S203_MEASURINGWORTH_USGDP_repull_20260701.csv` (loaded by `L01_S203._load_repull()`).
- Re-based 2017$ → book 2005$ level by **overlap reindex at 1929** (scale = book(1929)/repull(1929) =
  0.83778289). Decision 0008 named 2010, but the book column ends at 2000 (2001–2010 NaN in the salvaged
  workbook), so the anchor is the last non-corrupt year adjacent to the replaced span; 1945 far-boundary
  continuity = −1.05% (within ordinary MeasuringWorth vintage drift).
- Only the 15 corrupt rows 1930–1944 replaced; all other rows byte-identical. Corrected 1929→1933 =
  **−28.57%, strictly falling** — the registry plausibility rule `S203_depression_must_fall` (Decision 0011
  machinery) flipped RED→GREEN, and the anchor lib is now wired into `V03_S203` (a RED fails the validator;
  the corrected 1930–1944 span is excluded from the book-XLSX round-trip since the book source is corrupt there).
  `publish: true` stands — the block Decision 0008 imposed was "until landed", and the fix is landed + verified.

**F-04 (MED, D5, naming).** The registry name **"US GDP (MeasuringWorth)"** / research-JSON name "US Real GDP per
Capita (MeasuringWorth)" **omits "per Capita"** relative to the book figure title "US Real GDP per Capita,
1889–2010", and the stored `year_range` differs from the plotted figure range (`CH02_review.json` F-04;
`S203_research.json` methodology_notes[1]). This MHR uses the correct book title. Do not propagate the truncated
"US GDP (MeasuringWorth)" label downstream.

**Otherwise-honest construction.** Setting aside the corrupted Depression rows, S203 is a faithful direct port:
the chopped reads Shaikh's own retrieved MeasuringWorth column; expected MAE < 0.5% vs the salvaged book truth
(`S203_DPR.md` §9). No proxy, no synthetic interpolation — FRED NaN propagates, overlap-year NaN triggers
walk-back then hard fail (`S203_EPR.md` §3/§4/§5). CD2 divergence is informational only (§6). The failure here is
*source-integrity*, not method or fabrication.

## 6. Forward risk

- **~~The corruption ships until re-pulled~~ — RESOLVED 2026-07-01 (see §5).** The 1930–1944 span is now
  produced from the fresh MeasuringWorth re-pull (re-based at the 1929 overlap), the out-of-source sanity
  assertion (1929 > 1933, `S203_depression_must_fall`) is registered AND wired into V03_S203 (a plausibility
  RED fails the validator), and the corrected span is excluded from the corrupt-book round-trip. Residual risk:
  the re-pull raw CSV (`S203_MEASURINGWORTH_USGDP_repull_20260701.csv`) is now a committed pipeline input —
  do not delete it, or L01 falls back to flagging the fix SKIPPED (which the plausibility gate will catch as RED).
- **MeasuringWorth silent revisions.** MeasuringWorth periodically re-estimates historical values and re-splices
  its BEA leg on each NIPA benchmark; two extensions pulled on different dates can disagree in *both* the recent
  decades (BEA vintage) and the deep history (Kuznets/Balke–Gordon re-estimates). Always record the access date
  (`S203_research.json` open_questions; `S203_DPR.md` §7 caveat 2). Freeze the book series; never live-refresh it.
- **2005$ → 2017$ (and next) base drift.** The FRED extension's base year moves with BEA re-basing; the reindex
  must re-anchor at the 2010 overlap on every run, and the units string ("real 2005 dollars") must not be silently
  overwritten by the extension's 2017$ base.
- **Concept widening at 2013.** As with S202, the post-2013 GDP concept (IPP-inclusive) is broader than the
  pre-2013 book base; the extension segment silently measures a wider aggregate. Extend on one coherent post-2013
  vintage, re-anchored at 2010 (`NIPA_CHANGE_TIMELINE.md` §"Why this matters").
- **MeasuringWorth licensing/availability.** MeasuringWorth is academic-use-with-attribution and web-hosted
  (`S203_DPR.md` §7 caveat 1); loss of the site would leave only Shaikh's salvaged column (itself the corrupted
  one) — a re-pull to fix F-01 is time-sensitive against site availability.
