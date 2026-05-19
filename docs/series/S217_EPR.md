# S217 -- Extension Provenance Record

**Series**: S217 -- GDP per Capita of World Regions (Maddison), 1600-2000
**Phase**: 6 (Extension)
**Construction classification**: `direct`
**Extension status**: `deferred`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related**: `S217_DPR.md`, `Technical/research/S217_research.json`

---

## 1. Classification

Per the playbook content-type rule, S217 is classified `direct`. Extension recipe applied: per the Anu framework rule on lazy splices, this dictates the extension method below.

## 2. Method

Maddison Project Database 2023; manual rebase required because of 1990 GK -> 2011 PPP shift.

## 3. No-Proxy disclosure

MPD 2023 region definitions revised in 2018/2020; flagged in registry.

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

CD2's predecessor series may diverge from S217 due to (a) different extension anchor, (b) different proxy selection, or (c) a different vintage of the underlying source. Divergence is reported informationally in V03 and never causes a FAIL.

## 7. Extension status

Current: `deferred`. See DPR caveats for rationale.
