# RSCD Validation Architecture — Two Layers, and How We Prove They Bite

**Status:** canonical methodology · **Owner:** RSCD · **Created:** 2026-07-10 (remediation v1.6, agent P2.4)
**Companion tool:** `Technical/tools/mutation_check.py` (+ `mutation_exemptions.json`)
**Grounding:** anu-framework review PH6_6B (mutation testing), Decision 0011 (independent anchors),
G5-cert ruling (certification language), findings F-4C-02 / F-6B-01..05.

---

## 1. Why two layers

RSCD series are validated by two structurally different mechanisms. Neither alone is
sufficient; together they cover both *post-construction integrity* and *construction
correctness*.

### Layer A — Round-trip V03 (protects post-construction integrity)
The per-series `Technical/code/V03_validators/V03_<sid>.py` re-reads the same authoritative
source the `L01` loader read (the book workbook, the digitized-figure consensus CSV, …),
re-derives the expected values, and compares them cell-by-cell to the processed parquet.

A green round-trip proves the pipeline **L01 → P02 → chopped/parquet is lossless** — that
melt/reshape/rounding/joins did not corrupt what was loaded. This is real and necessary
coverage: it catches a transposed melt, a dropped column, a units rescale, a bad join.

**Its blind spot is structural.** Because Layer A reads *the same source* the loader read
and clips to the same book years, `MAE ≈ 0` proves *melt-fidelity only*. It is
constitutionally blind to:
- **wrong-source** bugs (the loader read the wrong file/column — the round-trip faithfully
  reproduces the wrong thing);
- **corrupt-source** bugs (the source itself is wrong — e.g. the S801 transposed-label xlsx);
- **silent-subset** bugs (the loader silently kept 6 of 12 columns — the round-trip of the
  6-column mean is internally consistent).

This is the **tautological-V03** pattern: the validator can only ever certify that the
pipeline faithfully transported whatever the loader chose to load.

### Layer B — Independent anchor suite (protects construction correctness)
`Technical/code/V03_validators/_v03_anchor_lib.py` (Decision 0011) asserts facts that are
**independent of the round-trip**, driven by `series_registry.json → validation`:
- **`independent_anchors`** — book-published point values (`year`/`country_key` → expected)
  or derived statistics (`mean`/`std`/`cov`/`count`/OLS `a`,`c`,`r2`) recomputed by hand
  from the raw source and hard-coded in the registry, checked at a tight tolerance.
- **`plausibility_rules`** — MHR §5/§6 economic-sanity guards (`strictly_falling`/`_rising`,
  `range`, `sign`), each carrying a `grounding` citation.
- **splice continuity** — a book→extension level-break guard at the splice year.

Because an anchor was recomputed *from the raw workbook by an independent path* (or is an
economic invariant), it fires precisely when the loader loaded the wrong thing. This is the
layer that breaks the tautology.

**Coverage is the UNION.** A series is validated iff Layer A **or** Layer B catches a defect.
For a `data_unavailable`-round-trip series (S214/S215, whose Layer A is
`PASS_DATA_UNAVAILABLE` and asserts nothing about values), Layer B is the *only* load-bearing
check — and vice-versa for a series with no independent anchors.

---

## 2. What the review found (PH6_6B + the remediation)

- **~87% of series were round-trip-only** at review time — protected by Layer A alone, hence
  exposed to the entire tautological-V03 blind-spot class above.
- **F-4C-02 (CRITICAL) — the case study.** `L01_S214`/`L01_S215` matched a hard-coded
  industry-name list against the Appendix-7 workbook; six of the twelve manufacturing columns
  are spelled differently in the file (`Machinery`→`Mach.`, `Petr.&Coal`→`Petroleum`, …), so
  `have = [c for c in NAMES if c in df.columns]` **silently kept 6 of 12 industries**. The
  shipped series was the mean of the wrong six. The round-trip V03 was **perfectly green** —
  it faithfully round-tripped the 6-column mean. The bug was invisible to Layer A by
  construction; only an independent 12-industry anchor (hand-recomputed) turns it RED
  (abs_pct_diff up to 42%, **sign-flips** in S215 for 1990/1996/1998/2002). Fix: explicit
  name→header map + a `len(matched) == 12` assert that fails loudly on any drift; six
  `independent_anchors` registered (RED on the bug → GREEN on the fix).
- **S801 — the variance-guard pattern.** The frozen digitized source had the
  Competitive/Oligopolistic columns **transposed** (a corrupt-source bug). An `MAE = 0.0`
  round-trip happily certified the transposition. The fix relabels at the loader **and** adds
  an independent structural guard inside `V03_S801`: `variance(Competitive) >
  variance(Oligopolistic)` (Shaikh p.372: concentrated/oligopolistic prices are the *smoother*
  line). A cheap, source-independent invariant now makes an MAE-0 round-trip unable to mask a
  transposition. This "add one independent invariant to a round-trip validator" is the
  reusable pattern for series that have no external anchor table.
- **The anchors genuinely fire (F-6B-05, POSITIVE).** Targeted mutation of the exact value an
  anchor asserts flips GREEN→RED (S1006 mean anchor, S703 point anchor). For S1006, a uniform
  +1% scale returns `divergence_count=0` on the round-trip (its abs-1.0pp criterion never
  trips on 5–12% returns) yet **FAILs solely via the mean anchor** — direct proof the anchor
  layer adds independent coverage the round-trip cannot.
- **Documented residual blind classes** (surfaced again, mechanically, by `mutation_check`):
  - `data_unavailable`-round-trip + sparse point anchors (S214/S215, S306/S307, F-6B-01): an
    internal swap of two *non-anchor* years is uncaught (real coverage gap — see §5).
  - external-study series validated only by sparse ±15% figure-read anchors (XS23xx,
    F-6B-02): a uniform sub-tolerance scale is invisible.
  - `+1%` scale sits exactly on the 1% tolerance boundary (strict `>`); a clean V03 certifies
    **≤~1%**, not strict `<1%` (F-6B-03).

---

## 3. The regression tool: `mutation_check.py`

Mutation testing operationalizes "do the validators actually bite?" It corrupts the processed
data in three orthogonal ways and asserts the two-layer union FAILs:

| mutation | corruption | what it probes |
|---|---|---|
| `scale_+1pct` | every `value` × 1.01 | uniform level bias (tolerance-boundary) |
| `shift_year_+1` | every `year` + 1 | temporal misalignment |
| `swap_2_mid` | swap two mid-region rows differing by >1% | internal value corruption |

For each series it (1) confirms the **unmutated baseline PASSES** (else `NOT-RUNNABLE` — the
harness refuses to certify a series whose validators already fire on pristine data), then (2)
runs the union of `V03_<sid>.run()` and the anchor suite against each mutation. A mutation is
**CAUGHT** if either layer fires, **BLIND** if both stay green, **EXEMPT** if the blindness is
a documented structural exemption. **Any non-exempt BLIND or NOT-RUNNABLE baseline → nonzero
exit.**

**Canonical safety:** the canonical tree is never written. A throwaway `RSCD/` mirror is built
under `tempfile`; `RSCD_PROJECT_ROOT` redirects every data read/write into it. Validator
*code* is imported from canonical `Technical/code`; only *data* is redirected. The mirror
copies the 118 processed parquets, the registry, the ~5 MB SalvagedInputs read-surface
(`book_data`, …; the 9.4 GB `methodology_library/` is skipped) and the digitized-figure
consensus CSVs under `Technical/remediation_campaign/` — the round-trip truth for S703/S704.

Modes: `--series SID…` · `--anchored` (all series carrying registry anchors/plausibility) ·
`--sample N --seed K` (seeded stratified draw across validation strata).

### Structural exemptions (`mutation_exemptions.json`)
A `(series, mutation)` pair is exempt only when the mutation is *semantically meaningless* for
that series — never to silence a real gap. Each entry cites a finding and gives the reason.
Current exemptions, all `shift_year_+1`:
- **S404–S407** (Inman cost curves, F-6B-04): `year` is a 1-based point index over a `y(x)`
  curve; the validator compares by position, so a +1 index shift corrupts nothing.
- **S1508/S1509** (Harberger/Ramamurthy country scatters): the processed `year` is a
  **constant stamp** (`n_distinct_years = 1`); the real key is `country_key`. A uniform +1
  relabels the stamp and corrupts nothing.
- **S903** (wage-profit curves at six discrete benchmark years): a +1 shift moves every
  benchmark to a non-existent year, so each point anchor selects an absent year and returns
  `NA`. Noted hardening opportunity: make `_eval_point_anchor` RED (not NA) when an *anchored*
  year is missing, so point anchors also catch a global shift.

---

## 4. Certification language (per ruling G5-cert)

**Never certify a flat "N series PASS."** A round-trip PASS and a book-verified PASS are not
the same claim, and conflating them re-introduces exactly the false confidence F-4C-02 lived
inside. Certification partitions series by `validation_class` (interim registry field per
G4-status; taxonomy to follow from the framework governance track):

| `validation_class` | what a green check actually proves |
|---|---|
| **book_verified** | processed values match an **independent** book anchor/table beyond the round-trip (Layer B bites). |
| **pipeline_consistent** | round-trip lossless (Layer A) but **no** independent external check — melt-fidelity only. |
| **theoretical** | illustrative/constructed series (e.g. seeded illustration); no empirical source to anchor against. |
| **extension_only** | book window genuinely unavailable; only the post-book extension is checked (sparse anchors). |
| **study_replication** | reproduces an external study's figures within that study's read tolerance (e.g. ±15%). |

Report as, e.g., *"N book-verified, M pipeline-consistent, K extension-only, …"* — never a
single blanket count. This makes the honest coverage legible and stops a `pipeline_consistent`
green from masquerading as `book_verified`.

---

## 5. When to run `mutation_check`

- **After any change to a loader (`L01`), processor (`P02`), validator (`V03`), or the anchor
  library.** A validator change that no longer bites is worse than no change. Run at least
  `--anchored`; run `--series` on the touched series.
- **In the P5 release gates.** `--anchored` must be green (all CAUGHT or documented EXEMPT);
  any new BLIND blocks release until adjudicated (exemption-grade → registry an exemption with
  a cited reason; real gap → densify anchors or add an independent invariant à la S801).
- **Quarterly, alongside the VREF vintage refresh.** New extension data can shift values onto
  or off an anchor/tolerance boundary; re-running catches a validator that silently stopped
  biting.
- **Whenever a new independent anchor or plausibility rule is added** — to confirm it actually
  turns RED on the corruption it was written to catch (the F-6B-05 discipline).

### Known open residual (do not paper over)
`--anchored` currently reports **S214/S215 `swap_2_mid` = BLIND**: their round-trip is
`PASS_DATA_UNAVAILABLE` and they carry only three point anchors (1990/1996/2002), so an
internal swap of two *non-anchor* extension years is uncaught. This is a genuine sparse-anchor
coverage gap (F-6B-01/-02 class), **not** a structural exemption (the swap corrupts real data).
Resolution is a data task (densify the anchor set, or add an extension self-consistency
invariant), tracked for P1.x/P4 — it is deliberately left RED so the gap stays visible.
