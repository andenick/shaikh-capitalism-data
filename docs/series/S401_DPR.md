# S401 — Average and Marginal Costs with Wage Paid per Worker (Fig 4.16)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S401
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch4-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S401_research.json`
- Adequacy: `Technical/docs/chapters/CH4_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S401_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S401`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `SHAIKH_APPENDIX_4_2`

---

## 1. Definition

**S401** reproduces Shaikh's Figure 4.16 (book p. 155) — the average fixed cost (`afc`), unit labor cost (`ulc'`), average variable cost (`avc'`), average total cost (`ac'`), and marginal cost (`mc'`) curves under the assumption that **wages are paid per worker** (wN per shift), tabulated against cumulative daily output `XR` across three shifts (8+8+4 hours) at normal intensity `i=1` for the 8-hour shifts and at the shift-3 truncation. The horizontal axis of Fig 4.16 is cumulative output `XR`; the vertical axis is cost per unit (money units).

**This is not a calendar time series.** It is a `derived` numerical illustration computed from Shaikh's Appendix 4.2 (book pp. 772–781).

## 2. Why it matters in Chapter 4

Chapter 4 ("Production and Costs") rebuilds the theory of the firm on a classical/post-Keynesian foundation. Fig 4.16 is the central numerical illustration of how cost curves behave when productivity follows the within-shift quadratic of eq. (4.2.1) and labor is hired by the worker-shift. The result — average total cost reaches near-equal minima at the end of shift 1 and shift 2, with mc flat at the materials-cost level within each shift and a discrete jump at each shift boundary — directly contradicts the smooth U-shape of neoclassical textbook cost curves.

S402 is the per-hour-wage twin; S403 derives the implied profit profile from S401 + S402.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S401-A** | XR rows 0–20 (21 points, indexed by row, not year) | Shaikh, *Capitalism* (2016), Appendix 4.2 Table 4.2.4, per-worker-wage columns | money units per unit of output | Reconstructed CSV `SalvagedInputs/book_data/Reconstructed/Appendix_4_2_Table4.csv`, columns `XR`, `afc`, `ulc_prime`, `avc_prime`, `ac_prime`, `mc_prime` |

The reconstructed CSV resolves Phase 5 blocker CH4-B1 (verbatim transcription from book PDF pp. 772–781, validated to <=0.02 rounding noise across all derived columns — see `Reconstructed/Appendix_4_2_README.md`).

## 4. Construction

S401 is `derived` (construction `formula`). Because the tabulated Appendix 4.2 values back-solve cleanly to the published formulas, the loader consumes the tabulated CSV directly and the processor writes the cost columns as-is (no re-derivation required for the book-period reproduction). The formula is documented here for traceability.

```
Per-worker wage:
  afc       = d * pMK * mk(H, i)            (declining as 1/XR via mk)
  ulc'      = wN * l'(H, i) = wN * N/XR     (jumps with N at each shift boundary)
  avc'      = ulc' + pa * a                 (a = 0.30, constant)
  ac'       = afc + avc'
  tc'       = ac' * XR
  mc'       = d(tc')/d(XR)                  (= pa*a inside a shift; spike at boundary)

Parameters (book p. 781):
  d = 0.05, pMK = 100, pa = 10, a = 0.30, wN = 100, p = 7,
  MK = 14, N ∈ {1, 2, 3}, i = 1 (for shifts 1–2), shift 3 truncated at h = 4.
```

S401 emits one long-form row per XR observation, with `subseries_id` carrying the cost-component label.

## 5. Year coverage

- **Book period**: not applicable (derived numerical illustration; the "axis" is cumulative output `XR`, not calendar year). Year-range fields in the registry are `[null, null]`; the loader stamps a synthetic ordinal index for downstream tooling.
- **Extension period**: not applicable — see `S401_EPR.md`.

## 6. Units

- Cost columns (`afc`, `ulc_prime`, `avc_prime`, `ac_prime`, `mc_prime`): money units per unit of output (illustrative; pa = 10, wN = 100, p = 7).
- `tc_prime`: money units (total daily cost).
- Axis (`XR`): physical units of cumulative daily output.

## 7. Caveats

1. **Not a time series.** The registry's `year_range` is `[null, null]`. We assign a synthetic ordinal `year = row_index` so the generic O06 chopped writer can persist the table. Downstream Phase 9 viz must plot against `XR` (not `year`).
2. **Appendix 4.2 published parameters are illustrative, not exactly reproducible.** Eq. (4.2.1) with the printed `a1=2, a2=1.2, a3=0.05` gives `xr(h=1)=3.15` whereas Table 4.2.1 prints `xr(h=1)=3.55` (+0.40 offset). Re-running the formula with back-solved `a1=2.40` recovers the tabulated values exactly. We do not re-derive in P02 — we consume the tabulated CSV directly. See `Reconstructed/Appendix_4_2_README.md` for full discussion.
3. **No CD/CD2 predecessor.** Fully fresh chapter (`CD2_to_RSCD_crosswalk.csv` has no Ch4 entries).
4. **Empty row at XR=0** is preserved with `afc=70` (fixed cost alone) and all other cost columns null — matches book's shaded entry on p. 779.

## 8. Cross-references

- **CD legacy ID**: none
- **CD2 legacy ID**: none
- **Book reference**: Shaikh (2016), Ch. 4, p. 155 (Fig 4.16); Appendix 4.2 pp. 772–781
- **Cross-series**: S402 (per-hour twin), S403 (profit derivation from S401 + S402)

## 9. Validation expectation

- **Tolerance**: ±0.5% per cost-component row (chapter playbook standard for `derived`).
- **Expected MAE**: 0 — we round-trip the same CSV the validator reads.
- The V03 validator compares the processed parquet against `Appendix_4_2_Table4.csv` directly; any deviation > 0.5% indicates pipeline corruption.
