# S504 — Extension Provenance Record

**Series**: S504 — US WPI in Gold and US Gold Price
**Phase**: 6 · **Construction**: `formula` · **Extension method**: re-compute (mandatory)
**Authored**: 2026-05-18

---

## 1. Why this is a formula series

Same as S503 but for the US: p'_US = USWPI / pG_US. The book-published p'_US comes from a ratio of two directly-observed indices on the 1930=100 base. Extension MUST recompute the ratio from extended USWPI and extended US gold price — never growth-splice p' itself.

## 2. v1 extension status: not attempted

| Component | Required for | Status v1 |
|---|---|---|
| USWPI 2011-2025 (BLS WPU00000000 via FRED) | numerator of p'_US | AVAILABLE via FRED (used by S502-C) but not re-fetched in S504 v1 (deferred to v2) |
| US gold price USD/oz 2011-2025 (LBMA Gold Price PM USD, annual avg) | denominator pG_US | NOT IMPLEMENTED — no LBMA helper in `S00_apis.py` |

Because the denominator is missing, the loader publishes book period only and records `extension_status: not_attempted_v1: missing_lbma_helper`.

## 3. Method (when LBMA helper exists)

```
INPUTS
  USWPI_ext[2011, 2025] = FRED_WPU * (USWPI[2010] / FRED_WPU[2010])
  pG_US_ext[2011, 2025] = LBMA_PM_USD_annual_avg * (USGoldpriceindex[2010] / LBMA[2010])

RECOMPUTE (NOT splice)
  p'_US_ext[year] = USWPI_ext[year] / pG_US_ext[year] * 100

PUBLISH
  S504-A = book[1800, 2010] U p'_US_ext[2011, 2025]
  S504-B = book[1800, 2010] U pG_US_ext[2011, 2025]
```

LBMA post-March-2015 reform: LBMA Gold Price PM is the direct successor to the London Gold Fix, same auction concept; no concept substitution.

## 4. Proxies

**None.** WPS → WPU is within-agency identifier change for the same All-Commodities PPI concept (`proxy: false`). LBMA Gold Price PM IS the London Fix continuation (`proxy: false`).

## 5. Synthetic data

None.

## 6. Failure modes

| Failure | Detection | Action |
|---|---|---|
| Appendix5 XLSX missing | loader | FAIL |
| Column USPPIGold or USGoldpriceindex missing | loader | FAIL |
| LBMA helper missing (current state) | not attempted | book period only |

## 7. CD2 divergence

CD2 `S025` listed COMEX/LBMA as primary; Appendix 5.2 says MeasuringWorth (which uses London Fix/LBMA underlying). Phase 3 corrected and Phase 4 ratified — MeasuringWorth canonical, LBMA underlying. S504 reproduces book values exactly within the book period because it reads Shaikh's pre-computed columns.
