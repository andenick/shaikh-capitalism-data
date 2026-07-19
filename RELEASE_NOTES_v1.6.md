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

---

## Final-gate certification (P5.3, 2026-07-10)

This section records the campaign's final release gate exactly as measured. All numbers
are from the P5.1d final re-verification run (`Technical/remediation_v16/evidence/P5.1d_gates.md`)
and the P5.1c registry audit, reconciled to the **post-register** state (the
`DIVERGENCE_REGISTER.json` was generated in P5.1, clearing the P10 WARN).

### Certification numbers (post-register)

| Gate | Result |
|------|--------|
| **anu-doctor** (`check_project.py`, 43 P-checks) | **0 FAIL / 3 WARN** (P28, P32b, P40 — post-register; P10 cleared by the generated register) |
| **Anchor suite** | **51 series checked / 0 RED** (0 anchor RED · 0 splice RED · 0 plausibility RED) |
| **Anchor census (registry)** | 30 independent anchors · 4 plausibility rules · 1 legacy anchor |
| **V03 batch (118 series)** | **118 non-FAIL / 0 FAIL**, by partition: PASS 106 · PASS_THEORETICAL 8 · PASS_CROSS_SECTIONAL_UNAVAILABLE 2 · PASS_EXTENSION_ONLY 2 |
| **`validation_class` (118)** | book_verified 12 · pipeline_consistent 88 · study_replication 8 · extension_only 2 · theoretical 8 |
| **Mutation harness** (33 series × 3) | 99 cells: **96 CAUGHT · 3 EXEMPT · 0 BLIND** · 0 NOT-RUNNABLE |
| **Framework** (`check_framework.py`, D1–D19) | **0 failures / 0 warnings** |
| **Live hub** (shaikh.heterodata.org) | **8/8 live checks GREEN** (S214/S215/S801/S1603-A/S1006 values, download disclaimer, 0 kb-comments, S306 held back) |
| **RED-injection drill** | fires (S1006 ×1.5 → `--gate` exit 1, anchor RED) — the safety net is proven live |
| **Deny-rule drill** | `Inputs/` + `SalvagedInputs/` writes DENIED |
| **Vintage manifest** | 15/15 live-FRED loaders covered — PASS |

### Certification language (G5 — partition claims, never blanket)

Per Gate G5-cert, RSCD makes **partitioned** validation claims and **never a blanket
"all 118 verified against the book."** Honestly:

- **12 series are book-verified** — an independent anchor was checked against the book's own
  printed values (Shaikh 2016 tables/figures/appendix regressions).
- **88 series are pipeline-consistent** — the V03 round-trip matches a reference derived from
  the same pipeline; faithful reproduction, but not an independent-of-the-loader check.
- **8 series are study-replication** (external-study XS series, validated against the source study).
- **8 series are theoretical** (analytical derivations; no empirical target — `PASS_THEORETICAL`).
- **2 series are extension-only** (S214/S215; the book period 1960–1989 is genuinely
  data-unavailable, so only the Appendix-7 extension exists — `PASS_EXTENSION_ONLY`).

The anchor / mutation / `--gate` architecture (see "validation architecture" above) is what makes
these claims mechanically enforceable rather than asserted.

### Four independent P5 re-verifier verdicts

| Verifier | Scope | Verdict |
|----------|-------|---------|
| **P5.1a** | The 4 data fixes + cross-surface integrity, re-derived from primary sources | **ALL 5 ITEMS VERIFIED** — no discrepant, no campaign blocker (S214/S215 12-industry mean, S801 swap, S1603-A T-Bill, S703 quote all agree across recompute/canonical/Publish/Web/hub) |
| **P5.1b** | Public bundle, adversarial outsider lens | **BLOCKERS** — repro faithfulness, LF endings, data-fix honesty, manifest hashes and WEB=113 verified good, but a re-scrub of flattened `Technical/` path + agent-ID/HDARP strings, a `viz/`-vs-README mismatch, and a stale `replicator/README.md` were flagged and routed to the blocker-fixer |
| **P5.1c** | P4 mass registry/metadata work | **CLEAN** — 20/20 spot-audit correct, `validation_class` census 12/88/8/2/8 exact, S707/S711 predecessor bijection correct, doctor 0 FAIL |
| **P5.1d** | Full gate stack | **ALL-GREEN** — `--gate` exit 0, mutation 96C/3E/0B, framework 0/0, RED-injection fires, deny-drill DENIED, vintage 15/15 |

### Three WARN backlog items (named honestly)

The 3 residual doctor WARNs are documented, non-blocking, and carried in the CLAUDE.md v1.x backlog:

- **P28** — non-standard decision-log filenames (`DECISION_NAMESPACE.md`,
  `RSCD-0020_v16_remediation.md`) that don't match the `NNNN-title.md` pattern.
- **P32b** — S1301 (theoretical) carries point-index `reference_values` keys rather than year keys;
  set `year_column_is_index` or move to `derived_statistics`.
- **P40** — 44/113 published series lack an independent anchor versus a loader-shared source. These
  are traceable to **book-appendix series where a printed per-year anchor is structurally impossible**;
  the shortfall is an honest, documented census, not a hidden tautology.

---

## Campaign statistics (RSCD v1.6 Post-Review Remediation)

- **Structure**: ≈50 Opus subagent work-items (fixer + independent-verifier pairs) across **6 execution
  phases** — P0 (freeze/baseline/rulings), P1 (data fixes), P2 (validation architecture),
  P3 (surface refresh), P4 (registry/state/docs/hygiene), P5 (re-review/gate/cert) — **plus a
  framework Technical-Debt (TD) track**. 34 evidence briefs in `Technical/remediation_v16/evidence/`.
- **Doctrine**: ANCHOR-BEFORE-FIX — every data fix registers an independent anchor, is proven RED on
  the defective data, fixed, then proven GREEN; each item carries an evidence bundle.
- **Four data fixes (v1.6) with magnitudes**:
  1. **S214** — manufacturing average profit rate: 6-of-12 → full 12-industry mean; **17–42% per-year**
     corrections (e.g. 1996: 0.2009 → 0.1615, −24.4%).
  2. **S215** — incremental profit rate: same 12-industry fix; **4 sign-flips** (1990/1996/1998/2002),
     |Δ| up to **0.319**.
  3. **S801** — Eichner competitive/oligopolistic price indices: **label transposition** corrected
     (Oligopolistic@1973 145.03 → 128.47); all values bit-identical.
  4. **S1603-A** — US short-term interest rate: **OECD-MEI → book's 3-mo T-Bill** (1981 0.15911 → 0.14029,
     +13%; 2011 0.003 → 0.0006, ~5×).
  - Reconciled here: **S203** (MeasuringWorth 1929–34 re-pull, −28.6% honest Depression fall) was a
    v1.5 fix; its stale "to-do" backlog line and `DIVERGENCE_REGISTER` ADR-008 were closed to RESOLVED
    in P5.3.
- **Surfaces refreshed to v1.6**: canonical `Technical/` tree · `Outputs/Publish/` bundle · `Web_v1.6.0`
  export (113 chopped + parquet + dictionary + scrubbed explainers/DPRs) · live hub
  `shaikh.heterodata.org` · Google-Drive package (`RSCD_Drive_v1.6`, USER STEP = sync) · Reports
  (Results/Executive/Methodology PDFs) · 116 regenerated Figures · `D:/ArcArchive/RSCD_v1.6` (SHA-256 manifest).
- **Framework versions shipped (TD track, framework 0/0 at gate)**: anu-doctor **v2.5** (P01–P43; P24/P20
  ledger-freshness + P40 round-trip census repaired; P32b/P41/P42/P43 added) · anu-ingestion **5.3**
  (`theoretical_validated` + `extension_only_validated` + `validation_class`) · anu-review **5.1** ·
  anu-extension **v4.2** (DIVERGENCE_REGISTER always-required + generator + `performed_by`) · anu-publish
  audit **v2.2** (P11 internal-reference detectors) · carson-visual **1.2** (HTML-comment leak detector) ·
  `DENY_RULE_SCOPING_STANDARD` **v1.0**.
- **Accountability ledger**: `Technical/remediation_v16/BACKLOG_DISPOSITION.csv` — all 257 review findings
  triaged; 100% disposition coverage on every CRITICAL/MAJOR/MODERATE row (65/65).
