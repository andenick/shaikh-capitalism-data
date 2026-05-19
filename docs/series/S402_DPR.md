# S402 — Average and Marginal Costs with Wage Paid per Hour (Fig 4.17)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S402
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch4-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S402_research.json`
- Adequacy: `Technical/docs/chapters/CH4_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S402_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S402`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `SHAIKH_APPENDIX_4_2`

---

## 1. Definition

**S402** reproduces Shaikh's Figure 4.17 (book p. 156) — `afc`, `ulc`, `avc`, `ac`, `mc` under the assumption that **wages are paid per hour** (`wh=12.5`/hr), tabulated against cumulative daily output `XR` across three shifts (8+8+4 hours). Same numerical scaffold as S401 (Appendix 4.2), different wage convention.

## 2. Why it matters in Chapter 4

Fig 4.17 is the per-hour-wage twin of Fig 4.16 (S401). The key qualitative difference is that within-shift marginal cost is not flat at `pa·a` (as under per-worker wages), but instead tracks `pa·a + wh / MPL(h)` — inheriting the within-shift U-shape of the marginal product of labor. The shift-boundary spikes remain, driven now by productivity discontinuities rather than by wage-bill jumps. The result is the same: the cost curves are emphatically not the smooth U of neoclassical theory.

Shaikh emphasizes (p. 156) that the resulting `avc` is "roughly flat" over the desired-operation range — one of "the most well-documented empirical patterns in the literature," consistent with the classical / post-Keynesian stylized fact.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S402-A** | XR rows 0–20 (21 points) | Shaikh, *Capitalism* (2016), Appendix 4.2 Table 4.2.4, per-hour-wage columns | money units per unit of output | Reconstructed CSV `SalvagedInputs/book_data/Reconstructed/Appendix_4_2_Table4.csv`, columns `XR`, `afc`, `ulc`, `avc`, `ac`, `mc` |

## 4. Construction

`derived` / `formula`. Loader consumes the tabulated CSV directly.

```
Per-hour wage:
  afc  = d * pMK * mk(H, i)                  (same as S401)
  ulc  = wh * l(H, i) = wh * H/XR
  avc  = ulc + pa * a
  ac   = afc + avc
  tc   = ac * XR
  mc   = pa*a + wh * dXRs(Hs,i)/dHs           (within-shift varies with MPL; spikes at boundary)

Parameters (book p. 781):
  d = 0.05, pMK = 100, pa = 10, a = 0.30, wh = 12.5, p = 7,
  MK = 14, N ∈ {1, 2, 3}, i = 1.

Consistency check: wh * 8 = 100 = wN (matches S401's baseline).
```

## 5. Year coverage

Not applicable. See S401_DPR §5.

## 6. Units

- Cost columns (`afc`, `ulc`, `avc`, `ac`, `mc`): money units per unit of output.
- `tc`: money units (total daily cost).

## 7. Caveats

Identical to S401 (XR axis, not year; Appendix 4.2 parameter offset; XR=0 row preserved with `afc=70` only). Additionally:

1. **mc differs from S401's mc' qualitatively.** Within-shift, S402's mc is NOT flat — it follows pa·a + wh/MPL(h) and so traces a within-shift U. This is the visually distinguishing feature of Fig 4.17 vs Fig 4.16.

## 8. Cross-references

- **Book reference**: Shaikh (2016), Ch. 4, p. 156 (Fig 4.17); Appendix 4.2 pp. 772–781.
- **Cross-series**: S401 (per-worker twin), S403 (profit derivation).

## 9. Validation expectation

- **Tolerance**: ±0.5%.
- **Expected MAE**: 0 — direct CSV round-trip.
