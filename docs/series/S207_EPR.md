# S207 -- Extension Provenance Record

**Series**: S207 -- US Manufacturing Productivity and Production Worker Real Compensation, 1889-2025

**Construction classification**: `composite`
**Extension status**: `feasible_with_substitute`
**Authored**: 2026-05-18 · **Revised**: 2026-07-17 (byte-instability/VREF narrative added)
**Author**: Anu Framework pipeline
**Related**: `S207_DPR.md`, research dossier

---

## 1. Classification

Per the playbook content-type rule, S207 is classified `composite`. Extension recipe applied: per the Anu framework rule on lazy splices, this dictates the extension method below.

## 2. Method

Direct continuation of each subseries via FRED, reindexed at last book year.

## 3. No-Proxy disclosure

FRED OPHMFG is US-only continuation of discontinued BLS FLS Table 1 (19-country); flagged proxy:true in registry with concept-narrowing justification.

## 4. No-Synthetic disclosure

No synthetic, interpolated, or placeholder values are introduced. Where the API returns NaN, the NaN propagates to the published series.

## 5. FRED Byte-Instability and VREF (Vintage Refresh)

**S207 is the live-FRED byte-instability exhibit for the project.** The extension source series (FRED `OPHMFG` and `COMPRMS`) are subject to periodic BLS/BEA revision — they are NOT in the set of FRED series that are never revised. Three vintages of the extension data have been observed:

1. **Initial extension (2026-05-18):** OPHMFG + COMPRMS fetched at the default FRED latest-vintage endpoint. Extension rows 2011–2024 produced.
2. **Byte-instability detected (mid-2026):** A subsequent fresh-env validation run produced slightly different extension values than the original fetch — the same FRED series IDs returned different bytes. This is expected behavior for revisable series but broke the project's byte-exact reproducibility assumption.
3. **VREF deliberate vintage refresh (2026-07-02):** The extension data were deliberately refreshed to the 2026-07-02 FRED/ALFRED vintage to ensure (a) the extension rows reflect the most recent BLS productivity revision, (b) a single coherent vintage is used for all extension subseries, and (c) the vintage pin is documented as an explicit realtime_start/realtime_end pair in the registry notes and `config/VINTAGE_MANIFEST.json`. The VREF produced: byte-identical book-period rows (as expected — the pre-2011 Shaikh data come from Appendix 2 workbooks, not FRED); S207-C (COMPRMS real compensation, `COMPRMS`) changed −0.020% at the 2025 tail; S207-D (OPHMFG productivity, `OPHMFG`) changed −0.078% at the 2025 tail.

**S207-D 2010 row removal (v1.5).** The 2010 extension row for S207-D was removed in v1.5 because it represented a single-year overlap that the splice-residuum check flagged as unreliable. The shipped S207-D now begins at 2011 (confirmed: 0 rows for year=2010 in chopped output).

## 6. Failure-mode table

| Failure | Detection | Action |
|---|---|---|
| API key not set | `S00_config.have_key` returns False | Loader returns `degraded`; processor publishes book period only; registry stamped `extension_status: api_key_missing` |
| API non-200 | `S00_apis._retry_get` raises after 3 retries | Same degradation as above |
| Overlap year NaN | Processor checks pre-splice | Walk back overlap year (e.g. 2010 -> 2009 -> 2008); fail hard if no valid overlap in 5-year window |
| Source URL discontinued | the adequacy step URL check | EPR documents the substitute (see section 3) |
| FRED vintage drift | V03 validation re-run on fresh fetch | VREF deliberate refresh (see section 5); vintage pin recorded in registry + VINTAGE_MANIFEST |

## 7. CD2 divergence pre-disclosure

CD2's predecessor series may diverge from S207 due to (a) different extension anchor, (b) different proxy selection, or (c) a different vintage of the underlying source. Divergence is reported informationally in V03 and never causes a FAIL.

## 8. Extension status

Current: `feasible_with_substitute`. See DPR caveats for rationale. Vintage: FRED/ALFRED 2026-07-02 (VREF).
