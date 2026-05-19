# Series ID Prefix Scheme

**Project**: RSCD — Shaikh (2016) Replication
**Convention**: Anu Framework v12.0, RMWND-compatible

This document is the binding spec for series identifiers. Every series in
`series_registry.json` MUST follow exactly one of the three patterns below.
Validators reject any ID that does not match.

---

## `S###` — Book Series

**Meaning**: Empirical data series that appears in Anwar Shaikh, *Capitalism: Competition, Conflict, Crises* (Oxford University Press, 2016). One series ≈ one underlying data construct, even if it appears in multiple figures or tables.

**Pattern**: `S{chapter}{seq}` where
- `{chapter}` = the 1- or 2-digit dominant chapter number (1–17). When a series spans chapters, use the chapter of its primary construction.
- `{seq}` = a 2-digit sequence within that chapter, starting at `01`.

**Examples**:
- `S201` — Chapter 2, series 01 (e.g., US Industrial Production Index, Fig 2.1)
- `S207` — Chapter 2, series 07
- `S1601` — Chapter 16, series 01
- `S503` — Chapter 5, series 03

**Capacity**: 99 series per chapter (more than the book ever uses).

**Migration note**: CD used flat `S001–S105` (no chapter info in ID). CD2 used flat `S001–S113`. RSCD's new IDs encode chapter, so a CD2 `S047` (a Chapter 6 series) becomes e.g. `S605` in RSCD. The crosswalk is at `MIGRATION/CD2_to_RSCD_crosswalk.csv`.

---

## `ES####` — External-Study Replication

**Meaning**: A series from a Shaikh-adjacent follow-up paper, replication study, or related empirical literature that the project chose to replicate alongside the book. Not in the book itself.

**Pattern**: `ES{group}{seq}` where
- `{group}` = 2-digit group code (one per source paper or study)
- `{seq}` = 2-digit sequence within the group

**Group codes** (frozen for v1.0 — see `docs/decisions/0001_external_study_scope.md`):

| Code | Study | v1.0 status |
|---|---|---|
| `10–17` | _reserved_ to avoid visual collision with chapter codes 10–17 (S{chapter}{seq} pattern) | unused |
| `20` | Shaikh (2020) — An Empirically Sufficient Form for Sraffa Prices | **IN SCOPE** |
| `21` | Shaikh, Coronado, Nassif-Pires (2020) — On the empirical regularities of Sraffa prices | **IN SCOPE** |
| `22` | Shaikh & Jacobo (2020) — Economic Arbitrage and the Econophysics of Income Inequality | **IN SCOPE** |
| `23` | Weber & Shaikh (2020) — The U.S.-China trade imbalance and the theory of free trade | **IN SCOPE** |

**Why codes 20+ instead of 10–17**: chapter numbers in the S prefix go up to 17 (`S1701`, `S1702`, `S1703` are Ch17 series). Reusing codes 10–17 for ES groups would visually collide (`ES1701` vs `S1701` — different prefixes but same trailing digits). Using ES codes ≥20 makes the two prefix families unambiguous at a glance. This diverges from RMWND's convention (RMWND uses ES10–17) but matches RSCD's chapter-encoded S scheme better.

**Examples**:
- `ES1301` — Shaikh 2020 Sraffa prices, series 01
- `ES1602` — Weber & Shaikh 2020, series 02

---

## `AS###` — Analytical / Framework-Derived

**Meaning**: A series that does not appear in any single source but is constructed by the project from one or more `S###`/`ES####` inputs to support cross-chapter analysis. Examples: aggregate profit decomposition, weighted productivity index, framework-derived shares.

**Pattern**: `AS{seq}` where `{seq}` is a 3-digit sequence starting at `001`.

**Examples**:
- `AS001` — Aggregate profit rate (national, Marxian)
- `AS002` — Composite productivity index across chapters 3–7

**Rule**: Every AS series must list its input series in `series_registry.json` under `"components": [...]`. The `construction` field MUST be `"formula"` or `"composite"`, never `"direct"`.

---

## Forbidden Patterns

The following IDs are explicitly invalid:
- Flat `S001–S999` (no chapter encoded) — CD/CD2 convention, **not** RSCD
- `T###` or `N###` — RMWND's pre-migration ST2 convention
- IDs containing spaces, lowercase letters, or hyphens
- Leading zeros that would produce ambiguous chapter numbers (e.g., `S0201` is invalid; chapter 2 series 01 is `S201`)

---

## Validator

`code/utils/id_validator.py` (to be authored in Phase 7) provides:
```python
def validate_series_id(sid: str) -> tuple[bool, str]:
    """Return (is_valid, reason)."""
```

It is called by every L01/P02/V03/O06 script as the first action on its `run()` entry point.

---

## Open Questions

1. **External study scope** — final decision deferred to `docs/decisions/0001_external_study_scope.md`. May leave ES blocks unpopulated for v1.0.
2. **Sub-chapter granularity** — book has appendices (e.g., 5.A, 5.B). Treat appendix series as belonging to the parent chapter (`S5XX`), with `book_table` field disambiguating.
3. **Chapter 17 special-casing** — the book's concluding chapter has no original empirical series; only re-uses earlier ones. RSCD will not assign new IDs for re-use, but the registry's `figures` field for existing series will include Chapter 17 figure refs.
