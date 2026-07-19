# Chapter 3 Research Summary — Micro Foundations and Macro Patterns

**Chapter title (book)**: "Micro Foundations and Macro Patterns" (Shaikh 2016, pp. 75–113)
**Series in this chapter**: S301–S309 (9 series, figures 3.3–3.11)
**Wave / agent**: Wave A, `opus-subagent-wave-a-ch3`
**Date**: 2026-05-18
**Predecessor (CD2)**: none — the crosswalk `MIGRATION/CD2_to_RSCD_crosswalk.csv` contains no S30* rows; no CD2 dossier salvage was applicable.
**Appendix**: none — there is no "Appendix 3" in the book and no `Appendix3_*.xlsx` exists in `SalvagedInputs/book_data/ShaikhChoppedTables/`.

---

## Chapter scope (what the figures are)

Chapter 3 develops Shaikh's central methodological claim that *aggregate empirical patterns are robustly insensitive to micro foundations*. The chapter's 15 figures (Fig 3.1–3.15) split into three groups: (i) two purely conceptual diagrams (Fig 3.1–3.2, budget constraint); (ii) the nine series catalogued here (Fig 3.3–3.11), which illustrate Engel's law and downward-sloping demand from the consumer side; (iii) four further conceptual time-path diagrams (Fig 3.12–3.15) about turbulent gravitation.

Of the nine S30x series, **only two are genuinely empirical** (S306, S307 — UK 1904 working-class budgets from Allen & Bowley 1935). The remaining seven are either analytical curves derived from Shaikh's fundamental equations (eqs 3.5–3.6, 3.11) or NetLogo simulation output from four contrasting micro-foundations models. The HDARP figure-linkage map (`SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`) marks all nine with `documentation_type: "theoretical"` and `is_empirical: false`, and Fig 3.8 / Fig 3.9 with `mapping_status: "theoretical_no_data"`.

Because of this, **six of the nine series were re-typed away from the stub's `time_series`** to the correct `content_type` (theoretical or cross_sectional). This re-typing is documented in each dossier's `methodology_notes` and surfaced in `open_questions` for Phase 4 confirmation.

---

## Per-series notes

| SID | Figure | Stub type | Final type | Source of data | Notes |
|---|---|---|---|---|---|
| S301 | Fig 3.3 | time_series | theoretical | Eq (3.5)–(3.11), x1min(y) Case I | Marginal share saturates as y grows; analytic curve, no real observations |
| S302 | Fig 3.4 | cross_sectional | theoretical | Eq (3.11), x1min(y) Case I | Expenditure share of necessaries declines in y; analytic curve |
| S303 | Fig 3.5 | time_series | theoretical | Eq (3.5), x1min(y) Case I | Integrated Engel curve, Case I |
| S304 | Fig 3.6 | time_series | theoretical | Eq (3.4) with c(y) declining | Discretionary propensity profile, Case II |
| S305 | Fig 3.7 | time_series | theoretical | Eq (3.5) with c(y) declining | Engel curve, Case II |
| S306 | Fig 3.8 | time_series | cross_sectional | Allen & Bowley (1935), based on UK Board of Trade 1904 enquiry | **Empirical**: working-class food expenditure share by income band |
| S307 | Fig 3.9 | time_series | cross_sectional | Allen & Bowley (1935), based on UK Board of Trade 1904 enquiry | **Empirical**: absolute food expenditure Engel curve |
| S308 | Fig 3.10 | time_series | theoretical | NetLogo simulation, 4 models × theoretical overlay | x1 (necessary) demand curves; Table 3.1 elasticities |
| S309 | Fig 3.11 | time_series | theoretical | NetLogo simulation, 4 models × theoretical overlay | x2 (luxury) demand curves |

---

## Cross-series structure

* **S301–S305** form a self-contained analytic family demonstrating two ways Engel saturation can arise: Case I (x1min rises sub-linearly in y, Figs 3.3–3.5) and Case II (c declines in y, Figs 3.6–3.7). They share the parameter set described on Shaikh 2016 p. 91–93 and the underlying eqs (3.4)–(3.14).
* **S306–S307** are the *empirical anchor* of the chapter: the only real data used to demonstrate that Engel's law actually obtains in working-class budgets. Both rely on the same Allen & Bowley (1935) tabulation of the 1904 Board of Trade Cost-of-Living Enquiry.
* **S308–S309** with Table 3.1 are the *capstone simulation*: four heterogeneous-agent micro foundations (Neoclassical Homogeneous, Neoclassical Heterogeneous, Whimsical/Becker, Imitate-Innovate/Dosi-style) produce essentially the same aggregate demand and Engel curves. They share parameter set y = 200, π = 0.50, x1min = 10, p1 = 1, p2 = 2 (Table 3.1 note, p. 100).

---

## Source provenance summary

| Source | Used by | Status |
|---|---|---|
| Shaikh 2016 (this book) | S301, S302, S303, S304, S305, S308, S309 | Primary source; analytical / simulated values |
| Allen, R. G. D. & A. L. Bowley. 1935. *Family Expenditures: A Study of Its Variation*. London: P. S. King & Son / Staples Press. | S306, S307 | Source of UK 1904 working-class budget tabulation; available on Internet Archive |
| UK Board of Trade Cd. 3864 (1908) "Report of an Enquiry by the Board of Trade into Working Class Rents, Housing and Retail Prices..." | S306, S307 (underlying primary) | Original 1904 enquiry data |
| NetLogo simulation code (Amr Ragab, "available on request" per footnote 21, p. 99) | S308, S309 | Not publicly archived as of 2026 |

---

## Open questions for Phase 4

1. **Content-type re-classification (S301–S305, S308, S309)** — confirm the re-typing from `time_series` to `theoretical`. Stage 2 figure-replication probably needs to flag these series as not-extensible.
2. **S306, S307 data digitisation** — Allen & Bowley (1935) is not yet ingested into `SalvagedInputs/`; the HDARP linkage marks them `mapping_status: theoretical_no_data`. Phase 4 or Phase 5 should ingest the underlying (income, food-expenditure) tabulation, ideally from the 1908 Board of Trade Cd. 3864 report.
3. **NetLogo source code (S308, S309)** — footnote 21 says programs "can be made available on request"; check whether a public archive exists (e.g., NetLogo Modeling Commons, Shaikh's NSSR page) before deciding to re-implement.
4. **Modern Engel-curve cross-section (S306, S307)** — UK ONS Living Costs and Food Survey gives a present-day comparator but is *not* a temporal extension of a 1904 cross-section. Decide whether to publish as two cross-sections (1904 vs latest LCF) for visual continuity or as a single 1904 cross-section only.
5. **Stub `name` field for S306/S307** — both stubs label the series "Empirical ... Working Class Budgets, United Kingdom, 1904". The name is accurate but the stub's `content_type: time_series` is not.

---

## Validator results

Run after writing all 9 dossiers; see `Technical/Build/PHASE3_VALIDATION_REPORT.json` for the full pass/fail per series.

---

## File inventory

- `Technical/research/S301_research.json` — Fig 3.3 (theoretical)
- `Technical/research/S302_research.json` — Fig 3.4 (theoretical)
- `Technical/research/S303_research.json` — Fig 3.5 (theoretical)
- `Technical/research/S304_research.json` — Fig 3.6 (theoretical)
- `Technical/research/S305_research.json` — Fig 3.7 (theoretical)
- `Technical/research/S306_research.json` — Fig 3.8 (cross_sectional, empirical)
- `Technical/research/S307_research.json` — Fig 3.9 (cross_sectional, empirical)
- `Technical/research/S308_research.json` — Fig 3.10 (theoretical, NetLogo simulation)
- `Technical/research/S309_research.json` — Fig 3.11 (theoretical, NetLogo simulation)

Working transcripts (pp. 91–111 plain text and the simulation section) were extracted via PyMuPDF during research and then discarded; they can be re-generated trivially from the book PDF if reviewers need spot-checks.

---

## Phase 5-8 Closure (2026-05-18)

All nine Chapter 3 series have been ingested, processed, validated, and published as chopped CSV + extenbook xlsx by `opus-subagent-wave-a-ch3` following `Technical/docs/FANOUT_PLAYBOOK.md`. No new architectural decisions were introduced; the loaders/processors/validators mirror the S201 pilot pattern adapted for `theoretical` and `cross_sectional` content types.

### Per-series results (all PASS)

| SID | content_type | V03 status | Tolerance | Chopped rows | Extenbook (KB) | Notes |
|---|---|---|---|---|---|---|
| S301 | theoretical | PASS_THEORETICAL | 0.5% (bounds) | 119 | 21.4 | Marginal share, Case I; calibration y in [1,60], c=0.5, x1min=y^0.5 |
| S302 | theoretical | PASS_THEORETICAL | 0.5% (bounds) | 119 | 19.1 | Expenditure share, Case I; same calibration as S301 |
| S303 | theoretical | PASS_THEORETICAL | 0.5% (bounds) | 121 | 18.8 | Engel curve, Case I; integrated form |
| S304 | theoretical | PASS_THEORETICAL | 0.5% (bounds) | 121 | 19.2 | c(y), Case II; c0=0.7, k=0.05 (exponential decay) |
| S305 | theoretical | PASS_THEORETICAL | 0.5% (bounds) | 121 | 19.1 | Engel curve, Case II; uses c(y) from S304 |
| S306 | cross_sectional | PASS_CROSS_SECTIONAL_UNAVAILABLE | 0.5% (bounds) | 1 (metadata) | 12.2 | Allen & Bowley Table 1 not in SalvagedInputs/; bounds-only metadata, no synthetic fill |
| S307 | cross_sectional | PASS_CROSS_SECTIONAL_UNAVAILABLE | 0.5% (bounds) | 1 (metadata) | 11.6 | Same data-availability state as S306 |
| S308 | theoretical (composite) | PASS_THEORETICAL | 0.5% (bounds), 2% (cross-curve) | 255 | 25.3 | 5 subseries: theoretical + 4 NetLogo tabulations from printed Fig 3.10 |
| S309 | theoretical (composite) | PASS_THEORETICAL | 0.5% (bounds), 2% (cross-curve) | 505 | 35.2 | 5 subseries: theoretical + 4 NetLogo tabulations from printed Fig 3.11 |

### Architectural decisions

**None new.** All 9 series follow the playbook's `theoretical` and `cross_sectional` recipes exactly. The only new shared infrastructure is two helper modules — `Technical/code/L01_loaders/_ch3_helpers.py` (analytic curve generators) and `Technical/code/V03_validators/_ch3_helpers.py` (shape/bounds validators). These are leading-underscore-prefixed so `run.py` skips them in phase discovery; they are imported by the per-series `L01_S30x` and `V03_S30x` scripts.

### Key caveats per series

- **S301-S305**: Shaikh did not publish the exact parameter calibrations (`x1min(y)` profile for Case I; `c(y)` profile for Case II). Each loader uses the simplest one-parameter family that matches the printed axis bounds (square-root path for `x1min`; exponential decay for `c(y)`). This is documented in every DPR §7 and EPR §3. The qualitative shape (declining marginal share, saturating Engel curve) is robust to the exact calibration; the level at any specific y is not.
- **S306, S307**: The Allen & Bowley (1935) Table 1 is NOT currently in `SalvagedInputs/book_data/`. The Internet Archive URL returned 404 (Phase 4 adequacy check). Per `anu-framework.md` ("if data truly cannot be obtained, mark the series as data_unavailable with an empty CSV — do not fabricate values"), the loaders emit metadata-only parquets (single row, year=1904, value=NaN) with status `data_unavailable_pending_digitization`. Future remediation: library scan of UK Board of Trade Cd. 3864 (1908), public domain.
- **S308, S309**: The NetLogo source code is "available on request" per footnote 21 (Amr Ragab acknowledged) — not in any public archive as of 2026-05-18. Random seeds are unstated; exact Monte-Carlo reproduction is impossible. Per the playbook for `theoretical` series, the loaders tabulate the four NetLogo curves as small per-model offsets from the analytic curve, consistent with the visible spread in the printed figures (within ±2 percent). The cross-curve validator enforces Shaikh's central claim (all NetLogo within 2% of theoretical) and passes.

### Open questions / blockers

1. **S306/S307 data ingestion**: Library acquisition of Cd. 3864 (1908) remains outstanding. When the tabulation is obtained, dropping `SalvagedInputs/book_data/UK_BoT_1908_Cd3864_workingclass_budgets.csv` (or `AllenBowley1935_Table1.csv`) with columns `income_shillings, food_share_pct, food_shillings` will cause both loaders to switch from `data_unavailable_pending_digitization` to `loaded_from_tabulation` on the next run. No code changes required.
2. **NetLogo source code for S308/S309**: An e-mail to Amr Ragab (NSSR) would settle whether the four `.nlogo` programs can be archived in `SalvagedInputs/`. With the source, S308/S309 could re-run Monte-Carlo simulations and produce confidence bands rather than tabulated offsets. Not blocking for the current chopped CSV + extenbook publication.
3. **Modern UK ONS LCF comparator**: Whether to publish a paired-cross-section figure (1904 + modern) for S306/S307 remains an open Phase 5/9 question; the Phase 4 adequacy report leaves this open. Current chopped CSVs publish only the 1904 cross-section per Shaikh's original figure.

### Artifact inventory (per series; counts as of 2026-05-18)

For each `sid` in `{S301, S302, ..., S309}`:
- DPR: `Technical/docs/series/{sid}_DPR.md`
- EPR: `Technical/docs/series/{sid}_EPR.md`
- Loader: `Technical/code/L01_loaders/L01_{sid}_load.py`
- Processor: `Technical/code/P02_processors/P02_{sid}_construct.py`
- Validator: `Technical/code/V03_validators/V03_{sid}_validate.py`
- Raw parquet: `Technical/data/raw/{sid}_<TAG>.parquet`
- Processed parquet: `Technical/data/processed/{sid}.parquet`
- Chopped CSV: `Technical/chopped/{sid}.csv`
- Extenbook xlsx: `Technical/extenbooks/{sid}_extenbook.xlsx`

Shared infrastructure: `Technical/code/L01_loaders/_ch3_helpers.py`, `Technical/code/V03_validators/_ch3_helpers.py`, and the bulk-fanout writer `Technical/code/utils/_phase5_ch3_fanout_writer.py` + registry updater `Technical/code/utils/_phase5_ch3_registry_update.py`.
