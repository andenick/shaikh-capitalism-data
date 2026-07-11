---
decision_id: "0016"
title: "Static site/ Regenerated with Registry-driven Publish Filter, XS Scheme, No JSON (D-9)"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "F1 (Decision Annex D-9)"
gate0_ruling: "D-9"
related:
  - 0010_s1006_sbbi_publish_false_damodaran.md
affected_series:
  - S306
  - S307
  - S408
  - S703
  - S704
  - XS2304
  - XS2305
  - S1006
campaign_phases:
  - phase_F
---

# 0016 — Static site/ Regenerated with Registry-driven Publish Filter, XS Scheme, No JSON (D-9)

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: D-9 (campaign plan §2 Decision Annex §7; CAMPAIGN_STATE.json `gate0_ratified.rulings["D-9"]`).

## Context

Decision Annex item **D-9**. The static `site/` surface predates the XS migration and the publish/triage
flags: it copies `chopped/*` wholesale (no publish filter, so it re-leaks the 7 `publish:false` series),
still carries the legacy AS/ES scheme and stale "v12.0 / 109 series" copy, and offers six `.json` provenance
links (a Carson "no JSON" violation). The choice: retire the static site, or regenerate it honestly.

## Decision

**Regenerate the static `site/` (do not retire) with a registry-driven publish filter, the XS scheme,
dropped JSON links, and updated copy.** Verbatim ruling:

> Static site/: REGENERATE with registry-driven publish filter (not retire); drop JSON links; XS scheme;
> updated copy.

Operational specifics (ratified):
- **Regenerate**, don't retire — rebuild from the post-fix `Outputs/Publish/` via `build_static_site.py`.
- Add a **registry-driven publish filter** to the generator so it excludes all 7 `publish:false` series
  (S306, S307, S408, S703, S704, XS2304, XS2305) plus the S1006 SBBI columns (Decision 0010 / D-3).
- Carry the **XS scheme** (retire legacy AS/ES); update stale copy to current version/series counts.
- **Drop the six `.json` provenance links** (Carson: no JSON) in favor of CSV/PDF equivalents.

## Consequences

- **Phase F (F1)**: regenerate the static site; F1 gate = leak-grep clean (the 7 publish:false SIDs + "SBBI"),
  zero JSON links, XS-scheme series only, updated copy.
- Couples with Decision 0010 (D-3): the SBBI columns are among what the publish filter must exclude.
- **Phase F (F2/F3)**: the same publish-filtered registry drives the web export (`_Web_v1.1.0`) and the hub
  dataset (`anu-vizsite/datasets/rscd.json`); SITE_SPEC authored (F3). No concordance download page (RMWND's).
