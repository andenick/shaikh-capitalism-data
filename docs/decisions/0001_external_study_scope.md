# 0001 — External Study Scope for RSCD v1.0

**Status**: CLOSED
**Date opened**: 2026-05-18 (Phase 2 close)
**Date closed**: 2026-05-18 (Phase 3 close)
**Decided by**: user

## Decision

**Option B — Book + 4 Shaikh successor papers**.

v1.0 ships with:
- 98 Shaikh 2016 series (S###)
- 9 Ch6 GPIM analytical-support series (AS001–AS009) — see decision 0002
- 3 additional Ch7 series (S709–S711) — see decision 0004
- ~N ES series across 4 Shaikh-adjacent 2020 papers (group codes 20–23)

ES group code assignments (codes 20+ instead of RMWND's 10–17 to avoid visual collision with chapter numbers in S{chapter}{seq}):

| Group | Paper | PDF |
|---|---|---|
| 20 | Shaikh (2020) — An Empirically Sufficient Form for Sraffa Prices | `Inputs/Capitalism Data/Technical/data/raw/01_SOURCE_MATERIALS/Web Folders/Shaikh Publications/[2020] Shaikh - An Empirically Sufficient Form for Sraffa Prices.pdf` |
| 21 | Shaikh, Coronado, Nassif-Pires (2020) — On the empirical regularities of Sraffa prices | `... /[2020] Shaikh Coronado & Nassif-Pires - On the empirical regularities of Sraffa prices.pdf` |
| 22 | Shaikh & Jacobo (2020) — Economic Arbitrage and the Econophysics of Income Inequality | `... /[2020] Shaikh & Jacobo - Economic Arbitrage and the Econophysics of Income Inequality.pdf` |
| 23 | Weber & Shaikh (2020) — The U.S.-China trade imbalance | `... /[2020] Weber & Shaikh - The U.S.-China trade imbalance ...pdf` |

## Consequences

- `Technical/series_registry.json` gains placeholder ES2001, ES2101, ES2201, ES2301 entries (status: `needs_decomposition`); next Phase 3 wave expands each paper to N series.
- `PREFIX_SCHEME.md` updated with codes 20–23 and the chapter-collision rationale.
- `external_study_groups` block in registry populated.
- Effort impact: ~30–50 hours added across Phases 3–7 (~12–16 additional series, 4 paper PDFs to mine).

## Rationale (user-confirmed)

Demonstrates the ES infrastructure, gives v1.0 a "Shaikh research family" angle, and the 4 papers are tightly tied to Ch9, Ch11, Ch15, Ch17 of the book — so their replication enriches the book's empirical content.
