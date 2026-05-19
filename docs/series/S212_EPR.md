# S212 -- Extension Provenance Record

**Series**: S212 -- US and UK Wholesale Prices in Ounces of Gold, 1790-2025 (1930=100, log scale)
**Phase**: 6 (Extension)
**Construction classification**: `formula`
**Extension status**: `feasible`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related**: `S212_DPR.md`, `Technical/research/S212_research.json`

---

## 1. Classification

Per the playbook content-type rule, S212 is classified `formula`. Extension recipe applied: per the Anu framework rule on lazy splices, this dictates the extension method below.

## 2. Method

Recompute WPI/gold ratio from extended S210 + extended gold price.

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

CD2's predecessor series may diverge from S212 due to (a) different extension anchor, (b) different proxy selection, or (c) a different vintage of the underlying source. Divergence is reported informationally in V03 and never causes a FAIL.

## 7. Extension status

Current: `feasible`. See DPR caveats for rationale.
