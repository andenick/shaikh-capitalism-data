# 0006 — ES2301 (Weber-Shaikh 2020) Decomposition

**Status**: APPROVED (user ratified 2026-05-18)
**Date opened**: 2026-05-18 (Phase 3 expansion close)
**Date Phase 4 recommendation written**: 2026-05-18 (CHES_ADEQUACY_REPORT.json)
**Recommended by**: opus-subagent-p4-wave3-es

## Phase 4 Recommendation: RECOMMENDS_SPLIT

The Phase 4 ES adequacy reviewer recommends APPROVING the 5-way split for v1.0 (4 new series ES2302-ES2305 added to ES2301-rescoped) and DEFERRING the optional ES2306 (relative ULC) to v1.1.

### Scheme

| New ID | Topic | Source | URL HEAD status (2026-05-18) |
|---|---|---|---|
| ES2301 (rescoped) | US-China bilateral merchandise trade balance (Fig 1) | U.S. Census Bureau FT900 / USA Trade Online | 200 OK |
| ES2302 | China current account balance, level (Billion USD) AND % of GDP (Fig 2; emit as 2 rows) | IMF World Economic Outlook database | 200 OK |
| ES2303 | China official foreign exchange reserves excluding gold (Fig 3) | World Bank WDI (FI.RES.XGLD.CD) | 200 OK |
| ES2304 | RMB misalignment under extended PPP approach (Fig 4) | Literature compilation per paper note 17 (Cline-Williamson 2007; Dunaway-Li 2005; Cheung-Chinn-Fujii 2010a; Cheung 2012) | n/a (no single URL) |
| ES2305 | RMB misalignment under macroeconomic balance approach (Fig 5) | Same 4 literature reviews as ES2304 | n/a (no single URL) |
| ES2306 (deferred to v1.1) | US/China relative manufacturing ULC (7.8:1 headline, 2000-2010) | Conference Board ILC (hi-fi) or OECD ULC_QUA (open) -- inherits Ch11 wave2 canonical resolution | 200 OK (Conf Board GET) / 200 OK (OECD) |

### Rationale

**Why split for v1.0:**

1. **5 distinct primary sources**: Census, IMF, World Bank, plus two distinct literature compilations -- unlike ES2001/ES2101/ES2201, each of which has a SINGLE underlying dataset. The dossier-per-figure pattern is cleaner for a multi-source paper.
2. **Asymmetric extension risk**: Figs 1-3 (Census/IMF/WDI) are mechanically extensible to 2024; Figs 4-5 (literature compilations) are intrinsically NOT extensible by paper construction. Single-dossier aggregation conceals this distinction.
3. **Distinct methodological prose required**: The literature-compilation methodology (paper note 17) is logically separate from API-driven extension and deserves its own dossier sections to avoid silent methodology drift in v1.1+ extensions.
4. **Low marginal effort**: ~8-10 hours total (Phase 3 dossier fills ~2h + Phase 4 catchup adequacy ~1h + Phase 5 loader impact ~3-5h + Phase 6 EPR impact ~1-2h) for substantial Phase 5/6 clarity gain.

**Why defer ES2306 to v1.1:**

1. **Not figured in paper**: Body-text citation only (Golub et al. 2018 7.8:1 ratio); the paper does NOT plot a year-by-year relative ULC trajectory.
2. **Substitution complexity already canonicalized in Ch11 wave2**: BLS ILC -> Conference Board ILC (hi-fi licensed) or OECD ULC_QUA (open CC-BY) is the canonical Ch11 wave2 resolution applying to S1102, S1103, S1104. Duplicating the Concept Match Justification block for ES2306 in v1.0 doubles documentation cost without adding analytical value.
3. **Methodological choices Weber-Shaikh did not make**: Reconstructing a year-by-year relative ULC TS for v1.0 introduces averaging-window and basket-definition choices the original 7.8:1 average does not specify. v1.1 inclusion under canonical Ch11 sourcing preserves analytical value with cleaner methodology.

### Alternatives considered (and rejected)

- **Ship ES2301 as single composite (defer all 5-way split to v1.1)**: Rejected because composite-dossier loader for ES2301 would hide 4 distinct source pipelines vs the clean single-pipeline loaders that work for ES2001/ES2101/ES2201. The 4-vs-1 source asymmetry is significant.
- **Full 6-way split including ES2306 in v1.0**: Rejected because of the Ch11 wave2 CMJ-duplication cost and the methodological-choice overhead noted above.

## Other ES papers' decomposition decisions (unchanged from original PENDING status)

- **ES2001**: KEEP AS SINGLE (subagent confirmed; tables and figures share one BEA-IO + BLS-labor pipeline; Phase 4 ratifies)
- **ES2101**: KEEP AS SINGLE (subagent confirmed; one IO + BLS pipeline across 7 figures; Phase 4 ratifies)
- **ES2201**: KEEP AS SINGLE (subagent confirmed; 5 fitted parameters share IRS Table 1.4 + Table 1; Phase 4 ratifies)
- **ES2301**: RECOMMENDS_SPLIT per Phase 4 (this document)

## Action (pending user ratification)

If user accepts the Phase 4 recommendation:

1. Update this decision document to status='APPROVED'
2. Run `_phase3b_registry_expansion.py` (or equivalent) to add 4 new ES placeholder rows: ES2302, ES2303, ES2304, ES2305
3. Rescope existing ES2301 row from composite parent to Fig-1 component only (US-China bilateral trade balance, Census FT900)
4. Update `PIPELINE_STATE.json` series scope-count from 114 -> 118
5. Dispatch 1 Phase 3 catchup subagent to fill ES2302/ES2303/ES2304/ES2305 dossiers (~2 hours estimated)
6. Dispatch 1 Phase 4 catchup subagent to write `CHES_ADEQUACY_REPORT_V2.json` covering the 4 new series (~1 hour estimated)
7. Record ES2306 in v1.1 backlog with Ch11 wave2 BLS ILC substitution inheritance note

If user rejects:

1. Update this decision document to status='CLOSED' with rationale='deferred to v1.1'
2. ES2301 ships as single composite for v1.0; 5-way breakdown documented in `ES2301_paper_summary.md` and `CHES_ADEQUACY_REPORT.json` decision_0006_recommendation block
3. v1.1 scope inherits ES2302-ES2306 backlog (5 series including optional ES2306)

## Cross-references

- `Technical/docs/chapters/CHES_ADEQUACY_REPORT.json` -- full Phase 4 ES adequacy report, decision_0006_recommendation block
- `Technical/docs/chapters/CHES_REGISTRY_DELTA.json` -- registry expansion metadata for the 4 new v1.0 series + 1 v1.1 deferred series
- `Technical/docs/chapters/CH11_ADEQUACY_REPORT.json` -- Ch11 wave2 canonical BLS ILC -> Conference Board ILC / OECD ULC substitution that ES2306 will inherit in v1.1
- `Technical/docs/decisions/0005_discontinued_apis_deferred.md` -- BLS ILC discontinuation context
- `Technical/research/ES2301_research.json` -- Phase 3 dossier with original 5-way decomposition recommendation from the research subagent
- `Technical/docs/external_studies/ES2301_paper_summary.md` -- paper summary with same 5-way decomposition recommendation
