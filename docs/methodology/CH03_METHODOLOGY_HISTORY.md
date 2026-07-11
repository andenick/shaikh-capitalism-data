# Chapter 3 — Micro Foundations and Macro Patterns — Methodology History (Dossier)

**Group:** ch3 · **Series:** S301–S309 (9) · **Figures:** 3.3–3.11 · **Book:** Shaikh (2016), *Capitalism*, pp. 75–113
**Generated:** 2026-06-30 by the Phase-2 methodological-historian agent (reasoning from Shaikh's perspective)
**Companion machine-readable:** `Technical/methodology_review/CH03_methodology.json`
**Per-series MHRs:** `Technical/docs/methodology/series/S30N_MHR.md` (9 files)
**Stance:** author-intent; every claim anchored to a citable path — research JSONs, the extracted KB
(`Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/{Body_Text/ch03_micro_foundations.md,
Equations/ch03_equations.md, Tables/ch03/ch03_table_3.1.csv}`), `CH3_RESEARCH_SUMMARY.md`, `CH03_review.json`,
the DPR/EPRs, the L01/V03 code, and `_timelines/NIPA_CHANGE_TIMELINE.md`. Nothing invented; where author
rationale is absent it is marked "not located in the corpus."

---

## Chapter headline

Chapter 3 is Shaikh's methodological keystone: **aggregate empirical patterns (downward-sloping demand,
Engel's Law) are "robustly insensitive" to micro foundations.** He proves this in three legs, and the nine
series map exactly onto them:

1. **Deductive leg — analytic curves (S301–S305).** Engel-curve saturation is *derived* from the fundamental
   consumer-choice equations (3.4)–(3.14), via two independent routes: **Case I**, `x1min(y)` rising sub-linearly
   (S301 marginal share / S302 average share / S303 Engel level, Figs 3.3–3.5), and **Case II**, `c(y)`
   declining (S304 propensity / S305 Engel level, Figs 3.6–3.7). These are deterministic `np.linspace`
   evaluations of book equations — **no external data source**.
2. **Empirical leg — real budgets (S306, S307).** The pattern is shown in observed data: the UK Board of Trade
   1904 working-class budgets (food share, Fig 3.8 / absolute food Engel curve, Fig 3.9), cited by Shaikh from
   Allen & Bowley (1935). Both are **`data_unavailable` scroungers** (`publish: false`): the tabulation was
   never digitized, so the loaders honestly emit metadata-only rows rather than fabricate.
3. **Simulation leg — four micro-worlds (S308, S309 + Table 3.1).** The pattern survives four incompatible
   behavioural models (Neoclassical Homogeneous / Heterogeneous, Whimsical/Becker, Imitate-Innovate/Dosi);
   Table 3.1's elasticities are near-identical across all four. In the RSCD build these are **analytic overlays**,
   not re-run simulations (see the NETLOGO mislabel below).

**Single most important cross-chapter fact:** *no ch3 series touches US NIPA, the benchmark I-O accounts, or a
SIC→NAICS concordance.* Unlike the NIPA-bound chapters (6, 7, 14…), Chapter 3 is **completely insulated from the
comprehensive-revision time-bombs** in `NIPA_CHANGE_TIMELINE.md` (2013 IPP +$400B, 2018 T7.11 +1 line shift,
2023 rebasing). S301–S305/S308/S309 are analytic; S306/S307 are a fixed 1904 UK historical cross-section. The
methodological-change exposure of this chapter is essentially zero on the *data-vintage* axis — its risks are
(a) un-stated parameter calibrations, (b) stale registry metadata, and (c) an honesty-of-provenance labelling
issue on the simulation series.

## Source map

| Series | Fig | Concept | Source | Empirical? | Publish |
|---|---|---|---|---|---|
| S301 | 3.3 | Marginal expenditure share, Case I | Shaikh eqs (3.4)–(3.11) | no (analytic) | true |
| S302 | 3.4 | Average expenditure share, Case I | Shaikh eq (3.11) | no (analytic) | true |
| S303 | 3.5 | Engel level, Case I | Shaikh eqs (3.5)/(3.11) | no (analytic) | true |
| S304 | 3.6 | Discretionary propensity c(y), Case II | Shaikh eq (3.4) | no (analytic) | true |
| S305 | 3.7 | Engel level, Case II | Shaikh eq (3.5), c→c(y) | no (analytic) | true |
| S306 | 3.8 | Food *share* Engel curve | Allen & Bowley 1935 / UK BoT 1904 Cd. 3864 | **yes** (unavailable) | false |
| S307 | 3.9 | Food *level* Engel curve | Allen & Bowley 1935 / UK BoT 1904 Cd. 3864 | **yes** (unavailable) | false |
| S308 | 3.10 + T3.1 | Necessary-good (x1) demand, 4 micro-foundations | Shaikh Fig 3.10 / eq (3.5) | no (analytic overlay) | true |
| S309 | 3.11 + T3.1 | Luxury-good (x2) demand, 4 micro-foundations | Shaikh Fig 3.11 / eq (3.6) | no (analytic overlay) | true |

## Why Shaikh built each leg this way (author intent)

- **Analytic first (S301–S305).** The chapter's argument requires showing the pattern is *implied by the
  shaping structures* (budget constraint + necessary minimum) before showing it in data — otherwise the reader
  could attribute the pattern to a particular behavioural assumption. So Figs 3.3–3.7 must be formula plots.
  Shaikh deliberately gives **two routes to saturation** (Case I via `x1min(y)`, Case II via `c(y)`) precisely
  because over-determination is the message: the aggregate shape does not depend on *which* micro story you tell.
- **Real data second (S306/S307).** Shaikh anchors the deduction in the canonical historical demonstration of
  Engel's Law — Allen & Bowley's 1904 UK working-class budgets — cited by name and page ("1935, 7"). He wants a
  *classic* cross-section, not a current survey; the age of the data is a feature (historical robustness), not a
  bug. He shows it in both share (3.8) and level (3.9) form, mirroring the analytic S302/S303.
- **Simulation last (S308/S309).** The strongest form of the claim: four *incompatible* micro-foundations —
  including a deliberately irrational (whimsical/Becker) and an evolutionary (imitate-innovate/Dosi) agent —
  produce the same aggregate demand and elasticities (Table 3.1). All models share the same fixed constants
  (`y=200, c=0.5, x1min=10, p1=1, p2=2`) so the behavioural rule is the only thing that varies.

## Rejected alternatives (chapter-wide)

- **A stated parameter calibration for the analytic curves.** Shaikh never prints the exact `x1min(y)` path
  (Case I) or `c(y)` formula (Case II); only qualitative behaviour + axis bounds. The build chose the simplest
  one-parameter families matching the printed figures — a replication choice, not Shaikh's stated numbers.
  *Author rationale for the exact parameters is not located in the corpus.*
- **Modern survey data as a substitute for the 1904 figures (S306/S307).** UK ONS LCF and US BLS CEX appear as
  `extension_candidates` but with `splice_strategy: none`: different population, "food" concept, and currency —
  a *comparison*, never an extension of Shaikh's 1904 cross-section.
- **Synthetic fill for the unavailable empirical series.** Forbidden by `anu-framework.md`; the S306/S307
  scroungers emit `data_unavailable` metadata rows instead — D13 PASS.
- **Re-running the NetLogo simulations (S308/S309).** Feasible from the verbal specs but seeds are unstated, so
  fresh Monte-Carlo draws could not reproduce the printed curves; faithful analytic near-copies were chosen.

## Methodological-change exposure (chapter-wide) — the key section

**Zero NIPA / I-O / concordance touch across all nine series.** For every series, `nipa_touch = none`,
`io_touch = none`, `concordance_touch = none`. Consequences:

- S301–S305, S308, S309: closed-form evaluations of book equations 3.4–3.14 → immune to every comprehensive
  NIPA revision and every SIC→NAICS benchmark change. There is nothing to re-vintage.
- S306, S307: a fixed UK **1904** historical cross-section (Allen & Bowley 1935) → no US-NIPA exposure at all;
  the only documentary risks are (i) which edition/table of Allen & Bowley, and (ii) concept-consistency of any
  future modern comparator (eating-out treatment, shilling→£ conversion) — a concept issue, not a data revision.

The `NIPA_CHANGE_TIMELINE.md` therefore applies to this chapter **only as a boundary condition**: if S306/S307
are ever paired with a modern ONS comparator, that comparator (not the 1904 data) would carry its own vintage
questions — and must be published as a *separate* cross-section, never spliced.

## Fidelity findings roll-up (from CH03_review.json)

| Finding | Sev | Series | Essence |
|---|---|---|---|
| **F-CH3-01** | HIGH | S304, S305 | Registry `reference_values` are **stale** vs the 2026-05-27 book-matched recalibration (S305 drift ~4×). Code correct; refs never regenerated. |
| **F-CH3-11** | HIGH | S301–S305, S308, S309 | V03 checks shape/bounds only, **never `registry.reference_values`** → the stale S304/S305 refs passed silently; V03 tol (0.5%) decoupled from registry tol (1%). |
| **F-CH3-03** | HIGH | S308, S309 | Subseries B–E are **analytic × fixed scalar** (0.998/1.003/0.995/1.005) but mislabelled `subsource_id NETLOGO_SIMS` with a "read off printed figure" step; V03 cross-curve ±2% check is **circular**. Disclosed (theoretical) → not a D13 fail, but provenance labels are misleading. |
| F-CH3-04 | MED | S306, S307 | Registry `status: book_period_validated` contradicts empty chopped → should be **`data_unavailable`**. |
| F-CH3-06 | MED | S306, S307 | DPR header status contradicts the DPR's own §4/§7. |
| F-CH3-05 | MED | S301–S305, S308, S309 | `x_value` abscissa (income/price) written to parquet but **dropped from the chopped**; figures not plottable vs true x-axis without a registry `domain` join. |
| F-CH3-07 | MED | S301–S309 | Triage reason falsely says "ch03 not HDARP-extracted, quotes unverifiable" — **false**: body/equations/Table 3.1 extracted; S301 quote verifies verbatim. Provenance under-sold. |
| F-CH3-08 | LOW | S301, S302 | Registry `n_points = 121` vs 119 emitted rows. |
| F-CH3-09 | LOW | S304, S306 | `CH3_RESEARCH_SUMMARY.md` documents the pre-2026-05-27 S304 calibration (doc drift). |
| F-CH3-10 | LOW | S304, S305 | Dead `c_case_ii` helper (rejected fast-decay curve) still importable. |
| F-CH3-12 | LOW | S301–S309 | No `*_DECOMPOSITION.md` (folded into DPR §4 + registry) — likely by-design; record a Decision. |
| F-CH3-13 | LOW | S301–S309 | Two uncoordinated tolerances (V03 0.5% vs registry 1%); reconcile with F-CH3-11. |

Gates: **D13 PASS (92)** — no synthetic fill; empirical S306/S307 correctly empty; theoretical curves disclosed.
**D14 BLOCK_EXTERNAL (82)** — chopped `year` is a point index not a calendar year, `x_value` absent from chopped,
explainers omit verifiable book quotes.

## Forward-risk priorities (chapter-wide)

1. **Regenerate S304/S305 `reference_values`** from the recalibrated loaders (F-CH3-01, HIGH) and reconcile
   `CH3_RESEARCH_SUMMARY.md` (F-CH3-09). S305 first (~4× drift).
2. **Relabel S308/S309 B–E provenance** away from `NETLOGO_SIMS` to state the true analytic × fixed-scalar
   construction; rewrite the "read off figure" construction step (F-CH3-03, HIGH). Metadata honesty, no data change.
3. **Harden V03:** add a `reference_values` comparison for theoretical series and de-circularize the S308/S309
   cross-curve check (test against Table 3.1 elasticities / printed read-off), reconciling the 0.5%/1% tolerances
   (F-CH3-11, F-CH3-13).
4. **Fix S306/S307 status enum to `data_unavailable`** + DPR headers (F-CH3-04, F-CH3-06); real remediation is
   digitizing Allen & Bowley 1935 Table 1 / UK BoT Cd. 3864 (1908) — then the scroungers auto-populate with no
   code change.
5. **D14 remediation:** restore the `x_value` abscissa to the chopped (F-CH3-05), publish the point-index `year`
   honestly, and surface the verified book quotes in the explainers (F-CH3-07).
6. **Housekeeping:** reconcile `n_points` 121→119 (S301/S302, F-CH3-08); delete the dead `c_case_ii` helper
   (F-CH3-10); record a Decision on the absent `*_DECOMPOSITION.md` (F-CH3-12).

**No ch3 series is extensible** — S301–S305/S308/S309 are analytic (no time dimension), S306/S307 are a fixed
1904 cross-section. Any "update" is a re-calibration, a digitization, or a modern-comparator *comparison*, never
a live data refresh.
