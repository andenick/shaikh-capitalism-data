# Phase 3 — Research: Detailed Execution Plan

**Goal**: Fill all 98 `Technical/research/{SID}_research.json` dossiers with KB-grounded, source-validated content. Phase 3 closes when every series has ≥ 2 verbatim book quotes, an identified primary source with URL, and at least one named extension candidate (for time_series).

**Effort**: ~50 hours total. Per-chapter agent dispatch, 5 chapters per wave, 3 waves.

**Inputs**:
- Book PDF: `Inputs/Capitalism Data/Inputs/[2016] Shaikh - Capitalism Competition, Conflict, Crises.pdf`
- KB: `SalvagedInputs/figures_reference/{FIGURE_MASTER_v4,HDARP_SERIES_LINKAGE}.json`
- CD2 dossier salvage: `SalvagedInputs/methodology_decisions/CD2_research_{json,md}/` (12 JSON + 114 MD ported)
- CD2 registry: `SalvagedInputs/methodology_decisions/CD2_series_registry_v2.0.json` (per-series source URLs)
- ShaikhChoppedTables: `SalvagedInputs/book_data/ShaikhChoppedTables/` (appendix values)
- Stubs: `Technical/research/{SID}_research.json` (98 pre-filled, awaiting content)

**Outputs**:
- 98 populated `research/{SID}_research.json`
- Per-chapter rollup `docs/chapters/CH{N}_RESEARCH_SUMMARY.md` (subagent-authored)
- Updated `PIPELINE_STATE.json` Stage 1 → complete

---

## Acceptance Criteria (per series)

Each dossier MUST contain:

1. **`book_quotes`**: ≥ 2 verbatim quotes from the book
   - At least 1 with `role: "definition"` (what the series is)
   - At least 1 with `role: "source"` (where Shaikh got the data)
   - Each quote has chapter, page, exact text
   - `verbatim_check: true` after human/agent confirms the quote matches the PDF
2. **`primary_source`**: agency + publication + table_or_series_id + url + units + frequency
   - URL must resolve (200 OK) at time of writing
   - `discontinued: false` unless explicitly so, with `replaced_by` filled
3. **`construction`**: one of `direct | formula | composite`, justified by a methodology_note
4. **`year_range_book`**: [start, end] matching what the book actually plots
5. **`extension_candidates`**: ≥ 1 for `time_series`; explicitly empty `[]` with explanation for `cross_sectional`/`theoretical`/`derived`
6. **`open_questions`**: any unresolved items (Phase 5/6 must handle these)
7. **`review_history`**: at least `{reviewer: "agent-or-name", date, status: "draft" | "reviewed"}`

**Cross-series quality**:
- No duplicate `primary_source.table_or_series_id` across two series unless intentional (and noted)
- Series that share a CD2 ancestor (per crosswalk) should reference each other in `cross_references` (TODO: add to template)

---

## Wave Structure

15 chapters of work (Ch1, Ch12 have no empirical series). 5 chapters per wave, 1 subagent per chapter.

| Wave | Chapters | Series count | Agents |
|---|---|---|---|
| A | 2, 3, 4, 5, 6 | 18+9+8+4+4 = **43** | 5 |
| B | 7, 8, 9, 10, 11 | 8+5+3+8+4 = **28** | 5 |
| C | 13, 14, 15, 16, 17 | 1+8+9+6+3 = **27** | 5 |
| **Total** | **15** | **98** | **15** |

Subagents run in **foreground**, in parallel (single message, multiple Agent tool calls per CLAUDE.md). Each subagent owns one chapter end-to-end.

---

## Per-Agent Workflow (one chapter)

Each subagent receives a self-contained prompt covering:

### Inputs

- Chapter number (e.g., 2)
- Series list (e.g., `[S201, S202, ..., S218]`)
- Book PDF path + page range (e.g., `Inputs/Capitalism Data/Inputs/[2016] Shaikh - Capitalism...pdf`, pp. 57–72)
- Stub paths (e.g., `Technical/research/S201_research.json`)
- CD2 salvage hint: any matching `SalvagedInputs/methodology_decisions/CD2_research_json/S{NNN}_research.json` (per crosswalk)
- CD2 registry path (for source URL hints)
- Chapter index entry from `docs/chapters/CHAPTER_FIGURE_TABLE_INDEX.json`

### Steps

1. Read the chapter PDF (multiple `Read` calls if > 10 pages)
2. For each series in the chapter:
   a. Open the stub
   b. Find the relevant figure(s) by `figures[]` field
   c. Locate Shaikh's narrative paragraph that defines/describes the series
   d. Extract verbatim quote(s) — at least one definition, one source citation
   e. Read the relevant appendix (Appendix 2.1, 2.2, etc.) for the data source
   f. Identify the primary modern source (FRED key, BEA table, BLS series ID, etc.); cross-reference CD2's dossier if it exists
   g. List extension candidates (URLs that resolve in 2026)
   h. Fill `methodology_notes` with any non-obvious construction choice
   i. Note open questions for Phase 4 adequacy review
   j. Write back to `Technical/research/{SID}_research.json`
3. Author chapter rollup: `Technical/docs/chapters/CH{N}_RESEARCH_SUMMARY.md`
   - One paragraph per series; cross-references; any chapter-wide issues
4. Run validator (see § Validator below) and report PASS/FAIL per series
5. Return to main: per-series status table + a summary paragraph + chapter rollup path

### Constraints

- **Verbatim quotes** — no paraphrasing. Use the book's exact words.
- **No fabricated sources** — if you can't find a URL, leave it null and flag in `open_questions`. Do NOT guess.
- **No proxies without justification** — if CD2 used a proxy (e.g., CPI for PPI), call it out in `open_questions` for Phase 4 to ratify.
- **No synthetic data assumptions** — if the book's source is discontinued and there's no clean modern equivalent, flag the series for Phase 4 reclassification.
- **Honor existing CD2 work** — if CD2 already identified a source, validate it (URL resolves, agency still hosts it) and port; don't redo from scratch.

---

## CD2 Salvage Map

12 of 98 RSCD series have an existing CD2 dossier. Map via crosswalk:

| RSCD ID | CD2 ID | CD2 dossier path |
|---|---|---|
| S201 | S001 | `SalvagedInputs/methodology_decisions/CD2_research_json/S001_research.json` |
| S202 | S002 | `... /S002_research.json` |
| S203 | S003 | `... /S003_research.json` |
| S204 | S004 | `... /S004_research.json` |
| S207 | S007 | `... /S007_research.json` |
| S208 | S008 | `... /S008_research.json` |
| S209 | S009 | `... /S009_research.json` |
| S217 | S017 | `... /S017_research.json` |
| ... | ... | (full map in `MIGRATION/CD2_to_RSCD_crosswalk.csv`) |

The CD2 JSON schema differs slightly from RSCD's (uses `entries[]` with `entry_type` instead of `book_quotes[]` with `role`). Port by mapping:
- CD2 `entry_type: methodology_description` → RSCD `methodology_notes[]`
- CD2 `entry_type: source_citation` → RSCD `primary_source` + (verbatim) `book_quotes[{role: "source"}]`
- CD2 `entry_type: figure_context` → RSCD `book_quotes[{role: "definition"}]` (after verbatim check)
- CD2 `citations[]` → RSCD `primary_source.url` + named in methodology_notes
- CD2 `methodology_summary` → RSCD `methodology_notes[]` (first entry)
- CD2 `known_issues` → RSCD `open_questions`

114 CD2 markdown docs at `SalvagedInputs/methodology_decisions/CD2_research_md/` provide additional narrative context for any series that has one.

---

## Validator

Author `Technical/code/utils/_phase3_research_validator.py` that:

1. Loads every `research/{SID}_research.json`
2. Checks acceptance criteria (book_quotes count, role coverage, primary_source completeness, etc.)
3. Emits per-series PASS/FAIL with reasons
4. Writes summary to `Technical/Build/PHASE3_VALIDATION_REPORT.json`
5. Returns exit code 0 if all PASS, 1 otherwise

Run after each wave; agent must achieve 100% PASS for the wave's series before main thread moves on.

---

## Gate close (Stage 1)

After all 3 waves complete:

1. `_phase3_research_validator.py` reports 98/98 PASS
2. Per-chapter `CH{N}_RESEARCH_SUMMARY.md` exists for chapters 2–17 (sans 1, 12)
3. Update `PIPELINE_STATE.json`:
   - `stage_1.status: "complete"`
   - `stage_1.gate_passed: true`
   - `stage_1.series_complete: 98`
   - `current_stage: 2`
4. Append `STEP_LOG.jsonl` + `BUILD_NARRATIVE.md`
5. Write `Technical/Handoffs/HANDOFF_phase3_close.md`

---

## Risks / failure modes

| Risk | Mitigation |
|---|---|
| Subagent invents a quote | Validator checks all quotes against PDF text via fuzzy match (Phase 3 enhancement; for now, human spot-check 10% per wave) |
| Source URL is dead | Agent must flag in `open_questions`, not fabricate. Phase 4 adequacy decides whether to find alternative |
| CD2 source was a wrong-concept proxy | Validator flags any port that retains `proxy: true` or has note `wrong-concept` for human review |
| Agent runs out of book context | Chapter ≤ 30 pages — single Read OK; >30 pages → multiple Reads. Built into prompt template |
| Two agents touch the same file | Each agent owns one chapter; series IDs partition cleanly (`S{ch}*`). No overlap. |

---

## Tracking

Per-wave TaskCreate entries (one per chapter, one per wave-close). Track `series_complete` on PIPELINE_STATE.json after each wave.
