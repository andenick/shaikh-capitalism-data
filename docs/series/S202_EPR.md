# S202 -- Extension Provenance Record

**Series**: S202 -- US Real Investment Index, 1832-2025
**Phase**: 6 (Extension)
**Construction classification**: `composite`
**Extension status**: `feasible`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related**: `S202_DPR.md`, `Technical/research/S202_research.json`

---

## 1. Classification

Per the playbook content-type rule, S202 is classified `composite`. Extension recipe applied: per the Anu framework rule on lazy splices, this dictates the extension method below.

## 2. Method

Direct continuation via BEA NIPA T1.1.6 line 9; overlap_anchor at 2010.

## 3. No-Proxy disclosure

Phase 4 flagged FRED GPDIC1 -> silent proxy. We use BEA NIPA T1.1.6 line 9 (concept-exact).

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

CD2's predecessor series may diverge from S202 due to (a) different extension anchor, (b) different proxy selection, or (c) a different vintage of the underlying source. Divergence is reported informationally in V03 and never causes a FAIL.

## 7. Extension status

Current: `feasible`. See DPR caveats for rationale.
