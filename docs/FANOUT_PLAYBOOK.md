# Bulk Fanout Playbook — Phases 5-8 per Chapter

**Purpose**: Capture the architecture decisions and patterns established by the S201 end-to-end pilot so per-chapter fanout agents don't re-derive them. Every per-chapter agent **reads this first**, then **mirrors** S201's pattern.

**Reference implementation**: S201 (US Industrial Production, Ch2). See:
- `Technical/code/L01_loaders/L01_S201_load.py`
- `Technical/code/P02_processors/P02_S201_construct.py`
- `Technical/code/V03_validators/V03_S201_validate.py`
- `Technical/docs/series/S201_DPR.md`
- `Technical/docs/series/S201_EPR.md`

---

## Architecture decisions (already made — DO NOT CHANGE)

### S00 setup (in `Technical/code/S00_setup/`)
- `S00_config.py` — env loader; zero pandas deps
- `S00_cache.py` — Parquet cache, SHA-256 key, 30-day default TTL
- `S00_apis.py` — FRED + BEA clients; `ApiUnavailable` raised on failure for clean degradation

For new APIs (BLS, World Bank, MeasuringWorth, IMF SDMX, etc.):
- Add a client function in `S00_apis.py` (e.g., `fetch_bls_series(series_id, start, end)`)
- Use the cache: every API call goes through `S00_cache.cached_fetch(source, query_dict, fetcher_fn)`
- Document in `S00_apis.py` module docstring

### Orchestrator (`Technical/code/run.py`)
- `--list`, `--health`, `--series SID`, `--validate-only`, `--report`, `--skip-validate`
- Phase order: `S00_setup → L01_loaders → P02_processors → V03_validators → M04_manual → A05_analysis → O06_output`
- Series-specific scripts: filename matches regex `_S\d{3,4}_` or `_AS\d{3}_` or `_ES\d{4}_`
- Series-generic scripts: filename doesn't match → runs for every `--series` request
- Each script defines `def run() -> dict` returning at minimum `{status: "OK"|"PASS"|"FAIL"|"SKIPPED", ...}`

**You do NOT modify run.py** unless you find a real bug. Extend by adding new scripts to the phase dirs.

### Validation tolerance
- Default `VALIDATOR_TOL_PCT = 1.0` (module-level constant in each V03 script)
- Tighten for direct/cached series (S201 hit 0.0%)
- Loosen for formula series with known book formula errors (e.g., S401-style derived: 2-3%)
- Always include CD2 informational comparison; never fail on CD2 mismatch

### Cache
- Static data (book chopped tables): `ttl_days=None` (never expire)
- Live API data: `ttl_days=30` default
- Force refresh: pass `ttl_days=0`

### Graceful degradation contract
Every loader returns dict with status fields per source: `{"status": "OK", "fred_status": "ok"|"missing_key"|"api_error", "fred_error": str|None, ...}`. The processor inspects raw parquet existence — never assumes a subseries was loaded. The validator marks extension years as `data_unavailable: api_key_missing` when applicable.

---

## Per-series workflow (copy this for every series in your chapter)

### Phase 5 — Ingestion artifacts

1. **DPR** at `Technical/docs/series/{SID}_DPR.md`:
   - Sections: Definition · Why It Matters · Sources (per-subseries) · Construction (with formula) · Year Coverage · Units · Caveats · Cross-references · Validation Expectation
   - Mirror `S201_DPR.md` structure exactly

2. **Registry subseries decomposition** — edit `Technical/series_registry.json` for the series:
   ```json
   "subseries": {
     "{SID}-A": {"name": "...", "source": "...", "subsource_id": "...", "period": [start, end], "units": "...", "color": "#...", "role": "book_period_primary"},
     "{SID}-B": {"name": "...", "source": "...", "subsource_id": "...", "period": [start, end], "units": "...", "color": "#...", "role": "extension"}
   }
   ```
   Update top-level `status: "ingested"`, `units: "..."`, `construction: "direct|formula|composite"`. For `formula` and `composite`, fill `formula` and `components` fields too.

3. **SUBSOURCE_METADATA** — add per-subsource entries to `Technical/SUBSOURCE_METADATA.json` (if not already present). Keys: agency, publication, table_id, frequency, units, license, retrieval_method, url, discontinued (bool), graceful_degradation_notes.

4. **ANU_LEDGER** — add to `Technical/ANU_LEDGER.json` under `series.{SID}` with phases_completed list + artifact paths.

### Phase 6 — Extension artifact

5. **EPR** at `Technical/docs/series/{SID}_EPR.md`:
   - Sections: Classification · Method · Worked example · No-Proxy disclosure · No-Synthetic disclosure · Failure-mode table · CD2 divergence pre-disclosure
   - For `formula` series: extension MUST re-fetch components and re-compute. Document why.
   - For `composite` series: document each subsource's extension URL and reindex method.
   - For `cross_sectional`/`theoretical`/`derived` series: state explicitly that no extension applies and why.

### Phase 7 — Replication code

6. **`Technical/code/L01_loaders/L01_{SID}_load.py`**:
   - Module-level constants: `SERIES_ID`, sources tuple
   - `def run() -> dict` that fetches each subsource (book data from `SalvagedInputs/book_data/...`, API data via `S00_apis`)
   - Writes one parquet per subsource: `Technical/data/raw/{SID}_{subsource}.parquet`
   - Returns `{"status": "OK", "rows_loaded": {...}, "sources_fetched": [...], "fred_status": "ok"|"missing_key", ...}`

7. **`Technical/code/P02_processors/P02_{SID}_construct.py`**:
   - `def run() -> dict` that reads raw parquet, applies construction (rebase, splice, formula, etc.)
   - Writes `Technical/data/processed/{SID}.parquet` with columns `year, value, subseries_id, source_id`
   - For `cross_sectional`/`derived`/`theoretical`: write what data exists (e.g., the single-year snapshot) and mark accordingly
   - Returns `{"status": "OK", "rows_processed": int}`

8. **`Technical/code/V03_validators/V03_{SID}_validate.py`**:
   - Module-level `VALIDATOR_TOL_PCT = 1.0` (tighten/loosen per series)
   - `def run() -> dict` that compares processed series against the book-truth column in `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix{N}_*.xlsx`
   - For series with no book chopped table: compare against the dossier's `book_quotes` numeric values, or against a CD2 benchmark if available, with a documented rationale
   - Returns `{"status": "PASS"|"FAIL", "mae": float, "max_abs_err": float, "max_pct_err": float, "n_compared": int, "divergence_years": [...]}`
   - Appends to `Technical/VALIDATION_REPORT.json`

### Phase 8 — Output (generic — already exists)

9. `Technical/code/O06_output/O06_chopped_writer.py` — generic, just runs for the series
10. `Technical/code/O06_output/O06_extenbook_writer.py` — generic, just runs for the series

Per-series O06 code is NOT needed unless the series has a special output shape (rare).

---

## Per-content-type recipes

### `time_series` (the common case — like S201)
- Full L01 + P02 + V03 + chopped + extenbook
- Extension via API
- Tolerance 1.0%

### `cross_sectional` (e.g., Ch9 IO scatter, Ch3 UK 1904 budgets)
- L01: fetch the single-year benchmark from book/source
- P02: emit as single-year row(s); no splice
- V03: compare against book values
- Extension: explicitly `not_applicable_cross_sectional` in EPR; extension_candidates empty in dossier (already true after Phase 4)
- chopped CSV is short (one or few rows)
- Tolerance 0.5%

### `derived` (e.g., Ch4 cost curves, S401-S407)
- L01: fetch the inputs (or the book's published table if no underlying data)
- P02: apply the book's formula
- V03: tighter tolerance because derived values can amplify noise
- chopped CSV may be entirely book-truth values (no extension possible)
- Tolerance 0.5%

### `theoretical` (e.g., Ch3 analytic curves, Ch4 illustrative)
- L01: load the book's plotted values (if tabulated) or skip
- P02: pass-through
- V03: compare to book figure or skip with `status: "PASS_THEORETICAL"`
- chopped CSV holds the plotted curve points
- No extension

### `data_unavailable` (e.g., S801, S703, S704, S707, S708)
- DPR + EPR documenting the chart-only source and why no underlying data exists
- L01 returns `{"status": "SKIPPED", "reason": "data_unavailable"}`
- P02 is not authored (or returns SKIPPED)
- V03 returns `{"status": "PASS_DATA_UNAVAILABLE"}`
- No chopped CSV. Extenbook contains only the DPR + EPR + Source pages.
- Phase 8 viz uses the book figure image directly.

---

## Per-chapter rollup

After all series in your chapter pass:

- Append to `Technical/docs/chapters/CH{N}_RESEARCH_SUMMARY.md` (already exists from Phase 3) — add a new section "Phase 5-8 Closure" with one paragraph per series noting validation status + extension status + any caveat.
- Update `Technical/PIPELINE_STATE.json` `pilot_series_complete` block (or its equivalent) for each series.
- Run `python Technical/code/run.py --series {SID}` for each series; collect outputs.
- Run `python Technical/code/run.py --validate-only` at the end; expect all your chapter's V03 scripts PASS.

---

## Anti-patterns (DO NOT DO)

- Don't re-author S00 setup or run.py
- Don't fabricate URLs, source values, or extension methods
- Don't paper over a V03 FAIL — investigate and either fix the construction, document the divergence, or loosen tolerance with explicit rationale
- Don't use proxies without flagging `proxy: true` in registry + Concept Match Justification in EPR
- Don't apply lazy splice on derived quantities — extension recomputes components
- Don't introduce new content_type classifications — those are frozen
- Don't modify the registry's `predecessor_ids` block
- Don't write Plotly/matplotlib in L01/P02 — visualization belongs in viz/ (Phase 9)

---

## Reporting

Each chapter-agent returns:
- Per-series table: SID | content_type | V03 status | MAE | extension_status
- Per-series file listing (DPR, EPR, L01, P02, V03 paths)
- Chopped CSV row counts
- Extenbook file sizes
- Architectural decisions made (should be zero new ones if you follow the playbook)
- Open questions / blockers
