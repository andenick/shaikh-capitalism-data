# Changelog — RSCD (Replication of Shaikh 2016)

All notable changes to the public replication bundle are documented here.
Versioning follows the project release line (see `RELEASE_NOTES_*`).

## v1.6 — 2026-07-10 — Data corrections + validation hardening

Two data series corrected (one CRITICAL magnitude error, one label transposition),
a fabricated explainer quote removed, the validation architecture hardened against
silent regressions, and registry metadata corrected across 12 items. The full
public bundle is re-mirrored from the post-campaign canonical tree.

**Bundle counts (exact):** 118 canonical series · 113 published (`publish:true`)
· 113 chopped CSVs · 112 extension workbooks (S1006 withheld) · 112 research
dossiers (S1006 withheld) · 226 series docs (113 DPR + 113 EPR) · 5 withheld
(`publish:false`) · 2 `data_unavailable` (S306, S307).

### Data corrections — values changed (S214/S215, CRITICAL)
`S214` (Rates of Profit across US Manufacturing Industries, 1987–2005) and `S215`
(Incremental Rates of Profit, 1988–2005) were silently computed from 6 of 12 intended
manufacturing industries due to a column-name mismatch in the Appendix-7 workbook.
Finding F-4C-02.

- **Magnitude**: S214 per-year relative difference 17–42%; S215 shows 4 sign-flips
  (1990, 1996, 1998, 2002) plus shifts of 16–319% at other years.
- **Prior values** were a 6-industry subset by defect, not the intended 12-industry
  mean. The corrected loaders use an explicit `MFG_INDUSTRY_MAP` (12 entries) and a
  hard `assert len(matched) == 12` that fires on any header drift. Motor Vehicles
  (`Mtr.Veh.`) is genuinely absent from the Appendix-7 panel; the recoverable set
  is 12 (ratified per Gate G1-s214).
- **Note**: S214/S215 remain `extension_only_validated`. The Appendix-7 extension
  data (1987–2005) is the only available period; no book-period observations exist and
  none are introduced.
- Three independent anchor points per series hand-recomputed from the raw workbook
  (not via the loader): RED before the fix, GREEN after at 0.0% difference.

### Data corrections — labels only (S801)
`S801` (Eichner 1973 Fig 8.1, administered-price divergence) had its Competitive and
Oligopolistic column labels transposed. All 9 values are bit-for-bit identical to prior
releases. Finding F-T2-01.

- The frozen digitized source xlsx carried the two series backwards relative to the
  printed figure. `L01_S801.py` now applies an explicit `column_relabel` citing
  Shaikh p.372: "the smoother prices of the concentrated [oligopolistic] industries."
- At 1973: Competitive = 145.03 (volatile, corrected) / Oligopolistic = 128.47
  (smooth, corrected); prior mapping was inverted.
- `V03_S801` gained an independent variance sanity check so a transposition cannot
  recur silently (var(Competitive) > var(Oligopolistic) is independently asserted).

### Data corrections — extension source (S1603)
S1603 extension source corrected: OECD-MEI interbank -> 3-mo T-Bill per book Fig 16.6/16.7.
`S1603-A` (US short-term interest rate, Ch16) was reading the OECD-MEI interbank rate
(`RXRRULCOECD`, which runs 0.24-2.36pp above the T-Bill every year) instead of the
3-month Treasury Bill rate the book actually plots (Shaikh Fig 16.6/16.7: "14.03% in
1981 ... 0.06% in 2011"). `L01_S1603.py` now reads Shaikh's own Appendix-16 ProfitRates
column "Interest Rate (3-mo. T-Bill)" (= ERP Table 73 / FRED TB3MS) and splices
continuously to the FRED TB3MS extension; an independent T-Bill anchor was proved RED
on the OECD series and GREEN after the fix. Finding F-P2.1-01.

### Documentation correction
`docs/explainers/S703_EXPLAINER.md` "From the book" section presented a re-worded
and embellished paraphrase as a verbatim, page-cited direct quote. Replaced with the
genuine Shaikh p.302 verbatim from the Knowledge Base (`ch07_real_competition.md`,
`verbatim_check: true`). Finding F-7C-01.

### Validation architecture hardened
- **Independent anchors (ANCHOR-BEFORE-FIX doctrine)**: 6 new point-anchors for
  S214/S215 and 3 figure-derived anchors for S801, each proved RED on defective data
  before the fix was committed. Anchor registration is now a pre-condition for any
  data change.
- **`validation_class` field**: all 118 registry entries carry a `validation_class`
  key recording honest validation scope: `book_verified` (12), `pipeline_consistent`
  (88), `theoretical` (8), `extension_only` (2: S214/S215), `study_replication` (8).
- **`run.py --gate`**: new command running anu-doctor + full anchor suite + all 118
  V03 validators; exits non-zero on any FAIL or anchor RED. CI updated to invoke this
  gate against the publish bundle tree.
- **Mutation harness** (`tools/mutation_check.py`): injects scale, shift, and swap
  mutations and asserts every one surfaces RED. Any validation-blind series is flagged.

### Registry metadata corrections
- S707/S711 predecessor IDs un-swapped (F-3D-03): `S707.cd_id` restored to `"S038"`;
  `S711.cd_id` and `S711.cd2_id` nulled (S038 is a false-name-match for S707, not a
  genuine S711 ancestor). P42 (predecessor↔crosswalk bijection) now PASS.
- S703/S704 `construction` field corrected to enum value `machine_digitized`;
  mojibake (`\xef\xbf\xbd`) corrected to em-dash (F-3C-05, F-4A-05).
- Units labels corrected: S1508/S1509 `rate_decimal`→`rate_percent`; S1402-B
  `index_1948_1951_avg=100`→`=1`; S1505/S1506/S1507 sigma-prime `rate_decimal`→
  `normalized_zscore`.
- Extension blocks populated for 96 series (`performed_by` field added); P36
  (extension-block binary invariant) now PASS (was FAIL 88+8).
- `validation_class` added to all 118; 8 theoretical series status updated to
  `theoretical_validated`; S214/S215 status updated to `extension_only_validated`.

### Replicator library re-sync
The self-contained `replicator/lib/` is refreshed from the canonical
`Technical/code/` tree, incorporating all loader fixes (S214, S215, S801, S1402,
S1505–S1507), the new `_v03_anchor_lib.py` infrastructure, and the `column_relabel`
parameter in `_ch7_validator_lib.py`.

### Bundle refreshed from canonical tree
Chopped CSVs, extenbooks, DPRs/EPRs, research JSONs, registry, ledger, validation
report, subsource metadata, correspondence matrix, code, MIGRATION, and the
self-contained replicator were re-mirrored from the post-campaign internal tree.
Publish filter applied: 5 `publish:false` series excluded (`S306`, `S307`, `S408`,
`XS2304`, `XS2305`).

### Scrub scope (honest statement)
The re-mirror is scrubbed to the **transparency-bundle** audit profile (pinned in
`.publish_audit_config`):
- **Hard-leak classes are zero** — no absolute workspace paths (`D:/Arcanum`,
  `C:/Users`), no `/Council/`, no `Druck`/`Robin` internal tool names. The only
  retained `andenick` token is the project's own GitHub repo URL (whitelisted in
  `.publish_ignore`).
- **Authoring agent-IDs neutralized** — internal `opus-subagent-*` / `*fanout`
  reviewer strings in registry/research/summary files were replaced with
  `automated-agent` (295 tokens, 217 files); they carried no reproducibility value.
- **Internal build state removed** — the stale `PIPELINE_STATE.json` (Anu build
  cursor; referenced the archived `viz/` app and in-progress campaign tracking) is
  no longer shipped; `paths.py` / `replicate.py` no longer depend on it.
- **Relative workspace paths in reproducibility artifacts are retained** (replicator
  code, registries, provenance docs, build narratives) as functional references and
  are classified WARN under the transparency-bundle profile — they are internal-state
  metadata describing their own source layout, not public-web surfaces. The public
  **web** export (`_Web_v1.6.0/`) is separately de-pathed to strict/FAIL zero.

---

## v1.5 — 2026-07-02 — Skeptical review & remediation + publish-leak fix

This release re-mirrors the public bundle from the canonical internal tree after
the RSCD v1.5 Skeptical Review & Remediation campaign (26-item backlog, 118/118
chapter skeptical sweep, Gate-0 rulings D-1…D-9 + Tier-5, decisions 0008–0018).
See `RELEASE_NOTES_v1.5.md` for the full change inventory, NUMERIC_CHANGES
tables, judgment calls, and the D14 re-score (all 16 chapters ≥ 90).

### Publish filter now applied to the mirror (leak fix)
- `deploy/sites/rscd.yml` serves `Outputs/Publish/` wholesale, so the mirror now
  applies a **registry-driven publish filter** (Decisions 0010 / 0016):
  - the 5 `publish:false` series (`S306`, `S307`, `S408`, `XS2304`, `XS2305`)
    are **excluded** from all data artifacts (chopped, extenbooks, research).
    `S703` and `S704` are **not** in this list — they were recovered by machine
    digitization in this same release (Decision 0019) and ship as `publish:true`
    (see §S703/S704 below).
  - the licensed **Ibbotson SBBI** subseries inside S1006 (`S1006-A/-B/-C`,
    Morningstar-licensed) are **dropped row-by-row** from `chopped/S1006.csv`
    (255 rows), the S1006 XLSX extenbook + research JSON are withheld, and the
    salvaged `Appendix10_Ibbotson.xlsx` is excluded from the bundled inputs.
    The open **Damodaran-NYU** alternates (`S1006-*-ext`) remain the public
    surface.
  - The `series_registry.json` copies (top-level + bundled) are **publish-filtered**:
    all 118 series entries are retained for transparency (with `publish` flag +
    `triage`), but SBBI subseries entries, `reference_values`, and SBBI
    independent-anchors are stripped so no withheld data values ship. This
    supersedes the v1.4 "retain withheld series' data with a flag" convention for
    the *data* surface, per the Decision 0010 licensing requirement.

### S703/S704 machine-digitization recovery (Decision 0019)
- `S703` (Fig 7.13 world manufacturing average rate of profit, 1970–1989) and
  `S704` (Fig 7.14 US manufacturing average rate of profit, 1960–1989) were
  previously `data_unavailable`. Both were recovered by dual independent machine
  digitization of the printed Christodoulopoulos (1995) figures, with per-year
  crop-level adjudication and adversarial verification.
- Decision 0019 (amends 0018) ratifies the `machine_digitized` construction method.
  Per-point transcription confidence is documented in `series_registry.json`.
  Human returns/ digitization remains the superseding path if ever filed.
- `publish:true` set on 2026-07-02. Triage reason: dual independent extraction,
  adversarial verifier rebuilt calibration from scratch, no point refuted.

### Data corrections carried into the bundle (see RELEASE_NOTES_v1.5 for tables)
- S1401-A wage share 2012–2025 (input A576RC1 → W209RC1 ÷ GDP; splice break fixed)
- S203-A US real GDP/capita 1930–1944 (MeasuringWorth re-pull, Depression trough
  corrected)
- S1406-B Phillips 2012–2024 (denominator hours → FTE; extended to 2024)
- S604 Fig 6.7 completed (+S604-C/-D reconstructed curves)
- S207-D 2010 duplicate splice row removed; S210-A 2026 partial-year row removed
- S1701 / XS2302 gained an `is_forecast` column (forecast rows flagged, not truncated)
- units-string corrections (S1502/S1503, XS002/3/5/6, S602, S308/S309) — values
  byte-identical

### Standing validation infrastructure added
- independent book-value anchors + splice-continuity + level-plausibility checks
- ALFRED vintage manifest, classification-vintage guard, generalized NIPA line
  resolver, run.py XS-regex + ES/XS truth-CSV fallback

### Bundle refreshed from canonical tree
- Chopped CSVs, Extenbooks, DPRs/EPRs, research JSONs, registry, ledger,
  validation report, subsource metadata, correspondence matrix, code, MIGRATION,
  and the self-contained replicator (lib/scripts/config/inputs_bundled) were all
  re-mirrored from the post-campaign internal tree, with the publish filter above.

---

## v1.4 — 2026-06-11 — Series-ID migration + provenance reconciliation

This release brings the public bundle into line with the internal canonical tree
after the AS/ES → XS series-ID migration (Series ID Spec v2.2, Anu Framework
v12.2) and a Knowledge-Base reconciliation pass.

### Series-ID migration (AS/ES → XS)
- The 9 analytical-construct series (legacy `AS001`–`AS009`) and 8 external-study
  series (legacy `ES2001`–`ES2305`) have been migrated to the canonical **`XS`**
  ("Extra Series") prefix per the Series ID Spec v2.2. `AS`/`ES` are now legacy
  prefixes rejected by the framework.
- Every `XS` entry carries `xs_class` (`appendix` for the former AS constructs,
  `external_study` for the former ES replications) and `xs_attribution`.
- The full old→new correspondence table is published at
  **`MIGRATION/crosswalk.csv`** (with `MIGRATION/PREFIX_SCHEME.md`). This is the
  authoritative public crosswalk for anyone who referenced the old IDs.
- Migration applied uniformly to: `series_registry.json`, all chopped CSVs,
  per-series Extenbooks (filenames **and** internals), DPRs/EPRs, research JSONs,
  replicator L01/P02/V03 scripts, and bundled inputs.

### Provenance reconciliation (KB)
- DPRs and research JSONs corrected against the Knowledge Base, removing
  hallucinated provenance statements carried by earlier bundles.
- Per-subseries `units` now declared where a series mixed dimensionless ratios
  with dollar/level components (e.g. the former AS002 Sigma ratio) — keeps charts
  dimensionally honest.

### Triage verdicts (transparency)
- The bundled `series_registry.json` now carries, for every series, a `publish`
  flag and a `triage` record (`{verdict, reason, date}`).
- **Culled series are retained in the bundle but marked `publish: false`** for
  full transparency: `S306`, `S307`, `S408` (data-unavailable / non-renderable
  cross-sections) and `XS2304`, `XS2305` (literature-compilation external-study
  stubs). `S703` and `S704` were also `publish:false` at this release; they were
  recovered in v1.5. Downstream consumers should honor `publish: false`.

### Bundle contents refreshed from canonical tree
- Chopped CSVs, Extenbooks, DPRs/EPRs, research JSONs, registry, ledger,
  validation report, subsource metadata, correspondence matrix, and the
  self-contained replicator package were all re-mirrored from the post-migration
  internal tree.

### Notes
- Public GitHub repository references (`github.com/andenick/shaikh-capitalism-data`)
  are the project's own publication target and are intentional.

---

## v1.0.2 and earlier

See `RELEASE_NOTES_v1.0.md` and the project-level `Outputs/RELEASE_NOTES_*` files
(v1.0, v1.0.1, v1.0.2, v1.1, v1.2, v1.3) for the pre-migration history.
