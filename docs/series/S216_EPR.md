# S216 -- Extension Provenance Record

**Series**: S216 -- Normalized Total Prices of Production Profit vs Total Unit Labor Costs, US 1972 (71 Industries)
**Phase**: 6 (Extension)
**Construction classification**: `cross_sectional`
**Extension status**: `not_applicable_cross_sectional`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related**: `S216_DPR.md`, `Technical/research/S216_research.json`

---

## 1. Classification

Per the playbook content-type rule, S216 is classified `cross_sectional`. Extension recipe applied: per the Anu framework rule on lazy splices, this dictates the extension method below.

## 2. Method

N/A. Multi-benchmark analysis requires separate registry rows per BEA benchmark year.

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

CD2's predecessor series may diverge from S216 due to (a) different extension anchor, (b) different proxy selection, or (c) a different vintage of the underlying source. Divergence is reported informationally in V03 and never causes a FAIL.

## 7. Extension status

Current: `not_applicable_cross_sectional`. See DPR caveats for rationale.
