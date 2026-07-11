# XS2101 — Methodological History Report (MHR)

**Series**: XS2101 — Sraffa Price Curvature Index / Theil Statistics, US BEA 2002 + 2007 (Shaikh-Coronado-Nassif-Pires 2020)
**Chapter**: 0 (`xs_class: external_study`) · **Group**: external-study family 21 · **Status**: study_complete
**Perspective**: authored *from Shaikh's perspective* — why *he* built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS2101_research.json`; `Technical/docs/series/XS2101_DPR.md` +
`XS2101_EPR.md`; `Technical/docs/external_studies/XS2101_paper_summary.md` + `ES_PHASE_5_8_CLOSURE.md`;
Phase-0 `Technical/docs/methodology/_timelines/IO_CHANGE_TIMELINE.md` (+ `NIPA_CHANGE_TIMELINE.md`);
`Technical/methodology_review/CH_XS_review.json`.

Paper of record: Shaikh, A., Coronado, J.A. & Nassif-Pires, L. (2020), "On the empirical regularities
of Sraffa prices", *European Journal of Economics and Economic Policies: Intervention* 17(2): 265–275,
DOI 10.4337/ejeep.2020.0069. Archival PDF:
`SalvagedInputs/methodology_library/B_shaikh_post2016/WL-B-Sraffa/` and
`Inputs/Capitalism Data/.../Shaikh Publications/[2020] Shaikh Coronado & Nassif-Pires - On the empirical regularities of Sraffa prices.pdf`
(`XS2101_paper_summary.md` header). Companion to XS2001 (same 2002 matrix, same labor pipeline).

---

## 1. What it is

XS2101 is Shaikh-Coronado-Nassif-Pires's **Curvature-Index (CI) distribution study** — a *derived*
dataset that measures the *shape* of individual Sraffa price curves across many matrix sizes. The
paper computes Sraffa price-of-production curves `p(r)` as the profit rate `r` runs from 0 to its
maximum `R` (i.e. `r/R` from 0 to 1) for **295 input-output matrices**: the 2002 US 403/425-order and
2007 US 383/387-order benchmark tables, successively aggregated into **8 nested NAICS levels each**,
plus the 1977/1982/1987/1992/1997 detailed benchmarks (paper Section 2, p.267, `research.json`
book_quotes[1], `verbatim_check: true`):

> "We used the US 2002 403-order and 2007 387-order benchmark tables of Sraffian basic commodities and
> successively aggregated them to get a total of 295 matrices for these two years ranging from
> 15-order to the largest in each year. We then further expanded our sample with the 1977, 1982, 1987,
> 1992, and 1997 benchmark tables at the detailed level."

For each matrix it computes the **Curvature Index** `CI = 1 − SI`, where `SI` = (length of the
Bienenfeld linear approximation) / (arc length of the actual Sraffa price curve): `CI = 0` means
perfect linearity (curve = Bienenfeld line), `CI → 1` means extreme tortuosity (`research.json`
methodology_notes[2]; `XS2101_paper_summary.md` §3). The paper's empirical object is the **statistical
distribution of CI across the 295 matrices** (Figure 6, Average CI by matrix size; Figure 7, Theil
index of CI), plus the headline switching counts.

**RSCD v1.0 ships only the verbatim named summary statistics** of paper **Section 5 (p.272)** — a
10-row transcription (`XS2101_DPR.md` §1; `ES_PHASE_5_8_CLOSURE.md` = 10 chopped rows). The headline
(paper Section 5, p.272, `research.json` book_quotes[3], `verbatim_check: true`):

> "Across all levels of aggregation in both benchmark years, the average CIs range between 0.03 to
> 0.06. In 2002 only 26 (6.1 percent) of 425 prices switch from one side of their labor value to the
> other. Only four (0.9 percent) switch with respect to the Bienenfeld line, none with a deviation
> greater than 1 percent."

The full ~295-point CI/Theil scatters of Figures 6–7 are **deferred to v1.1** alongside XS2001's
pipeline (`XS2101_DPR.md` §7 caveat 1). The Sraffa price definition Shaikh normalizes each curve to
(paper Section 3, p.267, `research.json` book_quotes[0], `verbatim_check: true`): each price curve is
normalized to its initial value = the labor value of that commodity, so the start equals 1
(Sraffa 1960:12, sec.14).

## 2. Source lineage

XS2101's *data of record* for v1.0 is the paper's own Section-5 summary numbers, transcribed to
`SalvagedInputs/book_data/Reconstructed/XS2101_summary_statistics.csv` (`XS2101_DPR.md` §3). Behind
those numbers is the same primary lineage as XS2001 — this is **IO-touch + concordance-touch, not
NIPA** (`research.json` primary_source; `XS2101_paper_summary.md` §3):

- **BEA Benchmark Input-Output Data** (Industry-by-Industry Direct Requirements / Use & Make tables),
  detailed level, benchmark years **1977, 1982, 1987, 1992, 1997, 2002, 2007** — the `A`-matrix source,
  derived from Use/Make via the Industry Technology Assumption. Post-exclusion orders 425/2002 and
  383/2007 (basic + non-basic); the 403/387 figures are the *basic-commodity-only* orders used for the
  companion eigenvalue analysis (`research.json` methodology_notes[5]).
- **BLS** use-matrix compensation-of-employees + employment → **skill-adjusted labor coefficients** `l`.
  The verbatim method (paper Appendix 2, p.275, `research.json` book_quotes[2], `verbatim_check: true`):
  "We create skill-adjusted sectoral labor inputs by using the compensation of employee entries in the
  use matrices published by the BLS, normalizing them by the ratio of aggregate employee compensation
  to aggregate employment (Shaikh 2012:98)."
- **Census NAICS classification** + BEA/BLS aggregation correspondences — the **8 nested aggregation
  levels** per benchmark year that generate the 295-matrix rollup (2002: 176 levels; 2007: 119 levels;
  `research.json` components[2], methodology_notes[4]; `research.json` primary_source
  secondary_sources_used[1]). This is the `concordance_touch`.

`concordance_touch` detail: the aggregation ladder (425/383 → 342/318 → 161/197 → 120/142 → 63/88 →
30–33/49 → 17 → 15/16 industries) plus BLS-170 and BEA-summary-71/133 crosswalks
(`research.json` components[2]) is the machinery that *produces* the CI distribution — the whole point
of the paper is how CI behaves **as matrix order changes**, so the concordances are load-bearing, not
incidental.

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

- **Why the Curvature Index, not raw curvature or a second-eigenvalue ratio.** The paper needs a
  *scale-free, comparable* measure of how far each price curve departs from linearity, poolable across
  matrices of wildly different order (15 to 425). `CI = 1 − SI` (arc-length ratio to the Bienenfeld
  line) is bounded in [0,1], has a clean interpretation (0 = linear, 1 = maximal tortuosity), and is
  invariant to the number of sectors — exactly what is required to test whether curvature *falls with
  matrix size* (Bródy's hypothesis). A raw curvature or a spectral-gap statistic would neither be
  bounded nor directly comparable across orders.
- **Why the Bienenfeld line as the reference, not a fitted regression or a chord.** Bienenfeld's (1988)
  linear approximation `p(r) = v + (r/R)(R p(R) H − v)` is not an arbitrary line: it **starts at the
  labor value `v` at r=0 and ends at the price of production `p(R)` at r=R**, sharing both endpoints
  (and the initial slope) with the true Sraffa curve (`research.json` formula; XS2001 book_quotes[0]).
  It is therefore the *theoretically privileged* straight line — the null against which "how nonlinear
  is the true curve" is the meaningful question. A least-squares line would confound endpoint mismatch
  with genuine curvature.
- **Why 295 aggregated matrices, not one detailed matrix.** The scientific target is **Bródy's
  random-matrix hypothesis** — that price curvature should *decline* as matrix size grows (large random
  matrices → near-linear). To test it you must vary matrix order systematically and watch CI. A single
  403-order matrix gives one CI; the nested-aggregation ladder gives a *distribution over order* that
  either confirms or (as the paper finds) **undercuts** Bródy: CI stays in 0.03–0.06 across *all*
  sizes, so curvature does not fall with size in the predicted way (`XS2101_paper_summary.md` §1).
- **Why restrict to US data.** Two reasons stated in the paper (p.267 fn 1; `research.json`
  methodology_notes[3]): (a) the US economy is relatively closed — ~90% of goods produced domestically
  1977–2007 — so a single-country closed I-O model is a good approximation; (b) BEA supplies
  high-quality benchmark tables at the required industry detail. Multi-country data (e.g. EU tables)
  exist only at much smaller 51–58 order (Iliadi/Mariolis et al. 2014, cited in XS2001) and would not
  support the large-matrix test.
- **Why skill-adjusted labor, not head-count.** Same rationale as XS2001 — direct prices are
  proportional to abstract (skill-reduced) labor time; compensation-weighting reduces heterogeneous
  concrete labor to a common standard (paper Appendix 2).
- **Rejected alternative — digitizing Figures 6/7 to recover the CI series.** Explicitly forbidden:
  "Replicators must NOT digitize figures; must reconstruct via equations A1–A3 from BEA + BLS source
  data (no-fabrication standard)" (`XS2101_paper_summary.md` §6 open-question 5; `research.json`
  open_questions[3]). The paper does **not** tabulate the CI/Theil values (they appear only as
  scatters), so v1.1 must **recompute** them, not trace the plots.
- **Rejected alternative — decomposing into XS2101/2102/2103/2104.** The dossier records that all
  seven figures derive from one primary dataset via one pipeline, so a split "would create artificial
  dependency chains"; kept as a **single composite series** (`research.json` open_questions[0]).

## 4. Methodological-change exposure — **the central section**

XS2101 is squarely in the **NAICS era** (2002 and 2007 benchmarks), so its exposure is *NAICS-benchmark
drift within NAICS*, not the SIC→NAICS wall that cleaves XS2001 and S901 — though the pre-2002 detailed
benchmarks it also samples (1977/1982/1987/1992 SIC; 1997 first-NAICS) do straddle the wall.

1. **NAICS industry-order drift across benchmarks.** Even within NAICS, "the summary/detail row-column
   order and aggregation are revised at each benchmark, so industry indices are **not stable across
   benchmark years**" (`IO_CHANGE_TIMELINE.md` "Industry order / detail notes"). The 2002-NAICS and
   2007-NAICS matrices are *not* the same industry scheme; the aggregation correspondences that build
   the 8 nested levels differ per year. This is why the paper reports CI **per year** (2002 vs 2007
   scatters kept separate in Figures 6–7) rather than pooling — the matrices are comparable in
   *statistical distribution of CI*, not in industry identity.
2. **1997 = first NAICS benchmark, hard break from SIC.** The paper's sample reaches back to
   1977/1982/1987/1992 (SIC-basis) and 1997 (first NAICS). Per the timeline, 1992 is the **LAST
   SIC-basis benchmark** and the pre-1997 tables "should not be used as a time series"
   (`IO_CHANGE_TIMELINE.md`). The paper sidesteps this because it never builds a *time series of A
   matrices* — it treats each benchmark as an independent matrix from which to draw CI observations, so
   the non-conformability of SIC vs NAICS orders does not corrupt the CI *distribution* (each matrix's
   CI is intrinsic to that matrix).
3. **Concordance authority (`concordance_touch`).** The nested-aggregation ladder depends on Census
   NAICS revision concordances (1997→2002→2007→…) and BEA/BLS crosswalks; these are staged under
   `concordances/_sources/naics/` (`IO_CHANGE_TIMELINE.md`; shared-brief). Any v1.1 recompute must pin
   the exact concordance vintage used per benchmark to reproduce the 176/119 aggregation levels.
4. **Extension to 2012/2017 benchmarks introduces fresh NAICS revisions.** BEA benchmark I-O is
   quinquennial; 2012 (2012 NAICS, incorporated into the 2018 NIPA update) and 2017 (2017 NAICS,
   incorporated into the 2023 harmonized update) each arrive on a revised NAICS with new sector
   boundaries — "bridging required for cross-year comparability of A matrices" (`research.json`
   extension_candidates concerns). The 2007→2012 I-O concordance is in SCB Aug 2018 App. A
   (`IO_CHANGE_TIMELINE.md`).
5. **BLS labor-input crosswalk staleness.** The paper cites `bls.gov/emp/classifications-crosswalks/
   sect300.xls` for the labor-input crosswalk; that URL is stale by 2026 (BLS reorganized Employment
   Projections data). v1.1 must substitute the current BLS EP industry data — "a URL migration within
   an active domain, NOT a data-source proxy" (`XS2101_EPR.md` §3; `XS2101_DPR.md` §7 caveat 3).
6. **NIPA vintage (indirect).** The 2002 and 2007 benchmarks were incorporated into the 2009 and 2013
   NIPA comprehensive revisions respectively (`IO_CHANGE_TIMELINE.md`). A re-pull of these Use/Make
   tables at a later vintage would land on restated magnitudes; stay on one coherent vintage
   (`NIPA_CHANGE_TIMELINE.md`).

## 5. Replication fidelity note

RSCD reproduces XS2101 **bit-exact to the paper's Section-5 named summary statistics** by verbatim
transcription: `XS2101_summary_statistics.csv` → chopped → parquet, V03 cell-by-cell against the CSV.
Result: **PASS, MAE 0.0, max %err 0.00%, 10 rows**, tolerance 0.5% (`ES_PHASE_5_8_CLOSURE.md` table;
`XS2101_DPR.md` §9). Honest limits, disclosed:

- **v1.0 is 10 numbers, not the 295-matrix distribution.** RSCD ships the *headline* stats (average CI
  band 0.03–0.06; 26/6.1% labor-value sign switches; 4/0.9% Bienenfeld switches; the aggregation-count
  constants) — **not** the underlying CI/Theil scatters of Figures 6–7. Those require the full
  BEA-to-Sraffa pipeline and are **deferred to v1.1**, shared with XS2001 (`XS2101_DPR.md` §7 caveat 1;
  `XS2101_EPR.md` §2). The "295 matrices = 176 (2002) + 119 (2007)" figure is a **methodology
  constant**, not a data point (`XS2101_DPR.md` §7 caveat 2).
- **Self-consistency, not independent re-read.** As with all external-study series, V03 confirms the
  transcription round-trips cleanly (melt vs reconstructed CSV) — it is **not** an independent re-read
  of the EJEEP PDF nor a recomputation from BEA/BLS source. MAE 0.0 = transcription fidelity only
  (shared-brief §5).
- **The pipeline is unbuilt in v1.0.** No `A`-matrix, no eigenvalue `R`, no `p(r)`, no CI is computed.
  v1.1 recomputes: 295 aggregated `A` matrices → per-matrix `p(r)` at 21 sample points → per-matrix
  `CI = 1 − SI` → per-matrix Theil → full Figures 6/7 reconstruction → extension to 2012/2017
  (`XS2101_EPR.md` §2). Estimated 3–5 days, jointly with XS2001 (`ES_PHASE_5_8_CLOSURE.md`
  v1.1-deferrals).
- **Skill-adjustment recipe is delegated upstream.** The exact compensation-weighting scheme is
  delegated to Shaikh (2012:98) and not fully restated in the paper; v1.1 must cross-reference that
  chapter for the precise construction (`research.json` open_questions[5]; `XS2101_paper_summary.md`
  §6 open-question 4).
- **No proxies, no synthetic data.** v1.0 is verbatim transcription; the only substitution contemplated
  is the BLS URL migration (same agency, renamed program), which is not a data proxy (`XS2101_EPR.md`
  §§3–5).

## 6. Forward risk

- **v1.1 shared pipeline is the whole extension** — and it is shared with XS2001, so both series unlock
  together. It must **recompute** CI/Theil from BEA+BLS via eqs A1–A3, never digitize Figures 6–7
  (`research.json` open_questions[3]; no-fabrication rule).
- **2012/2017 benchmark extension needs NAICS bridging.** Each new benchmark arrives on a revised NAICS
  with new sector boundaries; cross-year `A`-matrix comparability requires the documented I-O
  concordance (SCB Aug 2018 App. A for 2007↔2012), and the aggregation ladder must be rebuilt per
  vintage (`research.json` extension_candidates; §4 above).
- **BLS Employment Projections URL migration.** The paper's `sect300.xls` crosswalk is stale; v1.1 must
  locate the current BLS EP industry-data successor and pin it (`XS2101_DPR.md` §7 caveat 3;
  `XS2101_EPR.md` §3). Same-agency renaming, not a proxy — but a real re-verification task.
- **Companion-paper dependency.** The rank-size eigenvalue analysis referenced in Section 2 lives in
  Shaikh, Nassif & Coronado (2018) NSSR WP #1812; full replication of XS2101's basic-commodity ordering
  may need that pipeline, and it overlaps heavily with XS2001 (`research.json` open_questions[3];
  `XS2101_paper_summary.md` §6 open-question 3).
- **NIPA comprehensive revisions** keep restating the 2002/2007 Use/Make magnitudes under any re-pull;
  stay on one coherent vintage (`NIPA_CHANGE_TIMELINE.md`).
