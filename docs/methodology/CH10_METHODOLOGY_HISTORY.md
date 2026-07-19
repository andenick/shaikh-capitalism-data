# Chapter 10 — Competition, Finance, and Interest Rates — Methodology History Dossier

**Group:** ch10 · **Series:** S1001–S1008 (8) · **Book pages:** 462–474 (figures); 873–874 (Appendix 10.1 Sources and Methods)
**Reasoning stance:** from Anwar Shaikh's own perspective — why *he* constructed each series as he did.
**Companion per-series MHRs:** `Technical/docs/methodology/series/S100{1..8}_MHR.md`
**Machine-readable twin:** `Technical/methodology_review/CH10_methodology.json`

> Grounding: every claim is anchored to a citable path — the research JSONs (`Technical/research/S100N_research.json`),
> `Technical/docs/chapters/CH10_RESEARCH_SUMMARY.md`, the review (`Technical/methodology_review/CH10_review.json`),
> the DPRs/EPRs, the Phase-0 NIPA timeline (`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`),
> and the FISIM concordance (`Technical/docs/methodology/NIPA_T711_FISIM_remap.md`). No claim is invented.

---

## 1. What the chapter builds

Chapter 10 is Shaikh's **classical theory of interest, bond yields, equity returns and stock prices**. Its
empirical agenda has three anti-mainstream prongs (`CH10_RESEARCH_SUMMARY.md` "Chapter scope"):

1. **Anti-Fisher (Gibson's Law).** Long bond yields and corporate rates move with the *price level*, not
   around a constant real rate — S1002 (i vs p), S1003 (i/p real cost of finance), S1004 (the volatile
   HP-smoothed real rate). The micro-foundation is S1001: banking earns an incremental rate of profit
   equalized to all-private industry, so the interest rate is regulated by banking profitability.
2. **Anti-EMH (equity returns track the profit rate).** The equity yield diverges from the bond yield
   (S1005), and the realized equity *total* return sits far above bond returns (S1006, the equity-premium
   numbers); the equity return is turbulently equalized to the *corporate incremental rate of profit*, not a
   constant discount rate (S1007).
3. **The classical "warranted" stock price** computed from the profit rate tracks the actual real price's
   long swings far better than Shiller's constant-r "rational" price P* (S1008, eq. 10.31).

The eight series span **1857–2011** at annual frequency (S1006 1926–2010; S1001 1988–2005) and map
one-to-one to the chapter's figures:

| SID | Fig | What it is | Construction |
|-----|-----|------------|--------------|
| S1001 | 10.1 | Bank vs all-private incremental rate of profit | composite (extraction of App-7.2) |
| S1002 | 10.6 | Long bond yield + producer price index (Gibson's Law) | composite (two spliced series) |
| S1003 | 10.7 | Relative price of finance i/p (1947=1) | formula (transform of S1002) |
| S1004 | 10.8 | Real long bond yield + HP trend | formula (transform of S1002) |
| S1005 | 10.9 | Dividend yield vs govt & corporate bond yields | composite (Shiller + S1002-A) |
| S1006 | 10.10 | Stock / corporate-bond / govt-bond total returns | direct (Ibbotson Table 2-2) |
| S1007 | 10.11 | Real equity rate vs corporate IROP (2 variants) | composite (Shiller + NIPA) |
| S1008 | 10.13 | Actual vs Shiller-rational vs classical-warranted price | composite (eq. 10.31 recursion) |

## 2. The source families

Chapter 10 rests on a tightly-knit set of **public primary sources** plus two derivatives of Ch6/Ch7 IROP
work (`CH10_RESEARCH_SUMMARY.md` "Chapter scope"; per-series `research.primary_source`):

- **Bond yields:** NBER Macrohistory (Macaulay railroad, m13019, 1857–1937); Federal Reserve **HS-39** Aaa
  corporate (1936–2002) + ERP 2012 (2003–2010); modern mirror FRED `AAA`.
- **Prices:** **Jastram (1977) Table 7** WPI (1857–1976); **BLS PPI** growth rates thereafter; modern mirror
  FRED `PPIACO`.
- **Equity:** **Robert Shiller** annual S&P file `ie_data.xls` (price P, dividend D, P*, CPI, 10-yr govt),
  1871→; modern FRED `GS10`.
- **Total returns:** **Ibbotson SBBI 2004** Table 2-2 (Stubbs to 2010) — *Morningstar-commercial*; open
  modern substitute **Damodaran** NYU `histretSP`.
- **NIPA (S1007/S1008 only):** T1.1.9 gross investment deflator (via App. 6.8.II.7); T1.14 corporate NOS +
  **T7.11 monetary interest**; T5.2.3/5.6.3 gross investment; corporate profits.
- **Cross-chapter:** S1001 = the Ch7 App-7.2 industry IROP panel (RSCD **S215**).

**Only S1007 and S1008 touch NIPA.** S1001 touches BEA's Industry Economic Accounts only in its (deferred)
extension; S1002/S1003/S1004/S1005/S1006 rest entirely on bond-yield, price-index, Shiller, and Ibbotson
data and are **not** restated by any NIPA comprehensive update.

## 3. Why these sources — the recurring rationale, and the two concept battles

The chapter's method choices are unified by a single classical logic, and two concept decisions recur across
the eight series:

- **Concept battle 1 — the *incremental* rate of profit (IROP), not the average rate.** S1001 (banking vs
  all-private) and S1007 (equity vs corporate IROP) both anchor on the return to *new* investment,
  `ΔNOS / lagged gross investment (fixed + inventories)`, because Shaikh's turbulent-equalization theory acts
  on the marginal investment dollar (`S1001 research.formula`; `S1007 research.book_quotes[0,2]`). The
  average profit rate would blur the equalization the figures are built to show.
- **Concept battle 2 — the current-cost / production-price frame, NOT the consumption (CPI) frame.** Every
  price deflation in the chapter uses a *production*-side index so numerator and denominator stay
  commensurable: Gibson's Law uses the *producer/wholesale* price index (S1002/S1004, not the CPI); the
  equity return and warranted price are deflated by the *BEA gross investment deflator* (S1007/S1008, not the
  CPI) so they are commensurate with the current-cost profit rate they are equalized to
  (`S1002 research.book_quotes[2]`; `S1007 research.book_quotes[1]`; `S1008` footnote 25). This is Shaikh's
  whole-book capital-theoretic convention, and it is *why* S1008 goes to the trouble of un-deflating Shiller's
  CPI-real P* and re-deflating it by the investment index.

Other recurring choices: **total returns** (Ibbotson) where the point is realized cross-asset return (S1006),
but **running yields** (D/P, coupon) where the point is like-for-like income comparison (S1005); **nominal**
returns left un-deflated where a common deflator would not change the ranking (S1006); the **profit rate, not
a constant discount rate**, as the driver of the warranted price (S1008, eq. 10.31); **No-Lazy-Splices**
everywhere (ratios and HP trends recomputed end-to-end, never spliced — S1003, S1004); and the **1947
current-cost base year** shared with Ch6/Ch7 (S1003).

## 4. The two headline honesty findings

Two findings define ch10's honest limits and its distribution-gate FAIL (`CH10_review.gates.D14 = FAIL, 85`):

### 4a. S1004 "HP3" is really λ=100 — honestly handled, not a defect

Shaikh's Fig 10.8 caption says *"HP-filtered value (parameter = 3)"* and the workbook column is `iblongrealHP3`,
but a Phase-5 lambda sweep proves the operative smoothing parameter is **λ=100**: **MAE = 0.0000 at λ=100 vs
0.022 at λ=3** against the published column (`S1004_DPR.md` §7.4; `CH10_review.s1004_forensic_catch`). The
"HP3" name appears to be a cycle-frequency naming convention, not the Hodrick–Prescott smoothness parameter
Shaikh actually applied — and λ=100 is *also* the textbook annual-data default, so only the label is
idiosyncratic. **Verdict: `honestly_handled_not_a_data_defect`** — the loader pins `_hp_filter(y_book, 100.0)`,
V03 confirms the match, and the book label is preserved with an explicit disclosure across DPR §1/§7.4,
`CH10_RESEARCH_SUMMARY` Phase-5, and P02/V03. The one residual (**Finding H1, MEDIUM**) is that **six stale
"λ=3" labels** remain on public-facing surfaces (registry name/subseries_id/formula, EPR §2, DPR §3/§4, P02
docstring) — a doc-reconciliation debt with **zero data impact** that must be reconciled to satisfy D14
(`CH10_review.findings.H1`; `s1004_forensic_catch.propagation_gap`).

### 4b. S1006 Ibbotson SBBI 2004 is Morningstar-commercial — a redistribution constraint

S1006's book-period columns (`S1006-A/B/C`, large stocks / LT corporate / LT govt total returns, 1926–2010)
are transcribed from the **Ibbotson SBBI 2004 Valuation Yearbook, Table 2-2** (extended to 2010 by David
Stubbs) — now a **Morningstar-commercial product** that **cannot be redistributed**
(`S1006 research.primary_source.license`; `CH10_RESEARCH_SUMMARY.md` open question 1). Yet the registry marks
these columns `publish: true` (**Finding H3, MEDIUM**), which is a licensing/redistribution risk and the main
reason ch10's **D14 distribution gate is FAIL (85 < 90)** (`CH10_review.gates.D14`; `CH10_review.findings.H3`).
The chapter's honest design already provides the fix: the open-license **Damodaran (NYU)** reconstruction is
carried as the modern extension source (`S1006-A-ext`, `S1006-C-ext`, `S1006-B-ext-damodaran`), plus a
FRED-`AAA`-yield PROXY for the LT-corporate line that Damodaran does not publish (flagged `proxy: true` with a
distinct unit string so a yield is never silently mixed with a total return; `S1006_DPR.md` §7.2). Before any
external distribution, the Ibbotson book-period columns must be set `publish: false` (or licensed) and only
the Damodaran reconstruction shipped publicly.

## 5. Methodological-change exposure — the NIPA vintage problem (S1007/S1008 only)

Shaikh fixes all BEA data at the **~2011 vintage** (whole-book convention, `NIPA_CHANGE_TIMELINE.md` §"Why
this matters"). Only S1007 and S1008 are exposed, and S1007's exposure includes one *table-renumbering
time-bomb*:

- **2013 (14th):** R&D + entertainment capitalized (new IPP, ≈+$400B GDP); NOS/CFC and **FISIM/monetary-
  interest magnitudes restated by sector** — moves the S1007 IROP numerator and the investment denominator.
- **2018 (15th):** inserted a new monetary-interest sub-row in **T7.11 → +1 line shift** for every subsequent
  line. This is directly load-bearing: the **"Monetary Interest Paid by the Nonfinancial Sector"** that
  Shaikh adds back into NOS for the *adjusted* corporate IROP (S1007-B) is exactly a T7.11 FISIM magnitude.
  Any hard-coded 2011-vintage line number silently grabs the wrong row on a 2019+ vintage — the mandatory
  resolver is `NIPA_T711_FISIM_remap.md`, which keys on the BEA `LineDescription` stub label, not the line
  number.
- **2023 (16th):** reference year → 2017; re-bases the gross investment deflator that deflates all of S1008's
  three price lines and S1007's equity return.

Because `prweq` (S1008) is a **forward recursion** in S1007's `rI`, any S1007 vintage break **compounds** down
the whole warranted-price path — so S1007 must be fixed before S1008 is extended. Both extensions are
therefore honestly **deferred to Phase 6** pending NIPA vintage pinning and the exact monetary-interest line
lookup (`CH10_RESEARCH_SUMMARY.md` Phase-5 S1007/S1008; chapter open question 3); no ALFRED pin yet. The
non-NIPA series carry only *source-vintage* seams: the Jastram→BLS 1976/1977 PPI splice (S1002, growth-rate,
documented) and the clean same-concept FRED/Shiller/Damodaran extensions at 2011.

## 6. Replication fidelity, at a glance

- **Book period is exact for all 8** — V03 PASS, **MAE ≈ 0** on every book-period comparison (S1004-B at
  1e-06 machine precision); 8/8 PASS, 0 FAIL (`CH10_RESEARCH_SUMMARY.md` Phase-5 table;
  `CH10_review.validation_status`).
- **Three non-circular in-book anchors** (the rest are self round-trips against the salvaged workbook,
  `CH10_review.findings.L5`): **S1006** Table 10.1 means 11.88/6.24/5.91 (EXACT, 3 cells); **S1007** Table
  10.2 + Fig 10.11 mean/SD/CoV grid (EXACT, 9 cells); **S1004-B** Fig 10.8 prose 10/−3/8.3/−4.6 (WITHIN_TOL,
  4 cells) (`CH10_review.hand_checks_noncircular`).
- **D13 data-authenticity gate = PASS (100):** no synthetic/frozen data, no `np.random`; every value traces
  to Appendix 10.2 XLSX / FRED / Shiller / Ibbotson / Damodaran (`CH10_review.gates.D13`).
- **Integration score 95.2 (EXEMPLARY, borderline)** — honestly lowered from a mechanical 98.4 by the deep-read
  findings H1/H2/H3 (`CH10_review.integration_score`, `certification_note`).
- **Honest limits carried forward:** S1006 Ibbotson licensing (H3, blocks D14/external distribution); S1004
  stale λ=3 labels (H1); Fig 10.2/10.3 nominal-rate panels mapped but not shipped (H2); S1001 CD2-S050
  spot-value divergence (L4, informational); S1002/S1004/S1005/S1006 lack a structured `-EXT` extension block
  (L3).

## 7. Per-series index

| SID | Primary concept | NIPA touch | Key honest note |
|-----|-----------------|------------|-----------------|
| S1001 | Bank vs all-private incremental rate of profit | via App-7.2 (extension only → BEA IEA) | pass-through; CD2-S050 spot values diverge (L4); NAICS 52 vs 5221 open |
| S1002 | Long bond yield + PPI (Gibson's Law) | none | Jastram→BLS 1976 splice documented; clean FRED AAA/PPIACO at 2011 |
| S1003 | Relative price of finance i/p (1947=1) | none | formula on S1002; ratio recomputed never spliced |
| S1004 | Real long yield + HP trend | none | **"HP3" = λ=100, honestly handled**; 6 stale λ=3 labels (H1) |
| S1005 | Dividend yield vs bond yields | none | cleanest extension (same Shiller file); corp line inherits S1002-A |
| S1006 | Stock/corp/govt total returns | none | **Ibbotson SBBI 2004 commercial — publish:true is a redistribution risk (H3, D14 FAIL)** |
| S1007 | Real equity rate vs corporate IROP | T1.1.9 + T1.14 + **T7.11** + T5.2.3/5.6.3 | monetary-interest add-back hits the 2018 T7.11 +1 line shift; extension deferred |
| S1008 | Actual vs rational vs warranted price | via S1007 rI + T1.1.9 deflator | eq. 10.31 recursion compounds S1007's rI; adj=6.75 pinned; extension deferred |
