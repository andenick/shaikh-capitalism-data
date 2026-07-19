---
decision_id: "0018"
title: "Tier-5 S703/S704 Guided Digitization Scheduled as Separate User-gated Session; Proxies Forbidden"
status: approved
proposed_at: "2026-07-01T00:00:00Z"
approved_at: "2026-07-01T00:00:00Z"
decided_by: user
ratification: "Gate-0, RSCD v1.5 Skeptical Review & Remediation campaign"
backlog_item: "Tier-5 (S703/S704)"
gate0_ruling: "T5-S703-S704"
related:
  - 0005_discontinued_apis_deferred.md
affected_series:
  - S703
  - S704
campaign_phases:
  - post_phase_E
---

# 0018 — Tier-5 S703/S704 Guided Digitization Scheduled as Separate User-gated Session; Proxies Forbidden

**Status**: ACCEPTED — user ratified at Gate-0, 2026-07-01. **SUPERSEDED-IN-PART by Decision 0019
(2026-07-02):** machine digitization of the S703/S704 aggregate lines was subsequently authorized
by the user and executed (both series recovered to `book_period_validated`, `publish: true`). This
decision's **no-proxy prohibition survives untouched**, and a guided human digitization filed to
`returns/` remains a permanent **superseding** path. Only the "human-pass-only, deferred" scheduling
reservation is relaxed. See `0019_machine_digitization_s703_s704.md`.
**Decided by**: user (Gate-0 ratification of the RSCD v1.5 campaign Decision Gate 0).
**Ruling ID**: Tier-5 standing ruling (campaign plan §2 / §7; CAMPAIGN_STATE.json `gate0_ratified.rulings["T5-S703-S704"]`).

## Context

Tier-5 backlog. Series **S703** and **S704** (Christodoulopoulos Fig 7.13/7.14) remain `status:
data_unavailable` — the source is a 9-line spaghetti figure requiring **guided WebPlotDigitizer** of the
aggregate line (a human-in-the-loop browser packet). The other 7 originally-unavailable series were recovered
by figure digitization on 2026-05-26; S703/S704 are the last blockers to 118/118. Per project CLAUDE.md
anti-pattern #5 and the Anu no-synthetic-data / no-proxies rules, these must NOT be filled with proxies.

## Decision

**Schedule S703/S704 guided digitization as a separate, user-gated session after Phase E; never proxy them.**
Verbatim ruling:

> Guided digitization scheduled as separate user-gated session after Phase E; never proxied.

Operational specifics (ratified):
- Guided digitization of the S703/S704 aggregate line = a **separate user-driven, human-in-the-loop session**
  (browser packet / WebPlotDigitizer), scheduled **after Phase E**.
- **Proxies are forbidden** — S703/S704 stay `data_unavailable` (empty CSV, `publish:false`) until the guided
  digitization lands real values. No substitute/proxy series may stand in.

## Consequences

- **Not executed within this campaign's automated phases** — it is explicitly a §6 "leave for a later
  session" item, gated on the user.
- S703/S704 remain `status: data_unavailable`, `publish: false` through Phases A–H; the static-site /
  web-export publish filter (Decision 0016 / D-9) excludes them.
- This is the last blocker to 118/118; closing it is a post-campaign, user-scheduled activity.
