# Knowledge Base Coverage Inventory

**Generated**: 2026-05-18 (Phase 0.C.2)
**Sources**: CD's `FIGURE_MASTER_v4.json`, `HDARP_SERIES_LINKAGE.json`, `CROSS_REFERENCE_INDEX.json`

## Per-chapter coverage (Shaikh 2016)

| Chapter | Total Figures | Empirical | Time-series candidates | Status |
|---|---|---|---|---|
| 1  | 0   | 0   | 0   | introduction (no empirical figures) |
| 2  | 19  | 19  | 18  | strong |
| 3  | 15  | 9   | 9   | strong |
| 4  | 24  | 8   | 8   | strong |
| 5  | 4   | 4   | 4   | strong |
| 6  | 7   | 7   | 4   | strong (profit-rate construction) |
| 7  | 8   | 8   | 8   | strong |
| 8  | 6   | 6   | 5   | strong |
| 9  | 22  | 17  | 3   | **weak** — most empirical figures lack axis metadata, downgraded to cross_sectional. Phase 3 needs to verify by reading the chapter directly. |
| 10 | 10  | 10  | 8   | strong |
| 11 | 4   | 4   | 4   | strong |
| 12 | 4   | 0   | 0   | theoretical chapter |
| 13 | 10  | 1   | 1   | mostly theoretical — only Fig13.x empirical |
| 14 | 8   | 8   | 8   | strong |
| 15 | 9   | 9   | 9   | strong |
| 16 | 6   | 6   | 6   | strong |
| 17 | 3   | 3   | 3   | strong (concluding empirical refs) |
| **Total** | **159** | **119** | **98** | |

## Coverage Assessment

**No further figure extraction required** for v1.0. The salvaged figure
extraction (`FIGURE_MASTER_v4.json` with 205 figures + per-chapter JSONs) is
comprehensive enough to seed Phase 3 research without re-running an extraction
campaign.

**Chapters needing manual verification in Phase 3**:

- **Ch9** — Microeconomic foundations / wage-profit curves. Most figures
  in FIGURE_MASTER lack `has_axis: true` metadata, so the classifier
  downgraded them. The chapter does contain real empirical content
  (industry-level scatter plots, the 1998 wage-profit curve dataset);
  Phase 3 may merge several Fig9.x figures into a smaller number of
  underlying series, OR confirm that the classifier was correct and most
  of Ch9 is illustrative (theoretical) rather than empirical.
- **Ch13** — Confirm whether the single empirical figure is genuinely the
  only one, or whether other Fig13.x figures should be reclassified.
- **Ch3** — 6 of 15 figures are non-empirical; verify the classification.

**Source-quality gaps** (chapters likely to need fresh data acquisition):

None identified at scaffold time. CD2's 114-series pipeline already proved
that every series has a workable modern API source (FRED, BEA, BLS, World
Bank, Maddison, MeasuringWorth). Phase 4 (Adequacy) will formalize this
per chapter.

## Reference paths

Figure-level metadata used to seed Phase 3 research is bundled in the
replication package under:

- `SalvagedInputs/figures_reference/` — figure-level metadata
  (`FIGURE_MASTER_v4.json`, `HDARP_SERIES_LINKAGE.json`,
  `CD_CROSS_REFERENCE_INDEX.json`)

Broader predecessor knowledge-base material (historical sources, equations,
methodology) lives outside this public bundle and is not required to reproduce
the series.
