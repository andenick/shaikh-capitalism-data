# S205 -- Extension Provenance Record

**Series**: S205 -- Business Cycles, 1867-1902 (Ayres Index, Fig 2.4B)

**Construction classification**: `direct`
**Extension status**: `discontinued`
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related**: `S205_DPR.md`, research dossier

---

## 1. Classification

Per the playbook content-type rule, S205 is classified `direct`. Extension recipe applied: per the Anu framework rule on lazy splices, this dictates the extension method below.

## 2. Method

N/A. Historical-only.

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
| Source URL discontinued | the adequacy step URL check | EPR documents the substitute (see section 3) |

## 6. CD2 divergence pre-disclosure

CD2's predecessor series may diverge from S205 due to (a) different extension anchor, (b) different proxy selection, or (c) a different vintage of the underlying source. Divergence is reported informationally in V03 and never causes a FAIL.

## 7. Extension status

Current: `discontinued`. See DPR caveats for rationale.
