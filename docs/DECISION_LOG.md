# Decision Log — Shaikh (2016)

Structured record of all non-trivial data construction decisions. Each entry
documents what was decided, why, and what alternatives were considered.

Format: DEC-{NNN}

---

## DEC-001: Base year 1958 for S001 Industrial Production reindexing (2026-02-11)

**Decision**: Use 1958 as the reindex base year for S001-B.

**Rationale**: Matches Shaikh's published Figure 2.1 axis scaling. The chopped CSV
metadata for S001-A shows "Index 1913=100" but Shaikh's composite figure uses
1958=100. The registry transform confirms:
`S001-B[t] = S001-A[t] * (100 / S001-A[1958])`.

**Alternatives Considered**:
- 1913 (rejected: S001-A uses 1913 natively, but S001-C/D use 2017=100 which
  must be rebased to match — 1958 is the common reference year in Shaikh's figure)
- 2010 (rejected: would not match Shaikh's published figure scale)

**Impact**: Affects S001-B display values and downstream splice with S001-D.

**Series Affected**: S001

---

## DEC-002: Growth-rate splicing as default splice method (2026-02-11)

**Decision**: Use growth-rate splicing (not level splicing) as the default method
for joining subseries at splice points.

**Rationale**: Growth-rate splicing preserves the trend behavior of both segments
while matching levels at the splice point. This is standard practice in economic
data construction and matches Shaikh's methodology as described in Appendix 2.1.

**Alternatives Considered**:
- Level splicing / direct concatenation (rejected: creates discontinuities when
  segments have different base years or units)
- Weighted average in overlap zone (rejected: more complex, unclear if Shaikh used it,
  and overlap periods are often single years)

**Impact**: Affects all multi-segment series (S001, S002, S007, S009, and others
with splice construction steps).

**Series Affected**: S001, S002, S007, S009, S076

---

## DEC-003: Annual averaging for monthly FRED extension data (2026-02-11)

**Decision**: Convert monthly FRED data to annual using simple arithmetic average
of 12 monthly observations.

**Rationale**: Shaikh's original data is annual. FRED provides monthly data for
extension series (INDPRO, UNRATE, etc.). Annual averaging is appropriate for
flow-like variables and indices where the annual value represents the typical level
over the year.

**Alternatives Considered**:
- End-of-year value (rejected: introduces arbitrary December bias, not representative
  of annual level)
- Q4 average (rejected: same problem, plus inconsistent with Shaikh's annual data)
- Geometric average (rejected: unnecessary complexity for index data, arithmetic
  average is standard in official statistics)

**Impact**: Affects all FRED-extended series. The averaging is done in the extension
step of P## scripts via `monthly_to_annual(method="average")`.

**Series Affected**: S001, S002, S003, S007, S009, S076, S067

---

## DEC-004: Dual extension columns S###-EXT and S###-F in chopped CSVs (2026-03-15)

**Decision**: Every API-extended series produces two additional columns in its
chopped CSV: `S###-EXT` (raw API data in its native units) and `S###-F`
(re-indexed extension data spliced to the previous subsource's level).

**Rationale**: Users need to see both the raw FRED/BEA data and the
growth-rate-spliced extension on the same chart. The re-indexing formula
`S###-F[t] = prev_subsource[splice_year] * (API[t] / API[splice_year])`
preserves trend while matching levels, and exposing the raw column alongside
lets the viewer judge the splice quality visually.

**Alternatives Considered**:
- Single merged column (rejected: hides the splice point and raw API behavior;
  this was the original approach in P01-P07 and the root cause of the extension
  visibility bug)
- Raw column only without re-indexing (rejected: different base years make
  overlay comparison meaningless)

**Impact**: Requires all P## scripts to emit both columns into `data_dict`
before chopped CSV generation. `generate_shiny_subsources.py` reads the
registry `extension` block and creates subsource entries with
`is_extension: true` for both column types.

**Series Affected**: S001, S002, S003, S007, S008, S009 (all Ch2 extended
series); pattern applies to all future extensions.

---

## DEC-005: Registry-derived subsource metadata generation (2026-03-15)

**Decision**: All visualization subsource metadata (SHINY_SUBSOURCES.json) must
be programmatically generated from `series_registry.json` via
`generate_shiny_subsources.py`. Hand-written metadata files are prohibited.

**Rationale**: Hand-maintained SHINY_SUBSOURCES.json diverged from the registry
within two sessions, causing phantom subsources and missing extension entries.
The root cause of the extension visibility bug was that
`generate_shiny_subsources.py` had `is_extension = False` hardcoded because it
didn't read the registry's extension blocks. Making the registry the single
source of truth eliminates drift.

**Alternatives Considered**:
- Hand-curated JSON (rejected: proved unmaintainable — diverged within 2
  sessions and caused display bugs)
- Dual-source merge (rejected: adds complexity without benefit; registry
  already contains all needed metadata)

**Impact**: Any metadata change must go through `series_registry.json` first,
then regeneration. The Anu Suite skills (anu-chopped v1.3, anu-shiny v3.2)
were updated to codify this as mandatory.

**Series Affected**: All series (project-wide policy).

---

## DEC-006: S053 price denominator must use S042I (WPI 1947=100), not S042A (raw WPI) (2026-03-16)

**Decision**: The interest/price ratio S053 = i/p uses S042I (Wholesale Price
Index rebased to 1947=100) as its price denominator, not S042A (raw Jastram
WPI in original units).

**Rationale**: The book defines i/p such that the ratio equals 1.0 at the base
year 1947 (Appendix 10.1). Using S042A (raw Jastram) produced a 45% error at
2010 and i/p ≠ 1.0 at 1947. S042I is the rebased column where WPI(1947) = 100,
which yields the correct normalization.

**Alternatives Considered**:
- S042A with post-hoc normalization (rejected: introduces an extra transform
  step and obscures the source; S042I already exists in the chopped CSV)
- CPI as price denominator (rejected: Shaikh explicitly uses WPI for this
  ratio, not CPI)

**Impact**: P20 was updated to extract S042I with S042A as fallback. P21
docstring and fallback function were corrected. S052 and S053 final/chopped
CSVs were regenerated.

**Series Affected**: S052, S053

---

## DEC-007: CS027-D denominator is S013G (total corporate capital KTC), not S013F (inventories) (2026-03-16)

**Decision**: The concurrent-series denominator for S027 (corrected corporate
profit rate) must map to S013G (KTC = gross corporate capital + inventories),
not S013F (corporate inventories alone).

**Rationale**: The book's formula is rcorp = NOS / KTC(-1), where KTC is total
corporate capital stock. S013G contains KTC (≈$220B range) while S013F
contains only inventories (≈$25B range). Using S013F as the denominator
produced profit rates roughly 10× too high. Verification:
NOS/KTC(-1) = S013B/S013G(-1) matches the book's computed S013J at 0.00%
error for checked years (1948, 1982, 2007).

**Alternatives Considered**:
- S013F inventories (rejected: wrong concept — inventories are only one
  component of the capital stock denominator)
- Net capital stock instead of gross (rejected: Shaikh uses gross fixed
  capital plus inventories as stated in Appendix 6.1)

**Impact**: P10 CS_COLUMN_MAP updated, all metadata corrected,
S027_chopped.csv regenerated.

**Series Affected**: S027 (CS027-D component)

---

## DEC-008: Ch8 series ID collision resolved via S841-S846 registry prefix (2026-03-16)

**Decision**: Chapter 8 concentration series use registry IDs S841-S846 (with
`catalog_id` fields mapping to the book's S041-S046 numbering) to avoid
collision with Ch10 series S041/S042 already in the registry.

**Rationale**: The sequential numbering scheme (S0XX) assigned S041-S046 to
both Ch8 (concentration data from Bain/Stigler/Demsetz/Semmler) and Ch10
(interest rate / price level). Since Ch10 was registered first, Ch8 needed an
alternative prefix. The S8XX prefix signals "Chapter 8" while `catalog_id`
preserves the book's original numbering for display and cross-reference.

**Alternatives Considered**:
- Renumber Ch10 series (rejected: Ch10 was already in production with
  downstream references in scripts, metadata, and subsources)
- Use S1XX range (rejected: would collide with S102-S105 already assigned to
  Ch17 and Ch6)
- Alphabetic suffix (rejected: breaks the numeric-only convention used by all
  pipeline scripts)

**Impact**: Loading scripts L36-L41, processing scripts P62-P67, and all
metadata entries use S841-S846. Display layers use `catalog_id` for
user-facing labels.

**Series Affected**: S841, S842, S843, S844, S845, S846

---

## DEC-009: Cross-sectional data type for non-time-series chapters (2026-03-16)

**Decision**: Series from Ch8 (concentration), Ch9 (price theory), and Ch17
(distribution) use `data_type: "cross_sectional"` with appropriate
`index_axis` values (e.g., "industry", "percentile") rather than the default
year-based time-series format.

**Rationale**: These chapters present industry-level or distributional data at
a single point in time (or a small set of years), not annual time series.
Forcing them into the year-indexed schema caused validator failures
(CATALOG_YEARS_SINGLE, BAD_PERIOD) and made the data semantically misleading.
The cross-sectional flag tells validators and visualization code to skip
time-series checks and use appropriate axis labeling.

**Alternatives Considered**:
- Force year-indexed format with dummy years (rejected: misrepresents the data
  and requires ugly workarounds in every downstream consumer)
- Exclude from pipeline entirely (rejected: these series are empirical and
  belong in the replication package, just with a different structure)

**Impact**: Validators updated to skip BAD_PERIOD and CATALOG_YEARS_SINGLE
checks for cross-sectional series. SHINY_SUBSOURCES entries marked with
`is_cross_sectional` flag. Visualization code can branch on `data_type` for
chart formatting.

**Series Affected**: S047, S048, S049 (Ch9), S102, S103, S104 (Ch17),
S841-S846 (Ch8)

---

## DEC-010: S096 classified as theoretical — no empirical pipeline (2026-03-16)

**Decision**: S096 (Ch16 Fig16.4, "Golden Waves" schematic) is classified as a
theoretical/schematic figure with no empirical data pipeline. A placeholder
registry entry exists but no L##, P##, chopped CSV, or extenbook is generated.

**Rationale**: Fig16.4 in the book is a hand-drawn schematic illustrating the
concept of long waves — it contains no data points, no axes with empirical
values, and no reproducible series. Creating a synthetic pipeline for it would
be misleading.

**Alternatives Considered**:
- Synthetic placeholder data (rejected: would falsely imply empirical content)
- Omit from registry entirely (rejected: breaks the completeness invariant
  that every book figure has a registry entry; the placeholder makes the
  omission explicit and auditable)

**Impact**: S096 is excluded from pipeline runs, validation checks, and
extenbook generation. Ledger correctly reports 96 processable series out of
113 registered.

**Series Affected**: S096

---

## DEC-011: External API replicability over internal internal data store (2026-03-16)

**Decision**: All API-sourced data must use direct external API connections
(FRED, BEA, etc.) with results cached in `Inputs/API/[SOURCE]/`. The internal
internal data store must never be used as a data source for replicable series.

**Rationale**: The replication package must be reproducible by anyone with
internet access. internal data store is an internal project data store not available to
external researchers. By using public APIs directly, any user can re-fetch the
same data. Every extension subsource also requires a `source_url` field for
one-click verification of the upstream data.

**Alternatives Considered**:
- internal data store as primary source with API fallback (rejected: creates a hidden
  dependency; if internal data store diverges from the API, results become non-reproducible)
- No local cache (rejected: API calls are slow and rate-limited; caching in
  `Inputs/API/` enables offline pipeline runs)

**Impact**: All FRED data migrated from `Inputs/internal data store/FRED/` to
`Inputs/API/FRED/` (16 files). `fetch_fred_data.py` and E01-E07 extension
scripts updated. 21 FRED extension subsource entries gained `source_url`
fields. internal data store/FRED duplicate directory deleted.

**Series Affected**: All FRED-extended series (S001, S002, S003, S007, S009,
S051, S067, S076, S094, S095, S100, S101)

---

## DEC-012: Full-book pipeline expansion from 4 to 13 empirical chapters (2026-03-16)

**Decision**: Expand the Anu Replicator pipeline from 4 chapters (Ch2, Ch6,
Ch7, Ch10) to all 13 empirical chapters in a single batch session, accepting
that documentation artifacts (research JSONs, DPRs, decompositions) for the 9
new chapters would initially be stubs.

**Rationale**: The 4-chapter approach had proven the pipeline architecture.
Continuing chapter-by-chapter with full documentation per chapter would have
taken months. The batch approach captured all 113 series and 84 figures in one
session, establishing a complete but shallow pipeline that could be deepened
with documentation afterward (which was done in Sessions 21 and 23).

**Alternatives Considered**:
- Continue chapter-by-chapter with full docs (rejected: too slow — at ~2
  sessions per chapter, the remaining 9 chapters would take 18+ sessions)
- Batch without stubs (rejected: leaving series completely undocumented would
  cause validator failures and make the ledger health score meaningless)

**Impact**: 61 new series, 60 new L## and P## scripts, 86 chopped CSVs. Ledger
health dropped from 99% to 56% (honest accounting of documentation gaps) but
was restored to 91% in Session 21 and 100% in Session 23.

**Series Affected**: All series in Ch5, Ch8, Ch9, Ch11, Ch12, Ch14, Ch15,
Ch16, Ch17 (61 series total)

---

## DEC-013: NickyData validation framework with V00-V08 validation phases (2026-04-07)

**Decision**: Integrate a comprehensive validation framework (V00-V08) into the
pipeline, running automatically after processing (L→P→V) with eight
specialized validators: reference values, range check, continuity,
completeness, cross-series consistency, splice quality, extension overlap, and
hash integrity.

**Rationale**: The NickyData architecture demonstrated that validation should be
a first-class pipeline phase, not an afterthought. Without systematic
validation, errors like the S053/S042A bug (DEC-006) went undetected until
manual audit. The V## scripts catch such errors automatically on every
pipeline run.

**Alternatives Considered**:
- Ad-hoc spot checks (rejected: the S053 and CS027-D bugs proved that manual
  auditing misses systematic errors)
- Single monolithic validator (rejected: granular V01-V08 scripts allow
  targeted debugging and selective execution)
- Validation as a separate tool (rejected: integration into `replicate.py`
  via `--validate-only` and `--full` flags makes it frictionless)

**Impact**: Pipeline expanded to L→P→V→M. First validation run: 340/437 checks
pass, 0 failures (97 warnings from expected historical data patterns). CLI
flags added: `--validate-only`, `--skip-validation`, `--full`.

**Series Affected**: All series (project-wide infrastructure)

---

## DEC-014: Registry v2.0 with machine-readable source references (2026-04-07)

**Decision**: Add a `sources` block to `series_registry.json` containing
machine-readable SourceReference entries (with `ref_id`, `url`, `year`,
`publisher`), and add `source_refs` and `confidence` fields to individual
subseries entries linking them to specific sources.

**Rationale**: Source attribution was previously embedded in free-text
`data_source` strings that couldn't be queried programmatically. The
NickyData pattern of structured source references enables cross-series
provenance queries (e.g., "which series use FRED data?", "which subseries
cite Shaikh 2016?"). The `provenance_index.json` generator uses these
references to build a queryable source lineage.

**Alternatives Considered**:
- Keep free-text source strings (rejected: not queryable, not linkable,
  not auditable — the same source string appeared in 50+ subseries with
  minor spelling variations)
- External bibliography database (rejected: adds a dependency outside the
  registry; keeping sources in-registry maintains the single-source-of-truth
  principle)

**Impact**: 11 distinct SourceReference entries created from 292 subseries
source strings. 55 subseries gained `source_refs` links. Registry version
bumped to 2.0.0 (Anu Suite v6.0). `build_source_refs.py` and
`generate_provenance_index.py` created as utilities.

**Series Affected**: All series (registry-wide schema change)

---

## DEC-015: Reference-value extraction from final CSVs for validation (2026-04-08)

**Decision**: Populate `reference_values` in the series registry by
programmatically extracting 3-5 data points per series from the pipeline's
own final CSVs, using `extract_reference_values.py`.

**Rationale**: Reference values serve as regression-test anchors — if a
pipeline change causes a series to shift, V01 catches it immediately. Manually
entering reference values from the book would be ideal but requires
page-by-page lookup for 113 series. Extracting from the pipeline's own output
bootstraps the validation framework now; values can be replaced with
book-sourced figures incrementally.

**Alternatives Considered**:
- Book-sourced values only (rejected: would leave 80% of series without any
  reference check for months while values were manually transcribed)
- No reference values (rejected: V01 would be toothless — the S053 bug
  would not have been caught by range checks alone)
- Random sample points (rejected: deliberate selection of economically
  meaningful years — base years, crisis years, endpoints — provides better
  regression coverage)

**Impact**: Coverage jumped from 18 to 91 out of 113 series (81%). V01 now
validates 355 reference points (was 44), all passing. Remaining 22 series
lack final CSVs (input tables, theoretical entries).

**Series Affected**: 91 series with reference values populated

---

## DEC-016: S008 uses CES3000000008 (mfg hourly earnings) over COMPRNFB (2026-05-04)

**Decision**: Switch S008 extension proxy from FRED COMPRNFB (nonfarm business real compensation) to CES3000000008 (manufacturing average hourly earnings).

**Rationale**: CES3000000008 is manufacturing-specific (BLS CES, 1939-2026), matching Shaikh's source ("manufacturing production worker nominal compensation"). COMPRNFB is nonfarm-wide. The manufacturing-specific series reduces splice discontinuity from 2.64σ to 0.51σ — a 5× improvement.

**Alternatives Considered**:
- COMPRNFB (rejected as primary: nonfarm is too broad; kept as fallback if CES unavailable)
- BLS LCEAMN (not available via FRED; quarterly manufacturing compensation per hour)
- No extension (rejected: data exists and extension is valuable for Ch2 analysis)

**Impact**: S008 grade improved from B- to B. Extension now 1790-2026 (was 1790-2025 with COMPRNFB).

**Series Affected**: S008

---

## DEC-017: S076 extension via MeasuringWorth CPI at splice 2016 (2026-05-04)

**Decision**: Extend S076 (Consumer Price Level, Ch15) using MeasuringWorth USCPI data, growth-rate splice at 2016.

**Rationale**: Same source as Shaikh used (Officer & Williamson MeasuringWorth CPI). Perfect conceptual continuity. MW CPI data cached via internal data store import (USCPI_1774-2025.csv). Splice at 2016 = last year of previously loaded data.

**Alternatives Considered**:
- FRED CPIAUCSL (rejected: MW is the actual source Shaikh used; same-source continuity)
- No extension (rejected: MW data readily available via internal data store import)

**Impact**: S076 now 1774-2025 (was 1774-2016). Grade: A+ (0.37σ).

**Series Affected**: S076

---

## DEC-018: S051 extended via FRED DPRIME for prime rate component (2026-05-04)

**Decision**: Extend S051-B (prime rate) via FRED DPRIME (Bank Prime Loan Rate).

**Rationale**: Shaikh used the ERP Table 73 (3-month T-bill). DPRIME (bank prime rate) is a short-term rate that tracks the T-bill closely. Growth-rate splice borrows only rate dynamics, not levels. S051-A (profit rate) extends via S026 chain (BEA, to 2024).

**Alternatives Considered**:
- FRED DTB3 (3-month T-bill — exact match, but less coverage than DPRIME)
- No extension (rejected: DPRIME is readily available 1955-2026)

**Impact**: S051 prime rate extends to 2026. Profit rate extends to 2024 via S026.

**Series Affected**: S051

---

## DEC-019: S095 dual extension via COMPRNFB + OPHNFB (2026-05-04)

**Decision**: Extend S095 using FRED COMPRNFB (real compensation per hour) for wages and OPHNFB (output per hour) for productivity.

**Rationale**: Shaikh used BLS Major Sector Productivity and Costs Indexes — COMPRNFB and OPHNFB ARE the modern FRED versions of these exact series. Direct continuation.

**Alternatives Considered**:
- Manufacturing-specific only (rejected: Shaikh used "business sector" for Fig 16.3)
- Single-component extension (rejected: both components have FRED equivalents)

**Impact**: S095 now 1947-2025 (was 1947-2012). Grade: A (1.47σ).

**Series Affected**: S095

---

## DEC-020: S100 ratio extended via FRED CMDEBT/PI (2026-05-04)

**Decision**: Extend S100-C (debt-to-income ratio) using FRED CMDEBT / PI ratio.

**Rationale**: Shaikh used Flow of Funds TD3 (household debt) / NIPA T2.1 (disposable personal income). CMDEBT is the same Flow of Funds series. PI (Personal Income) is broader than disposable PI but growth rates track closely. Growth-rate splice means only the ratio trend is borrowed.

**Alternatives Considered**:
- FRED DPI (Disposable Personal Income — exact match but shorter coverage)
- No extension (rejected: both components readily available)

**Impact**: S100 ratio extends to 2025. Debt/income levels (S100-A, S100-B) remain at 2012.

**Series Affected**: S100

---

## DEC-021: S101 extended via FRED FODSP (2026-05-04)

**Decision**: Extend S101-A (financial obligations ratio) using FRED FODSP.

**Rationale**: Shaikh used Federal Reserve FOR/FOR/DTFD%YPD.Q. FODSP IS this exact series (Household Financial Obligations as % of DPI). Direct continuation. Divided by 100 to match Shaikh's decimal units.

**Alternatives Considered**:
- FRED TDSP (Debt Service Payments — narrower than financial obligations)
- No extension (rejected: FODSP is the same series)

**Impact**: S101 now 1980-2023 (was 1980-2012). Grade: A (0.89σ).

**Series Affected**: S101

---

## DEC-022: V07 modified to check all columns for extension (2026-05-04)

**Decision**: Modify V07_extension_overlap.py to check ALL numeric columns in a final CSV, not just column 0, when determining whether a series extends beyond its splice year.

**Rationale**: Multi-column series (S051, S100) have extensions in non-primary columns. V07 previously checked only `df.columns[0]`, causing false-positive warnings for series that ARE extended but have the extension data in a later column.

**Alternatives Considered**:
- Restructure P19/P60 to put extended column first (rejected: would break V01 reference value checks which expect specific column ordering)
- Add a registry field `primary_extended_column` (rejected: over-engineering for 2 series)

**Impact**: V07 now 16/16 PASS (was 14/16). False positives eliminated.

**Series Affected**: S051, S100 (and any future multi-column series)

---

## DEC-023: S097 interest rate path extended via FRED DPRIME (2026-05-04)

**Decision**: Extend S097-A (interest rate component) via FRED DPRIME.

**Rationale**: Same as DEC-018. S097 plots interest rate vs corporate profit rate. The interest rate component uses the same ERP T-bill source. Profit rate component (S097-B) comes from S026 chain (already extended to 2024).

**Alternatives Considered**: Same as DEC-018.

**Impact**: S097 now 1948-2026 (was 1948-2011). Grade: B+ (0.09σ — smoothest proxy splice).

**Series Affected**: S097

---

## DEC-024: Level-based extensions for rate/percent and constructed ratio series (2026-05-04)

**Decision**: All extensions are now classified into three categories with different methods:
1. **Index series** (different base years): Growth-rate splice (= mathematical reindexing). No information lost.
2. **Rate/percent series** (same units as Shaikh): Direct level append from FRED. Actual market/government values used.
3. **Constructed ratios** (formulas): Compute the actual formula from component levels (e.g., wage_share = EC/GDP, debt_ratio = CMDEBT/PI).

Growth-rate splicing is ONLY used where base years differ (Category 1). It is NOT used for rates or constructed ratios because it introduces an artificial layer — Shaikh used actual table values, and so should we.

**Rationale**: Shaikh went to BEA NIPA Table 1.10 and read the actual dollar value of NOS. He did not growth-rate-splice an old profit rate with a new one. The extensions should follow the same philosophy: use actual published data values, not derived growth-rate approximations, wherever the same-unit data exists.

**Alternatives Considered**:
- Growth-rate splice for everything (rejected: artificial for same-unit series; hides data revisions)
- Level-shift splice (rejected: adjusts modern data to match Shaikh's vintage; less honest)

**Impact**: S051, S052, S068, S069, S094, S097, S100 now use actual levels or computed formulas instead of growth-rate splices. S100 unit bug (CMDEBT in millions vs PI in billions) caught and fixed. Bond yield (S052-A) now shows actual Moody's Aaa values.

**Series Affected**: S051, S052, S068, S069, S094, S097, S100

---

## DEC-025: S100 CMDEBT unit conversion (millions → billions) (2026-05-04)

**Decision**: Divide FRED CMDEBT by 1000 before computing debt/income ratio with FRED PI.

**Rationale**: FRED CMDEBT is in millions of dollars. FRED PI is in billions. Shaikh's original S100-A (household debt) was in billions (same unit as PI). Without the conversion, the computed ratio was ~800× instead of ~0.8×.

**Alternatives Considered**: None — this is a straightforward unit alignment fix.

**Impact**: S100 debt/income ratio now correctly shows ~0.78-0.86 for 2021-2025 (household deleveraging), vs the incorrect ~800 that appeared before.

**Series Affected**: S100

---
