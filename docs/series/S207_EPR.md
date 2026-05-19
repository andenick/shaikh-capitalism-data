# S207 -- Extension Provenance Record

**Series**: S207 -- US Manufacturing Productivity and Production Worker Real Compensation, 1889-2025
**Phase**: 6 (Extension)
**Construction classification**: `composite`
**Extension status**: `feasible_with_substitute`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related**: `S207_DPR.md`, `Technical/research/S207_research.json`

---

## 1. Classification

Per the playbook content-type rule, S207 is classified `composite`. Extension recipe applied: per the Anu framework rule on lazy splices, this dictates the extension method below.

## 2. Method

Direct continuation of each subseries via FRED, reindexed at last book year.

## 3. No-Proxy disclosure

FRED OPHMFG is US-only continuation of discontinued BLS FLS Table 1 (19-country); flagged proxy:true in registry with concept-narrowing justification.

## 4. No-Synthetic disclosure

No synthetic, interpolated, or placeholder values are introduced. Where the API returns NaN, the NaN propagates to the published series.

## 5. Failure-mode table

| Failure | Detection | Action |
|---|---|---|
| API key not set | `S00_config.have_key` returns False | Loader returns `degraded`; processor publishes book period only; registry stamped `extension_status: api_key_missing` |
| API non-200 | `S00_apis._retry_get` raises after 3 retries | Same degradation as above |
| Overlap year NaN | Processor checks pre-splice | Walk back overlap year (e.g. 2010 -> 2009 -> 2008); fail hard if no valid overlap in 5-year window |
| Source URL discontinued | Phase 4 adequacy URL check | EPR documents the substitute (see section 3) |

## 6. CD2 divergence pre-disclosure

CD2's predecessor series may diverge from S207 due to (a) different extension anchor, (b) different proxy selection, or (c) a different vintage of the underlying source. Divergence is reported informationally in V03 and never causes a FAIL.

## 7. Extension status

Current: `feasible_with_substitute`. See DPR caveats for rationale.
