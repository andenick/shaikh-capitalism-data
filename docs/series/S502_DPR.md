# S502 — US and UK Wholesale Price Indexes, 1790-2010

**Data Provenance Record (DPR)** · **Phase**: 5 (Ingestion) · **Series ID**: S502
**Status**: ingested · **Authored**: 2026-05-18 · **Author**: opus-fanout-wave3-ch5

---

## 1. Definition

**S502** is the annual US and UK Wholesale Price Indexes (1930=100) over the **full long-run period 1790-2010** — Fig 5.4. It is the parent series from which S501 (1790-1940 slice), S503 (UK WPI-in-gold ratio), and S504 (US WPI-in-gold ratio) are drawn.

## 2. Why it matters

Fig 5.4 is the empirical centerpiece of Ch5's argument that the post-1939/40 fiat-money epoch broke a 150-year regularity. Shaikh quantifies the magnitude as a 58x rise in the UK price level since 1939 and a 14x rise in the US level since 1940 — these are direct regression-test values for V03.

## 3. Sources (per subseries)

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S502-A** | 1790-2010 | Jastram (1977, table 7) for 1800-1976 + US CPI rescaled for 1790-1799 + BLS WPS00000000 growth rates 1977-2010 — all combined in Shaikh's `USWPI` column, 1930=100 | Index 1930=100 | `Appendix5_DATALRprices.xlsx` column `USWPI` |
| **S502-B** | 1790-2010 | Jastram (1977, table 2) for 1790-1938, 1946-1976 + NBER `m04053` 1939-1945 + ONS PLLU growth rates 1977-2010, in Shaikh's `UKWPI` column, 1930=100 | Index 1930=100 | Same XLSX, column `UKWPI` |
| **S502-C** (extension, optional) | 2011-2026 | BLS PPI All Commodities (= WPU00000000, successor to WPS00000000 frozen 1974) via FRED mirror identifier `PPIACO` | Index 1982=100 | FRED fredgraph CSV (no key): `PPIACO`, monthly→annual avg. Anchored to S502-A at 2010. |
| **S502-D** (extension, optional) | 2011-2025 | UK ONS PLLU (Output of Manufactured Products) | Index 2015=100 | **Not currently fetched** (ONS PLLU CDN returns 502 from our IP per Phase 4 review; no helper). UK leg of extension is documented but degrades gracefully. |

## 4. Construction

**Composite** — pass-through of the book's two pre-spliced country columns from `Appendix5_DATALRprices.xlsx`, then optional post-2010 extension via FRED WPU00000000 (US only).

```
S502-A[year] = Appendix5.USWPI[year]                  for year in [1790, 2010]
S502-B[year] = Appendix5.UKWPI[year]                  for year in [1790, 2010]
S502-C[year] = FRED_WPU00000000[year] * scale_US      for year in [2011, 2025]
              where scale_US = USWPI[2010] / FRED_WPU00000000[2010]
S502-D[year] = NaN  (UK extension unavailable from current toolkit; ONS PLLU CDN 502)
```

## 5. Year coverage

- Book period: 1790-2010 (US 221 obs, UK 221 obs).
- Extension (US): 2011-2025 (15 obs) when FRED key present.
- Extension (UK): not fetched in v1 (documented gap).

## 6. Units

`index_1930=100` throughout the published series.

## 7. Caveats

1. **WPS00000000 → WPU00000000 substitution** (US extension): BLS publicly identifies WPU as the successor identifier; same All-Commodities concept. Phase 4 verified WPS00000000 is frozen at 1974 via BLS public API. The substitution is documented in EPR §5 with `proxy: false` rationale (within-agency identifier change, same concept).
2. **Anchor point 2010, not 1930.** We anchor the FRED extension at the latest book year (2010), not at the 1930=100 base, to preserve exact level continuity at the splice. The result remains expressed on the 1930=100 base.
3. **UK extension gap.** ONS PLLU CDN returns 502 from our IP (Phase 4 reachability check 2026-05-18). We do NOT substitute a different UK PPI concept and we do NOT carry the UK 2010 value forward. UK 2011-2025 is left NaN with `extension_status: api_unavailable`.
4. **58x and 14x regression checks.** Shaikh's text: UK 2010/UK 1939 = 58x; US 2010/US 1940 = 14x. V03 reports both as informational diagnostics.

## 8. Cross-references

- CD/CD2 legacy ID: `S023`.
- Book: Shaikh (2016), Ch5 pp.188-189; Appendix 5.2 pp.788-789.
- Parent of: S501, S503 (UK WPI used), S504 (US WPI used).

## 9. Validation expectation

- Tolerance: **±1.0%** per year on the book period 1790-2010.
- Truth source: `Appendix5_DATALRprices.xlsx` columns `USWPI`, `UKWPI`.
- Expected MAE: 0% (read-the-truth-column pattern).
- Informational diagnostics: 58x UK ratio (1939→2010), 14x US ratio (1940→2010).
