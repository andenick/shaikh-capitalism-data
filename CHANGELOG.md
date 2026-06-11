# Changelog — RSCD (Replication of Shaikh 2016)

All notable changes to the public replication bundle are documented here.
Versioning follows the project release line (see `RELEASE_NOTES_*`).

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
  full transparency: `S306`, `S307`, `S408`, `S703`, `S704` (data-unavailable /
  superseded primary series) and `XS2304`, `XS2305` (literature-compilation
  external-study series). Downstream consumers should honor `publish: false`.

### Bundle contents refreshed from canonical tree
- Chopped CSVs, Extenbooks, DPRs/EPRs, research JSONs, registry, ledger,
  validation report, subsource metadata, correspondence matrix, and the
  self-contained replicator package were all re-mirrored from the post-migration
  internal tree.

### Notes
- Public GitHub repository references (`github.com/andenick/shaikh-capitalism-data`)
  are the project's own publication target and are intentional.

## v1.0.2 and earlier

See `RELEASE_NOTES_v1.0.md` and the project-level `Outputs/RELEASE_NOTES_*` files
(v1.0, v1.0.1, v1.0.2, v1.1, v1.2, v1.3) for the pre-migration history.
