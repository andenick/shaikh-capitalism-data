# Chapter 14 — The Theory of Wages and Unemployment — Methodology History Dossier

**Group:** ch14 · **Series:** S1401–S1408 (8) · **Book pages:** 657–673 (chapter); 889–895 (Appendix 14.1/14.2/14.3)
**Reasoning stance:** from Anwar Shaikh's own perspective — why *he* constructed each series as he did.
**Companion per-series MHRs:** `Technical/docs/methodology/series/S140{1..8}_MHR.md`
**Machine-readable twin:** `Technical/methodology_review/CH14_methodology.json`

> Grounding: every claim is anchored to a citable path — the research JSONs (`Technical/research/S140N_research.json`),
> `Technical/docs/chapters/CH14_RESEARCH_SUMMARY.md`, the review (`Technical/methodology_review/CH14_review.json`),
> the DPRs/EPRs, the concept-guard helper (`Technical/code/L01_loaders/_ch14_helpers.py`), and the Phase-0
> NIPA timeline (`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`). No claim is invented.

---

## 1. What the chapter builds

Chapter 14 develops the **Classical theory of wages and unemployment**. Its empirical core (Sec. VI,
pp. 663–672) introduces Shaikh's own construct — **unemployment intensity** `uInt_L = unemployment_rate ×
duration_index` — and uses it to derive three nested "Phillips-type" curves (`CH14_RESEARCH_SUMMARY.md`):

1. **Classical wage-share curve** `σ̇W/σW = f(uInt_L)` — Eq. 14.15 (S1404 raw, S1405 filtered).
2. **Real-wage curve** `ẇr/wr = ẏr/yr + f(uInt_L)` — Eq. 14.18 (S1407).
3. **Nominal-wage curve** `ẇ/w = ṗ/p + ẏ/y + f(uInt_L)` — Eq. 14.19 (S1408).

The eight series map one-to-one to Figures 14.10–14.17:

| SID | Fig | What it is | Construction |
|-----|-----|------------|--------------|
| S1401 | 14.10 | Nominal GDP growth + wage-share level | composite (EC/GDP, ΔGDP) |
| S1402 | 14.11 | Unemployment rate, duration index, intensity | composite (BLS CPS) |
| S1403 | 14.12 | Wage share vs intensity — quarterly HP(100) phase spiral | composite (phase plot) |
| S1404 | 14.13 | Wage-share growth vs intensity — raw scatter | direct |
| S1405 | 14.14 | Wage-share growth vs intensity — HP(100) + Phillips fits | direct (Classical curve) |
| S1406 | 14.15 | Inflation + productivity growth | composite |
| S1407 | 14.16 | Real-wage growth vs intensity — HP(100) + fit | direct |
| S1408 | 14.17 | Nominal-wage growth vs intensity — HP(100) + fit; Table 14.3 | direct |

## 2. The two source families — all eight rest on NIPA T1.10

Every series traces to just two public-domain providers, fixed verbatim in Shaikh's Appendix 14.2 (p. 892):

- **BEA NIPA Historical Tables** (the wage/price/productivity spine):
  - **T1.10 line 1** — GDP (wage-share denominator; nominal-growth level)
  - **T1.10 line 2** — **Compensation of employees, paid** (wage-share numerator; nominal wage `w = EC*100/FEE`)
  - **T1.1.9 line 1** — GDP deflator `p` (→ FRED `GDPDEF`)
  - **T6.5A–D** — Full-time equivalent employees FEE (→ FRED `B4701C0A222NBEA`)
- **BLS CPS**: LNS14000000 unemployment rate (→ `UNRATE`); LNS13008275 mean duration (→ `UEMPMEAN`).

**All eight series rest on NIPA T1.10.** S1401/S1403/S1404/S1405 use it as the wage-share (EC/GDP);
S1406/S1407/S1408 use line 2 (EC) for the wage level plus T1.1.9 (deflator) and T6.5 (FTE). Even S1402
(pure BLS CPS) carries `touches_nipa=true` through the shared chapter framing — it is the common
Phillips-curve x-axis joined against the NIPA-based y-variables (`CH14_review.touchpoints`).

The correct FRED mirror of T1.10 line 2 is **`W209RC1`** (total compensation of employees), used correctly
by S1403. GDP mirrors to FRED `GDP`.

## 3. Why these sources — Shaikh's rationale, and the two concept battles

Two methodological concepts define the chapter, and each has a rejected alternative that the *code* either
enforces (productivity) or fails to enforce (wage-share numerator):

- **Concept battle 1 — total Compensation of Employees, NOT wage & salary disbursements (and NOT BLS AHE).**
  Shaikh's wage share and nominal wage are built from *total* compensation (T1.10 line 2 = wages + salaries
  **plus supplements**), because the classical share of value added going to labor must count all labor
  compensation, measured inside the same NIPA frame as GDP. Wage & salary disbursements omit supplements and
  run ~20% low (and by a rising fraction as fringe benefits grew); BLS average hourly earnings is a
  per-worker micro wage, not an aggregate. **This is exactly the concept the S1401 extension bug violates**
  (see §4).
- **Concept battle 2 — real-GDP-per-FTE productivity, NOT BLS output-per-hour.** Shaikh's `yr =
  (GDP*100/p)/(FEE/1000)` is labor productivity *per worker*; substituting BLS per-hour productivity
  silently breaks the wage-share decomposition (Eqs 14.18–14.19: different labor input, different sector
  coverage). **The code enforces this**: `_ch14_helpers.assert_no_per_hour_substitution()` fails at import if
  any of `OPHNFB / PRS85006092 / OPHPBS / OPHMFG` is added (S1406/S1407/S1408). This is exemplary
  concept-policing — and the CH14 review explicitly contrasts it with the *unguarded* wage-share numerator
  that let the S1401 defect through (`CH14_review.F8`).

Other shared choices: unemployment **intensity** over the raw rate (duration multiplies the reserve-army
pressure; S1402); the official rate over U-6/U-7 (only from 1994; footnote 9); **HP(100)** for all
frequencies, even quarterly (`HP_LAMBDA_CH14=100`, not 1600; S1403); GDP (not NDP/GDI) as the wage-share
denominator; and Phillips's own `y = a + bx^c` form with **b constrained to 1** (S1405).

## 4. The S1401 compensation-vs-earnings story (the chapter's headline defect)

The most instructive methodological event in ch14 is a **code defect that illuminates a concept**
(`CH14_review.F1/F2`, both HIGH):

- Shaikh's intended wage-share numerator is **total Compensation of Employees** (T1.10 line 2 → FRED
  `W209RC1`, ~$15.1T in 2024).
- The S1401 extension loader (`L01_S1401.py:54`) instead fetches **FRED `A576RC1`** — *wage & salary
  disbursements* (~$12.4T in 2024) — which excludes supplements and runs ~20% low.
- Result: a spurious **~0.548 → ~0.426 (≈22%) downward break** at the 2011→2012 splice.
- The **EPR itself proves the intent was total compensation**: its worked example expects `A576RC1 2024 =
  15,108.5 → wage share 0.524` (continuous with the book's 0.548), yet the code ships 12,387.9 → 0.423.
  15,108.5 is the **W209RC1** value. So Shaikh's intent — and the author's own intent — is unambiguously
  total compensation; only the FRED id in code is wrong (`CH14_review.F2`).
- **S1403 is the correct reference model**: it resolves T1.10 line 2 to `W209RC1` correctly (and even
  rejected the GDI-based `W270RE1Q156NBEA` share). The F1 fix is to make S1401 copy S1403: swap `A576RC1 →
  W209RC1`, re-run L01/P02/V03, verify splice continuity, regenerate artifacts (`CH14_review.F1.fix`).

**This MHR documents the CORRECT lineage — total compensation, T1.10 line 2 — throughout, and flags
A576RC1 strictly as a to-fix code defect. A576RC1 is NOT Shaikh's intent and must not be propagated.** The
same A576RC1 mislabel appears in the S1404/S1407/S1408 research extension_candidates and must be corrected
to W209RC1 alongside the S1401 loader fix. The defect evaded all gates because V03 `compare_range ≤ 2011`
and `reference_values` are FRED self-echoes (`CH14_review.F4`).

## 5. Methodological-change exposure — the NIPA vintage problem

Shaikh fixes all BEA data at the **~2011 vintage**; every comprehensive update after 2011 restates the
magnitudes ch14 rests on (`NIPA_CHANGE_TIMELINE.md` §"Why this matters"):

- **2013 (14th):** R&D + entertainment/artistic originals **capitalized** → new IPP category; **≈ +$400B to
  GDP level**; CFC/NOS/capital-stock rise. Moves the wage-share denominator (GDP) and the deflator/
  productivity numerators.
- **2018 (15th):** 2012 benchmark I-O; financial-services + nonprofit methods; T7.11 +1 line shift (matters
  for ch6, not ch14 directly).
- **2023 (16th):** reference year → 2017; chain deflator re-based (current `GDPDEF` is 2017=100 vs Shaikh's
  2009=100 book vintage).

Because the extension pulls the **current FRED vintage with no ALFRED pin**, a live re-fetch straddles the
2013/2018/2023 boundaries. The build's correct principle is to **re-derive end-to-end on one coherent
vintage** (never a lazy ratio/growth splice across a comprehensive-revision boundary) — undermined only by
the S1401 wrong-series defect. Growth-rate series (S1404/S1406 inflation & productivity growth) are more
robust to level re-benchmarks than the level shares (S1401/S1403), but not to within-window revisions. The
one BLS-side event is the **UEMPMEAN Jan-2011 top-coding break** (2yr→5yr cap), annotated and left
unadjusted (S1402; `CH14_review.F9`).

## 6. Replication fidelity, at a glance

- **Book period is bit-exact for all 8** — V03 MAE = 0.0, max %err 0.0% (exact pass-through of Appendix 14.3
  columns; `CH14_RESEARCH_SUMMARY.md` closure table). Hand-check vs the Shaikh XLSX is cell-for-cell for
  every sampled series/year (`CH14_review.hand_checks`).
- **S1405 has the chapter's one non-circular anchor** — the constrained-b=1 Phillips fits reproduce
  published Appendix 14.2 statistics exactly (Era 1 R²=0.931; Era 2 R²=0.965), a match to *published
  results*, not a self-round-trip (`CH14_review.touchpoints` S1405).
- **Honest limits carried forward:** S1401 extension wrong-series defect (F1/F2, HIGH — blocks D14/external
  distribution); S1408 Table 14.3 residual regression deferred to a raw-OLS placeholder (F5, no
  data-authenticity impact); S1403 Fig 14.12 shipped HP100-2D vs book HP40-3D (F3); circular extension
  validation across all 8 (F4).
- **Best practice to preserve:** the productivity concept-guard (F8) — extend an analogous guard to the
  wage-share numerator so the S1401 defect class cannot recur.

## 7. Per-series index

| SID | Primary concept | NIPA touch | Key honest note |
|-----|-----------------|------------|-----------------|
| S1401 | Wage share (EC/GDP) + nominal GDP growth | T1.10 L1+L2 | **A576RC1 extension defect — intended = total comp W209RC1** |
| S1402 | Unemployment rate, duration index, intensity | via chapter framing (inputs BLS CPS) | UEMPMEAN 2011 top-coding break, annotated |
| S1403 | Wage share vs intensity (quarterly HP100 spiral) | T1.10 L1+L2 | correct W209RC1 mirror = model for S1401 fix; Fig HP40-3D not reproduced |
| S1404 | Wage-share growth vs intensity (raw scatter) | T1.10 L1+L2 | pass-through; inherits S1401 numerator |
| S1405 | HP100 wage-share Phillips (Classical curve) | T1.10 L1+L2 | non-circular in-book anchor (a/c/R² exact) |
| S1406 | Inflation + real-GDP-per-FTE productivity | T1.1.9 + T6.5 (+T1.10 L1) | productivity concept-guard (exemplary) |
| S1407 | HP100 real-wage Phillips | T1.10 L2 + T1.1.9 + T6.5 | inherits productivity guard |
| S1408 | HP100 nominal-wage Phillips; Table 14.3 | T1.10 L2 + T6.5 (+T1.1.9) | Table 14.3 residual regression deferred |
