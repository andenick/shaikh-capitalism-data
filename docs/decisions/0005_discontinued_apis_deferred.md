# 0005 — Discontinued API Substitutions (Deferred to Phase 4)

**Status**: DEFERRED to Phase 4 ADEQUACY (not a single up-front decision)
**Date opened**: 2026-05-18 (Phase 3 close, multiple subagents)
**Date deferred**: 2026-05-18

## Context

Several CD2-listed primary source APIs are discontinued, unstable, or have
schema changes that affect extension feasibility:

| Source | Issue | Affected series |
|---|---|---|
| BLS International Labor Comparisons (ILC) | Sunset 2013 | S207, S1102, S1103, S1104 |
| Ibbotson SBBI | Now Morningstar commercial license | S1006 |
| IMF IFS line numbering | Changed post-2009 SDDS+ migration | S1504, S1508, S1509 |
| OECD ISDB 1994 | Discontinued | S703, S704 |
| Christodoulopoulos 1995 raw data | Not publicly available | S703, S704, S705, S706 |
| anwarshaikhecon.org companion site | 2026 status uncertain | many series, all chapters |
| Tsoulfidis & Tsaliki (2011) Greek industry panels | Not in SalvagedInputs | S707, S708 |
| NBER macrohistory database | Reorganized; URLs moved | S210, S211 |

## Why deferred

These are **per-series adequacy questions**, not a single binding decision.
The Anu Framework rule (`.claude/rules/anu-framework.md` "No Proxies Without
Disclosure") requires that each substitution be flagged in the EPR with a
"Concept Match Justification" — that's Phase 6 work, not Phase 0/2 work.

Phase 4 (ADEQUACY) is where each chapter's adequacy report scores source
reachability per series and proposes substitutions. The user ratifies the
adequacy reports before Phase 5 begins.

## Action

No action now. Each Phase 4 chapter adequacy report will list the affected
series, propose a substitution (or flag as `data_unavailable` per the
no-synthetic-data rule), and request user ratification.

## Reference list of substitution candidates (for Phase 4 reviewers)

- **BLS ILC** → likely OECD Productivity (PDB.LV); concept-narrow (US-only, manufacturing only)
- **Ibbotson SBBI** → Damodaran NYU dataset (open, recommended) or Multpl.com
- **IMF IFS** → IFS WEO + IFS SDMX with code remap; or BIS Statistics
- **OECD ISDB** → OECD STAN (requires ISIC Rev3→Rev4 industry crosswalk)
- **Tsoulfidis & Tsaliki Greek panels** → BoG (Bank of Greece) industry statistics, or contact author
- **anwarshaikhecon.org** → host appendix datasets in `SalvagedInputs/book_data/` + cite Internet Archive snapshot

Some affected series may resolve as `cross_sectional` or `data_unavailable` in
the new content-type classification — no extension required.
