---
decision_id: "RSCD-0020"
title: "v1.6 Remediation Campaign — Gate Rulings, Status Taxonomy, Anchor Doctrine, and Namespace"
status: approved
proposed_at: "2026-07-10T00:00:00Z"
approved_at: "2026-07-10T00:00:00Z"
decided_by: user
ratification: "user ruling 2026-07-10 ('/megaexecute')"
campaign: "RSCD Post-Review Remediation v1.6"
plan: "RSCD_POST_REVIEW_REMEDIATION_PLAN.md"
related:
  - RSCD-0018
  - RSCD-0019
  - Technical/remediation_v16/REMEDIATION_STATE.json
  - Technical/remediation_v16/evidence/
affected_series:
  - S214
  - S215
  - S801
  - S1104
  - S1301
  - S703
  - S704
  - "and all 118 series (validation_class rollout)"
---

# RSCD-0020 — v1.6 Remediation Campaign Summary

**Status**: APPROVED
**Date**: 2026-07-10
**Decided by**: user (ratification via `/megaexecute` command)
**Campaign plan**: `RSCD_POST_REVIEW_REMEDIATION_PLAN.md`
**Evidence bundle**: `Technical/remediation_v16/evidence/`

---

## Summary of Key Rulings

This decision records the gate rulings, framework adoptions, and doctrine decisions made
during the RSCD v1.6 Skeptical Review Remediation campaign.

### G1-s214: 12-Industry Mean (corrected)

S214 (US Industry Average Rates of Profit) was previously computing a 15-industry mean.
The correct figure is a 12-industry mean per Shaikh's book methodology. The fix:
- S214 values corrected (−17% to −42% corrections vs the prior pipeline; S215 had 4 sign flips
  including 1990, 1996, 2002)
- Loader hard-fails on industry-count drift (guard added)
- Status confirmed as `extension_only_validated` (no book-period chopped rows)
- Decision: default (a) — corrected 12-industry mean with header-resolved hard assert

### S801 Relabel (F-T2-01)

S801 subseries label corrected from a stale label to the correct 'concentrated'/'competitive'
industry labels per Eichner (1973). Pure label swap — no value changes. 9/9 reference
values confirmed value-identical after the swap. Variance guard probed RED on the defective
labels, GREEN on the corrected labels.

### Status Taxonomy Extensions (G4-status)

Interim `validation_class` field introduced for all 118 series. Values:
`book_verified` / `pipeline_consistent` / `theoretical` / `extension_only` / `study_replication`.

Framework-level taxonomy extension (anu-ingestion v5.3, TD.4) introduced:
- `theoretical_validated`: for S301–S309, S1301 and other theoretical model figures
- `extension_only_validated`: for S214, S215

Project-level certification language must partition series by `validation_class` — never a
blanket "N PASS" headline.

### Anchor Doctrine Adoption

Formal adoption of the ANCHOR-BEFORE-FIX doctrine:
> Every data fix registers an independent anchor, proves it RED on defective data, fixes,
> proves GREEN on corrected data. Evidence bundle per item.

Applied throughout the campaign (P1.1 S214/S215, P1.2 S801). All future fixes to data
series in RSCD follow this doctrine.

### Decision Namespace (TD.5)

Framework-global decisions use prefix `FW-` (framework authority).
Project-local decisions use prefix `RSCD-` (this directory).
Existing files are not renamed; prefix is citation convention only.
See `DECISION_NAMESPACE.md` in this directory for the id↔file map.

### G3: Hub Deployment

Hub-only regeneration (standing ruling 2026-07-02). Static site regenerated but not
deployed. Drive refresh to v1.6 approved.

### G5: Certification Language

Adopt book-verified / pipeline-consistent certification language. Blanket "N validated"
headlines are replaced with class-partitioned counts per the v5.3 certification-language
rule.

---

## Affected Files

- `Technical/series_registry.json` — P4.1 agent (validation_class rollout, S801 labels,
  S703/S704 flips, S214/S215 status, XS prefix registrations)
- `Technical/docs/decisions/DECISION_NAMESPACE.md` — NEW (this campaign)
- `Technical/MIGRATION/PREFIX_SCHEME.md` — rewritten for XS era
- `Technical/MIGRATION/CD2_to_RSCD_crosswalk.csv` — 9 AS### rows re-targeted to XS###
- `Technical/MIGRATION/divergences_from_CD2.md` — NEW (consolidated divergence table)
- `Technical/docs/explainers/S1301_EXPLAINER.md` — "From the book" section added
- `Technical/docs/explainers/S702_EXPLAINER.md` — stale Table-28 note corrected
- `Technical/docs/series/S404_DPR.md` through `S407_DPR.md` — banner method corrected
- `Technical/research/S703_research.json` et al. — back-annotations per dossier convention
- Framework skills: anu-ingestion v5.3, anu-review v5.1 (TD.4); TD.5 namespace (framework)
