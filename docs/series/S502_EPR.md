# S502 — Extension Provenance Record

**Series**: S502 — US and UK Wholesale Price Indexes, 1790-2010
**Phase**: 6 (Extension) · **Construction**: `composite`
**Extension method**: overlap-anchor splice on US leg only (BLS WPU00000000 via FRED), anchored at 2010; UK leg degrades gracefully (ONS PLLU CDN unavailable).
**Authored**: 2026-05-18

---

## 1. Why this series is extendable

S502-A (US) is a directly-observed WPI that BLS continues to publish under identifier `WPU00000000` (PPI All Commodities), the same conceptual continuation Shaikh planned for post-2010 (Appendix 5.2). Phase 4 verified WPU is live through 2026-04. ONS continues to publish PLLU (UK Output of Manufactured Products) but the CDN is unreachable from our IP at this time.

## 2. Classification

`composite`, not `formula`. The book series is a splice of two directly-observed national WPI columns. Per the No-Lazy-Splices rule, the extension may use a level-anchored splice of the **same observational series** (FRED WPU continues BLS WPS), not a growth-rate splice on a derived quantity.

## 3. Method (US extension)

```
INPUTS
  S502-A_book   = Appendix5.USWPI[1790, 2010], base 1930=100
  FRED_WPU_raw  = FRED.WPU00000000 annual avg [2005-2025], native 1982=100

OVERLAP
  overlap_year = 2010 (last book year)
  scale_US = USWPI[2010] / FRED_WPU[2010]

EXTEND
  S502-C[year] = FRED_WPU[year] * scale_US   for year in [2011, 2025]

OUTPUT
  S502_extended_US = book[1790, 2010] U S502-C[2011, 2025], single 1930=100 base
```

## 4. UK extension

**Not fetched in v1.** ONS PLLU returns 502 from our IP (Phase 4 reachability). We do not substitute a different UK PPI concept. The UK extension status is set to `api_unavailable: ons_pllu_cdn_502`. UK 2011-2025 published as NaN. A retry in a later session (potentially via ONS bulk MM22 download) is the documented next step.

## 5. Proxies

**US extension is NOT a proxy.** `WPS00000000` (Shaikh's identifier) and `WPU00000000` (modern identifier) are the same All-Commodities PPI series; BLS rebranded the prefix during the PPI program reclassification in the 1970s-80s. Same concept, same agency, same release. The registry records `proxy: false` on S502-C with rationale documented here.

## 6. Synthetic data

None. No NaN-fill, no carry-forward of UK 2010 across 2011-2025.

## 7. Failure modes

| Failure | Detection | Action |
|---|---|---|
| `FRED_API_KEY` missing | S00_config check | Loader writes only S502-A/B; processor publishes book period only; `extension_status: api_key_missing` |
| FRED returns non-200 | retry helper | After 3 retries → graceful degrade (book period only) |
| FRED 2010 NaN | processor overlap check | Walk back: try 2009, 2008, ..., 2005 |
| ONS PLLU 502 (current state) | not retried in v1 | UK extension is NaN, status = `api_unavailable: ons_pllu_cdn_502` |

## 8. CD2 divergence

CD2 `S023` recorded representative values consistent with the book chopped table. S502 reads the same column and so reproduces CD2's `S023-A`/`S023-B` exactly within the book period.
