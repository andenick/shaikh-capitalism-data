# SalvagedInputs Manifest

Curated subset of CD and CD2 material pulled forward into RSCD's clean rebuild.
Every file here was deemed irreplaceable, a validation benchmark, or a
decision-context anchor that the active pipeline references.

Frozen legacy lives at `Inputs/Capitalism Data/` and `Inputs/CD2/` (write-denied).
Active pipeline reads from this `SalvagedInputs/` tree only — never directly
from `Inputs/`.

**Location note**: Per RMWND convention this should be at `Inputs/Salvaged/`,
but the project-wide `Write(Inputs/**)` deny rule in `.claude/settings.json`
forces it to live at the root as `SalvagedInputs/`. Functionally identical.

---

## `book_data/` — Shaikh's published values (ground truth)

| Source | Files | Used for |
|---|---|---|
| `book_data/ShaikhChoppedTables/` (73 files, 1.7 MB) | CSV + Excel of every appendix table Shaikh published | V03 validators compare extension output against these |

These are extracted from CD's `Inputs/ShaikhChoppedTables/`. They are the
definitive "this is what the book says" values for every series in the registry.

---

## `extension_benchmarks/` — CD/CD2 final outputs as validation truth

| Source | Files | Used for |
|---|---|---|
| `extension_benchmarks/CD_v_latest/` | `capitalism_data_1790_2025.csv` + 3 metadata files | CD's final consolidated database — compare RSCD output for regression |
| `extension_benchmarks/CD2_v1.3/` (6 root + 99 series = 105 files, ~1.1 MB) | CD2's published Drive package | CD2's per-series CSVs — compare RSCD per-series against CD2's per-series |

Any divergence from these benchmarks must be documented in
`Technical/MIGRATION/divergences_from_CD2.md` (P6+) with rationale.

---

## `figures_reference/` — HDARP figure metadata

| File | Provenance | Used for |
|---|---|---|
| `FIGURE_MASTER_v4.json` | CD's HDARP v4.2 (205 figures from book + supplement) | Figure inventory; source for `docs/chapters/CHAPTER_FIGURE_TABLE_INDEX.json` |
| `HDARP_SERIES_LINKAGE.json` | CD 2026-01-05 build | Figure → series mapping; source for `SERIES_CANDIDATE_LIST.json` grouping |
| `CD_CROSS_REFERENCE_INDEX.json` | CD HDARP Integration | Cross-reference lookup for entities/equations/tables |
| `CD_HDARP_EXTENBOOK_INTEGRATION.json` | CD's chapter-Extenbook mapping | Reference for Phase 8 extenbook authoring |

The 205 figures (159 empirical, ~46 conceptual) are the universe from which
the 98 RSCD series candidates were derived. Phase 3 research may add/remove
candidates by reading the book text directly.

---

## `methodology_decisions/` — Salvaged decision context

| File | Used for |
|---|---|
| `CD2_series_registry_v2.0.json` | CD2's final 114-series registry — schema reference for `Technical/series_registry.json`; provides series names, subseries decomposition, source URLs that Phase 3 can mine |

(More decision logs may be added during Phase 3 as research identifies
methodology questions that CD2 already resolved.)

---

## Discipline

- Anything pulled forward stages here first, never read directly from `Inputs/`.
- Per-file provenance: filename prefix (`CD_*`, `CD2_*`) or directory path
  (`CD_v_latest/`, `CD2_v1.3/`) makes the source unambiguous.
- This MANIFEST is updated every time a file is added; keep the table in sync
  with the actual contents.
