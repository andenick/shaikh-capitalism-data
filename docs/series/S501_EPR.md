# S501 — Extension Provenance Record

**Series**: S501 — US and UK Wholesale Price Indexes, 1790-1940
**Phase**: 6 (Extension) · **Construction classification**: `direct` (chronological slice)
**Extension method**: **none** — S501 is a fixed chronological window (Fig 5.3)
**Authored**: 2026-05-18 · **Author**: opus-fanout-wave3-ch5

---

## 1. Why no extension applies

S501 is by Shaikh's own definition a 1790-1940 figure (Fig 5.3). The 1941-onward period is treated separately in Fig 5.4 because the post-WWII fiat-money epoch breaks the stationary-price pattern. The full-range continuation is **S502**, not S501.

## 2. Classification

`content_type = "time_series"` (Phase 3 + Phase 4 ratified), `construction = "direct"`. The "direct" classification is what allows S501 to be a clean window onto S502's two columns without any algebraic recomputation. Phase 4 remediation flags S501 as a chronological view of S502 to enforce single-loader policy; the loader uses the same Appendix5_DATALRprices.xlsx columns.

## 3. Method

Year-window filter:
```
S501-A = Appendix5.USWPI[1790 <= year <= 1940]
S501-B = Appendix5.UKWPI[1790 <= year <= 1940]
```

No reindex, no splice, no API call.

## 4. Proxies

**None within the 1790-1940 window.** The historical fills inside the book period are not proxies:
- 1790-1799 US WPI imputed from US CPI (documented in Appendix 2.1) — flagged `proxy_flag=pre1800_uswpi_via_uscpi` at ingestion.
- 1939-1940 UK WPI taken from NBER macrohistory m04053 fill — flagged `proxy_flag=wartime_interpolated_NBER_m04053`.

These are Jastram/Shaikh-documented historical fills inside the published Jastram (1977) tables, not modern substitutions.

## 5. Synthetic data

None permitted.

## 6. Failure modes

| Failure | Detection | Action |
|---|---|---|
| Appendix5_DATALRprices.xlsx missing | loader check | `FAIL` — replication is impossible without local salvage |
| Column USWPI or UKWPI missing | loader check | `FAIL` |
| Year coverage incomplete | processor check | publish only available years; mark `year_range_observed` in registry |

## 7. CD2 divergence

CD2 `S022` recorded validation reference values (1790=74.40 US, 1850=66.6 US, 1940=90.8 US per Appendix5). S501 reproduces these exactly because it reads the same column.
