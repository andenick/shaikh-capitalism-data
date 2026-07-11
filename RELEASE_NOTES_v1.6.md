# RSCD v1.6 — Release Notes

**Release date**: 2026-07-10
**Tag**: `v1.6`
**Framework**: Anu v12.2 · Schema v2.3.0
**Predecessor**: v1.5 (2026-07-02, skeptical review & remediation + publish-leak fix)
**Campaign**: RSCD v1.6 Post-Review Remediation

---

## Summary

v1.6 corrects two data series discovered during the comprehensive review campaign,
hardens the validation architecture so these classes of defect cannot recur silently,
and closes a documentation integrity finding. The public bundle is re-mirrored from
the corrected canonical tree.

---

## Data corrections

### S214 / S215 — Manufacturing rates of profit (values changed, F-4C-02 CRITICAL)

**What changed**: The extension data for S214 (Rates of Profit across US Manufacturing
Industries, Appendix-7, 1987–2005) and S215 (Incremental Rates of Profit, 1988–2005)
are materially different from all prior releases.

**Root cause**: The loaders averaged only 6 of 12 intended manufacturing industries.
Six column names in the Appendix-7 workbook differ from the loader's hard-coded
`MFG_INDUSTRIES` list (e.g. `Machinery`→`Mach.`, `Petroleum`→`Petr.&Coal`); the
guard that was supposed to catch missing columns fired only when *all* columns were
absent, so a 6-of-12 miss was silently treated as success. The corrected loaders use
an explicit `MFG_INDUSTRY_MAP` (12 intent→header pairs) and a hard
`assert len(matched) == 12` that fires on any single mismatch.

**Magnitude of the correction**:

| Series | Measure | Range |
|--------|---------|-------|
| S214 | Per-year relative difference | 17–42% (e.g. 1996: 0.2009→0.1615, −24.4%) |
| S215 | Sign-flips (direction reversed) | 4 years: 1990, 1996, 1998, 2002 |
| S215 | Max absolute difference (non-flip years) | |Δ| up to 0.319 (2004; S215 refval ≈ 0.395) |

The prior values represented a 6-industry subset by defect. The corrected values are
the faithful 12-industry mean Shaikh's Appendix-7 companion data was designed to
produce. Three independent anchor points per series were hand-recomputed from the raw
workbook (not via the loader) and proved RED against the prior data and GREEN against
the corrected data at 0.0% difference.

**Scope note**: S214 and S215 remain `extension_only_validated`. The 1987–2005
Appendix-7 workbook is the only available data period for these series; no book-period
(1960–1989) observations exist and none are introduced. Motor Vehicles (`Mtr.Veh.`)
is genuinely absent from the Appendix-7 industry panel; the recoverable set is 12,
ratified per Gate G1-s214.

---

### S801 — Industry price-level indices (labels corrected, values unchanged, F-T2-01)

**What changed**: The Competitive and Oligopolistic column labels in S801 (Eichner
1973, Fig 8.1, administered-price divergence, 1953–1971) were transposed. All data
values are bit-for-bit identical to prior releases.

**Root cause**: The frozen digitized source file
(`SalvagedInputs/.../Eichner_1973_Fig8_1_S801.xlsx`, deny-listed) carried the two
industry columns backwards relative to the printed figure. `L01_S801.py` now applies
an explicit `column_relabel` after loading the panel, citing Shaikh p.372: *"the
smoother prices of the concentrated [oligopolistic] industries."*

| Subseries | Before (wrong) | After (correct) | Figure ground truth |
|-----------|----------------|-----------------|---------------------|
| Oligopolistic@1973 | 145.03 (volatile) | 128.47 (smooth) | dashed ≈ 127.9 |
| Competitive@1973 | 128.47 (smooth) | 145.03 (volatile) | solid ≈ 142.4 |

Three figure-derived anchors independently measured (not from the pipeline's own
xlsx) were RED before the fix and GREEN after. `V03_S801` gained an independent
variance sanity check — `var(Competitive) > var(Oligopolistic)` — so a transposition
cannot recur silently even if an MAE round-trip returns 0.0.

---

## Why this cannot silently recur: validation architecture

The campaign diagnosed that the prior validation surface was insufficient: V03
round-trip validators compare a loader's output against a reference file they help
generate, and so cannot independently catch systematic errors (wrong columns, inverted
labels). Three defences are now in place for every release gate:

### 1. Independent anchors (ANCHOR-BEFORE-FIX doctrine)

Before any data fix is committed, hand-derived reference values (computed from
primary sources, *not via the loader*) are registered in
`validation.independent_anchors` in the registry. These anchors must be shown RED
against the defective data, and GREEN after the fix, before the change is accepted.
This creates a regression surface that is independent of the loader and the
round-trip validator.

### 2. Mutation harness (`tools/mutation_check.py`)

Systematically injects scale (×1.5), shift (+0.05), and swap mutations into each
anchored series' processed parquet, then re-runs the anchor suite and asserts every
mutation returns RED. A series where mutations pass silently is flagged as
"validation-blind." For S214/S215 the mutation matrix is 100%: all three injected
mutations are caught; the control (unmutated) returns GREEN.

### 3. `run.py --gate`

One command runs anu-doctor (`check_project.py`) + the full anchor suite + all 118
V03 validators in sequence, and exits non-zero if any step returns FAIL or any anchor
returns RED. CI (`ci.yml`, `replicator_check.yml`) now invokes `--gate` against the
publish bundle tree on every commit.

### Validation scope tracking (`validation_class`)

Every series entry in `series_registry.json` now carries a `validation_class` field
that records the honest validation scope:

| Class | Count | Meaning |
|-------|-------|---------|
| `book_verified` | 12 | Independent anchor against the book's own printed values |
| `pipeline_consistent` | 88 | V03 round-trip against reference derived from the same pipeline |
| `theoretical` | 8 | Theoretical derivation; no empirical target |
| `extension_only` | 2 | S214, S215: only extension data exists; book period genuinely absent |
| `study_replication` | 8 | External-study replications (XS series) |

---

## Other changes in v1.6

- **S703 explainer (F-7C-01)**: the "From the book" section previously presented a
  re-worded paraphrase as a verbatim, page-cited direct quote. Replaced with the
  genuine Shaikh p.302 verbatim, KB-verified (`ch07_real_competition.md`,
  `verbatim_check: true`).
- **Registry — S707/S711 predecessors (F-3D-03)**: `S707.cd_id` restored to `"S038"`;
  `S711.cd_id` and `S711.cd2_id` nulled (S038 is a false-name-match for S707, not a
  genuine S711 ancestor). P42 (predecessor↔crosswalk bijection) now PASS.
- **Registry — units labels**: S1508/S1509 `rate_decimal`→`rate_percent`;
  S1402-B `index_1948_1951_avg=100`→`=1`; S1505/S1506/S1507 sigma-prime
  `rate_decimal`→`normalized_zscore`.
- **Registry — extension blocks**: populated for 96 series (`performed_by` field
  added); P36 (extension-block binary invariant) now PASS (was FAIL 88+8).
- **Registry — `validation_class`**: added to all 118 entries; 8 theoretical
  series flipped to `theoretical_validated`; S214/S215 to `extension_only_validated`.
- **Code hygiene**: orphaned bootstrap and migration scripts archived to
  ArcArchive; `Technical/tmp/` and `Technical/comparison/` dated backup trees swept.
- **Replicator library re-sync**: `replicator/lib/` refreshed from canonical
  `Technical/code/` (incorporates loader fixes for S214/S215/S801/S1402/S1505–S1507
  and new `_v03_anchor_lib.py`).

---

## v1.4 release notes

See `RELEASE_NOTES_v1.4.md` (backfill stub) and `CHANGELOG.md §v1.4` for the
AS/ES → XS series-ID migration and provenance reconciliation that shipped in v1.4.
