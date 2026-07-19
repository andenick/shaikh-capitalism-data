# Chapter 15 — Modern Money and Inflation — Methodology History Dossier

**Group:** ch15 · **Series:** S1501–S1509 (9) · **Book pages:** 696–719 (chapter); 895–897 (Appendix 15.1)
**Reasoning stance:** from Anwar Shaikh's own perspective — why *he* constructed each series as he did.
**Companion per-series MHRs:** `Technical/docs/methodology/series/S150{1..9}_MHR.md`
**Machine-readable twin:** `Technical/methodology_review/CH15_methodology.json`

> Grounding: every claim is anchored to a citable path — the research JSONs (`Technical/research/S150N_research.json`),
> `Technical/docs/chapters/CH15_RESEARCH_SUMMARY.md`, the review (`Technical/methodology_review/CH15_review.json`),
> the DPRs/EPRs, the IMF IFS remap (`Technical/docs/methodology/IFS_line_to_SDMX_remap.md`), and the Phase-0
> NIPA/IO timelines (`Technical/docs/methodology/_timelines/{NIPA,IO}_CHANGE_TIMELINE.md`). No claim is invented.

---

## 1. What the chapter builds

Chapter 15 develops Shaikh's **classical theory of fiat-money inflation**: under modern fiat money, the extra
nominal demand each period is financed by newly created credit plus net foreign inflows, and inflation follows
the pressure that credit growth puts on the economy's growth capacity. The empirical content runs along three
threads (`CH15_RESEARCH_SUMMARY.md` "Chapter scope"):

1. **The two-century US price level** — the motivating fact (Fig 15.1 = S1501): flat under gold, monotonically
   rising under fiat.
2. **The postwar US "new purchasing power" nexus** — nominal GDP growth vs credit + current account (Figs
   15.3/15.4 = S1504), the industry-growth backdrop (Figs 15.2A/B = S1502/S1503), and Shaikh's **Classical
   vs Conventional Phillips curves** (Figs 15.7–15.9 = S1505/S1506/S1507).
3. **International credit→inflation cross-sections** — Harberger's 29 countries (Fig 15.12 = S1508) and
   Ramamurthy's 39-country update (Fig 15.13 = S1509).

| SID | Fig | What it is | Construction |
|-----|-----|------------|--------------|
| S1501 | 15.1 | US consumer price level, 1774–2011 | direct (MeasuringWorth USCPI) |
| S1502 | 15.2A | Real-output growth, 8 goods/trade industries | formula (BEA GDP-by-Industry) |
| S1503 | 15.2B | Real-output growth, 9 services/gov industries | formula (BEA GDP-by-Industry) |
| S1504 | 15.3/15.4 | Nominal GDP growth vs relative new purchasing power | composite (BEA NIPA + IMF IFS) |
| S1505 | 15.7 | Classical vs Conventional Phillips curves, 1948–2010 | composite (π, σ, uL) |
| S1506 | 15.8 | Same, 1948–1981 (pre-neoliberal) | derived_subperiod of S1505 |
| S1507 | 15.9 | Same, 1982–2010 (post-neoliberal) | derived_subperiod of S1505 |
| S1508 | 15.12 | World inflation vs credit growth, 29 countries | direct (Harberger 1988) |
| S1509 | 15.13 | World inflation vs credit growth, 39 countries | direct (Ramamurthy 2014) |

All nine have CD2 predecessors (S076–S089), so ch15 was a **port-and-validate** exercise, not greenfield
research (`CH15_RESEARCH_SUMMARY.md`). The chapter review scores **80.2 (ADEQUATE)**, with the **D14 gate
BELOW_THRESHOLD (84)** — external distribution is blocked until units labels and source citations reconcile
(`CH15_review.gates.D14`).

## 2. The source families — NIPA-heavy, with an honest IMF IFS remap

Seven of nine series touch **BEA NIPA**; three additionally rest on **IMF IFS Monetary Survey** credit/CPI
lines; two rest on secondary scholarly compilations (Harberger 1988, Ramamurthy 2014):

- **BEA NIPA** (the spine):
  - **T1.1.5 line 1** — nominal GDP (S1504; book prints the typo "Table 1.15" → corrected to T1.1.5).
  - **T1.1.4** — GDP deflator → inflation `π` (S1504 pGDP; S1505–S1507 π).
  - **T4.1 line 29** — current account balance CA (S1504).
  - **T5.3.5 line 2** (Nonresidential Private Fixed Investment) and **T1.16 line 2** (Net Operating Surplus) —
    Shaikh's growth-utilization rate `σ = I/Profit`, per **Handfas (2012)** (S1505–S1507).
  - **BEA GDP-by-Industry** real value added — industry growth rates (S1502/S1503).
- **IMF IFS Monetary Survey** (the credit spine): **line 32** (Total Domestic Claims) and Shaikh's US 4-line
  hand-sum **31 + (78 − 88) + 79 + 81**; **line 64** (CPI inflation). Feeds S1504 (US), S1508 (Harberger),
  S1509 (Ramamurthy).
- **MeasuringWorth USCPI** (S1501); **BLS** civilian unemployment `uL` via Ch14 Appendix 14.2 (S1505–S1507).

**Cross-chapter reuse:** `uL` is the Ch14 Phillips-curve x-axis (S1404/S1405); `σ` first appears in Appendix
14.2; inflation `π` is reused in Ch12 Figs 12.5–12.8 (`CH15_RESEARCH_SUMMARY.md` cross-references).

## 3. The three methodological set-pieces of the chapter

### 3a. The IMF IFS line→SDMX remap — a *code-remap*, not a proxy (the exemplary honest disclosure)

Shaikh's IFS references (lines 31, 32, 64, 78, 79, 81, 88) are **pre-2009 print/CSV-era identifiers**, retired in
two events: the **2009 SDDS+ migration** (→ SRF codes `FOSAOP_XDC` …) and the **~2024 SDMX-3.0 portal migration**
(→ indicator codes `DCORP_*`, `ODCORP_*`, `CBANK_*` on `api.imf.org`). The resolver
(`Technical/code/loaders/_imf_ifs_resolver.py`) maps the legacy lines through both eras; Shaikh's 4-line US
composite collapses to the single modern aggregate **`DCORP_N_DC`** (Net Domestic Claims, DCS, `MFS_DC`), and
line 64 → **`PCPI_IX`** (`IFS_line_to_SDMX_remap.md` §2, verified live 2026-05-18, HTTP 200).

**Why this is the chapter's model of honest provenance:** the remap is recorded as `code_remap: true`, **NOT** as
a `proxy` (`S1504_DPR.md` §7.1). It is the *same real-world concept* ("Total Domestic Claims") re-coded across
IMF's own reorganizations — with concept continuity validated against Shaikh's hand-sum at ±2% over the overlap
(`validate_against_shaikh()`). The **pre-2001 gap** (`MFS_DC` publishes only from 2001) is disclosed, not papered
over: the 1948–2000 US segment and the pre-2001 halves of the Harberger/Ramamurthy windows survive only in the
hand-compiled xlsx or the IMF archive bulk download (`IFS_line_to_SDMX_remap.md` §6.1). For S1508/S1509 the remap
is **audit-only** — the published Harberger/Ramamurthy panels are canonical and the loaders document but do not
re-fetch. This is exactly the code-remap-vs-proxy discipline the whole RSCD project is built to enforce.

### 3b. The S1502/S1503 units-label defect — the data is SIMPLE PERCENT CHANGE, not log-difference (F01)

The industry-growth panels S1502/S1503 carry `units = rate_decimal_log_diff` in the registry, the chopped
`units` column, and DPR §3/§6 — but the **verified method is simple percent change**
`g_i(t) = (YR_i(t) − YR_i(t−1)) / YR_i(t−1)`, matching the book's own "Calculated Growth Rate" columns
(`S1502_DPR.md` §1; `CH15_review.hand_checks` S1502: *"DURMFG 1988 chopped 0.063481 == simple-pct 0.063481 ==
book precomputed 0.06348, NOT log-diff 0.061547"*). Log and simple growth agree to first order but diverge for
large swings (1999 Utilities +17.85% simple vs +16.42% log). **The data is correct and reproduces the book; only
the units *label* lies.** This is finding **F01 (MEDIUM_HIGH)**, the chapter's top defect and a **D14 blocker**:
fix `rate_decimal_log_diff → rate_decimal_pct_change` across the registry, chopped column, and DPRs
(`CH15_review.F01`, `gates.D14`). *(Note: S1504's `gGDP` genuinely IS a log-difference `ln(GDP_t/GDP_{t−1})` —
the mislabel is specific to the S1502/S1503 industry panels.)*

### 3c. The Harberger table-citation discrepancy (F02) — unreconciled, recorded honestly

The Harberger source is cited three ways: `source_id HARBERGER_1988_TABLE_12_11`, narrative + Appendix 15.1
say **"table 12.11"**, but the **Fig 15.12 caption (p. 719) says "table 12.1"** and the salvaged data sheet
header itself reads *"(Table 12.1, p. 223)"* (`CH15_review.F02`, `S1508_research.book_quotes[1]`). Which is
correct is **undetermined**; the provenance string does not match the data sheet's own citation. Recorded as an
open MEDIUM finding to be resolved against the actual Harberger (1988) volume and aligned to one number with
page 223. The companion Ramamurthy citation is also incomplete (2013 sheet vs `RAMAMURTHY_2014_CH3`; missing
ProQuest title/institution — F12) (`CH15_review.F12`).

## 4. Methodological-change exposure — the NIPA vintage problem, per thread

Shaikh fixes all BEA data at the **~2011 vintage**; every comprehensive update after 2011 restates the
magnitudes ch15 rests on (`NIPA_CHANGE_TIMELINE.md` §"Why this matters"):

- **2013 (14th):** R&D + entertainment/artistic originals **capitalized** → new IPP category, **≈ +$400B to GDP
  level**; NOS/CFC/corporate-profit restatement. Moves S1504's GDP denominator and S1505–S1507's σ *Profit*
  denominator (T1.16 line 2).
- **2018 (15th):** 2012 benchmark I-O; financial-services methods; restates investment and surplus again; the
  T7.11 +1 line shift (not directly ch15, but the same hard-coded-line-number hazard applies to T1.16/T5.3.5).
- **2023 (16th):** reference year → **2017**; chain deflator re-based → moves inflation `π` (T1.1.4).

**Thread-by-thread:** growth-rate series are robust to base-year rebasing but not to within-window revisions —
this protects S1502/S1503 (rates invariant to the 2005=100 → 2017=100 change) and S1504's `gGDP`, but **not** the
level-ratio `σ` of the Phillips series (a ratio of two revised NIPA levels) nor S1504's `pp` (carries the GDP
level in its denominator). The **T1.16 "Sources and Uses of Private Enterprise Income" line-order drift** is a
live time-bomb for σ — resolve line 2 = Net Operating Surplus by BEA `LineDescription` label, not by number
(`CH15_RESEARCH_SUMMARY.md` open-q 3; `NIPA_CHANGE_TIMELINE.md` "Table-renumbering events"). The **industry
panels also hit the SIC→NAICS wall**: last SIC benchmark 1992, first NAICS 1997, pre-1997 tables *"should not be
used as a time series"* (`IO_CHANGE_TIMELINE.md`) — barring long-history back-splices for S1502/S1503.

## 5. Replication fidelity, at a glance

- **Book period is exact for all 9** — V03 PASS across the board; the manual review hand-checked S1501/S1504/
  S1502/S1503/S1508/S1509 cell-for-cell against the Appendix 15 xlsx ground truth (`CH15_review.hand_checks`;
  `gates.D13` PASS = no synthetic/frozen/placeholder data).
- **V03 is a cell-identity round-trip for all 9 (F03, MEDIUM).** Each loader reads the same chopped column the
  validator compares against, so MAE=0 is tautological (disclosed in `CH15_RESEARCH_SUMMARY.md`). Real fidelity
  rests on the registry `reference_values` + the review's manual xlsx cross-check + (for the parent/child
  Phillips slices) the S1506/S1507 re-merge against S1505. Remediation: add an independent-source V-check for the
  API-extendable series (BEA Industry API for S1502/S1503; IMF resolver `validate_against_shaikh` for S1504).
- **Honest limits carried forward (all documentation/labeling, no data-authenticity impact):** S1502/S1503 units
  label (F01, MEDIUM_HIGH, D14 blocker); Harberger table-number (F02) and Ramamurthy citation (F12); S1508/S1509
  `rate_percent` units question (F05) and placeholder-year convention (F06); S1504 modern-CR unit-mismatch trap
  shipped in the chopped (F04) and GDP-column agency ambiguity (F11); V03 `V03_S1501` informational hardcode
  (F09, NOT a D13 violation). D0 gate artifacts partly absent (F07); no standalone DECOMPOSITION.md (F08) or FPRs
  (F10) — project-wide conventions, not ch15-specific.

## 6. Per-series index

| SID | Primary concept | NIPA touch | IFS/concordance | Key honest note |
|-----|-----------------|------------|-----------------|-----------------|
| S1501 | US consumer price level 1774–2011 | none (MeasuringWorth; deflator-adjacent only) | — | V03 hardcode informational (F09) |
| S1502 | Real-output growth, goods/trade | GDP-by-Industry real VA | NAICS concordance; SIC→NAICS 1997 wall | **units say log-diff, method is simple pct (F01)** |
| S1503 | Real-output growth, services/gov | GDP-by-Industry real VA | NAICS concordance; FIRE/Information drift | **same F01 label defect** |
| S1504 | Nominal GDP growth vs new purchasing power | T1.1.5 + T1.1.4 + T4.1 | IFS 31+(78−88)+79+81 → `DCORP_N_DC` (code-remap) | modern-CR unit-mismatch shipped (F04); T1.15 typo; GDP agency (F11) |
| S1505 | Classical vs Conventional Phillips (1948–2010) | T1.1.4 + T5.3.5 L2 + T1.16 L2 | — | σ per Handfas 2012; T1.16 line-order drift |
| S1506 | Phillips, 1948–1981 (pre-neoliberal) | inherits S1505 (slice) | — | closed window, no extension |
| S1507 | Phillips, 1982–2010 (post-neoliberal) | inherits S1505 (slice) | — | open window = extension target |
| S1508 | World inflation vs credit, 29 ctry (Harberger) | none | IFS line 32 → `DCORP_N_DC` (audit-only) | table 12.1 vs 12.11 unreconciled (F02); `rate_percent`? (F05); placeholder year (F06) |
| S1509 | World inflation vs credit, 39 ctry (Ramamurthy) | none | IFS lines 32/64 → `DCORP_N_DC`/`PCPI_IX` (audit-only) | Ramamurthy citation incomplete (F12); Romania = 2 episodes; F05/F06 |
