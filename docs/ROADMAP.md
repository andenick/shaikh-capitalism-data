# RSCD Roadmap

**v0.1** (current, 2026-05-18): Scaffold + Phase 2 candidates

| Phase | Status | Output |
|---|---|---|
| 0. Freeze + salvage | ✅ done | SalvagedInputs/ populated with 200+ files; CD/CD2 frozen by deny rule |
| 1. Anu Framework scaffold | ✅ done | Technical/ tree, state files, Build cascade, anu-build-v12.0 schema |
| 2. Taxonomy | 🟡 partial | series_registry.json v0.1 (98 candidates); CD/CD2 crosswalks written |
| 3. Research | ⏳ not started | per-series research dossiers |
| 4. Adequacy | ⏳ not started | per-chapter readiness reports |
| 5. Ingestion | ⏳ not started | subseries decomposition, DPRs |
| 6. Extension | ⏳ not started | EPRs |
| 7. Replication | ⏳ not started | L01/P02/V03 + run.py |
| 8. Output | ⏳ not started | chopped/ + extenbooks/ |
| 9. Visualization | ⏳ not started | viz/app.py (Plotly Dash) |
| 10. Distribution | ⏳ not started | Outputs/Publish + Drive + Archive |

**v1.0 target**: book-only (per decision 0001 draft recommendation), ~98
series, ~450 wall-clock hours from Phase 3 start.

## Immediate next session

1. Confirm decision 0001 (external study scope)
2. Phase 3.A.1 — author research template at `docs/series/_RESEARCH_TEMPLATE.json`
3. Phase 3.A.2+ — start per-series research dossiers (parallelizable;
   ~4 series per focused session)
4. Phase 4.A — adequacy reports per chapter once research is done

## Critical path

Phase 7 (replication code) is the bulk of effort (200–400 hours). Everything
upstream (research, adequacy, ingestion, extension docs) is necessary
preparation. Parallelize per-series work via `/dispatching-parallel-agents`
once Phase 4 closes and the orchestrator + S00_setup are in place.

## What's NOT in v1.0

- External study replications (ES####) — reserved for v1.1
- Per-figure SVG re-rendering — Dash app suffices
- IO-table reconstruction (Ch9 fixed/circulating capital) — likely promoted
  to v1.1 if Phase 3 confirms Ch9 has more empirical depth than the
  classifier estimated
