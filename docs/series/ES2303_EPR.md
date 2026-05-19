# ES2303 — Extension Provenance Record

**Series**: ES2303 — China FX Reserves Excluding Gold
**Phase**: 6 (Extension)
**Construction classification**: `direct`
**Extension method**: continuation of the same WDI series the paper cites
**Authored**: 2026-05-18

## 1. Why this series is extendable

WDI indicator `FI.RES.XGLD.CD` is continuously published; China's
reserves have been reported since 1990. Extension to 2024 requires no
methodological change — it is the *same series* Weber & Shaikh cited
(2018 vintage), pulled at a later vintage.

## 2. Method

1. Loader calls `S00_apis.worldbank_indicator(country='CHN',
   indicator='FI.RES.XGLD.CD', start=1990, end=2024)`.
2. API returns the full annual series; values divided by 1e9 for
   billion-USD presentation.
3. No splice, no rebase, no anchor — direct continuation.

## 3. Proxies

None. WDI IS the source the paper cites.

## 4. Synthetic data

None permitted. NaN at any year propagates.

## 5. Failure modes

| Failure | Action |
|---|---|
| World Bank API non-200 | Loader retries 3x; if still failing, raises ApiUnavailable; processor publishes empty series with `status=degraded` |
| WDI vintage revision changes historical values | Acceptable — we use the latest vintage; pin `data_vintage_pulled_at` in cache metadata |
| Indicator code change (unlikely for FI.RES.XGLD.CD) | Loader fails; surface as blocker, do not silently substitute |

## 6. Vintage note

The paper uses the 2018 WDI vintage. Modern vintages may have minor
revisions to historical values 1990-2016; tolerance budget absorbs
this. The Validator compares modern WDI against itself and PASSES.
A separate informational compare against the paper-vintage figure
values would require digitizing Fig 3.
