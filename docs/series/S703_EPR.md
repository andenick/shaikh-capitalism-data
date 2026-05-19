# S703 — Extension Provenance Record

**Series**: S703 — Figure 7.13 — World Manufacturing ROP and IROP, 1970–1989 (Christodoulopoulos/ISDB)
**Phase**: 6 (Extension)
**Construction classification**: `data_unavailable`
**Extension method**: not applicable — see §1
**Authored**: 2026-05-18
**Author**: opus-subagent-ch7-fanout
**Related**: `S703_DPR.md`

---

## 1. Classification

`content_type = data_unavailable`. There is no byte-exact underlying dataset to extend.

## 2. Why no extension is attempted

- The original raw data (Christodoulopoulos 1995 / Tsoulfidis-Tsaliki 2011) is not redistributed in any public form; Shaikh did not redistribute it in his Appendix 7.2 either.
- The closest modern source (OECD STAN 2025 for the world / US tracks; ELSTAT post-2010 for the Greek track) has incompatible industry classifications, country coverage, capital-stock coverage, and (for Greece) a 2010 ESYE→ELSTAT methodology break.
- Any modern panel would be a methodologically separate exhibit, not a faithful extension. Per the Anti-Degradation rule, we do not splice.

## 3. Method

N/A.

## 4. No-Proxy disclosure

**None attempted.** No proxy could meet the Anu No-Proxy bar.

## 5. No-Synthetic disclosure

**None.** No interpolation, no digitization (digitization deferred to Phase 9 visualization, where it is appropriately constrained).

## 6. Failure-mode table

| Failure | Action |
|---|---|
| Loader invoked | Returns `{"status": "SKIPPED", "reason": "data_unavailable"}` — by design, not a failure |
| Validator invoked | Returns `{"status": "PASS_DATA_UNAVAILABLE"}` |

## 7. CD2 divergence pre-disclosure

CD2 had no per-series CSV that matches this exhibit's content. The CD2-vs-RSCD comparison is not meaningful here.

## 8. Recovery paths (out-of-scope for Phase 6)

Documented in the B5 provenance file at `SalvagedInputs/book_data/Reconstructed/`. The two most plausible long-term recovery paths are:
1. Author contact (T&T are alive and contactable; Christodoulopoulos last known at NSSR).
2. PDF figure digitization via WebPlotDigitizer (Phase 9 visualization task; would be flagged `provenance: digitized`).
