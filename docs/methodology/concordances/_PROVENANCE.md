# Concordance Seed Tables — Provenance & Known Limits

**RSCD Phase-3 concordance-synthesis stage** for the replication of Shaikh, *Capitalism* (2016).
Companion to the three seed CSVs in this folder and to `../CONCORDANCE_COMPENDIUM.md`.

- **Compiled:** 2026-06-30 (RSCD Phase-3 concordance-synthesis agent)
- **Aggregated from:** `_sources/SOURCES.md` + `_sources/naics/` (14 official Census bridges),
  `../_timelines/{IO,NIPA}_CHANGE_TIMELINE.md`, all 16 `methodology_review/CH*_methodology.json`
  `concordance_touch` records, the ch7/ch8/ch9 methodology histories, and
  `replicator/inputs_bundled/SalvagedInputs/book_data/Reconstructed/Shaikh_2008_Appendix_B_industries.csv`.
- **Method:** synthesis + direct derivation from the staged official Census CSVs (no re-fetch, no fabrication).
- **Golden rule (from the timelines):** concordances are **never** applied inside the book period — the book
  period is reproduced *historically* on its own frozen classification. A crosswalk is only ever exercised
  when a series is **extended** past its book period onto a live modern classification.

---

## `rscd_series_classification_map.csv`

- **Rows:** 65 — one per (series, classification-system) touch across all 16 chapters.
- **Header:** `sid, chapter, classification_system, industry_scheme_detail,
  needs_crosswalk_for_extension, official_source_table`.
- **Source:** the `concordance_touch` field of every `methodology_review/CH*_methodology.json`,
  cross-checked against the ch7/ch8/ch9 methodology histories and the two Phase-0 timelines.
- **`needs_crosswalk_for_extension = TRUE`** is reserved for series whose *extension* requires an
  **industry / IO-order / NIPA-line classification crosswalk** (SIC↔NAICS, ISIC Rev3↔Rev4, BEA
  IO 71/65-order, or a T7.11 line-label vintage resolve). **31 of the 65 rows are TRUE.**
- **`needs_crosswalk_for_extension = FALSE`** covers three distinct non-industry cases that are *also*
  concordance touches but are **not** industry crosswalks: (a) within-agency **source-code remaps**
  (BLS WPI→PPI / WPS→WPU, IMF IFS→SDMX, Fed legacy-DDP→FRED, FRED concept fixes) — these are id
  migrations, not classification bridges; (b) **country/base rebases** (Maddison 1990-GK→2011-PPP,
  ISO3 country-codes, HS trade-code revisions); (c) **frozen/irrecoverable walls** where no crosswalk
  is *possible* (pre-SIC Salter, UK SIC-1958 row label, Greek ISIC→NACE figure-recovery, Bain-1935
  pre-SIC-precursor). These are recorded so the map is exhaustive, not because they unblock an extension.
- **Known limits:** the map is at series granularity; a few series carry *multiple* touch types
  (e.g. ch6 combines a T7.11 line-label resolve with an FA legal-form split) — the `industry_scheme_detail`
  column names the dominant one and mentions the rest. "Inherited" touches (a formula series depending on
  another series' concordance) are marked TRUE when the parent's crosswalk propagates.

## `sic_naics_bridge_seed.csv`

- **Rows:** 24 — the RSCD-relevant industries actually used by ch7 (the 30/31-industry panel),
  ch8 (SIC-era manufacturing concentration), and ch9 (IO orders).
- **Header:** `naics_1997_3digit, rscd_industry_label, rscd_chapters_using_it,
  corresponding_1987_sic_2digit_divisions, is_many_to_many, note_and_source`.
- **DERIVED DIRECTLY** from the official Census reverse bridge
  `_sources/naics/1997_NAICS_to_1987_SIC.csv` (US Census, retrieved 2026-06-30): for each RSCD NAICS
  3-digit industry, the seed lists the **distinct 1987-SIC 2-digit divisions** that map into it. The NAICS
  3-digit industry list itself is anchored to the project's ch7 stability table
  `Inputs/Capitalism Data/Technical/Divergence_Reports/ADR-005_NAICS/data/naics_concordance_master.csv`
  and the Appendix-B exclusion key. The forward bridge `1987_SIC_to_1997_NAICS.csv` was consulted to
  confirm 1-SIC→N-NAICS multiplicity.
- **Known limits — MANY-TO-MANY is the headline:** **19 of 24 rows** draw a single NAICS 3-digit
  industry from **more than one** 1987 SIC 2-digit division (NAICS 541 professional services spans
  **15** SIC divisions; NAICS 336 transportation equipment spans 8). This is a **sector-level**
  correspondence table, **not** a bijective crosswalk — it cannot be used to mechanically re-map a
  Shaikh SIC-era value onto a NAICS industry without a share-based allocation. The seed deliberately
  stops at the 2-digit-division level; the underlying 4-6-digit rows in the Census file are even more
  fragmented. **5 rows** look one-to-one at the 2-digit division level (air/rail/water transport,
  management, hospitals) but remain many-to-many below 4 digits.
- **Not fabricated:** every `corresponding_1987_sic_2digit_divisions` value is a set actually present in
  the Census CSV for that NAICS prefix.

## `io_benchmark_industry_seed.csv`

- **Rows:** 13 — the ch9 benchmark cross-sections (Ochoa 71-order 1947–1972; BEA 65-order 1997) plus
  the SIC→NAICS wall years and the ch7 NAICS-native / ISIC international panels.
- **Header:** `benchmark_year, classification_system, industry_order, rscd_series_using_it, notes`.
- **Source:** `../_timelines/IO_CHANGE_TIMELINE.md` (benchmark-year table, web-verified against bea.gov)
  + the ch9 `concordance_touch` records. BEA I-O↔NAICS concordances are cited by their SCB-PDF-appendix
  URL (SCB Dec 2002 / Oct 2007 / Aug 2018) as recorded in `_sources/SOURCES.md`.
- **Known limits:** the BEA I-O↔SIC/NAICS concordances themselves are **NOT staged as CSV** — they live
  in SCB PDF appendix tables (URLs only). The Ochoa-71 (SIC) and BEA-65 (NAICS) orders are **not
  conformable**; each benchmark year is a frozen cross-section and the 1972→1998 gap is not
  reconstructable as a continuous panel (CH9 open-Q3). No 1947–1992 SIC-era **I-O code** concordance
  is staged. The 1997 benchmark **capital-flow matrix** is the last one BEA produced (discontinued
  after 1997), a structural obstacle to any post-1998 fixed-capital extension (CH9 open-Q4).

## `concordance_edges.csv` — SI-2 P2 (added 2026-07-02, FU-2)

- **Rows:** 19,607 directed edges — the universal edge list (CONCORDANCE_BUILD_SPEC.md
  Sec 2.1), materializing all 14 official Census SIC↔NAICS + NAICS-revision-chain CSVs.
  md5 `4f08d85f9665a7e5158e781883a825fa`.
- **Generator:** `../../../remediation_campaign/scripts/build_concordance_edges.py`
  (deterministic + idempotent: reruns reproduce the CSV byte-for-byte).
- **Columns (15):** `concordance_id, from_scheme, from_code, from_title, to_scheme,
  to_code, to_title, part_indicator, cardinality, allocation_weight, source_file,
  source_url, retrieval_date, confidence, notes`.
- **Codes** are strings with leading zeros preserved (SIC `0111`, `01`).
- **`cardinality`** is DERIVED COMPUTATIONALLY from the directed edge multiset, NOT from
  the bold/italic typography (which did not survive the Excel→CSV export, per
  `_sources/SOURCES.md`): a from_code with >1 to_code = split (`1:N`); a to_code fed by
  >1 from_code = merge (`N:1`); both = `N:N`; neither = `1:1`. Per-direction 1:N/N:1
  counts are exact mirror-images of the reverse file — the correctness sanity check.
- **`part_indicator`** = the genuine Census "Part Indicator" cell (`*` etc.) where the
  source file carries such a column (the two 1997-chain bridges); `""` elsewhere.
- **`allocation_weight` is EMPTY on every edge, by design.** The Census files carry no
  economic-share weights; weights must never be fabricated (build-spec Sec 2.1 / Sec 3).
  A share-based reallocation of a Shaikh SIC-era value onto a NAICS industry therefore
  still requires external economic-share data — see the many-to-many caveat under
  `sic_naics_bridge_seed.csv` above. Documented in each row's `notes`.
- **`confidence` = "official"** for every edge (each mapping is a direct Census
  correspondence; only the cardinality label is a lossless derivation).
- **Validation (build-spec Sec 4):**
  - **Seed cross-validation:** 24/24 `sic_naics_bridge_seed.csv` rows reproduced exactly
    (0 mismatches) by aggregating 1997_NAICS→1987_SIC edges to NAICS-3-digit → distinct
    SIC-2-digit sets. Confirms no fabrication.
  - **Round-trip:** forward vs reverse edge counts symmetric except 1987_SIC↔1997_NAICS
    (1852 vs 1861, Δ−9) — EXPECTED (two independently-compiled official files). Reverse-edge
    containment: 15/1861 (~0.8%) 1997_NAICS↔1987_SIC edges have no reverse in the counterpart
    file — documented non-invertibility (build-spec Sec 4.1), not a structural failure. All
    other pairs 100% consistent.
- **Not staged as edges (still walls):** the BEA I-O↔SIC/NAICS concordances (SCB PDF
  appendices, URLs only — build-spec P3) and the ISIC Rev3↔Rev4 crosswalk (external — P4).

---

## Cross-references

- Full narrative: `../CONCORDANCE_COMPENDIUM.md`
- Build plan for machine-readable resolvers: `../CONCORDANCE_BUILD_SPEC.md`
- Official Census bridges + BEA URLs: `_sources/SOURCES.md`
- Vintage timelines: `../_timelines/IO_CHANGE_TIMELINE.md`, `../_timelines/NIPA_CHANGE_TIMELINE.md`
- Working resolver this stage generalizes: `../NIPA_T711_FISIM_remap.md` +
  `code/L01_loaders/_nipa_t711_line_resolver.py`
