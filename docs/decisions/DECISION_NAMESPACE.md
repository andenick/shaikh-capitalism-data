---
schema: decision-namespace-v1
authority: RSCD project
prefix: RSCD-
created: "2026-07-10"
source: "Technical/remediation_v16/TD.4_TD.5_taxonomy_namespace.md (template from TD.5 framework agent)"
---

# Decision Namespace — RSCD Project

**Authority**: RSCD project (`Projects/RSCD/Technical/docs/decisions/`)
**Prefix**: `RSCD-`
**Scope**: project-local decisions (this directory only)
**Counterpart**: framework-global decisions live in the framework's decision registry under prefix `FW-`

## Namespace Rules (per TD.5 / FD-10)

1. **Existing files are NOT renamed.** The bare integer (`0007_methodology_library_location.md`)
   IS the prefixed id `RSCD-0007`. The integer is the canonical form on disk; `RSCD-` is how
   you CITE it in prose, decision refs, and YAML `related:` fields.

2. **All NEW decisions use a prefixed id** in their filename and `decision_id` frontmatter field:
   `RSCD-{NNNN}_{slug}.md` (e.g. `RSCD-0020_v16_remediation.md`).

3. **Citations always use the prefixed id** (`RSCD-0007`, not `0007`) to distinguish from
   framework-global `FW-0007` (which is a different decision).

4. **Next free id**: `RSCD-0021` (as of 2026-07-10; RSCD-0020 assigned to v1.6 remediation).

## Current Decision Map

| RSCD id | File | Title | Status |
|---|---|---|---|
| RSCD-0001 | `0001_external_study_scope.md` | External Study Scope for RSCD v1.0 | approved |
| RSCD-0002 | `0002_ch6_gpim_variants_disposition.md` | Ch6 GPIM Construction Internals Disposition | approved |
| RSCD-0003 | `0003_crosswalk_cleanup.md` | Crosswalk Mismap Cleanup | approved |
| RSCD-0004 | `0004_ch7_additional_series.md` | Ch7 Additional Series | approved |
| RSCD-0005 | `0005_discontinued_apis_deferred.md` | Discontinued API Substitutions (Deferred to Phase 4) | proposed |
| RSCD-0006 | `0006_es2301_decomposition_pending.md` | ES2301 Decomposition Pending | proposed |
| RSCD-0007 | `0007_methodology_library_location.md` | Methodology Library Location | approved |
| RSCD-0008 | `0008_s203_measuringworth_repull_rebase.md` | S203 MeasuringWorth Re-pull and Rebase | proposed |
| RSCD-0009 | `0009_project_wide_forecast_policy.md` | Project-Wide Forecast Policy | approved |
| RSCD-0010 | `0010_s1006_sbbi_publish_false_damodaran.md` | S1006 SBBI Publish False Damodaran | approved |
| RSCD-0011 | `0011_v03_independent_anchors_tolerance.md` | V03 Independent Anchors Tolerance | approved |
| RSCD-0012 | `0012_rscd_5sheet_extenbook_variant.md` | RSCD 5-Sheet Extenbook Variant | approved |
| RSCD-0013 | `0013_ch7_panels_content_type_time_series.md` | Ch7 Panels Content Type Time Series | approved |
| RSCD-0014 | `0014_classification_vintage_tag.md` | Classification Vintage Tag | approved |
| RSCD-0015 | `0015_xs_s6xx_components_documentary_lineage.md` | XS→S6xx Components Re-scoped as Documentary Lineage | approved |
| RSCD-0016 | `0016_static_site_regenerate_publish_filter.md` | Static Site Regenerate Publish Filter | approved |
| RSCD-0017 | `0017_decisions_dir_canonical_provenance_substitution.md` | Decisions Dir Canonical Provenance Substitution | approved |
| RSCD-0018 | `0018_tier5_s703_s704_guided_digitization_scheduling.md` | Tier-5 S703/S704 Guided Digitization Scheduled | superseded-in-part |
| RSCD-0019 | `0019_machine_digitization_s703_s704.md` | Machine Digitization Recovers S703/S704 | approved |
| RSCD-0020 | `RSCD-0020_v16_remediation.md` | v1.6 Remediation Campaign Summary | approved |
