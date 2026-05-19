# S503 — Extension Provenance Record

**Series**: S503 — UK WPI in Gold and UK Gold Price
**Phase**: 6 · **Construction**: `formula` · **Extension method**: re-compute (mandatory; no lazy splice)
**Authored**: 2026-05-18

---

## 1. Why this is a formula series

p'_UK = UKWPI / pG_UK. The book series is the ratio of two directly-observed indices, rebased. Per the **No Lazy Splices on Derived Quantities** rule, post-2010 extension of S503-A (p') is permitted ONLY by re-computing the same ratio from extended numerator and denominator — never by growth-splicing p' itself.

## 2. v1 extension status: not attempted

Extension requires BOTH of the following components for post-2010 years, neither of which is in the current toolkit:

| Component | Required for | Status v1 |
|---|---|---|
| UKWPI 2011-2025 (= ONS PLLU rebased) | numerator of p'_UK | UNAVAILABLE — ONS PLLU CDN returns 502 from our IP (Phase 4 reachability) |
| UK gold price £/oz 2011-2025 (LBMA Gold Price PM / BoE XUDLGBD FX) | denominator pG_UK | NOT IMPLEMENTED — no LBMA helper in `S00_apis.py` and no BoE FX helper |

Therefore the loader publishes only the book period (1790-2010) for S503-A and S503-B, with registry-stamped `extension_status: not_attempted_v1` and explicit per-component reasons.

## 3. Method (when both components are available)

```
INPUTS
  UKWPI_ext[2011, 2025]  = ONS PLLU rebased to 1930=100 using S502-B[2010] / PLLU[2010]
  pG_UK_ext[2011, 2025]  = (LBMA_PM_USD[year] / XUDLGBD[year]) rebased to 1930=100
                            using S503-B[2010] / (LBMA[2010]/FX[2010])

RECOMPUTE (NOT splice)
  p'_UK_ext[year] = UKWPI_ext[year] / pG_UK_ext[year] * 100

PUBLISH
  S503-A[year] = book[1790, 2010] U p'_UK_ext[2011, 2025]
  S503-B[year] = book[1790, 2010] U pG_UK_ext[2011, 2025]
```

The 1930=100 base survives because both numerator and denominator are reindexed to it before the ratio is taken.

## 4. Proxies

**None in v1.** Phase 4 ratified the correction of CD2's mis-attribution (CD2 listed BLS PPI as the UK gold-price extension; actual source is MeasuringWorth + Officer FX). When v2 implements the extension, LBMA Gold Price PM is the direct successor to the London Gold Fix that MeasuringWorth uses underlying — same concept, same auction, post-March-2015 reform documented as a structural splice point.

## 5. Synthetic data

None. The book-period 1939-1945 wartime values are flagged as `proxy_flag=ww2_gold_suspension_interpolated_measuringworth` because MeasuringWorth's underlying Officer & Williamson series interpolates — Shaikh adopted this and so do we, but with explicit provenance marking, not silent acceptance.

## 6. Failure modes

| Failure | Detection | Action |
|---|---|---|
| Appendix5 XLSX missing | loader | FAIL |
| UKPPIGold or UKGoldpriceindex column missing | loader | FAIL |
| ONS PLLU 502 (current state) | not attempted | book period only, status documented |
| LBMA / BoE not implemented | not attempted | book period only, status documented |

## 7. CD2 divergence

CD2 `S024` source-attribution (UK gold-price extension = BLS PPI) is wrong per Appendix 5.2. Phase 3 corrected and Phase 4 ratified the corrected attribution (MeasuringWorth + Officer FX). S503 reproduces book values exactly because it reads Shaikh's pre-computed columns.
