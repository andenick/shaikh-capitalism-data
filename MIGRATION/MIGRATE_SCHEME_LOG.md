# RSCD AS/ES → XS Series-ID Migration Log

**Date:** 2026-06-10
**Framework:** Anu v12.2 / Series ID Spec v2.2
**Procedure:** anu-ingestion migrate-scheme, AS/ES→XS recipe (steps 8–12)
**Operator:** agent-executed (no blind automation)
**Result:** anu-doctor project mode **0 FAIL / 0 WARN** (39/39 PASS); replicator end-to-end PASS

---

## 1. Summary

Migrated all 17 legacy-prefixed series in RSCD to the v2.2 canonical `XS`
("Extra Series") prefix. Pure prefix swap, digit counts preserved
(`AS003 → XS003`, `ES2301 → XS2301`); 3-digit AS and 4-digit ES occupy disjoint
ranges, so no collisions. Each migrated series was classified as `appendix`
(book-appendix series) or `external_study` (replication of another study) and
given `xs_class` + `xs_attribution`. The registry `prefix_scheme` was collapsed
to the v2.2 `{primary: S, extra: XS}` shape.

## 2. Crosswalk (17 confirmed rows)

Canonical file: `MIGRATION/crosswalk.csv`. All rows `status: confirmed`.

| old_id | new_id | name | xs_class |
|--------|--------|------|----------|
| AS001 | XS001 | GDP/GDI Decomposition and Business NOS | appendix |
| AS002 | XS002 | Wage Equivalent and Corp/Noncorp Split | appendix |
| AS003 | XS003 | Imputed Interest Adjustment and Sectoral Profit Rates | appendix |
| AS004 | XS004 | GPIM Corporate Capital Stock (Operational Baseline) | appendix |
| AS005 | XS005 | GPIM Variant - BEA 2011 Reference (Pure GPIM Regenerator) | appendix |
| AS006 | XS006 | GPIM Variant - BEA 1993 Depreciation Rates | appendix |
| AS007 | XS007 | GPIM Variant - IRS Adjusted | appendix |
| AS008 | XS008 | GPIM Variant - Interwar Adjustment Multiplier | appendix |
| AS009 | XS009 | IRS Corporate Inventories and Total Capital Stock | appendix |
| ES2001 | XS2001 | Shaikh (2020) Sraffa Price-Value Aggregates, US 1947-1998 (Tables 1-2) | external_study |
| ES2101 | XS2101 | Shaikh-Coronado-Nassif-Pires (2020) Sraffa CI/Theil Summary Stats | external_study |
| ES2201 | XS2201 | Shaikh-Jacobo (2020) Econophysics Two-Class Income Parameters, US 2002-2016 | external_study |
| ES2301 | XS2301 | Weber-Shaikh (2020) Fig 1 — US Trade Balance vs World and China | external_study |
| ES2302 | XS2302 | Weber-Shaikh (2020) Fig 2 — China Current Account Balance | external_study |
| ES2303 | XS2303 | Weber-Shaikh (2020) Fig 3 — China FX Reserves ex-Gold (WDI) | external_study |
| ES2304 | XS2304 | Weber-Shaikh (2020) Fig 4 — RMB Misalignment Extended PPP | external_study |
| ES2305 | XS2305 | Weber-Shaikh (2020) Fig 5 — RMB Misalignment Macro Balance | external_study |

## 3. xs_class classification decisions

| Series | xs_class | xs_attribution | Rationale (evidence) |
|--------|----------|----------------|----------------------|
| XS001–XS009 | `appendix` | `Shaikh (2016), Appendix Table 6.8` | All carry `primary_source: SHAIKH_APPENDIX_6_8`; every subseries `source` = "Shaikh (2016) Appendix Table 6.8 (verbatim transcription)"; chapter 6 GPIM construction internals (per project Decision 0002). These are derived/formula series built from the **main book's own appendix tables**, not from a separate study. |
| XS2001 | `external_study` | `Shaikh (2020), An Empirically Sufficient Form for Sraffa Prices` | `external_study_group: 20`, `status: study_complete`, `external_study_pdf` points to the Shaikh 2020 paper. |
| XS2101 | `external_study` | `Shaikh, Coronado & Nassif-Pires (2020), On the empirical regularities of Sraffa prices` | `external_study_group: 21`. |
| XS2201 | `external_study` | `Shaikh & Jacobo (2020), Economic Arbitrage and the Econophysics of Income Inequality` | `external_study_group: 22`. |
| XS2301–XS2305 | `external_study` | `Weber & Shaikh (2020), The US-China trade imbalance and the theory of free trade` | `external_study_group: 23`; subseries sourced from US Census FT900 / IMF / WDI replicating the Weber-Shaikh (2020) figures. |

Classification was read from each entry's `primary_source`, subseries `source`,
`external_study_group`, `status`, and `external_study_pdf` fields, cross-checked
against the project CLAUDE.md series-scheme description ("AS = GPIM construction
internals, chapter 6 … ES = external study replications, chapter 0"). The split
is unambiguous: 9 appendix + 8 external_study = 17.

## 4. Mechanical rewrite — per-directory counts

Script: `MIGRATION/migrate_xs_20260610.py` (regex `\bAS(\d{3}) → XS\1`,
`\bES(\d{4}) → XS\1`; dry-run-first; `ES1001` protected). Two passes were run
because the first filename pass used a `\b` boundary that does not fire after an
underscore (`L01_AS001.py`); the script's filename regex was upgraded to a
separator-aware lookbehind `(?:^|[_\-./\\])` and re-run to catch the 103
`code/`+`replicator/` script files.

### Pass A (contents + boundary-anchored filenames)

| Directory | renamed | content-edited | replacements |
|-----------|--------:|---------------:|-------------:|
| series_registry.json | 0 | 1 | 296 |
| research | 17 | 17 | 275 |
| chopped | 17 | 17 | 2808 |
| docs | 38 | 70 | 1319 |
| code | 0 | 62 | 557 |
| replicator | 10 | 79 | 1488 |
| Build | 0 | 9 | 199 |
| tools | 0 | 2 | 41 |
| reports_latex | 0 | 4 | 62 |
| extenbooks | 17 | 0 (binary) | 0 |
| config / viz | 0 | 0 (no legacy IDs) | 0 |
| **TOTAL A** | **99** | **261** | **7045** |

### Pass B (separator-anchored filenames — L01/P02/V03 scripts)

| Directory | renamed | content-edited | replacements |
|-----------|--------:|---------------:|-------------:|
| code | 51 | 0 | 0 |
| replicator | 52 | 0 | 0 |
| **TOTAL B** | **103** | **0** | **0** |

(Pass B included the one double-ID file
`replicator/inputs_bundled/SalvagedInputs/.../XS2304_ES2305_README.md →
XS2304_XS2305_README.md`.)

### Registry surgery (step 4, beyond the mechanical pass)

- `prefix_scheme` replaced with v2.2 shape:
  `{primary: {prefix: S, …}, extra: {prefix: XS, meaning: "Extra Series — book-appendix series (xs_class: appendix) and series from other studies (xs_class: external_study)", pattern: "XS### / XS####", example: "XS003"}}`.
  The legacy `external` + `analytical` keys were removed.
- `xs_class` + `xs_attribution` inserted into all 17 migrated entries.
- The same v2.2 `prefix_scheme` was applied to the derived/stale copies so they
  stay coherent (the mechanical pass had only half-swept their `example` field):
  `replicator/inputs_bundled/series_registry.json`,
  `replicator/workdir/RSCD/Technical/series_registry.json`,
  `Build/ANU_BUILD_MANIFEST.json`, and the two
  `_phase2_registry_seeder.py` copies (`code/utils/`, `replicator/lib/utils/`).

### Root-level state/metadata sweep (P19 fix)

The auto-generated artifact/state files at `Technical/` root are not under a
subdirectory and so were swept in a targeted second pass (same regex + `ES1001`
protection), to keep ledger/validation/metadata consistent with the renamed IDs
and clear an anu-doctor P19 ledger-sync WARN:

| File | replacements |
|------|-------------:|
| ANU_LEDGER.json | 17 |
| REPLICATION_GROUNDTRUTH_INDEX.json | 34 |
| VALIDATION_REPORT.json | 62 |
| SUBSOURCE_METADATA.json | 12 |
| PIPELINE_STATE.json | 1 |
| RSCD_REPLICATION_STATE.json | 12 |
| COMPARISON_STATE.json | 3 |
| RSCD_vs_RMWND_COMPARISON_PLAN.md | 1 (live `AS004` series ref) |
| **TOTAL** | **142** |

`SERIES_CORRESPONDENCE_MATRIX.json` was also migrated (17 XS keys, all in
registry, no legacy survivors). `PROGRESS_LOG.md` was deliberately **not** swept
(its single `ES2301` is version-history narrative).

## 5. Verification gates

### 5a. Registry JSON validity
`json.load()` on `Technical/series_registry.json` → **VALID**. All derived
registry copies + Build manifest re-validated.

### 5b. Straggler grep
Final scan of all in-scope dirs + root state files for `\bAS\d{3}\b|\bES\d{4}\b`:
**3 content survivors, 0 filename survivors**, all justified:

| File:line | token | justification |
|-----------|-------|---------------|
| `docs/reviews/RSCD_vs_RMWND_COMPARISON_REPORT.md:71` | `ES1001` | **Foreign-project ID** — RMWND's own series, cited verbatim in the cross-project comparison narrative. Not an RSCD series; must not migrate. (In `PROTECTED_TOKENS`.) |
| `reports_latex/RSCD_vs_RMWND_Comparison.tex:90` | `ES1001` | Same RMWND foreign reference (LaTeX twin). |
| `PROGRESS_LOG.md:38` | `ES2301` | **Version-history narrative** ("ES2301 template normalized across cohort"); anu-doctor ignores version-history lines. Left intact per migration policy. |

Note on other ES tokens encountered (`ES2002/ES2102/ES2103/ES2104/ES2306`): these
are forward-looking/optional RSCD split IDs mentioned in research-JSON and
external-study docs (same RSCD namespace) and were correctly migrated to
`XS####`. `ES1701` appeared only as a stale `prefix_scheme.example` and was
resolved by the prefix_scheme rewrite.

### 5c. anu-doctor (project mode) — baseline vs post

Command: `python check_project.py --project ./Technical`
(the doctor treats `Technical/` as the project root — that is where
`series_registry.json` lives).

| Phase | Baseline (pre) | Post | Note |
|-------|----------------|------|------|
| P12 prefix scheme | **FAIL** (17 legacy AS/ES) | **PASS** | migration target |
| P13 status/artifact | PASS | PASS | (transient FAIL during migration — caused by un-renamed `L01_/P02_/V03_AS00x.py`; fixed in Pass B) |
| P14 crosswalk | PASS (skipped) | **PASS** (17 rows acted on) | crosswalk now present |
| P19 ledger sync | PASS | PASS | (transient WARN — caused by stale ledger IDs; fixed by root-file sweep) |
| P23 artifact coverage | PASS | PASS | (transient WARN during migration; fixed in Pass B) |
| all others (P01–P39) | PASS/skip | PASS/skip | unchanged |
| **Summary** | **1 FAIL / 0 WARN** | **0 FAIL / 0 WARN** | |

The only baseline failure (P12) is resolved; no net-new failures. All
migration-induced regressions (the transient P13 FAIL, P19 WARN, P23 WARN
observed mid-migration) were fixed within this run.

### 5d. replicator end-to-end
`replicator/scripts/replicate.py`:
- `--list` → enumerates the renamed scripts (118 L01, 116 P02, 118 V03), all `XS*`.
- `--health` → **HEALTHY** (registry parses 118 series; all phase scripts discovered; core deps import). API keys (FRED/BEA/BLS) MISSING — runtime credential gap only, expected; does not affect book-period validation.
- `--series XS001` → **PASS** (exit 0); all 17 migrated validators `V03_XS001…V03_XS2305` PASS against book-period reference values; chopped + extenbook writers OK; 27 chopped CSVs + 27 extenbooks staged.

## 6. Downstream regeneration TODO (later phase)

- **Extenbooks** (`Technical/extenbooks/XS*.xlsx`): the 17 `.xlsx` files were
  **renamed** (filenames now `XS*`), but their **internal cell contents still
  carry the old AS/ES IDs** (xlsx internals were intentionally not edited — see
  recipe step 12, "regenerate, do not rename"). **Regenerate via anu-extenbook**
  (`/anu-extenbook` for each migrated series, or the replicator
  `O06_extenbook_writer`) so workbook internals match the XS IDs.
- **Viz caches** (if any built): regenerate so legend/column IDs reflect XS.
- **Outputs/ publish bundles**: out of scope here; regenerate in the publish
  phase (already gated for separate path-config work per project CLAUDE.md).

## 7. Files created by this migration

- `MIGRATION/crosswalk.csv` — the public correspondence table (recipe step 11).
- `MIGRATION/migrate_xs_20260610.py` — the one-off mechanical rewriter.
- `MIGRATION/MIGRATE_SCHEME_LOG.md` — this log.

Legacy IDs receive **no public aliases** (recipe step 11); the crosswalk is the
sole correspondence record.
