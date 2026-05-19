# S201 — Extension Provenance Record

**Series**: S201 — US Industrial Production Index
**Phase**: 6 (Extension)
**Construction classification**: `composite`
**Extension method**: direct continuation of one of the book's source components (FRB G.17 → FRED INDPRO), reindexed to 1958=100 at the 2010 overlap year
**Authored**: 2026-05-18
**Author**: opus-pilot-S201
**Related**: `S201_DPR.md`, `Technical/research/S201_research.json`, `Technical/SUBSOURCE_METADATA.json`

---

## 1. Why this series is extendable

S201 is a `time_series` series (per registry `content_type`). All three components are continuously published government indices; the modern half of the book period (1919–2010) is the **FRB G.17 Industrial Production Index**, which the Federal Reserve Board has produced monthly without interruption since 1919. FRED republishes the FRB release as `INDPRO`. The extension is therefore a continuation of the **same time series** Shaikh used for the back half of his Figure 2.1.

## 2. Construction classification

Per the Anu rule on lazy splices:

> "Growth-rate splice is ONLY valid when the original series was itself a directly-observed time series. If the original computed a formula, the extension must compute the same formula with extended component data."

S201 is `composite`, not `formula`. The book's published series is a splice of two directly-observed indices. The lazy-splice prohibition therefore does **not** require us to recompute a formula; it requires us to re-fetch the same observed component (FRB G.17, now via FRED INDPRO) and append it on the same base.

**This is allowed because**: extension uses the *same observational series* the book used — not a growth rate computed on top of a derived quantity.

## 3. Method

```
INPUTS
  S201_book   = processed series from Phase 7 P02, 1860–2010, base 1958=100
  FRED_INDPRO_raw = pulled from FRED API, frequency=annual avg, native base 2017=100
                    (St. Louis Fed republishes FRB G.17, identical underlying series)

OVERLAP CHECK
  overlap_year = 2010
  Assert: S201_book[2010] is not NaN AND FRED_INDPRO_raw[2010] is not NaN
  If either is NaN, fall back to next overlap candidate: 2009, then 2008, ...
  If no overlap in 2005–2010, FAIL — do not splice.

REINDEX
  scale_factor = S201_book[overlap_year] / FRED_INDPRO_raw[overlap_year]
  S201-C[year] = FRED_INDPRO_raw[year] * scale_factor   for year in [2011, 2025]

SPLICE
  S201_extended[year] = S201_book[year]   for year in [1860, 2010]
  S201_extended[year] = S201-C[year]      for year in [2011, 2025]

OUTPUT
  S201_extended is the final series, annual, 1860–2025, 1958=100
```

### 3.1 The reindex calculation — worked example

Suppose at runtime FRED returns:
- `FRED_INDPRO[2010] = 87.4124` (on 2017=100 base, annual avg)
- `S201_book[2010]   = 445.2739` (Shaikh's value, 1958=100)

Then:
- `scale_factor = 445.2739 / 87.4124 = 5.0939`
- For any year 2011–2025: `S201-C[year] = FRED_INDPRO[year] * 5.0939`

The scale factor depends on FRED's current base year — every time FRED rebases (~5-year cadence), the *level* changes but the ratios stay constant. Recomputing the scale factor on every run from the **live overlap** is what keeps the splice base-invariant.

## 4. Component re-fetching

Per the composite construction rule, the extension does *not* simply append a growth rate to S201's 2010 value. It re-fetches FRED INDPRO (= the same FRB G.17 series) and re-indexes the entire post-book segment from FRED's level to the book's 1958 base via the overlap-anchor. If FRED ever rebases mid-pipeline, the next loader run pulls fresh values and the splice is recomputed — no stale level survives across runs.

## 5. Proxies

**None.** FRED INDPRO is not a proxy for FRB G.17 — it IS FRB G.17, republished by St. Louis Fed with negligible latency under the same public-domain license. The registry records `"proxy": false` on S201-C with `"proxy_justification": null`. This is documented here so a future reviewer does not flag S201-C as a substitution.

## 6. Synthetic data

**None permitted.** If FRED returns NaN for any year (e.g., the most recent year before the annual aggregate is finalized — FRED publishes "annual" only after Dec data lands), that NaN propagates to S201. No interpolation, no carry-forward, no projection.

## 7. Failure modes & graceful degradation

| Failure | Detection | Action |
|---|---|---|
| `FRED_API_KEY` not set | `S00_config` raises at startup if `--series S201` requested | Loader returns `{status: degraded, fred: skipped}`; processor publishes 1860–2010 only; registry stamped `extension_status: api_key_missing` |
| FRED API returns non-200 | `S00_apis.fred_get()` raises | Loader retries 3× w/ 2s backoff; if still failing, same degradation as above |
| FRED cache stale (> 30 days) | `S00_cache.is_fresh()` returns False | Loader refetches; cache hit only when within TTL |
| FRED returns NaN at overlap_year=2010 | Processor checks | Walk back: try 2009, 2008, …, 2005; if none, FAIL hard (don't silently splice on wrong year) |
| FRED returns fewer years than expected | Processor checks | Publish only the years FRED returned; NaN fill the rest; registry stamped `extension_partial` with `last_year_observed` |

## 8. Splice diagnostics (reported by V03)

V03 validator emits, in addition to PASS/FAIL:

- The scale_factor actually used at runtime
- The overlap year actually used
- The number of post-2010 years observed
- The latest year published
- Whether the level continuity at the splice (2010→2011 growth rate) is within the historical 1-year band (±30%)

## 9. CD2 divergence

CD2's `S001-D [R:1958]` reindexed FRB G.17 differently — using FRED's 2017-base values rather than Shaikh's own FRB-1958 anchor. As a result CD2's 2010 value is ~453.7 vs the book chopped table's 445.3 (1.9% high). S201 reproduces the **book's** recipe exactly, so an intentional ~1.9% divergence from CD2 in the 1919–2010 segment is expected and acceptable.
