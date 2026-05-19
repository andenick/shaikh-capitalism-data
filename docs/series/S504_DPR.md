# S504 — US WPI in Gold and US Gold Price, 1800-2009

**DPR** · **Phase**: 5 · **Series ID**: S504 · **Status**: ingested · **Authored**: 2026-05-18

---

## 1. Definition

**S504** is the US analogue of S503, decomposing US WPI into:
- `p'_US` — US WPI expressed in gold, 1930=100
- `pG_US` — US $-price of gold per oz, 1930=100

Together: `USWPI = p'_US * pG_US / 100`. **Figure 5.6** plots both on log axes for 1800-2009.

## 2. Why it matters

Same role as S503 for the United States: isolates real-relative-price changes from monetary-anchor effects. The 1933/34 FDR devaluation ($20.67/oz → $35.00/oz) is the most visible feature, fully accounted for in pG.

## 3. Sources (per subseries)

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S504-A** (p'_US) | 1790-2010 | Computed: USWPI / pG_US, rebased 1930=100 by Shaikh | Index 1930=100 | `Appendix5_DATALRprices.xlsx` column `USPPIGold` |
| **S504-B** (pG_US) | 1790-2010 | MeasuringWorth: official 1786-1790, market thereafter (London Fix / LBMA underlying); 1780-1785 imputed via UK ratio in Jastram. Rebased 1930=100 by Shaikh. | Index 1930=100 | Same XLSX, column `USGoldpriceindex` |

## 4. Construction

**Formula** series: p = p' · pG (book eq. 5.9). Pass-through of Shaikh's pre-computed 1930=100 columns. Extension (Phase 6) MUST re-fetch components and recompute the ratio.

## 5. Year coverage

Book period: 1800-2009 (Fig 5.6 caption); data available 1780-2010. Published 1800-2010 (cf. S503 1790-2010).

## 6. Units

`index_1930=100` for both subseries.

## 7. Caveats

1. **1933/34 jump.** The visible discontinuity is the Gold Reserve Act of 1934 ($20.67 → $35.00, +69.4%). The data shows USGoldpriceindex moving from 118.2 (1933) → 169.0 (1934) → 169.3 (1935), reproducing the +69.4% jump (118.2 × 1.4302 = 169.05). This is a real historical feature, not a data artifact.
2. **Pre-1786 imputation.** US gold price 1780-1785 is estimated from the UK Jastram series using the 1786 US/UK gold-price ratio. Flagged `proxy_flag=pre1786_usgold_imputed_via_uk_ratio` if those years are included (they sit outside Fig 5.6's 1800 start so default S504 window 1800-2010 does not include them).
3. **WPS → WPU substitution** for any future v2 US WPI extension (same as S502).
4. **LBMA reform March 2015.** When v2 extends pG_US via LBMA Gold Price PM USD, the post-March-2015 LBMA Price replaces the older London Gold Fix; same auction concept, structural splice point documented for the overlap-anchor calibration.
5. **Extension not implemented in v1.** Requires BOTH WPU00000000 (available — FRED) AND LBMA gold price helper (not implemented). S502-C already extends USWPI; what's missing for S504 is the gold-price denominator. EPR documents.

## 8. Cross-references

- CD/CD2 legacy ID: `S025`. (CD2 listed COMEX/LBMA; corrected to MeasuringWorth canonical with LBMA underlying.)
- Book: Shaikh (2016) Ch5 p.199; Appendix 5.2 pp.788-789.
- Companion: S503 (UK analogue).

## 9. Validation expectation

- Tolerance: **±1.0%** per year (time_series).
- Truth source: `Appendix5_DATALRprices.xlsx` columns `USPPIGold`, `USGoldpriceindex`.
- Expected MAE: 0% (read-the-truth-column pattern).
- Sanity check: USWPI ≈ USPPIGold × USGoldpriceindex / 100 at 1930 (100·100/100 = 100 ✓), 2010 (20.84 × 5950.65/100 = 1240.0, matches USWPI = 1240.0).
- 1934 jump diagnostic: pG_US[1934]/pG_US[1933] = 169.04/118.24 = 1.430 ≈ 35/24.44 = 1.432 (within 0.2%; rounding).
