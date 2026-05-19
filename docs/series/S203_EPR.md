# S203 -- Extension Provenance Record

**Series**: S203 -- US Real GDP per Capita (MeasuringWorth), 1889-2025
**Phase**: 6 (Extension)
**Construction classification**: `direct`
**Extension status**: `feasible`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related**: `S203_DPR.md`, `Technical/research/S203_research.json`

---

## 1. Classification

Per the playbook content-type rule, S203 is classified `direct`. Extension recipe applied: per the Anu framework rule on lazy splices, this dictates the extension method below.

## 2. Method

Same MeasuringWorth methodology continues; FRED A939 used for automated reindex.

## 3. No-Proxy disclosure

No proxies used. All extension sources are the same agency/program as the original.

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

CD2's predecessor series may diverge from S203 due to (a) different extension anchor, (b) different proxy selection, or (c) a different vintage of the underlying source. Divergence is reported informationally in V03 and never causes a FAIL.

## 7. Extension status

Current: `feasible`. See DPR caveats for rationale.
