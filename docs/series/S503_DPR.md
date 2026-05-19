# S503 — UK WPI in Gold and UK Gold Price, 1790-2009

**DPR** · **Phase**: 5 · **Series ID**: S503 · **Status**: ingested · **Authored**: 2026-05-18

---

## 1. Definition

**S503** decomposes the UK price level into Marx's two components per Shaikh's eq. (5.9):
- `p'_UK` — UK WPI expressed in gold (commodities priced in ounces of gold), 1930=100
- `pG_UK` — UK market £-price of gold, 1930=100

Together they reconstruct the UK WPI: `UKWPI = p'_UK * pG_UK / 100`. **Figure 5.5** plots both on a single log y-axis.

## 2. Why it matters

The decomposition isolates the part of price-level change due to **real factors** (relative-price drift of commodities vs gold) from the part due to **monetary-anchor change** (the £ price of gold itself). Shaikh's empirical claim is that p' is "modest" over 1790-2009 — i.e., long-run real prices are driven by slowly-changing structural factors, and the dramatic post-1939 inflation visible in S502 lives almost entirely in pG.

## 3. Sources (per subseries)

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S503-A** (p'_UK) | 1790-2010 | Computed: `UKWPI / pG_UK` rebased to 1930=100 by Shaikh in DATALRprices | Index 1930=100 | `Appendix5_DATALRprices.xlsx` column `UKPPIGold` |
| **S503-B** (pG_UK) | 1790-2010 | Jastram (1977) 1780-1785 + MeasuringWorth UK £-price of gold 1786-1949 + US$ MeasuringWorth + Officer FX 1950-on, then rebased 1930=100 by Shaikh | Index 1930=100 | Same XLSX, column `UKGoldpriceindex` |

## 4. Construction

S503 is **formula** (per Anu classification): p = p' · pG (book eq. 5.9). Both p' and pG are pre-computed by Shaikh in DATALRprices on the 1930=100 base; we read them directly. Extension (Phase 6) MUST re-fetch the underlying UKWPI and UK gold price components and recompute the ratio — no growth-rate splice on p'_UK is permitted (No Lazy Splices on Derived Quantities).

## 5. Year coverage

Book period: 1790-2009 (matching Fig 5.5 caption); data available 1780-2010. We publish 1790-2010 (using through-2010 so the S502/S503 anchoring is consistent).

## 6. Units

`index_1930=100` for both subseries.

## 7. Caveats

1. **UK 1939-1945 wartime gold suspension.** The London gold market was suspended during WWII. MeasuringWorth's Officer & Williamson series interpolates these years; Shaikh adopts the interpolation. Per Phase 4 ratification, every observation in 1939-1945 is flagged `proxy_flag=ww2_gold_suspension_interpolated_measuringworth` at ingestion.
2. **1950 currency-quote transition.** MeasuringWorth quotes UK gold in £ for 1780-1949 and in US$ thereafter, requiring Officer's dollar-pound FX conversion for the post-1950 segment. The result still lives in the `UKGoldpriceindex` column after Shaikh's harmonization; this DPR does not re-implement the conversion.
3. **Extension not implemented in v1.** Re-computing post-2010 p'_UK requires (a) extended UKWPI (S502-D, currently NaN due to ONS PLLU 502) AND (b) extended UK gold price (LBMA Gold Price PM divided by BoE XUDLGBD FX — no helper exists yet). EPR documents both gaps; extension status is `not_attempted_v1` with reasons.
4. **No proxy substitutions** within the book period.

## 8. Cross-references

- CD/CD2 legacy ID: `S024`. (Note: CD2 mis-attributed UK gold-price extension to BLS PPI; corrected in Phase 3/4 to MeasuringWorth + Officer FX.)
- Book: Shaikh (2016) Ch5 pp.197-198; Appendix 5.2 pp.788-789.
- Companion: S504 (US analogue).

## 9. Validation expectation

- Tolerance: **±1.0%** per year (time_series).
- Truth source: `Appendix5_DATALRprices.xlsx` columns `UKPPIGold`, `UKGoldpriceindex`.
- Expected MAE: 0% (read-the-truth-column pattern).
- Internal consistency check: `UKWPI ≈ (UKPPIGold * UKGoldpriceindex) / 100` to within rounding — confirmed at sample years (1930: 100 ≈ 100·100/100; 2010: 5726.7 ≈ 30.8·18588.7/100 = 5725.3, within 0.025%).
