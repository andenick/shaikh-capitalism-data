# Phase 4 — ADEQUACY: Detailed Execution Plan

**Goal**: Per-chapter readiness reports formally ratifying that every series in the registry can be reconstructed and (where applicable) extended with verified sources, no proxies-without-disclosure, valid units, and ≥80/100 chapter score.

**Effort**: ~25 hours estimated. Per-chapter agent dispatch, 5 chapters per wave, 3 waves.

**Inputs**:
- 114 filled `Technical/research/{SID}_research.json` (Phase 3 output, all PASS)
- 15 chapter rollups `Technical/docs/chapters/CH{N}_RESEARCH_SUMMARY.md`
- `Technical/series_registry.json` v0.1 (114 series)
- 5 closed decision docs + 1 pending (0006)
- Discontinued APIs noted in decision 0005

**Outputs**:
- 16 per-chapter adequacy reports `Technical/docs/chapters/CH{N}_ADEQUACY_REPORT.json`
  - Chapters 2–11 (skipping 1 — no empirical), 13–17 (skipping 12), plus ES (treated as one chapter-equivalent)
- 1 chapter-level decision ratification: each report ratifies (a) Phase 3 content-type corrections, (b) substitution recommendations for discontinued APIs per series, (c) registry adjustments needed before Phase 5
- Updated `series_registry.json` with `adequacy` block per series
- Decision 0006 (ES2301 split) ratified or rejected by ES wave
- `Technical/Build/PHASE4_VALIDATION_REPORT.json` — chapter-by-chapter score table

---

## Scoring Rubric (per chapter, max 100)

| Dimension | Weight | What's scored |
|---|---|---|
| **D1 Source Reachability** | 25 | % of series with `primary_source.url` that resolves (HEAD 200) or is documented offline-archival |
| **D2 Year Coverage** | 20 | % of book year range with no data gap; for extension, % of post-book years available |
| **D3 License Compatibility** | 15 | All sources public-domain or CC-BY-compatible; commercial sources (Ibbotson, Morningstar) flagged with open substitute |
| **D4 Units Consistency** | 15 | Every series has explicit `units` field; loaders' expected units match source units |
| **D5 Extension Feasibility** | 15 | For time_series series: extension subsource identified with URL/API; for cross_sectional/derived: explicit acknowledgement |
| **D6 No-Proxy Compliance** | 10 | Any substitution from CD2 documented with "Concept Match Justification"; no silent proxies |

**Gate threshold**: ≥ 80/100 per chapter. < 80 → chapter goes to remediation queue (subagent re-runs with explicit gap-closure instructions).

---

## Adequacy Report Schema

`Technical/docs/chapters/CH{N}_ADEQUACY_REPORT.json`:

```json
{
  "schema_version": "rscd-adequacy-v1.0",
  "chapter": 2,
  "reviewer": "opus-subagent-p4-wave1-ch2",
  "review_date": "2026-05-18",
  "series_count": 18,
  "scores": {
    "D1_source_reachability": {"value": 23, "max": 25, "details": "..."},
    "D2_year_coverage": {"value": 18, "max": 20, "details": "..."},
    "D3_license_compatibility": {"value": 14, "max": 15, "details": "..."},
    "D4_units_consistency": {"value": 14, "max": 15, "details": "..."},
    "D5_extension_feasibility": {"value": 13, "max": 15, "details": "..."},
    "D6_no_proxy_compliance": {"value": 9, "max": 10, "details": "..."}
  },
  "total_score": 91,
  "gate_passed": true,
  "per_series": [
    {
      "sid": "S201",
      "name": "...",
      "content_type_correction": null,
      "url_status": "200 OK | 404 | discontinued | offline-archival",
      "year_coverage_pct": 100,
      "license": "public-domain",
      "units": "index_1958=100",
      "extension_status": "feasible | discontinued | data_unavailable",
      "proxy_flags": [],
      "remediation": []
    }
  ],
  "chapter_level_recommendations": [
    "Reassign S707 cd2_id to null (decision 0003 already actioned)",
    "Add `adequacy.status: ready_for_phase5` to all 18 series in registry"
  ],
  "blockers_for_phase5": [],
  "open_questions": []
}
```

---

## Wave Structure

16 chapter-groups of work. 5 per wave × 3 waves + 1 ES catchup.

| Wave | Chapter-groups | Series | Agents |
|---|---|---|---|
| 1 | Ch2 (18), Ch3 (9), Ch4 (8), Ch5 (4), Ch6+AS (4+9=13) | **52** | 5 |
| 2 | Ch7+S709-711 (11), Ch8 (5), Ch9 (3), Ch10 (8), Ch11 (4) | **31** | 5 |
| 3 | Ch13+Ch17 combined (4), Ch14 (8), Ch15 (9), Ch16 (6), ES papers (4) | **31** | 5 |
| **Total** | **15 chapter-groups + ES** | **114** | **15** |

---

## Per-Agent Workflow

Each subagent receives:
- Chapter assignment + series list
- Per-series Phase 3 dossier paths
- Discontinued-API watchlist from decision 0005
- Adequacy template path
- Reachability check requirements (HEAD requests on URLs)
- Output paths (per-chapter report + registry update instructions)

### Steps (per agent)

1. Read `PHASE4_ADEQUACY_PLAN.md`
2. For each series in chapter:
   a. Read its `research/{SID}_research.json` dossier
   b. **URL reachability check** — `urllib.request` HEAD on `primary_source.url` and each `extension_candidates[].url`. Record HTTP status.
   c. **Content-type ratification** — confirm Phase 3 reclassification (Ch3/4/9/13) is correct, or push back
   d. **Substitution proposal** — if URL is dead or source discontinued, propose substitute from decision 0005 watchlist (or new)
   e. **Units check** — confirm `primary_source.units` is explicit and matches what loaders will expect
   f. **No-proxy compliance** — any subseries/substitution flagged with "Concept Match Justification"
3. Author `Technical/docs/chapters/CH{N}_ADEQUACY_REPORT.json`
4. For each series in registry, append/update an `adequacy` block:
   ```json
   "adequacy": {
     "status": "ready_for_phase5" | "blocked" | "data_unavailable",
     "score_contribution": <int>,
     "reviewed_at": "...",
     "issues_resolved": [...],
     "issues_outstanding": [...]
   }
   ```
5. Run validator: `python Technical/code/utils/_phase4_adequacy_validator.py --chapter N`
6. Report PASS/FAIL with per-series breakdown

### Constraints

- URL checks must be REAL HEAD requests (with timeout=10s); don't fabricate status codes
- If a URL needs API key (FRED, BEA), document the auth requirement; don't fail it
- Discontinued ≠ blocked — propose substitute and mark `status: ready_for_phase5_with_substitute`
- No new content_type changes (Phase 3 owns those); only ratify or escalate
- No new registry rows (Phase 3 owns the count)

---

## Gate close (Stage 2)

After 3 waves:

1. `_phase4_adequacy_validator.py` confirms 16 chapter reports exist, all ≥ 80
2. Decision 0006 ratified by ES wave (split or defer)
3. Registry has `adequacy` block on every series
4. `PIPELINE_STATE.json` advanced: `current_stage: 3` (INGESTION), `stage_2.gate_passed: true`
5. `Build/PHASE4_VALIDATION_REPORT.json` written
6. Handoff document for Stage 2 close

---

## Risks

| Risk | Mitigation |
|---|---|
| URL check rate-limited / blocked | Use User-Agent header, timeout 10s, retry once with backoff; mark as `unverified` not `failed` |
| Subagent makes up HTTP status | Validator spot-checks 10% of URLs via second-pass HEAD; mismatches fail the chapter |
| Discontinued source has no substitute | Mark series `data_unavailable`, exclude from extension, document in adequacy report. Don't fabricate a substitute. |
| Decision 0006 (ES2301 split) deadlocks Wave 3 | Subagent makes the recommendation; main thread executes registry expansion if approved |
