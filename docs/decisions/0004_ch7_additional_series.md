# 0004 — Add Ch7 Series S709–S711

**Status**: CLOSED
**Date opened**: 2026-05-18 (Phase 3 Ch7 subagent finding)
**Date closed**: 2026-05-18
**Decided by**: user

## Context

The Phase 2 builder grouped Ch7 into 8 series candidates (S701–S708). Phase 3
subagent found that 3 Ch7 figures (7.16, 7.18, 7.21) had CD2 ancestors
(S035, S037, S038) but were not represented in the candidate list.

## Decision

**Add 3 series: S709, S710, S711.**

| New ID | Figure | CD2 ancestor | Topic |
|---|---|---|---|
| S709 | Fig 7.16 | S035 | US ROP deviations from average |
| S710 | Fig 7.18 | S037 | US IROP deviations from average |
| S711 | Fig 7.21 | S038 | OECD IROP deviations from average |

## Rationale (user-confirmed)

CD2 already did the research; porting is ~1 hour. Completes Ch7 coverage so
the reader of the v1.0 viz doesn't notice Fig 7.16/18/21 having no companion
data. Three additional series is a small marginal effort.

## Consequences

- Ch7 series count: 8 → 11
- Total RSCD series: 98 → 98 + 3 = 101 (before AS and ES additions)
- 3 new stubs + 3 new dossiers in next Phase 3 wave
